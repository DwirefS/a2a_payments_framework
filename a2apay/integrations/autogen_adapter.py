from a2apay import Agent, Wallet

class AutoGenAgentAdapter:
    """Wraps an A2APay agent to simulate AutoGen-style communication."""

    def __init__(self, name: str, wallet: Wallet):
        self.name = name
        self.wallet = wallet
        self.agent = Agent(name, wallet=wallet)

    def on_message(self, sender: str, task: dict, price: int, payer_wallet: Wallet) -> dict:
        """Process task, send result, and trigger payment from payer_wallet."""
        print(f"[{self.name}] Received task from {sender}: {task}")
        result = self.agent.handle_request(task)
        print(f"[{self.name}] Task result: {result['result']}")
        payer_wallet.send(self.wallet, price, memo="AutoGen adapter payment")
        return result