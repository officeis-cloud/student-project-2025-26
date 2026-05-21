import sys
import os
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
import numpy as np
from PIL import Image
import io
import base64
import traceback

# ──────────────────────────────────────────────
# Path setup — everything is relative to this file
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.resolve()

DENSENET_MODEL_PATH  = BASE_DIR / "DenseNet"  / "tuberModel.onnx"
RESNET_MODEL_PATH    = BASE_DIR / "ResNet"    / "tb_resnet50_clean.onnx"
DENSENET_GAN_MODEL_PATH = BASE_DIR / "DenseNet_GAN" / "densenet121_tb.onnx"

# ──────────────────────────────────────────────
# Load ONNX sessions (done once at startup)
# ──────────────────────────────────────────────
import onnxruntime as ort

densenet_session = None
resnet_session   = None

try:
    densenet_session = ort.InferenceSession(
        str(DENSENET_MODEL_PATH), providers=["CPUExecutionProvider"]
    )
    print(f"[OK] DenseNet ONNX loaded from {DENSENET_MODEL_PATH}")
except Exception as e:
    print(f"[ERROR] Failed to load DenseNet ONNX: {e}")

try:
    resnet_session = ort.InferenceSession(
        str(RESNET_MODEL_PATH), providers=["CPUExecutionProvider"]
    )
    print(f"[OK] ResNet ONNX loaded from {RESNET_MODEL_PATH}")
except Exception as e:
    print(f"[ERROR] Failed to load ResNet ONNX: {e}")

# ──────────────────────────────────────────────
# Load DenseNet-GAN ONNX model (done once)
# ──────────────────────────────────────────────
gan_session = None

try:
    # Need to change working directory for onnxruntime to find the external data file
    # This ensures the .onnx.data file is located correctly if we are running from a different dir
    # But usually ort handles relative path natively as long as they are in same dir.
    gan_session = ort.InferenceSession(
        str(DENSENET_GAN_MODEL_PATH), providers=["CPUExecutionProvider"]
    )
    print(f"[OK] DenseNet-GAN ONNX loaded from {DENSENET_GAN_MODEL_PATH}")
except Exception as e:
    print(f"[ERROR] Failed to load DenseNet-GAN ONNX: {e}")

# ──────────────────────────────────────────────
# ImageNet normalisation constants
# ──────────────────────────────────────────────
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD  = np.array([0.229, 0.224, 0.225], dtype=np.float32)

# ──────────────────────────────────────────────
# Prediction helpers
# ──────────────────────────────────────────────
def predict_densenet(pil_image: Image.Image):
    """DenseNet ONNX — input NCHW, class 0=Normal 1=TB"""
    img = pil_image.convert("RGB").resize((224, 224))
    arr = np.array(img).astype(np.float32) / 255.0
    arr = (arr - MEAN) / STD
    arr = np.transpose(arr, (2, 0, 1))          # HWC → CHW
    arr = np.expand_dims(arr, axis=0)            # (1, 3, 224, 224)

    input_name  = densenet_session.get_inputs()[0].name
    output_name = densenet_session.get_outputs()[0].name
    logits = densenet_session.run([output_name], {input_name: arr})[0][0]

    exp   = np.exp(logits - np.max(logits))
    probs = exp / exp.sum()
    pred  = int(np.argmax(probs))
    return pred, probs.tolist()   # [prob_normal, prob_tb]


def predict_resnet(pil_image: Image.Image):
    """ResNet ONNX — input NHWC, probabilities are reversed in original code"""
    img = pil_image.convert("RGB").resize((224, 224))
    arr = np.array(img).astype(np.float32) / 255.0
    arr = (arr - MEAN) / STD
    arr = np.expand_dims(arr, axis=0)            # (1, 224, 224, 3)  NHWC

    input_name  = resnet_session.get_inputs()[0].name
    output_name = resnet_session.get_outputs()[0].name
    logits = resnet_session.run([output_name], {input_name: arr})[0][0]

    exp   = np.exp(logits - np.max(logits))
    probs = (exp / exp.sum()).tolist()
    # Original test.py flips probs and swaps class index
    probs_fixed = probs[::-1]   # [prob_normal, prob_tb]
    pred = 1 if probs_fixed[1] > probs_fixed[0] else 0
    return pred, probs_fixed


def predict_gan(pil_image: Image.Image):
    """DenseNet-GAN ONNX — grayscale input mapped to 3 channels, class 0=Normal 1=TB"""
    img_gray = pil_image.convert("L").resize((224, 224))
    img_rgb = Image.merge("RGB", (img_gray, img_gray, img_gray))
    arr = np.array(img_rgb).astype(np.float32) / 255.0
    arr = (arr - MEAN) / STD
    arr = np.transpose(arr, (2, 0, 1))          # HWC → CHW
    arr = np.expand_dims(arr, axis=0)            # (1, 3, 224, 224)

    input_name  = gan_session.get_inputs()[0].name
    output_name = gan_session.get_outputs()[0].name
    logits = gan_session.run([output_name], {input_name: arr})[0][0]

    exp   = np.exp(logits - np.max(logits))
    probs = (exp / exp.sum()).tolist()
    pred  = int(np.argmax(probs))
    return pred, probs

# ──────────────────────────────────────────────
# Flask app
# ──────────────────────────────────────────────
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024   # 16 MB max upload

ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        return jsonify({"error": f"Unsupported file type: {ext}"}), 400

    try:
        img_bytes = file.read()
        pil_image = Image.open(io.BytesIO(img_bytes))
    except Exception as e:
        return jsonify({"error": f"Cannot open image: {e}"}), 400

    results = {}

    # ── DenseNet ONNX ──
    if densenet_session is None:
        results["densenet"] = {"error": "Model not loaded"}
    else:
        try:
            pred, probs = predict_densenet(pil_image)
            results["densenet"] = {
                "prediction": "Tuberculosis" if pred == 1 else "Normal",
                "class_index": pred,
                "prob_normal": round(probs[0] * 100, 2),
                "prob_tb":     round(probs[1] * 100, 2),
            }
        except Exception as e:
            results["densenet"] = {"error": str(e), "traceback": traceback.format_exc()}

    # ── ResNet ONNX ──
    if resnet_session is None:
        results["resnet"] = {"error": "Model not loaded"}
    else:
        try:
            pred, probs = predict_resnet(pil_image)
            results["resnet"] = {
                "prediction": "Tuberculosis" if pred == 1 else "Normal",
                "class_index": pred,
                "prob_normal": round(probs[0] * 100, 2),
                "prob_tb":     round(probs[1] * 100, 2),
            }
        except Exception as e:
            results["resnet"] = {"error": str(e), "traceback": traceback.format_exc()}

    # ── DenseNet-GAN PyTorch ──
    if gan_session is None:
        results["densenet_gan"] = {"error": "Model not loaded"}
    else:
        try:
            pred, probs = predict_gan(pil_image)
            results["densenet_gan"] = {
                "prediction": "Tuberculosis" if pred == 1 else "Normal",
                "class_index": pred,
                "prob_normal": round(probs[0] * 100, 2),
                "prob_tb":     round(probs[1] * 100, 2),
            }
        except Exception as e:
            results["densenet_gan"] = {"error": str(e), "traceback": traceback.format_exc()}

    # ── Ensemble majority vote ──
    votes = []
    for key in ["densenet", "resnet", "densenet_gan"]:
        r = results.get(key, {})
        if "class_index" in r:
            votes.append(r["class_index"])

    if votes:
        tb_votes     = votes.count(1)
        normal_votes = votes.count(0)
        ensemble     = "Tuberculosis" if tb_votes > normal_votes else "Normal"
    else:
        ensemble = "Unable to determine"

    results["ensemble"] = {
        "prediction":   ensemble,
        "tb_votes":     tb_votes if votes else 0,
        "normal_votes": normal_votes if votes else 0,
        "total_votes":  len(votes),
    }

    return jsonify(results)


if __name__ == "__main__":
    print("\n" + "="*60)
    print(" TB Detection Web App")
    print("="*60)
    print(f" DenseNet  ONNX : {DENSENET_MODEL_PATH}")
    print(f" ResNet    ONNX : {RESNET_MODEL_PATH}")
    print(f" DenseNet-GAN   : {DENSENET_GAN_MODEL_PATH}")
    print("="*60)
    print(" Open http://127.0.0.1:5000 in your browser")
    print("="*60 + "\n")
    app.run(debug=False, port=5000)
