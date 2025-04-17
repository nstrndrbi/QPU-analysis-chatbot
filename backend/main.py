"""
Main entry point for the QPU Analysis Chatbot backend
"""
import argparse
import os
import uvicorn
import logging
from data_handler import QPUDataHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="QPU Analysis Chatbot Backend")
    parser.add_argument(
        "--host", 
        type=str, 
        default="0.0.0.0", 
        help="Host to run the server on"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to run the server on"
    )
    parser.add_argument(
        "--reload", 
        action="store_true", 
        help="Enable auto-reload on code changes"
    )
    parser.add_argument(
        "--data-path", 
        type=str, 
        default="./data/qpc_data.json", 
        help="Path to QPU data JSON file"
    )
    return parser.parse_args()

def main():
    """Main entry point"""
    args = parse_args()
    
    # Initialize data handler with provided data path
    data_handler = QPUDataHandler(data_path=args.data_path)
    data_handler.load_data()  # Pre-load data
    
    logger.info(f"Starting QPU Analysis Chatbot backend on {args.host}:{args.port}")
    logger.info(f"Using data path: {args.data_path}")
    
    # Start the FastAPI server
    uvicorn.run(
        "app:app", 
        host=args.host, 
        port=args.port, 
        reload=args.reload
    )

if __name__ == "__main__":
    main()
