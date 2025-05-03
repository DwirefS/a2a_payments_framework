from langchain.tools import BaseTool
from a2apay import Agent, Wallet
from typing import Optional, Type
from pydantic import BaseModel, Field, ConfigDict, PrivateAttr

class A2APayInput(BaseModel):
    task: str = Field(..., description="The task to perform, e.g. 'translate:Bonjour:EN'")
    price: int = Field(..., description="Payment amount in smallest currency unit (e.g. cents)")
    payer_wallet: Wallet = Field(..., description="Wallet of the requesting agent paying for the task")

    model_config = ConfigDict(arbitrary_types_allowed=True)

class A2APayAgentTool(BaseTool):
    name: str = "a2apay_agent_tool"
    description: str = "LangChain tool that wraps an A2APay agent with payment enforcement after task execution."
    args_schema: Type[BaseModel] = A2APayInput

    _agent: Agent = PrivateAttr()

    def __init__(self, agent_name: str, agent_wallet: Wallet):
        super().__init__()
        self._agent = Agent(agent_name, wallet=agent_wallet)

    def _run(self, input_data: A2APayInput) -> str:
        try:
            parts = input_data.task.split(":")
            if parts[0] == "translate":
                structured_task = {
                    "action": "translate",
                    "text": parts[1],
                    "lang": parts[2]
                }
                result = self._agent.handle_request(structured_task)
                input_data.payer_wallet.send(self._agent.wallet, input_data.price, memo="LangChain tool payment")
                return result["result"]
            else:
                return "Unsupported task."
        except Exception as e:
            return f"Error in A2APayAgentTool: {e}"