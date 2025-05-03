from a2apay import Wallet
from a2apay.integrations.langchain_tool import create_a2apay_agent_tool

def test_langchain_structured_tool_translation_and_payment():
    payer = Wallet("Payer", balance=1000, currency="RLUSD")
    receiver = Wallet("Receiver", balance=0, currency="RLUSD")

    tool = create_a2apay_agent_tool(agent_name="Receiver", agent_wallet=receiver)

    result = tool.run({
        "task": "translate:Ciao:EN",
        "price": 400,
        "payer_wallet": payer
    })

    assert "Translated(Ciao) to EN" in result
    assert payer.balance == 600
    assert receiver.balance == 400
    assert len(payer.history) == 1
    assert len(receiver.history) == 1