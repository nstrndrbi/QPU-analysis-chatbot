import pandas as pd
import json
import os
from typing import Dict, List, Any

# Sample data - in a real scenario, this would come from a database or API
def get_sample_data():
    # This is mockup data - replace with actual data loading in production
    sample_data = {
        "qpc_blocks": [
            {"id": "qpc001", "type": "Quantum", "workloads_executed": 1250, "cost_per_hour": 120},
            {"id": "qpc002", "type": "Atom", "workloads_executed": 980, "cost_per_hour": 45},
            {"id": "qpc003", "type": "Quantum", "workloads_executed": 1500, "cost_per_hour": 130},
            {"id": "qpc004", "type": "Atom", "workloads_executed": 850, "cost_per_hour": 40},
            {"id": "qpc005", "type": "Quantum", "workloads_executed": 1750, "cost_per_hour": 125},
            {"id": "qpc006", "type": "Atom", "workloads_executed": 920, "cost_per_hour": 42},
            {"id": "qpc007", "type": "Quantum", "workloads_executed": 1100, "cost_per_hour": 115},
            {"id": "qpc008", "type": "Atom", "workloads_executed": 1050, "cost_per_hour": 48},
            {"id": "qpc009", "type": "Quantum", "workloads_executed": 1300, "cost_per_hour": 128},
            {"id": "qpc010", "type": "Atom", "workloads_executed": 990, "cost_per_hour": 46},
            {"id": "qpc011", "type": "Quantum", "workloads_executed": 1450, "cost_per_hour": 135},
            {"id": "qpc012", "type": "Atom", "workloads_executed": 930, "cost_per_hour": 44},
        ],
        "daily_costs": [
            {"date": "2023-09-01", "total_cost": 12500},
            {"date": "2023-09-02", "total_cost": 13200},
            {"date": "2023-09-03", "total_cost": 12800},
            {"date": "2023-09-04", "total_cost": 14500},
            {"date": "2023-09-05", "total_cost": 15200},
            {"date": "2023-09-06", "total_cost": 14800},
            {"date": "2023-09-07", "total_cost": 15500},
        ]
    }
    return sample_data

# Get top 10 most active QPC blocks
def get_top_active_qpc_blocks():
    data = get_sample_data()
    df = pd.DataFrame(data["qpc_blocks"])
    top_blocks = df.sort_values(by="workloads_executed", ascending=False).head(10)
    
    result = ""
    for i, row in top_blocks.iterrows():
        result += f"{i+1}. Block ID: {row['id']} (Type: {row['type']}), Workloads: {row['workloads_executed']}\n"
    
    return result

# Analyze cost impact of using only Atom blocks
def analyze_cost_impact():
    data = get_sample_data()
    df = pd.DataFrame(data["qpc_blocks"])
    
    current_total_cost = (df["workloads_executed"] * df["cost_per_hour"]).sum()
    
    # Calculate the cost if only using Atom blocks
    atom_blocks = df[df["type"] == "Atom"]
    quantum_blocks = df[df["type"] == "Quantum"]
    
    # For simplicity, assume workloads would be distributed proportionally among Atom blocks
    total_quantum_workloads = quantum_blocks["workloads_executed"].sum()
    atom_workload_increase = total_quantum_workloads / len(atom_blocks)
    
    atom_only_cost = ((atom_blocks["workloads_executed"] + atom_workload_increase) * atom_blocks["cost_per_hour"]).sum()
    
    cost_difference = current_total_cost - atom_only_cost
    percentage = (cost_difference / current_total_cost) * 100
    
    if cost_difference > 0:
        return f"Using only Atom blocks would save approximately ${cost_difference:.2f}, which is {percentage:.1f}% of your current costs."
    else:
        return f"Using only Atom blocks would increase costs by approximately ${-cost_difference:.2f}, which is {-percentage:.1f}% more than your current costs."

# Get daily costs data for graph generation
def get_daily_costs():
    data = get_sample_data()
    return data["daily_costs"]
