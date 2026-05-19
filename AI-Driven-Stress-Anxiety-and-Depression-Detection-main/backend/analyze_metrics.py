"""
Metrics Analysis Script
Analyzes and visualizes training metrics from the metrics folder
"""

import json
import os
import sys
from pathlib import Path

def analyze_metrics(model_dir):
    """Analyze metrics from a trained model"""
    
    metrics_file = os.path.join(model_dir, 'metrics', 'metrics_report.json')
    
    if not os.path.exists(metrics_file):
        print(f"❌ Metrics file not found: {metrics_file}")
        print("Make sure the model has been trained and metrics were generated.")
        return
    
    print("=" * 80)
    print("METRICS ANALYSIS")
    print("=" * 80)
    print()
    
    # Load metrics
    with open(metrics_file, 'r') as f:
        metrics = json.load(f)
    
    # Overall summary
    print("📊 Overall Performance:")
    print(f"  Model: {metrics['model_name']}")
    print(f"  Training Mode: {'Quick Training' if metrics.get('quick_training') else 'Production Training'}")
    
    if 'training_duration' in metrics:
        print(f"  Training Duration: {metrics['training_duration']}")
    elif 'training_time_minutes' in metrics:
        print(f"  Training Time: {metrics['training_time_minutes']} minutes")
    
    print()
    print("  Metrics:")
    overall = metrics['overall_metrics']
    print(f"    Micro F1:    {overall['micro_f1']*100:>6.2f}%")
    print(f"    Macro F1:    {overall['macro_f1']*100:>6.2f}%")
    print(f"    Exact Match: {overall['exact_match']*100:>6.2f}%")
    print()
    
    # Per-emotion analysis
    print("🎯 Per-Emotion Analysis:")
    print()
    
    per_emotion = metrics['per_emotion_metrics']
    
    # Sort by F1 score
    sorted_emotions = sorted(per_emotion.items(), key=lambda x: x[1]['f1'], reverse=True)
    
    # Best performing
    print("  ✅ Top 5 Best Performing Emotions:")
    for i, (emotion, data) in enumerate(sorted_emotions[:5], 1):
        print(f"    {i}. {emotion:<15} F1: {data['f1']*100:>6.2f}%  (P: {data['precision']*100:.1f}%, R: {data['recall']*100:.1f}%)")
    
    print()
    
    # Worst performing
    print("  ⚠️  Bottom 5 Emotions (Need Attention):")
    for i, (emotion, data) in enumerate(sorted_emotions[-5:], 1):
        print(f"    {i}. {emotion:<15} F1: {data['f1']*100:>6.2f}%  (P: {data['precision']*100:.1f}%, R: {data['recall']*100:.1f}%)")
    
    print()
    
    # Statistics
    f1_scores = [data['f1'] for data in per_emotion.values()]
    avg_f1 = sum(f1_scores) / len(f1_scores)
    min_f1 = min(f1_scores)
    max_f1 = max(f1_scores)
    
    print("📈 Statistics:")
    print(f"  Average F1:  {avg_f1*100:.2f}%")
    print(f"  Min F1:      {min_f1*100:.2f}%")
    print(f"  Max F1:      {max_f1*100:.2f}%")
    print(f"  Range:       {(max_f1-min_f1)*100:.2f}%")
    print()
    
    # Performance categories
    excellent = sum(1 for f1 in f1_scores if f1 >= 0.9)
    good = sum(1 for f1 in f1_scores if 0.8 <= f1 < 0.9)
    fair = sum(1 for f1 in f1_scores if 0.7 <= f1 < 0.8)
    poor = sum(1 for f1 in f1_scores if f1 < 0.7)
    
    print("🎨 Performance Distribution:")
    print(f"  Excellent (≥90%): {excellent:>2d} emotions")
    print(f"  Good (80-89%):    {good:>2d} emotions")
    print(f"  Fair (70-79%):    {fair:>2d} emotions")
    print(f"  Poor (<70%):      {poor:>2d} emotions")
    print()
    
    # Recommendations
    print("💡 Recommendations:")
    if overall['micro_f1'] >= 0.95:
        print("  ✅ Model is production-ready!")
    elif overall['micro_f1'] >= 0.85:
        print("  ⚠️  Model is good but could be improved with more training")
    else:
        print("  ❌ Model needs more training")
    
    if poor > 0:
        print(f"  ⚠️  {poor} emotions performing below 70% - consider more training data")
    
    if max_f1 - min_f1 > 0.3:
        print("  ⚠️  Large performance variance - some emotions may need attention")
    
    print()
    print("=" * 80)
    print(f"📁 Full reports available in: {os.path.join(model_dir, 'metrics')}")
    print("=" * 80)
    print()

def compare_models(model_dir1, model_dir2):
    """Compare metrics between two models"""
    
    metrics_file1 = os.path.join(model_dir1, 'metrics', 'metrics_report.json')
    metrics_file2 = os.path.join(model_dir2, 'metrics', 'metrics_report.json')
    
    if not os.path.exists(metrics_file1) or not os.path.exists(metrics_file2):
        print("❌ One or both metrics files not found")
        return
    
    with open(metrics_file1, 'r') as f:
        metrics1 = json.load(f)
    with open(metrics_file2, 'r') as f:
        metrics2 = json.load(f)
    
    print("=" * 80)
    print("MODEL COMPARISON")
    print("=" * 80)
    print()
    
    print(f"Model 1: {Path(model_dir1).name}")
    print(f"Model 2: {Path(model_dir2).name}")
    print()
    
    # Compare overall metrics
    overall1 = metrics1['overall_metrics']
    overall2 = metrics2['overall_metrics']
    
    print("Overall Metrics Comparison:")
    print(f"{'Metric':<15} {'Model 1':>10} {'Model 2':>10} {'Difference':>12}")
    print("-" * 50)
    
    for metric in ['micro_f1', 'macro_f1', 'exact_match']:
        val1 = overall1[metric] * 100
        val2 = overall2[metric] * 100
        diff = val2 - val1
        sign = "+" if diff > 0 else ""
        print(f"{metric:<15} {val1:>9.2f}% {val2:>9.2f}% {sign}{diff:>10.2f}%")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python analyze_metrics.py <model_directory>")
        print("  python analyze_metrics.py <model_dir1> <model_dir2>  (for comparison)")
        print()
        print("Examples:")
        print("  python analyze_metrics.py models/quick-training")
        print("  python analyze_metrics.py models/distilbert-goemotions-mental")
        print("  python analyze_metrics.py models/quick-training models/distilbert-goemotions-mental")
        sys.exit(1)
    
    model_dir1 = sys.argv[1]
    
    if len(sys.argv) == 3:
        # Compare mode
        model_dir2 = sys.argv[2]
        compare_models(model_dir1, model_dir2)
    else:
        # Analyze mode
        analyze_metrics(model_dir1)
