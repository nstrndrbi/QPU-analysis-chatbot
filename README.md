# QPU Analysis Chatbot

This project implements a sophisticated LLM-based chatbot for QPU (Quantum Processing Unit) analysis. It uses LangChain and Hugging Face models to answer questions about QPC blocks, costs, and trends.

## Features

- Interactive chat interface with LLM-powered responses
- Analysis of QPU block activity 
- Cost impact analysis
- Dynamic graph generation for cost trends
- Agentic AI framework using LangChain

## Architecture

The project consists of:

- **Backend**: FastAPI application with LangChain integration
- **Frontend**: React-based chat interface
- **LLM Integration**: Uses Hugging Face models for natural language understanding
- **Data Processing**: Sample data processing for QPC analysis
- **Visualization**: Dynamic graph generation using Matplotlib

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js and npm (for local frontend development)
- Python 3.8+ (for local backend development)

### Running with Docker Compose

1. Clone the repository
2. Navigate to the project directory
3. Run the application:

```bash
docker-compose up -d
```

4. Access the application at http://localhost:3000

### Running Locally

#### Backend

1. Navigate to the backend directory:

```bash
cd backend
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the backend:

```bash
python main.py
```

#### Frontend

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Run the frontend:

```bash
npm start
```

4. Access the application at http://localhost:3000

## Sample Questions

The chatbot can answer questions like:

- "Tell me the top 10 most active QPU blocks"
- "What will happen to the cost if I only use Atom blocks?"
- "Generate a graph to show the trend of daily costs"

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- LangChain for providing the agentic AI framework
- Hugging Face for providing the LLM models
- React for the frontend framework
