"""
Visualization Script for Chatbot Architecture and Performance
Generates charts for research paper/presentation
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Note: Run this after you have some chatbot_metrics_*.json files


def plot_metrics_from_file(filename):
    """Load and visualize metrics from a JSON file"""
    with open(filename, 'r') as f:
        data = json.load(f)
    
    metrics = data['metrics']
    
    # Create a 2x2 subplot
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Chatbot Performance Metrics - Research Analysis', fontsize=16, fontweight='bold')
    
    # 1. Intent Distribution (Pie Chart)
    intents = list(metrics['intents_detected'].keys())
    counts = list(metrics['intents_detected'].values())
    colors = plt.cm.Set3(np.linspace(0, 1, len(intents)))
    
    ax1.pie(counts, labels=intents, autopct='%1.1f%%', colors=colors, startangle=90)
    ax1.set_title('Intent Distribution', fontweight='bold')
    
    # 2. Sentiment Analysis (Bar Chart)
    sentiments = list(metrics['sentiment_distribution'].keys())
    sent_counts = list(metrics['sentiment_distribution'].values())
    colors_sent = {'positive': '#4CAF50', 'neutral': '#FFC107', 'negative': '#F44336'}
    bar_colors = [colors_sent.get(s, '#999') for s in sentiments]
    
    ax2.bar(sentiments, sent_counts, color=bar_colors, alpha=0.7, edgecolor='black')
    ax2.set_title('Sentiment Distribution', fontweight='bold')
    ax2.set_ylabel('Count')
    ax2.set_xlabel('Sentiment')
    for i, v in enumerate(sent_counts):
        ax2.text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')
    
    # 3. Key Metrics (Table)
    ax3.axis('off')
    metrics_table = [
        ['Metric', 'Value'],
        ['Total Interactions', str(metrics['total_interactions'])],
        ['Human Escalations', str(metrics['escalations_to_human'])],
        ['Escalation Rate', f"{metrics['escalation_rate']*100:.1f}%"],
        ['Avg Response Time', f"{metrics['average_response_time_ms']:.2f}ms"],
        ['Avg Satisfaction', f"{metrics['average_satisfaction']:.2f}/5.0"],
    ]
    
    table = ax3.table(cellText=metrics_table, cellLoc='left', loc='center',
                      colWidths=[0.6, 0.4])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style header row
    for i in range(2):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, len(metrics_table)):
        for j in range(2):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f0f0f0')
    
    ax3.set_title('Performance Summary', fontweight='bold', pad=20)
    
    # 4. Satisfaction Scores (Histogram)
    if metrics['satisfaction_scores']:
        scores = metrics['satisfaction_scores']
        bins = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
        ax4.hist(scores, bins=bins, color='#2196F3', alpha=0.7, edgecolor='black', rwidth=0.8)
        ax4.set_title('Customer Satisfaction Distribution', fontweight='bold')
        ax4.set_xlabel('Rating (1-5 stars)')
        ax4.set_ylabel('Frequency')
        ax4.set_xticks([1, 2, 3, 4, 5])
        ax4.grid(axis='y', alpha=0.3)
    else:
        ax4.text(0.5, 0.5, 'No satisfaction data available', 
                ha='center', va='center', fontsize=12)
        ax4.set_title('Customer Satisfaction Distribution', fontweight='bold')
    
    plt.tight_layout()
    
    # Save the figure
    output_filename = f"chatbot_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"✓ Chart saved as {output_filename}")
    
    plt.show()


def compare_multiple_sessions(filenames):
    """Compare metrics across multiple sessions"""
    sessions_data = []
    
    for filename in filenames:
        with open(filename, 'r') as f:
            data = json.load(f)
            sessions_data.append(data['metrics'])
    
    # Create comparison charts
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Multi-Session Comparison Analysis', fontsize=16, fontweight='bold')
    
    sessions = [f"Session {i+1}" for i in range(len(sessions_data))]
    
    # 1. Satisfaction scores
    satisfactions = [d['average_satisfaction'] for d in sessions_data]
    ax1.bar(sessions, satisfactions, color='#4CAF50', alpha=0.7, edgecolor='black')
    ax1.set_title('Average Satisfaction Score', fontweight='bold')
    ax1.set_ylabel('Score (out of 5)')
    ax1.axhline(y=4.0, color='r', linestyle='--', label='Target (4.0)')
    ax1.legend()
    ax1.set_ylim(0, 5)
    
    # 2. Escalation rates
    escalation_rates = [d['escalation_rate'] * 100 for d in sessions_data]
    ax2.bar(sessions, escalation_rates, color='#FF9800', alpha=0.7, edgecolor='black')
    ax2.set_title('Escalation Rate (%)', fontweight='bold')
    ax2.set_ylabel('Percentage')
    ax2.axhline(y=15, color='g', linestyle='--', label='Target (10-20%)')
    ax2.legend()
    
    # 3. Response times
    response_times = [d['average_response_time_ms'] for d in sessions_data]
    ax3.plot(sessions, response_times, marker='o', linewidth=2, markersize=8, color='#2196F3')
    ax3.set_title('Average Response Time', fontweight='bold')
    ax3.set_ylabel('Time (ms)')
    ax3.grid(True, alpha=0.3)
    
    # 4. Total interactions
    interactions = [d['total_interactions'] for d in sessions_data]
    ax4.bar(sessions, interactions, color='#9C27B0', alpha=0.7, edgecolor='black')
    ax4.set_title('Total Interactions per Session', fontweight='bold')
    ax4.set_ylabel('Count')
    
    plt.tight_layout()
    
    # Save comparison
    output_filename = f"session_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"✓ Comparison chart saved as {output_filename}")
    
    plt.show()


def generate_research_summary():
    """Generate a summary table for research paper"""
    import glob
    
    metrics_files = glob.glob('chatbot_metrics_*.json')
    
    if not metrics_files:
        print("⚠ No metrics files found. Run the chatbot first!")
        return
    
    all_data = []
    for file in metrics_files:
        with open(file, 'r') as f:
            all_data.append(json.load(f))
    
    # Aggregate statistics
    total_interactions = sum(d['metrics']['total_interactions'] for d in all_data)
    avg_satisfaction = np.mean([d['metrics']['average_satisfaction'] for d in all_data if d['metrics']['average_satisfaction'] > 0])
    avg_escalation = np.mean([d['metrics']['escalation_rate'] for d in all_data])
    avg_response_time = np.mean([d['metrics']['average_response_time_ms'] for d in all_data])
    
    print("\n" + "="*60)
    print("RESEARCH SUMMARY - AGGREGATE STATISTICS")
    print("="*60)
    print(f"Total Sessions Analyzed: {len(all_data)}")
    print(f"Total Customer Interactions: {total_interactions}")
    print(f"Average Satisfaction Score: {avg_satisfaction:.2f}/5.0")
    print(f"Average Escalation Rate: {avg_escalation*100:.1f}%")
    print(f"Average Response Time: {avg_response_time:.2f}ms")
    print("="*60 + "\n")
    
    # Create summary visualization
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    metrics_names = ['Satisfaction\n(out of 5)', 'Escalation\nRate (%)', 
                     'Response Time\n(ms)', 'Sessions\nAnalyzed']
    metrics_values = [avg_satisfaction, avg_escalation*100, avg_response_time, len(all_data)]
    
    # Normalize for better visualization
    normalized = [
        avg_satisfaction / 5 * 100,  # Convert to percentage
        avg_escalation * 100,
        min(avg_response_time, 100),  # Cap at 100ms for viz
        len(all_data) * 10  # Scale for visibility
    ]
    
    bars = ax.barh(metrics_names, normalized, color=['#4CAF50', '#FF9800', '#2196F3', '#9C27B0'], alpha=0.7)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, metrics_values)):
        if i == 0:
            label = f"{val:.2f}/5.0"
        elif i == 1:
            label = f"{val:.1f}%"
        elif i == 2:
            label = f"{val:.2f}ms"
        else:
            label = f"{int(val)}"
        
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, 
               label, va='center', fontweight='bold', fontsize=12)
    
    ax.set_xlabel('Normalized Value', fontweight='bold')
    ax.set_title('Research Summary - Key Performance Indicators', fontweight='bold', fontsize=14)
    ax.set_xlim(0, 120)
    
    plt.tight_layout()
    plt.savefig(f"research_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png", 
                dpi=300, bbox_inches='tight')
    print("✓ Research summary chart saved")
    plt.show()


if __name__ == "__main__":
    import glob
    
    # Find all metrics files
    metrics_files = glob.glob('chatbot_metrics_*.json')
    
    if not metrics_files:
        print("⚠ No metrics files found!")
        print("Run the chatbot first with: python chatbot.py")
        print("Then run this visualization script again.")
    else:
        print(f"Found {len(metrics_files)} metrics file(s)\n")
        
        # Visualize the most recent session
        latest_file = max(metrics_files, key=lambda x: x.split('_')[2] + x.split('_')[3].replace('.json', ''))
        print(f"Visualizing latest session: {latest_file}")
        plot_metrics_from_file(latest_file)
        
        # If multiple sessions, create comparison
        if len(metrics_files) > 1:
            print(f"\nCreating comparison across {len(metrics_files)} sessions...")
            compare_multiple_sessions(metrics_files)
        
        # Generate research summary
        print("\nGenerating research summary...")
        generate_research_summary()
