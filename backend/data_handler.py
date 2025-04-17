import pandas as pd
import json
import os
from typing import Dict, List, Any, Optional
import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QPUDataHandler:
    """
    Handles loading, saving, and processing of QPU related data
    """
    def __init__(self, data_path: Optional[str] = None):
        self.data_path = data_path
        self._data = None
        
    def load_data(self, force_reload: bool = False) -> Dict[str, Any]:
        """
        Load QPU data from file or use mock data if file doesn't exist
        """
        if self._data is not None and not force_reload:
            return self._data
        
        if self.data_path and os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r') as f:
                    self._data = json.load(f)
                logger.info(f"Data loaded from {self.data_path}")
            except Exception as e:
                logger.error(f"Error loading data from {self.data_path}: {e}")
                self._data = self._generate_mock_data()
        else:
            logger.info("Using mock data")
            self._data = self._generate_mock_data()
            
            # Save mock data if path is provided
            if self.data_path:
                self.save_data()
                
        return self._data
    
    def save_data(self) -> bool:
        """
        Save current data to file
        """
        if not self.data_path or not self._data:
            return False
        
        try:
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            with open(self.data_path, 'w') as f:
                json.dump(self._data, f, indent=2)
            logger.info(f"Data saved to {self.data_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving data to {self.data_path}: {e}")
            return False
    
    def _generate_mock_data(self) -> Dict[str, Any]:
        """
        Generate mock data for QPU analysis
        """
        # Generate QPU blocks data
        QPU_blocks = []
        
        # Quantum blocks (higher cost, higher capacity)
        for i in range(1, 8):
            QPU_blocks.append({
                "id": f"QPU{i:03d}",
                "type": "Quantum",
                "workloads_executed": 1000 + (i * 100) + (i * 50 * (i % 3)),
                "cost_per_hour": 110 + (i * 5),
                "capacity": 300 + (i * 30),
                "uptime_percentage": 98.5 - (i * 0.5 * (i % 2))
            })
            
        # Atom blocks (lower cost, lower capacity)
        for i in range(8, 15):
            QPU_blocks.append({
                "id": f"QPU{i:03d}",
                "type": "Atom",
                "workloads_executed": 800 + (i * 30) + (i * 20 * (i % 4)),
                "cost_per_hour": 40 + (i * 2),
                "capacity": 150 + (i * 15),
                "uptime_percentage": 99.5 - (i * 0.2 * (i % 3))
            })
        
        # Generate daily cost data for the last 30 days
        daily_costs = []
        base_date = datetime.datetime.now() - datetime.timedelta(days=30)
        base_cost = 10000
        
        for i in range(30):
            current_date = base_date + datetime.timedelta(days=i)
            # Create some variation in daily costs
            variation = (i % 7) * 300 + (i % 3) * 500
            # Add a trend component
            trend = i * 100
            
            daily_costs.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "total_cost": base_cost + variation + trend,
                "quantum_cost": int((base_cost + variation + trend) * 0.7),
                "atom_cost": int((base_cost + variation + trend) * 0.3)
            })
        
        # Generate workload history
        workload_history = []
        
        for i in range(30):
            current_date = base_date + datetime.timedelta(days=i)
            
            workload_history.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "total_workloads": 5000 + (i * 100) + (i % 7) * 300,
                "successful_workloads": 4800 + (i * 95) + (i % 7) * 280,
                "failed_workloads": 200 + (i * 5) + (i % 7) * 20
            })
        
        return {
            "QPU_blocks": QPU_blocks,
            "daily_costs": daily_costs,
            "workload_history": workload_history,
            "last_updated": datetime.datetime.now().isoformat()
        }
    
    def get_QPU_blocks_df(self) -> pd.DataFrame:
        """
        Return QPU blocks data as a pandas DataFrame
        """
        data = self.load_data()
        return pd.DataFrame(data["QPU_blocks"])
    
    def get_daily_costs_df(self) -> pd.DataFrame:
        """
        Return daily costs data as a pandas DataFrame
        """
        data = self.load_data()
        df = pd.DataFrame(data["daily_costs"])
        df["date"] = pd.to_datetime(df["date"])
        return df
    
    def get_workload_history_df(self) -> pd.DataFrame:
        """
        Return workload history data as a pandas DataFrame
        """
        data = self.load_data()
        df = pd.DataFrame(data["workload_history"])
        df["date"] = pd.to_datetime(df["date"])
        return df
    
    def get_top_blocks(self, n: int = 10, metric: str = "workloads_executed") -> pd.DataFrame:
        """
        Return top N blocks by specified metric
        """
        df = self.get_QPU_blocks_df()
        return df.sort_values(by=metric, ascending=False).head(n)
    
    def get_block_types_summary(self) -> pd.DataFrame:
        """
        Return summary statistics by block type
        """
        df = self.get_QPU_blocks_df()
        return df.groupby("type").agg({
            "workloads_executed": ["sum", "mean", "std"],
            "cost_per_hour": ["sum", "mean", "std"],
            "capacity": ["sum", "mean", "std"],
            "uptime_percentage": ["mean", "min", "max"]
        })

# Create a singleton instance for easy import
QPU_data_handler = QPUDataHandler()
