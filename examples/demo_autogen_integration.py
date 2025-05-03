from a2apay import Wallet
from a2apay.integrations.autogen_adapter import AutoGenAgentAdapter

# Setup two AutoGen-compatible agents
alice_wallet = Wallet("Alice", balance=5000, currency="RLUSD")
bob_wallet = Wallet("Bob", balance=0, currency="RLUSD")

alice = AutoGenAgentAdapter("Alice", alice_wallet)
bob = AutoGenAgentAdapter("Bob", bob_wallet)

# Simulate message: Alice sends task to Bob
task = {
    "action": "translate",
    "text": "Bonjour",
    "lang": "EN",
    "reply_to_wallet": alice_wallet  # For mock send-back, not real AutoGen wiring yet
}
price = 500

# Execute task and payment manually (mock AutoGen loop)
result = bob.on_message("Alice", task, price)
print("[Result]", result)
print("[Balances]")
print("Alice:", alice_wallet.balance)
print("Bob:", bob_wallet.balance)