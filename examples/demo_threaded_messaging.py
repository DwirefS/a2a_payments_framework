import queue
import time
from a2apay import Wallet
from a2apay.messaging.threaded_bus import AgentThread

# Create shared queues
alice_inbox = queue.Queue()
bob_inbox = queue.Queue()

# Create wallets
alice_wallet = Wallet("Alice", balance=5000, currency="RLUSD")
bob_wallet = Wallet("Bob", balance=0, currency="RLUSD")

# Create agent threads
alice = AgentThread("Alice", wallet=alice_wallet, inbox=alice_inbox)
bob = AgentThread("Bob", wallet=bob_wallet, inbox=bob_inbox)

# Start agents
alice.start()
bob.start()

# Simulate task from Alice to Bob
task = {
    "action": "translate",
    "text": "Hola",
    "lang": "EN",
    "payer_wallet": alice_wallet  # Alice pays Bob
}
price = 750

# Alice sends task to Bob's inbox
bob_inbox.put(("Alice", task, price))

# Allow some time for processing
time.sleep(2)

# Stop agents
alice.stop()
bob.stop()
alice.join()
bob.join()

# Final balances
print("\n[Final Balances]")
print(f"Alice: {alice_wallet.balance} RLUSD")
print(f"Bob:   {bob_wallet.balance} RLUSD")