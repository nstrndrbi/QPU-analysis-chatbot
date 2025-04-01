import matplotlib.pyplot as plt
import pandas as pd
import os
from data_processor import get_daily_costs
import tempfile
import seaborn as sns

def generate_trend_graph():
    # Get the daily costs data
    daily_costs = get_daily_costs()
    
    # Convert to DataFrame
    df = pd.DataFrame(daily_costs)
    df['date'] = pd.to_datetime(df['date'])
    
    # Set style
    sns.set(style="darkgrid")
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['total_cost'], marker='o', linewidth=2, color='#3366cc')
    
    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Daily Cost ($)')
    plt.title('Trend of Daily Costs')
    
    # Format y-axis as currency
    plt.gca().yaxis.set_major_formatter('${x:,.0f}')
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Rotate date labels for better readability
    plt.xticks(rotation=45)
    
    # Tight layout
    plt.tight_layout()
    
    # Create a temporary file to save the graph
    temp_dir = tempfile.gettempdir()
    graph_path = os.path.join(temp_dir, 'daily_costs_trend.png')
    plt.savefig(graph_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return graph_path
