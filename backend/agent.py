from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from langchain.schema import AgentAction, AgentFinish
from langchain.memory import ConversationBufferMemory
from langchain.llms.base import BaseLLM
import re
from typing import List, Union, Any, Dict
import json

from llm_handler import init_llm
from data_processor import (
    get_top_active_qpc_blocks, 
    analyze_cost_impact, 
    get_daily_costs,
    get_qpu_summary,
    get_block_efficiency,
    get_daily_workloads
)
from visualization import generate_trend_graph, generate_workloads_graph, generate_efficiency_graph
from optimisation_strategies import optimize_block_mix, simulate_batch_scheduling, negotiate_costs

# Define the tools our agent can use
def get_tools():
    tools = [
        Tool(
            name="QPU_Block_Activity",
            func=get_top_active_qpc_blocks,
            description="Useful for finding the most active QPU blocks by number of workloads executed"
        ),
        Tool(
            name="Cost_Analysis",
            func=analyze_cost_impact,
            description="Useful for analyzing cost impact of using only Atom blocks"
        ),
        Tool(
            name="Cost_Trend_Graph",
            func=generate_trend_graph,
            description="Useful for generating a graph showing the trend of daily costs"
        ),
        Tool(
            name="Optimize_Block_Mix",
            func=optimize_block_mix,
            description="Estimates cost savings by increasing the ratio of Atom blocks to a target value"
        ),
        Tool(
            name="Batch_Scheduling",
            func=simulate_batch_scheduling,
            description="Simulates cost savings by batching daily workloads into multi-day windows"
        ),
        Tool(
            name="Negotiate_Costs",
            func=negotiate_costs,
            description="Estimates cost savings by negotiating a reduction in fixed cost components"
        ),
        # New tools
        Tool(
            name="QPU_Summary",
            func=get_qpu_summary,
            description="Returns summary statistics about QPU blocks and workloads (total blocks, avg workloads per block, etc.)"
        ),
        Tool(
            name="Block_Efficiency",
            func=get_block_efficiency,
            description="Returns efficiency metrics for different block types including cost per workload"
        ),
        Tool(
            name="Daily_Workloads",
            func=get_daily_workloads,
            description="Returns daily workload data for visualization purposes"
        ),
        Tool(
            name="Workloads_Graph",
            func=generate_workloads_graph,
            description="Generates a graph showing daily workloads over time"
        ),
        Tool(
            name="Efficiency_Graph",
            func=generate_efficiency_graph,
            description="Generates a graph showing block efficiency metrics over time"
        )
    ]
    return tools

# Define a custom prompt template
class QpcPromptTemplate(StringPromptTemplate):
    template: str
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""

        for action, observation in intermediate_steps:
            thoughts += f"Action: {action.tool}\nAction Input: {action.tool_input}\nObservation: {observation}\n"

        tools_str = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        kwargs["tools"] = tools_str
        kwargs["thoughts"] = thoughts
        return self.template.format(**kwargs)

# Define output parser for the agent
class QpcOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if the output indicates the agent is finished
        if "Final Answer:" in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        
        # Parse action and input
        regex = r"Action: (.*?)[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        
        if match:
            action = match.group(1).strip()
            action_input = match.group(2).strip()
            return AgentAction(tool=action, tool_input=action_input, log=llm_output)
        else:
            # If no action is found, return a default response
            return AgentFinish(
                return_values={"output": "I wasn't able to determine what to do next. Could you please clarify your question?"},
                log=llm_output,
            )

# Create the LLM and agent
def create_qpc_agent(llm=None):
    if llm is None:
        llm = init_llm()
    
    tools = get_tools()
    memory = ConversationBufferMemory(memory_key="chat_history")
    
    template = """You are a QPU Analysis agent that can answer questions about QPU blocks and costs.

Available tools:
{tools}

Use the following format:
Question: The question you need to answer
Thought: Consider what tools might help you answer this question
Action: The tool to use (must be one of the tool names listed above)
Action Input: Input for the tool
Observation: Result from using the tool
... (repeat Action/Action Input/Observation as needed)
Thought: Now I have the information to answer the question
Final Answer: The final answer to the original question

Chat History:
{chat_history}

{thoughts}

Question: {input}
{agent_scratchpad}
"""

    prompt = QpcPromptTemplate(
        template=template,
        tools=tools,
        input_variables=["input", "chat_history", "agent_scratchpad"]
    )
    
    output_parser = QpcOutputParser()
    
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["Observation:"],
        allowed_tools=[tool.name for tool in tools],
    )
    
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
    )
    
    return agent_executor

# Function to execute agent with a query
async def process_query_with_agent(query: str, history: List[Dict[str, str]]):
    agent_executor = create_qpc_agent()
    
    # Format history for agent
    chat_history = ""
    for entry in history:
        if 'user' in entry and entry['user']:
            chat_history += f"Human: {entry['user']}\n"
        if 'assistant' in entry and entry['assistant']:
            chat_history += f"AI: {entry['assistant']}\n"
    
    result = await agent_executor.arun(
        input=query,
        chat_history=chat_history
    )
    
    return result
