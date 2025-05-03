# 📜 Architectural Decisions Log - A2APay Framework

This file records major design decisions and why they were made. It helps new developers understand trade-offs, prevents regressions, and documents evolution.

---

## ✅ Decision: Use StructuredTool Instead of BaseTool (LangChain)

**Problem:** `BaseTool` + `args_schema` with Pydantic v2 caused recurring `TypeError` and `tool_input` binding failures.

**Why:** LangChain’s `BaseTool.run()` signature changed subtly and inconsistently between versions. Tests failed despite correct annotations.

**Solution:** Switched to `StructuredTool` which:
- Accepts native Pydantic input via `.run()` or `.invoke()`
- Integrates cleanly with LangChain agents and chains
- Removes ambiguity around argument unpacking

**Impact:** Stable testable tools that are agent-compatible.

---

## ✅ Decision: Replace reply_to_wallet with payer_wallet

**Problem:** Early versions of task communication passed `reply_to_wallet`, but payment logic was unclear.

**Why:** reply-to suggests response routing, not financial responsibility.

**Solution:** Renamed to `payer_wallet` across all integration layers.

**Impact:** Clearer direction of funds, easier auditing, less risk of circular payment references.

---

## ✅ Decision: Use queue.Queue and threading for simulated messaging

**Problem:** Needed real-time agent-to-agent simulation.

**Solution:** Used `queue.Queue` and `AgentThread` abstraction to simulate async task processing.

**Impact:** Validated timing, logging, payment flows. Basis for future event bus or distributed RPC.

---

## ✅ Decision: Keep mock wallets for all tests

**Problem:** Can't use real RLUSD or USDC APIs in unit tests.

**Solution:** Use `Wallet` class with in-memory balances and full transaction logging.

**Impact:** Isolated, secure, easy to simulate transfers. Easy to stub out with real API later.