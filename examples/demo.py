from a2a import Agent, Wallet, ResourceProvider

alice = Agent("Alice", Wallet("Alice", balance=5000, currency="RLUSD"))
bob = Agent("Bob", Wallet("Bob", balance=0, currency="RLUSD"))
databank = ResourceProvider("DataBank", Wallet("DataBank", balance=0, currency="RLUSD"))
databank.set_resource("weather.csv", 250, "CSV_DATA")

print("--- Agent to Agent Task ---")
task = {"action": "translate", "text": "Bonjour", "lang": "EN"}
result = alice.request_task(bob, task, 500)
print("Result:", result["result"])
print(f"Alice Balance: {alice.wallet.balance}, Bob Balance: {bob.wallet.balance}")

print("\n--- Agent to Resource Provider ---")
data = databank.provide("weather.csv")
print("Data Received:", data)
alice.wallet.send(databank.wallet, databank.get_price("weather.csv"), memo="Payment for resource")
print(f"Alice Balance: {alice.wallet.balance}, DataBank Balance: {databank.wallet.balance}")
