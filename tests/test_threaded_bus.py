import queue
import time
from a2apay import Wallet
from a2apay.messaging.threaded_bus import AgentThread

def test_threaded_agent_task_flow():
    alice_inbox = queue.Queue()
    bob_inbox = queue.Queue()

    alice_wallet = Wallet("Alice", balance=1000, currency="RLUSD")
    bob_wallet = Wallet("Bob", balance=0, currency="RLUSD")

    alice = AgentThread("Alice", wallet=alice_wallet, inbox=alice_inbox)
    bob = AgentThread("Bob", wallet=bob_wallet, inbox=bob_inbox)

    alice.start()
    bob.start()

    task = {
        "action": "translate",
        "text": "Bonjour",
        "lang": "EN",
        "payer_wallet": alice_wallet
    }
    price = 300

    bob_inbox.put(("Alice", task, price))
    time.sleep(2)

    alice.stop()
    bob.stop()
    alice.join()
    bob.join()

    assert alice_wallet.balance == 700
    assert bob_wallet.balance == 300
    assert len(alice_wallet.history) == 1
    assert len(bob_wallet.history) == 1