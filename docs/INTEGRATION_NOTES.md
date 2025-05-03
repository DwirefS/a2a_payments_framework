# 🔗 Integration Notes - A2APay Framework

This document tracks gotchas, conventions, and integration boundaries with external libraries and agent systems.

---

## 🧠 LangChain Integration Notes

- Use `StructuredTool` not `BaseTool` for predictable Pydantic behavior.
- Pydantic v2 support requires:
  ```python
  model_config = ConfigDict(arbitrary_types_allowed=True)
  ```
- Always pass inputs using:
  ```python
  tool.run({"task": "...", "price": ..., "payer_wallet": ...})
  ```

---

## 🤖 AutoGen Adapter

- All tasks must conform to the standard schema:
  ```json
  {
    "action": "translate",
    "text": "Hello",
    "lang": "FR"
  }
  ```
- Payment logic must be triggered using:
  ```python
  payer_wallet.send(receiver_wallet, amount)
  ```
- `on_message()` receives sender ID, task, price, and payer wallet

---

## 🧪 Testing Integration Contracts

- All tests use mock wallets
- Task flows always validate balance after execution
- Logs are printed from agent threads and adapters to show side-effects

---

## 🧭 Future Plug-in Interfaces

- LangChain plugin loader
- AutoGen hook for `on_result()` to trigger payment confirmation
- DSP registry for service discovery and pricing