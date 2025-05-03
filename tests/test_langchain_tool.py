from a2apay import Wallet
from a2apay.integrations.langchain_tool import A2APayAgentTool, A2APayInput

def test_langchain_tool_translation_and_payment():
    payer = Wallet("Payer", balance=1000, currency="RLUSD")
    receiver = Wallet("Receiver", balance=0, currency="RLUSD")

    tool = A2APayAgentTool(agent_name="Receiver", agent_wallet=receiver)

    tool_input = A2APayInput(
        task="translate:Ciao:EN",
        price=400,
        payer_wallet=payer
    )

    result = tool.invoke(tool_input)

    assert "Translated(Ciao) to EN" in result
    assert payer.balance == 600
    assert receiver.balance == 400
    assert len(payer.history) == 1
    assert len(receiver.history) == 1