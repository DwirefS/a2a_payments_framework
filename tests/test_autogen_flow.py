from a2apay import Wallet
from a2apay.integrations.autogen_adapter import AutoGenAgentAdapter

def test_autogen_agent_task_and_payment():
    alice_wallet = Wallet("Alice", balance=1000, currency="RLUSD")
    bob_wallet = Wallet("Bob", balance=0, currency="RLUSD")

    alice = AutoGenAgentAdapter("Alice", alice_wallet)
    bob = AutoGenAgentAdapter("Bob", bob_wallet)

    task = {
        "action": "translate",
        "text": "Hola",
        "lang": "EN",
        "reply_to_wallet": alice_wallet
    }
    price = 300

    result = bob.on_message("Alice", task, price)
    assert result["result"] == "Translated(Hola) to EN"
    assert alice_wallet.balance == 700
    assert bob_wallet.balance == 300