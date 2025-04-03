from data_processor import get_sample_data

def optimize_block_mix(target_atom_ratio=0.8):
    """
    Estimate cost savings by increasing the proportion of Atom blocks.
    The simulation assumes that if the overall Atom block ratio increases,
    the effective cost per workload reduces proportionally (up to a maximum of 10% reduction).
    
    Parameters:
        target_atom_ratio (float): Desired overall ratio of Atom blocks (e.g., 0.8 for 80%)
    
    Returns:
        str: A message with the estimated cost savings.
    """
    df = get_sample_data()
    # Calculate the current overall Atom ratio
    overall_current_ratio = df['new_blocks_atom'].sum() / df['new_blocks_total'].sum()
    
    # Determine improvement factor (max 10% reduction)
    if overall_current_ratio >= target_atom_ratio:
        improvement_factor = 0.0
    else:
        improvement_factor = (target_atom_ratio - overall_current_ratio) * 0.10 / (1 - overall_current_ratio)
        improvement_factor = min(improvement_factor, 0.10)
    
    # Estimate new total cost based on the cost improvement factor
    current_total_cost = df['total_daily_cost'].sum()
    new_total_cost = current_total_cost * (1 - improvement_factor)
    cost_saving = current_total_cost - new_total_cost
    
    return (f"By increasing the Atom block ratio to {target_atom_ratio*100:.1f}%, "
            f"estimated cost savings are approximately ${cost_saving:,.2f} "
            f"({improvement_factor*100:.1f}% reduction in cost per workload).")

def simulate_batch_scheduling(batch_window=3):
    """
    Simulate cost savings by batching daily workloads over a specified window.
    This strategy assumes that fixed costs (acquisition, lease, workload trigger)
    can be incurred once per batch, while variable costs remain proportional to workload.
    
    Parameters:
        batch_window (int): Number of days to batch together.
    
    Returns:
        str: A message with the estimated cost savings.
    """
    df = get_sample_data()
    n = len(df)
    batches = [df.iloc[i:i+batch_window] for i in range(0, n, batch_window)]
    
    original_total_cost = df['total_daily_cost'].sum()
    new_total_cost = 0
    
    for batch in batches:
        # Sum variable cost (assumed to be workload_execution_cost)
        variable_cost = batch['workload_execution_cost'].sum()
        # Fixed cost for the batch: use the fixed costs from the first day of the batch
        fixed_cost = (batch.iloc[0]['acquisition_cost'] +
                      batch.iloc[0]['lease_fee_cost'] +
                      batch.iloc[0]['workload_trigger_cost'])
        new_total_cost += variable_cost + fixed_cost
    
    cost_saving = original_total_cost - new_total_cost
    percentage = (cost_saving / original_total_cost) * 100
    
    return (f"Batch scheduling every {batch_window} days could save approximately "
            f"${cost_saving:,.2f} ({percentage:.1f}% reduction in costs) over the period.")

def negotiate_costs(reduction_percent=10):
    """
    Estimate cost savings by negotiating a reduction in fixed cost components:
    acquisition_cost, lease_fee_cost, and workload_trigger_cost.
    
    Parameters:
        reduction_percent (float): The percentage reduction to apply to the fixed costs.
    
    Returns:
        str: A message with the estimated cost savings.
    """
    df = get_sample_data()
    
    # Original fixed cost components per day and their total sum
    fixed_costs = df['acquisition_cost'] + df['lease_fee_cost'] + df['workload_trigger_cost']
    original_total_fixed_cost = fixed_costs.sum()
    
    # Apply the reduction
    new_fixed_cost = fixed_costs * (1 - reduction_percent/100)
    new_total_fixed_cost = new_fixed_cost.sum()
    
    # Variable cost remains the same (workload_execution_cost)
    variable_cost_total = df['workload_execution_cost'].sum()
    
    original_total_cost = original_total_fixed_cost + variable_cost_total
    new_total_cost = new_total_fixed_cost + variable_cost_total
    
    cost_saving = original_total_cost - new_total_cost
    percentage = (cost_saving / original_total_cost) * 100
    
    return (f"Negotiating a {reduction_percent}% reduction in fixed costs could save approximately "
            f"${cost_saving:,.2f} ({percentage:.1f}% reduction in total costs) over the period.")
