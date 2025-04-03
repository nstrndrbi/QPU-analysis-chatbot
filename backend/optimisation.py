import pandas as pd

# Cost parameters (daily lease cost assumes 24 hours)
LEASE_COST_PER_HOUR = {
    'Atom': 3.00,
    'Photon': 1.50,
    'Spin': 0.40
}

WORKLOAD_EXECUTION_COST = {
    'Atom': 0.01,
    'Photon': 0.05,
    'Spin': 0.20
}

# Workload trigger cost (same for all categories)
WORKLOAD_TRIGGER_COST = 0.01

def compute_block_cost(qpu_units, workload_count, category, hours=24):
    """
    Compute the daily cost for a block given:
      - qpu_units: Number of QPU units in the block.
      - workload_count: Number of workloads executed on that block.
      - category: The block category ('Atom', 'Photon', or 'Spin').
      
    The cost includes:
      - Lease fee: lease rate * hours * qpu_units
      - Workload execution cost: execution rate * qpu_units * workload_count
      - Workload trigger cost: flat rate per workload trigger
    """
    lease_fee = LEASE_COST_PER_HOUR[category] * hours * qpu_units
    execution_cost = WORKLOAD_EXECUTION_COST[category] * qpu_units * workload_count
    trigger_cost = WORKLOAD_TRIGGER_COST * workload_count
    return lease_fee + execution_cost + trigger_cost

def optimize_block_category(qpu_units, workload_count):
    """
    For a given block, compute the cost in each category and return the category
    that minimizes the cost along with that cost value.
    """
    best_category = None
    best_cost = float('inf')
    
    for cat in ['Atom', 'Photon', 'Spin']:
        cost = compute_block_cost(qpu_units, workload_count, cat)
        if cost < best_cost:
            best_cost = cost
            best_category = cat
            
    return best_category, best_cost

def optimize_distribution(df):
    """
    Given a DataFrame 'df' with the following columns:
      - 'block_id': Unique identifier for the block.
      - 'qpu_units': The number of QPU units in the block.
      - 'workload_count': The number of workloads executed on that block.
    
    This function computes the optimal category for each block (minimizing the daily cost)
    and adds two new columns:
      - 'optimal_category'
      - 'optimal_cost'
    """
    # Apply the optimization function row by row
    optimal_results = df.apply(
        lambda row: optimize_block_category(row['qpu_units'], row['workload_count']),
        axis=1
    )
    df[['optimal_category', 'optimal_cost']] = pd.DataFrame(optimal_results.tolist(), index=df.index)
    return df

def compute_daily_total_cost(df, hours=24):
    """
    Compute the total daily cost for all blocks in the DataFrame using their optimal category.
    Adds a 'daily_cost' column for each block.
    """
    def block_daily_cost(row):
        # Use the optimal category computed by optimize_distribution
        return compute_block_cost(row['qpu_units'], row['workload_count'], row['optimal_category'], hours)
    
    df['daily_cost'] = df.apply(block_daily_cost, axis=1)
    total_cost = df['daily_cost'].sum()
    return total_cost

# Example usage:
if __name__ == "__main__":
    # Replace the following dummy data with your CSV file loading if needed:
    data = {
        'block_id': [1, 2, 3],
        'qpu_units': [1000, 5000, 2000],
        'workload_count': [100, 50, 200]
    }
    df = pd.DataFrame(data)
    
    print("Before optimization:")
    print(df)
    
    # Optimize the category for each block
    df_optimized = optimize_distribution(df.copy())
    print("\nAfter optimization:")
    print(df_optimized)
    
    # Compute total daily cost using the optimal category assignments
    total_cost = compute_daily_total_cost(df_optimized)
    print(f"\nTotal daily cost (optimized): ${total_cost:.2f}")
