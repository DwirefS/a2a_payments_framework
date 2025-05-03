from a2apay import Wallet
from a2apay.integrations.autogen_adapter import AutoGenAgentAdapter

def test_autogen_adapter_task_and_payment():
    payer = Wallet("Payer", balance=1000, currency="RLUSD")
    receiver = Wallet("Receiver", balance=0, currency="RLUSD")

    agent = AutoGenAgentAdapter(name="Receiver", wallet=receiver)

    task = {
        "action": "translate",
        "text": "Bonjour",
        "lang": "EN"
    }
    price = 300

    result = agent.on_message(sender="Payer", task=task, price=price, payer_wallet=payer)

    assert result["result"] == "Translated(Bonjour) to EN"
    assert payer.balance == 700
    assert receiver.balance == 300
    assert len(payer.history) == 1
    assert len(receiver.history) == 1