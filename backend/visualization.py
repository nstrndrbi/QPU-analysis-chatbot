import matplotlib.pyplot as plt
import pandas as pd
import os
from data_processor import get_daily_costs, get_daily_workloads, get_block_efficiency
import tempfile
import seaborn as sns

def generate_trend_graph():
    # Get the daily costs data
    daily_costs = get_daily_costs()  # should return columns: 'date', 'total_daily_cost'
    
    # Convert to DataFrame
    df = pd.DataFrame(daily_costs)
    df['date'] = pd.to_datetime(df['date'])
    
    # Set style
    sns.set(style="darkgrid")
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['total_daily_cost'], marker='o', linewidth=2, color='#3366cc')
    
    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Daily Cost ($)')
    plt.title('Trend of Daily Costs')
    
    # Format y-axis as currency
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Rotate date labels for better readability
    plt.xticks(rotation=45)
    
    # Tight layout
    plt.tight_layout()
    
    # Save the graph to a temporary location
    temp_dir = tempfile.gettempdir()
    graph_path = os.path.join(temp_dir, 'daily_costs_trend.png')
    plt.savefig(graph_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return graph_path

def generate_workloads_graph():
    """
    Generate a graph showing daily workloads over time
    """
    # Get daily workloads data
    workloads_data = get_daily_workloads()
    
    # Convert to DataFrame
    df = pd.DataFrame(workloads_data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Set style
    sns.set(style="darkgrid")
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(df['date'], df['workloads'], color='#5cb85c', alpha=0.8)
    
    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Number of Workloads')
    plt.title('Daily Workloads Over Time')
    
    # Format y-axis with commas for thousands
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Rotate date labels for better readability
    plt.xticks(rotation=45)
    
    # Tight layout
    plt.tight_layout()
    
    # Save the graph to a temporary location
    temp_dir = tempfile.gettempdir()
    graph_path = os.path.join(temp_dir, 'daily_workloads.png')
    plt.savefig(graph_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return graph_path

def generate_efficiency_graph():
    """
    Generate a graph showing block efficiency metrics over time
    """
    # Get efficiency data
    efficiency_data = get_block_efficiency()
    
    # Convert to DataFrame
    df = pd.DataFrame(efficiency_data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Set style
    sns.set(style="darkgrid")
    
    # Create the plot with dual y-axes
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    # Plot atom block ratio
    color = '#3366cc'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Atom Block Ratio', color=color)
    ax1.plot(df['date'], df['atom_block_ratio'], color=color, marker='o', linestyle='-', label='Atom Block Ratio')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(0, 1.0)  # Ratio is between 0 and 1
    
    # Create second y-axis for cost per workload
    ax2 = ax1.twinx()
    color = '#ff7f0e'
    ax2.set_ylabel('Cost per Workload ($)', color=color)
    ax2.plot(df['date'], df['cost_per_workload'], color=color, marker='s', linestyle='-', label='Cost per Workload')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.2f}'))
    
    # Title
    plt.title('Block Efficiency Metrics Over Time')
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    # Rotate date labels for better readability
    plt.xticks(rotation=45)
    
    # Tight layout
    fig.tight_layout()
    
    # Save the graph to a temporary location
    temp_dir = tempfile.gettempdir()
    graph_path = os.path.join(temp_dir, 'block_efficiency.png')
    plt.savefig(graph_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return graph_path