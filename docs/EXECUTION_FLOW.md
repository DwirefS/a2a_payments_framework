# 🧠 A2A Payments Framework: Execution Flow

This document explains how the components of the A2A Payments Framework interact and execute in sequence, from a high-level request to a completed transaction.

---

## 🔁 End-to-End Flow

### Scenario 1: Agent-to-Agent Task and Payment

```text
[Agent A] --request_task()--> [Agent B]
    |                            |
    |<--handle_request()--------|
    |                            |
    |--validate result---------->|
    |--wallet.send()------------>|
    |--log + receipt------------>|
```

1. **Agent A** initiates a task request to Agent B using `request_task()`.
2. **Agent B** handles the task (e.g., translation) using `handle_request()`.
3. Once the result is returned, Agent A verifies success.
4. Agent A sends payment to Agent B via `wallet.send()`.
5. A transaction receipt is generated (optional) and optionally logged to disk.

---

### Scenario 2: Agent-to-Resource Provider (MCP-style)

```text
[Agent A] --request_resource()--> [ResourceProvider]
    |                                  |
    |<--resource + price--------------|
    |--wallet.send()----------------->|
    |--log receipt------------------->|
```

1. Agent A requests a resource (e.g., dataset) from a provider.
2. The provider responds with data and a defined price.
3. Agent A sends payment using wallet.
4. A receipt is saved for auditing.

---

## ⚙️ Module Interaction Map

| Module          | Description                                              |
|------------------|----------------------------------------------------------|
| `agent.py`      | Handles task logic and payment flow initiation           |
| `wallet.py`     | Manages balances, performs transactions                  |
| `resource.py`   | MCP-like provider interface                              |
| `protocol.py`   | Defines task, result, and payment message schemas        |
| `transaction.py`| Logs persistent transaction data                         |
| `receipt_generator.py` | Outputs signed receipts as JSON                   |
| `demo.py`       | Simulates a complete scenario                            |

---

## 🧪 Expected Output (Demo Run)

```bash
--- Agent to Agent Task ---
Result: Translated(Bonjour) to EN
Alice Balance: 4500, Bob Balance: 500

--- Agent to Resource Provider ---
Data Received: CSV_DATA
Alice Balance: 4250, DataBank Balance: 250
```

---

## 🛠 How to Use It

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run the demo: `python examples/demo.py`
4. Run tests: `pytest tests/`
5. Extend with real payment APIs (RLUSD) or Azure integrations

---

## 📌 Integration Points for Future Expansion

- Azure Key Vault: Secure API key storage (for RLUSD API)
- Azure Blob: Store receipts and logs safely
- RLUSD: Replace mock wallets with API-backed stablecoin wallets
- AutoGen: Inject payments after `on_message()` task processing

---

This is the foundation for a machine-native economy — extensible, secure, and useful.