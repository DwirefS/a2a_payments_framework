from a2apay import Wallet
from a2apay.integrations.langchain_tool import A2APayAgentTool, A2APayInput
from langchain.tools import Tool

# Create wallets
payer = Wallet("UserAgent", balance=5000, currency="RLUSD")
receiver = Wallet("LangToolAgent", balance=0, currency="RLUSD")

# Initialize the tool with an A2A agent
tool = A2APayAgentTool(agent_name="LangToolAgent", agent_wallet=receiver)

# Simulate tool input: translate 'Hola' to English, price 500
args = A2APayInput(task="translate:Hola:EN", price=500, payer_wallet=payer)

# Run the tool manually
output = tool.run(args)

print("\n[LangChain Tool Output]")
print("Result:", output)
print("\n[Wallet Balances]")
print("Payer:", payer.balance)
print("Receiver:", receiver.balance)