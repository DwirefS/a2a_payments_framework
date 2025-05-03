from langchain.tools import StructuredTool
from a2apay import Agent, Wallet
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# -----------------------------
# Integration Notes:
# -----------------------------
# Originally attempted to subclass `BaseTool` with args_schema and Pydantic v2
# - Failed due to LangChain internal inconsistencies in how .run() and ._run() are called
# - Unexpected TypeError: 'tool_input' missing even with correct args_schema
# Resolution:
# ✅ Use StructuredTool which bypasses _run complexity and is agent-compatible by default
# ✅ Clean, stable interface with predictable behavior

class A2APayInput(BaseModel):
    task: str = Field(..., description="A string like 'translate:Bonjour:EN'")
    price: int = Field(..., description="Amount to pay for task (in smallest units)")
    payer_wallet: Wallet = Field(..., description="Wallet that will send payment")

    model_config = ConfigDict(arbitrary_types_allowed=True)

def a2apay_agent_tool_runner(task: str, price: int, payer_wallet: Wallet, agent_name: str, agent_wallet: Wallet) -> str:
    try:
        parts = task.split(":")
        if parts[0] == "translate":
            agent = Agent(agent_name, wallet=agent_wallet)
            structured_task = {
                "action": "translate",
                "text": parts[1],
                "lang": parts[2]
            }
            result = agent.handle_request(structured_task)
            payer_wallet.send(agent.wallet, price, memo="LangChain StructuredTool payment")
            return result["result"]
        return "Unsupported task."
    except Exception as e:
        return f"Error in structured tool: {e}"

def create_a2apay_agent_tool(agent_name: str, agent_wallet: Wallet) -> StructuredTool:
    return StructuredTool.from_function(
        name="a2apay_agent_tool",
        description="Executes a paid task using an A2A agent. Task format: 'translate:Bonjour:EN'",
        func=lambda task, price, payer_wallet: a2apay_agent_tool_runner(task, price, payer_wallet, agent_name, agent_wallet),
        args_schema=A2APayInput,
    )