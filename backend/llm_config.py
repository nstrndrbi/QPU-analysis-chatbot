from dataclasses import dataclass
from typing import Dict, Any, Optional, List

@dataclass
class ModelConfig:
    """Configuration for LLM models"""
    model_id: str
    max_new_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.95
    repetition_penalty: float = 1.15
    streaming: bool = False
    use_cache: bool = True
    device_map: str = "auto"

# Available models configuration
AVAILABLE_MODELS = {
    "gpt2": ModelConfig(
        model_id="gpt2",
        max_new_tokens=512,
    ),
    "gpt2-medium": ModelConfig(
        model_id="gpt2-medium",
        max_new_tokens=768,
    ),
    "facebook/opt-350m": ModelConfig(
        model_id="facebook/opt-350m",
        max_new_tokens=512,
    ),
    "facebook/opt-1.3b": ModelConfig(
        model_id="facebook/opt-1.3b",
        max_new_tokens=512,
    ),
    "google/flan-t5-base": ModelConfig(
        model_id="google/flan-t5-base",
        max_new_tokens=256,
    ),
    "google/flan-t5-large": ModelConfig(
        model_id="google/flan-t5-large",
        max_new_tokens=256,
    ),
}

# Default model to use
DEFAULT_MODEL = "gpt2"

# System prompt templates for different tasks
SYSTEM_PROMPTS = {
    "qpc_analysis": """You are an AI assistant specialized in analyzing Quantum Processing Center (QPC) blocks and costs.
You can provide insights on workload distribution, cost analysis, and performance metrics.
Be precise, helpful, and provide data-backed explanations.""",
    
    "cost_analysis": """You are a cost optimization specialist for Quantum Processing Centers (QPC).
Analyze cost data and provide insights on how to optimize resource allocation and reduce expenses.
Provide concrete recommendations based on the data.""",
    
    "general": """You are an AI assistant specializing in Quantum Processing Centers (QPC).
Answer questions clearly and concisely based on the available data.
If you don't know the answer, be honest about your limitations."""
}

def get_model_config(model_name: Optional[str] = None) -> ModelConfig:
    """Get the configuration for the specified model or default model"""
    if not model_name:
        model_name = DEFAULT_MODEL
    
    if model_name not in AVAILABLE_MODELS:
        raise ValueError(f"Model {model_name} not found in available models")
    
    return AVAILABLE_MODELS[model_name]
