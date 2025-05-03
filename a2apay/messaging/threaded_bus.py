import threading
import queue
import time
from a2apay import Agent, Wallet

class AgentThread(threading.Thread):
    def __init__(self, name: str, wallet: Wallet, inbox: queue.Queue):
        super().__init__(name=name)
        self.agent = Agent(name, wallet)
        self.inbox = inbox
        self.running = True

    def run(self):
        print(f"[{self.name}] Agent thread started.")
        while self.running:
            try:
                sender, task, price = self.inbox.get(timeout=1)
                print(f"[{self.name}] Received task from {sender}: {task}")
                result = self.agent.handle_request(task)
                print(f"[{self.name}] Task result: {result['result']}")
                # Correct: sender (requestor) pays this agent
                payer_wallet = task.get("payer_wallet")
                if payer_wallet:
                    payer_wallet.send(self.agent.wallet, price, memo="Threaded payment")
                self.inbox.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[{self.name}] Error processing task: {e}")

    def stop(self):
        self.running = False