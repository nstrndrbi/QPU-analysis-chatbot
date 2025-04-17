from langchain import LLMChain, PromptTemplate
from langchain.llms import HuggingFacePipeline
from langchain.memory import ConversationBufferMemory
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from typing import List, Dict

# Initialize the language model
def init_llm():
    model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"  # You can replace with any preferred Hugging Face model
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.95,
        repetition_penalty=1.15
    )
    
    llm = HuggingFacePipeline(pipeline=pipe)
    return llm

# Process user query with LLM
async def process_query_with_llm(query: str, history: List[Dict[str, str]]):
    llm = init_llm()
    
    # Create a template for the LLM prompt
    template = """
    You are an AI assistant specialized in answering questions about QPU (Quantum Processing Unit) blocks and cost analysis.
    
    Chat History:
    {history}
    
    Human: {query}
    AI: 
    """
    
    # Format the history for the template
    formatted_history = ""
    for entry in history:
        formatted_history += f"Human: {entry['user']}\nAI: {entry['assistant']}\n"
    
    prompt = PromptTemplate(
        input_variables=["history", "query"],
        template=template
    )
    
    # Create the chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Run the chain
    response = chain.run(history=formatted_history, query=query)
    return response.strip()
