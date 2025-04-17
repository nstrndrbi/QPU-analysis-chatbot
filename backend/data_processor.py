import pandas as pd
import json
import os
from typing import Dict, List, Any

# Sample data - in a real scenario, this would come from a database or API
def get_sample_data():
    # This is mockup data - replace with actual data loading in production
    # sample_data = {
    #     "qpc_blocks": [
    #         {"id": "qpc001", "type": "Quantum", "workloads_executed": 1250, "cost_per_hour": 120},
    #         {"id": "qpc002", "type": "Atom", "workloads_executed": 980, "cost_per_hour": 45},
    #         {"id": "qpc003", "type": "Quantum", "workloads_executed": 1500, "cost_per_hour": 130},
    #         {"id": "qpc004", "type": "Atom", "workloads_executed": 850, "cost_per_hour": 40},
    #         {"id": "qpc005", "type": "Quantum", "workloads_executed": 1750, "cost_per_hour": 125},
    #         {"id": "qpc006", "type": "Atom", "workloads_executed": 920, "cost_per_hour": 42},
    #         {"id": "qpc007", "type": "Quantum", "workloads_executed": 1100, "cost_per_hour": 115},
    #         {"id": "qpc008", "type": "Atom", "workloads_executed": 1050, "cost_per_hour": 48},
    #         {"id": "qpc009", "type": "Quantum", "workloads_executed": 1300, "cost_per_hour": 128},
    #         {"id": "qpc010", "type": "Atom", "workloads_executed": 990, "cost_per_hour": 46},
    #         {"id": "qpc011", "type": "Quantum", "workloads_executed": 1450, "cost_per_hour": 135},
    #         {"id": "qpc012", "type": "Atom", "workloads_executed": 930, "cost_per_hour": 44},
    #     ],
    #     "daily_costs": [
    #         {"date": "2023-09-01", "total_cost": 12500},
    #         {"date": "2023-09-02", "total_cost": 13200},
    #         {"date": "2023-09-03", "total_cost": 12800},
    #         {"date": "2023-09-04", "total_cost": 14500},
    #         {"date": "2023-09-05", "total_cost": 15200},
    #         {"date": "2023-09-06", "total_cost": 14800},
    #         {"date": "2023-09-07", "total_cost": 15500},
    #     ]
    # }
    #sample_data = pd.read_csv('data/simulated_qpu_data_enhanced.csv')
    sample_data = pd.read_csv('data/qpu_dataset_hybrid.csv')
    
    return sample_data

def get_top_active_qpc_blocks():
    df = get_sample_data()
    top_days = df.sort_values(by="daily_workloads", ascending=False).head(10)
    
    result = ""
    for i, row in top_days.iterrows():
        result += f"{i+1}. Date: {row['date']}, Workloads: {row['daily_workloads']}\n"
    
    return result

def analyze_cost_impact():
    df = get_sample_data()

    total_cost = df["total_daily_cost"].sum()
    total_workloads = df["daily_workloads"].sum()

    # Hypothetical: assume all workloads were done on Atom blocks
    # Use a ratio of Atom blocks to total blocks to estimate cost impact
    atom_ratio = df["new_blocks_atom"].sum() / df["new_blocks_total"].sum()
    
    estimated_atom_cost_per_workload = df["cost_per_workload"].mean() * atom_ratio
    estimated_total_cost = estimated_atom_cost_per_workload * total_workloads

    cost_difference = total_cost - estimated_total_cost
    percentage = (cost_difference / total_cost) * 100

    if cost_difference > 0:
        return f"Using only Atom blocks would save approximately ${cost_difference:,.2f}, which is {percentage:.1f}% of your current costs."
    else:
        return f"Using only Atom blocks would increase costs by approximately ${-cost_difference:,.2f}, which is {-percentage:.1f}% more than your current costs."


def get_daily_costs():
    df = get_sample_data()
    return df[["date", "total_daily_cost"]]

# New summary functions
def get_qpu_summary():
    """
    Returns summary statistics about QPU blocks and workloads
    """
    df = get_sample_data()
    
    total_blocks = df['new_blocks_total'].sum()
    atom_blocks = df['new_blocks_atom'].sum()
    photon_blocks = df['new_blocks_photon'].sum() if 'new_blocks_photon' in df.columns else 0
    spin_blocks = df['new_blocks_spin'].sum() if 'new_blocks_spin' in df.columns else 0
    
    total_workloads = df['daily_workloads'].sum()
    avg_workloads_per_block = total_workloads / total_blocks if total_blocks > 0 else 0
    
    days_count = len(df)
    avg_daily_workloads = total_workloads / days_count if days_count > 0 else 0
    
    summary = {
        "total_blocks_leased": int(total_blocks),
        "atom_blocks": int(atom_blocks),
        "photon_blocks": int(photon_blocks),
        "spin_blocks": int(spin_blocks),
        "total_workloads": int(total_workloads),
        "avg_workloads_per_block": round(avg_workloads_per_block, 2),
        "avg_daily_workloads": round(avg_daily_workloads, 2),
        "days_analyzed": days_count
    }
    
    return summary

def get_block_efficiency():
    """
    Calculate efficiency metrics for different block types
    """
    df = get_sample_data()
    
    # Group by date to get daily figures
    daily_stats = []
    
    for _, row in df.iterrows():
        atom_ratio = row['new_blocks_atom'] / row['new_blocks_total'] if row['new_blocks_total'] > 0 else 0
        cost_per_workload = row['total_daily_cost'] / row['daily_workloads'] if row['daily_workloads'] > 0 else 0
        
        daily_stats.append({
            "date": row['date'],
            "atom_block_ratio": round(atom_ratio, 2),
            "cost_per_workload": round(cost_per_workload, 2),
            "daily_workloads": int(row['daily_workloads']),
            "total_cost": float(row['total_daily_cost'])
        })
    
    return daily_stats

def get_daily_workloads():
    """
    Return daily workload data suitable for visualization
    """
    df = get_sample_data()
    result = []
    
    for _, row in df.iterrows():
        result.append({
            "date": row['date'],
            "workloads": int(row['daily_workloads'])
        })
    
    return result
