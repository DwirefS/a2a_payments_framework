from a2apay import Agent, Wallet
from typing import Any

class AutoGenAgentAdapter:
    def __init__(self, name: str, wallet: Wallet):
        self.agent = Agent(name, wallet)
        self.name = name

    def on_message(self, sender: str, task: dict, price: int) -> dict:
        print(f"[AutoGenAdapter] Received task from {sender}: {task}")
        result = self.agent.handle_request(task)
        self.agent.wallet.send(to_wallet=task.get("reply_to_wallet"), amount=price, memo="AutoGen payment")
        return result