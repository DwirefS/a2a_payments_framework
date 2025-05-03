import json
from datetime import datetime
from pathlib import Path
import uuid

class ReceiptGenerator:
    def __init__(self, output_dir: str = "./receipts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_receipt(self, sender: str, receiver: str, task: str, amount: int, currency: str, tx_id: str, memo: str = "") -> Path:
        receipt = {
            "receipt_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "sender": sender,
            "receiver": receiver,
            "task": task,
            "amount": amount,
            "currency": currency,
            "tx_id": tx_id,
            "memo": memo
        }

        filename = f"receipt_{receipt['receipt_id']}.json"
        receipt_path = self.output_dir / filename

        with receipt_path.open("w") as f:
            json.dump(receipt, f, indent=2)

        return receipt_path
