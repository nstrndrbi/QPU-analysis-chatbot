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
