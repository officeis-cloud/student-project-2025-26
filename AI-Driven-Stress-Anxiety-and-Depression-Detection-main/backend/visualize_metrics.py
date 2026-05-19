"""
Metrics Visualization Module
Creates comprehensive visualizations for training metrics
"""

import json
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.metrics import roc_curve, auc

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def create_metrics_visualizations(metrics_dir, metrics_data):
    """
    Create comprehensive visualizations for training metrics
    
    Args:
        metrics_dir: Directory to save plots
        metrics_data: Dictionary containing metrics from metrics_report.json
    """
    
    print("Creating metric visualizations...")
    
    plots_dir = os.path.join(metrics_dir, 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    
    per_emotion = metrics_data['per_emotion_metrics']
    overall = metrics_data['overall_metrics']
    
    # 1. Overall Metrics Bar Chart (Enhanced)
    print("  - Overall metrics chart...")
    fig, ax = plt.subplots(figsize=(14, 6))
    metrics_names = ['Micro F1', 'Macro F1', 'ROC-AUC\nMicro', 'ROC-AUC\nMacro', 'Subset\nAccuracy', 'Sample\nAccuracy']
    metrics_values = [
        overall.get('micro_f1', 0) * 100,
        overall.get('macro_f1', 0) * 100,
        overall.get('roc_auc_micro', 0) * 100,
        overall.get('roc_auc_macro', 0) * 100,
        overall.get('subset_accuracy', overall.get('exact_match', 0)) * 100,
        overall.get('sample_accuracy', 0) * 100
    ]
    colors = ['#2ecc71', '#3498db', '#9b59b6', '#8e44ad', '#e74c3c', '#e67e22']
    bars = ax.bar(metrics_names, metrics_values, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}%',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylabel('Score (%)', fontsize=12)
    ax.set_title('Overall Model Performance', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.axhline(y=90, color='green', linestyle='--', alpha=0.5, label='Excellent (90%)')
    ax.axhline(y=80, color='orange', linestyle='--', alpha=0.5, label='Good (80%)')
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, '01_overall_metrics.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Per-Emotion F1 Scores (Sorted)
    print("  - Per-emotion F1 scores...")
    emotions = list(per_emotion.keys())
    f1_scores = [per_emotion[e]['f1'] * 100 for e in emotions]
    
    # Sort by F1 score
    sorted_indices = np.argsort(f1_scores)
    emotions_sorted = [emotions[i] for i in sorted_indices]
    f1_sorted = [f1_scores[i] for i in sorted_indices]
    
    # Color code by performance
    colors = []
    for score in f1_sorted:
        if score >= 90:
            colors.append('#2ecc71')  # Green
        elif score >= 80:
            colors.append('#f39c12')  # Orange
        elif score >= 70:
            colors.append('#e67e22')  # Dark orange
        else:
            colors.append('#e74c3c')  # Red
    
    fig, ax = plt.subplots(figsize=(14, 10))
    bars = ax.barh(emotions_sorted, f1_sorted, color=colors, alpha=0.7)
    ax.set_xlabel('F1 Score (%)', fontsize=12)
    ax.set_title('F1 Score by Emotion (Sorted)', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 100)
    ax.axvline(x=90, color='green', linestyle='--', alpha=0.3)
    ax.axvline(x=80, color='orange', linestyle='--', alpha=0.3)
    ax.axvline(x=70, color='red', linestyle='--', alpha=0.3)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, f1_sorted)):
        ax.text(val + 1, i, f'{val:.1f}%', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, '02_emotion_f1_scores.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Precision vs Recall Scatter
    print("  - Precision vs Recall scatter...")
    precisions = [per_emotion[e]['precision'] * 100 for e in emotions]
    recalls = [per_emotion[e]['recall'] * 100 for e in emotions]
    
    fig, ax = plt.subplots(figsize=(12, 10))
    scatter = ax.scatter(precisions, recalls, c=f1_scores, cmap='RdYlGn', 
                        s=200, alpha=0.6, edgecolors='black', linewidth=1)
    
    # Add emotion labels
    for i, emotion in enumerate(emotions):
        ax.annotate(emotion, (precisions[i], recalls[i]), 
                   fontsize=8, ha='center', va='center')
    
    ax.set_xlabel('Precision (%)', fontsize=12)
    ax.set_ylabel('Recall (%)', fontsize=12)
    ax.set_title('Precision vs Recall by Emotion', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.plot([0, 100], [0, 100], 'k--', alpha=0.3, label='Perfect Balance')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('F1 Score (%)', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, '03_precision_recall_scatter.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Performance Distribution
    print("  - Performance distribution...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['Excellent\n(≥90%)', 'Good\n(80-89%)', 'Fair\n(70-79%)', 'Poor\n(<70%)']
    counts = [
        sum(1 for f1 in f1_scores if f1 >= 90),
        sum(1 for f1 in f1_scores if 80 <= f1 < 90),
        sum(1 for f1 in f1_scores if 70 <= f1 < 80),
        sum(1 for f1 in f1_scores if f1 < 70)
    ]
    colors_dist = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']
    
    bars = ax.bar(categories, counts, color=colors_dist, alpha=0.7, edgecolor='black', linewidth=2)
    
    # Add value labels
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}\nemotions',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_ylabel('Number of Emotions', fontsize=12)
    ax.set_title('Performance Distribution Across Emotions', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, '04_performance_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Top 10 and Bottom 10 Emotions
    print("  - Top/Bottom performers...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Top 10
    top_10_indices = sorted_indices[-10:]
    top_10_emotions = [emotions[i] for i in top_10_indices]
    top_10_f1 = [f1_scores[i] for i in top_10_indices]
    
    ax1.barh(top_10_emotions, top_10_f1, color='#2ecc71', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('F1 Score (%)', fontsize=12)
    ax1.set_title('Top 10 Best Performing Emotions', fontsize=13, fontweight='bold')
    ax1.set_xlim(min(top_10_f1) - 5, 100)
    
    for i, val in enumerate(top_10_f1):
        ax1.text(val + 0.5, i, f'{val:.1f}%', va='center', fontsize=10)
    
    # Bottom 10
    bottom_10_indices = sorted_indices[:10]
    bottom_10_emotions = [emotions[i] for i in bottom_10_indices]
    bottom_10_f1 = [f1_scores[i] for i in bottom_10_indices]
    
    ax2.barh(bottom_10_emotions, bottom_10_f1, color='#e74c3c', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('F1 Score (%)', fontsize=12)
    ax2.set_title('Bottom 10 Emotions (Need Improvement)', fontsize=13, fontweight='bold')
    ax2.set_xlim(0, max(bottom_10_f1) + 10)
    
    for i, val in enumerate(bottom_10_f1):
        ax2.text(val + 0.5, i, f'{val:.1f}%', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, '05_top_bottom_performers.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. Metrics Heatmap (Precision, Recall, F1)
    print("  - Metrics heatmap...")
    metrics_matrix = []
    emotion_names = []
    
    for emotion in emotions_sorted:
        emotion_names.append(emotion)
        metrics_matrix.append([
            per_emotion[emotion]['precision'] * 100,
            per_emotion[emotion]['recall'] * 100,
            per_emotion[emotion]['f1'] * 100
        ])
    
    metrics_matrix = np.array(metrics_matrix)
    
    fig, ax = plt.subplots(figsize=(8, 14))
    sns.heatmap(metrics_matrix, 
                xticklabels=['Precision', 'Recall', 'F1'],
                yticklabels=emotion_names,
                annot=True, fmt='.1f', cmap='RdYlGn', 
                vmin=0, vmax=100, cbar_kws={'label': 'Score (%)'},
                ax=ax, linewidths=0.5)
    ax.set_title('Emotion Metrics Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, '06_metrics_heatmap.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 7. Summary Statistics
    print("  - Summary statistics...")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    stats_text = f"""
    COMPREHENSIVE METRICS SUMMARY
    ════════════════════════════════════════════════════════════
    
    Model: {metrics_data['model_name']}
    Training Mode: {'Quick Training' if metrics_data.get('quick_training') else 'Production Training'}
    Training Duration: {metrics_data.get('training_duration', metrics_data.get('training_time_minutes', 'N/A'))}
    
    OVERALL PERFORMANCE
    ────────────────────────────────────────────────────────────
    Micro F1:     {overall['micro_f1']*100:6.2f}%
    Macro F1:     {overall['macro_f1']*100:6.2f}%
    Subset Accuracy: {overall.get('subset_accuracy', overall.get('exact_match', 0))*100:6.2f}%
    Sample Accuracy: {overall.get('sample_accuracy', 0)*100:6.2f}%
    ROC-AUC (Micro): {overall.get('roc_auc_micro', 0)*100:6.2f}%
    ROC-AUC (Macro): {overall.get('roc_auc_macro', 0)*100:6.2f}%
    
    PER-EMOTION STATISTICS
    ────────────────────────────────────────────────────────────
    Average F1:   {np.mean(f1_scores):6.2f}%
    Median F1:    {np.median(f1_scores):6.2f}%
    Min F1:       {np.min(f1_scores):6.2f}%  ({emotions[np.argmin(f1_scores)]})
    Max F1:       {np.max(f1_scores):6.2f}%  ({emotions[np.argmax(f1_scores)]})
    Std Dev:      {np.std(f1_scores):6.2f}%
    
    PERFORMANCE BREAKDOWN
    ────────────────────────────────────────────────────────────
    Excellent (≥90%):  {sum(1 for f1 in f1_scores if f1 >= 90):2d} emotions
    Good (80-89%):     {sum(1 for f1 in f1_scores if 80 <= f1 < 90):2d} emotions
    Fair (70-79%):     {sum(1 for f1 in f1_scores if 70 <= f1 < 80):2d} emotions
    Poor (<70%):       {sum(1 for f1 in f1_scores if f1 < 70):2d} emotions
    
    ════════════════════════════════════════════════════════════
    Generated: {metrics_data.get('training_date', 'N/A')}
    """
    
    ax.text(0.1, 0.95, stats_text, transform=ax.transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.savefig(os.path.join(plots_dir, '00_summary_statistics.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 8. ROC Curves (if data available)
    if 'roc_curve_data' in metrics_data and metrics_data['roc_curve_data']:
        print("  - ROC curves (top 10 emotions)...")
        roc_data = metrics_data['roc_curve_data']
        
        # Get top 10 emotions by ROC-AUC
        emotions_by_auc = sorted(
            [(emotion, per_emotion[emotion].get('roc_auc', 0)) for emotion in per_emotion.keys()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        fig, axes = plt.subplots(2, 5, figsize=(20, 8))
        axes = axes.flatten()
        
        for idx, (emotion, auc_score) in enumerate(emotions_by_auc):
            if emotion in roc_data:
                y_true = np.array(roc_data[emotion]['y_true'])
                y_probs = np.array(roc_data[emotion]['y_probs'])
                
                # Calculate ROC curve
                if len(np.unique(y_true)) > 1:
                    fpr, tpr, _ = roc_curve(y_true, y_probs)
                    roc_auc = auc(fpr, tpr)
                    
                    axes[idx].plot(fpr, tpr, color='darkorange', lw=2, 
                                 label=f'ROC (AUC = {roc_auc:.2f})')
                    axes[idx].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', 
                                 label='Random')
                    axes[idx].set_xlim([0.0, 1.0])
                    axes[idx].set_ylim([0.0, 1.05])
                    axes[idx].set_xlabel('False Positive Rate')
                    axes[idx].set_ylabel('True Positive Rate')
                    axes[idx].set_title(f'{emotion}')
                    axes[idx].legend(loc="lower right", fontsize=8)
                    axes[idx].grid(True, alpha=0.3)
                else:
                    axes[idx].text(0.5, 0.5, 'Only one class present', 
                                 ha='center', va='center')
                    axes[idx].set_title(f'{emotion}')
        
        plt.suptitle('ROC Curves - Top 10 Emotions by AUC', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(os.path.join(plots_dir, '07_roc_curves.png'), dpi=300, bbox_inches='tight')
        plt.close()
    
    # 9. Accuracy vs ROC-AUC Comparison
    print("  - Accuracy vs ROC-AUC scatter...")
    if 'accuracy' in list(per_emotion.values())[0] and 'roc_auc' in list(per_emotion.values())[0]:
        accuracies = [per_emotion[e].get('accuracy', 0) * 100 for e in emotions]
        roc_aucs = [per_emotion[e].get('roc_auc', 0) * 100 for e in emotions]
        
        fig, ax = plt.subplots(figsize=(12, 10))
        scatter = ax.scatter(accuracies, roc_aucs, c=f1_scores, cmap='RdYlGn',
                           s=200, alpha=0.6, edgecolors='black', linewidth=1)
        
        # Add emotion labels
        for i, emotion in enumerate(emotions):
            ax.annotate(emotion, (accuracies[i], roc_aucs[i]),
                       fontsize=8, ha='center', va='center')
        
        ax.set_xlabel('Accuracy (%)', fontsize=12)
        ax.set_ylabel('ROC-AUC (%)', fontsize=12)
        ax.set_title('Accuracy vs ROC-AUC by Emotion', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.plot([0, 100], [0, 100], 'k--', alpha=0.3, label='Perfect Correlation')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('F1 Score (%)', fontsize=11)
        
        plt.tight_layout()
        plt.savefig(os.path.join(plots_dir, '08_accuracy_vs_roc.png'), dpi=300, bbox_inches='tight')
        plt.close()
    
    # 10. Comprehensive Metrics Dashboard
    print("  - Comprehensive metrics dashboard...")
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Overall metrics radar/bar
    ax1 = fig.add_subplot(gs[0, :])
    metrics_keys = ['Micro F1', 'Macro F1', 'ROC-AUC\nMicro', 'ROC-AUC\nMacro', 'Subset\nAccuracy']
    metrics_vals = [
        overall.get('micro_f1', 0) * 100,
        overall.get('macro_f1', 0) * 100,
        overall.get('roc_auc_micro', 0) * 100,
        overall.get('roc_auc_macro', 0) * 100,
        overall.get('subset_accuracy', overall.get('exact_match', 0)) * 100
    ]
    bars = ax1.barh(metrics_keys, metrics_vals, color='#3498db', alpha=0.7)
    for i, (bar, val) in enumerate(zip(bars, metrics_vals)):
        ax1.text(val + 1, i, f'{val:.1f}%', va='center')
    ax1.set_xlim(0, 100)
    ax1.set_title('Overall Performance Metrics', fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # F1 scores distribution
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.hist(f1_scores, bins=15, color='#2ecc71', alpha=0.7, edgecolor='black')
    ax2.axvline(np.mean(f1_scores), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(f1_scores):.1f}%')
    ax2.set_xlabel('F1 Score (%)')
    ax2.set_ylabel('Count')
    ax2.set_title('F1 Score Distribution', fontweight='bold')
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    # Accuracies distribution  
    if 'accuracy' in list(per_emotion.values())[0]:
        ax3 = fig.add_subplot(gs[1, 1])
        accuracies_all = [per_emotion[e].get('accuracy', 0) * 100 for e in emotions]
        ax3.hist(accuracies_all, bins=15, color='#9b59b6', alpha=0.7, edgecolor='black')
        ax3.axvline(np.mean(accuracies_all), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(accuracies_all):.1f}%')
        ax3.set_xlabel('Accuracy (%)')
        ax3.set_ylabel('Count')
        ax3.set_title('Accuracy Distribution', fontweight='bold')
        ax3.legend()
        ax3.grid(alpha=0.3)
    
    # ROC-AUC distribution
    if 'roc_auc' in list(per_emotion.values())[0]:
        ax4 = fig.add_subplot(gs[1, 2])
        roc_aucs_all = [per_emotion[e].get('roc_auc', 0) * 100 for e in emotions if per_emotion[e].get('roc_auc', 0) > 0]
        if roc_aucs_all:
            ax4.hist(roc_aucs_all, bins=15, color='#e74c3c', alpha=0.7, edgecolor='black')
            ax4.axvline(np.mean(roc_aucs_all), color='darkred', linestyle='--', linewidth=2, label=f'Mean: {np.mean(roc_aucs_all):.1f}%')
        ax4.set_xlabel('ROC-AUC (%)')
        ax4.set_ylabel('Count')
        ax4.set_title('ROC-AUC Distribution', fontweight='bold')
        ax4.legend()
        ax4.grid(alpha=0.3)
    
    # Performance breakdown pie chart
    ax5 = fig.add_subplot(gs[2, :])
    categories = ['Excellent (≥90%)', 'Good (80-89%)', 'Fair (70-79%)', 'Poor (<70%)']
    counts = [
        sum(1 for f1 in f1_scores if f1 >= 90),
        sum(1 for f1 in f1_scores if 80 <= f1 < 90),
        sum(1 for f1 in f1_scores if 70 <= f1 < 80),
        sum(1 for f1 in f1_scores if f1 < 70)
    ]
    colors_pie = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']
    wedges, texts, autotexts = ax5.pie(counts, labels=categories, colors=colors_pie,
                                        autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    ax5.set_title('Performance Distribution Across Emotions', fontweight='bold', pad=20)
    
    plt.suptitle('Comprehensive Metrics Dashboard', fontsize=18, fontweight='bold', y=0.98)
    plt.savefig(os.path.join(plots_dir, '09_metrics_dashboard.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n✓ All visualizations saved to: {plots_dir}")
    print(f"  Total: 10 plots generated")
    
    return plots_dir

def generate_visualization_index(plots_dir):
    """Generate an HTML index for easy viewing of all plots"""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Training Metrics Visualizations</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            h1 { color: #333; text-align: center; }
            .container { max-width: 1400px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .plot { margin: 30px 0; }
            .plot img { width: 100%; border: 1px solid #ddd; border-radius: 5px; }
            .plot h2 { color: #2c3e50; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Training Metrics Visualizations</h1>
            
            <div class="plot">
                <h2>Summary Statistics</h2>
                <img src="00_summary_statistics.png" alt="Summary Statistics">
            </div>
            
            <div class="plot">
                <h2>Overall Model Performance</h2>
                <img src="01_overall_metrics.png" alt="Overall Metrics">
            </div>
            
            <div class="plot">
                <h2>F1 Scores by Emotion</h2>
                <img src="02_f1_scores_by_emotion.png" alt="F1 Scores">
            </div>
            
            <div class="plot">
                <h2>Precision vs Recall Analysis</h2>
                <img src="03_precision_recall_scatter.png" alt="Precision vs Recall">
            </div>
            
            <div class="plot">
                <h2>Performance Distribution</h2>
                <img src="04_performance_distribution.png" alt="Performance Distribution">
            </div>
            
            <div class="plot">
                <h2>Top and Bottom Performers</h2>
                <img src="05_top_bottom_performers.png" alt="Top Bottom Performers">
            </div>
            
            <div class="plot">
                <h2>Comprehensive Metrics Heatmap</h2>
                <img src="06_comprehensive_heatmap.png" alt="Metrics Heatmap">
            </div>
            
            <div class="plot">
                <h2>ROC Curves - Top 10 Emotions</h2>
                <img src="07_roc_curves.png" alt="ROC Curves">
            </div>
            
            <div class="plot">
                <h2>Accuracy vs ROC-AUC Comparison</h2>
                <img src="08_accuracy_vs_roc.png" alt="Accuracy vs ROC-AUC">
            </div>
            
            <div class="plot">
                <h2>Comprehensive Metrics Dashboard</h2>
                <img src="09_metrics_dashboard.png" alt="Metrics Dashboard">
            </div>
        </div>
    </body>
    </html>
    """
    
    index_path = os.path.join(plots_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ HTML index created: {index_path}")
    print(f"  Open this file in a browser to view all plots together")
    
    return index_path

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python visualize_metrics.py <metrics_directory>")
        print("Example: python visualize_metrics.py models/quick-training/metrics")
        sys.exit(1)
    
    metrics_dir = sys.argv[1]
    metrics_file = os.path.join(metrics_dir, 'metrics_report.json')
    
    if not os.path.exists(metrics_file):
        print(f"❌ Metrics file not found: {metrics_file}")
        sys.exit(1)
    
    with open(metrics_file, 'r') as f:
        metrics_data = json.load(f)
    
    plots_dir = create_metrics_visualizations(metrics_dir, metrics_data)
    generate_visualization_index(plots_dir)
    
    print("\n✅ Visualization complete!")
