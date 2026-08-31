"""Small local persistence layer for calculator history and memory."""

import json
from pathlib import Path


class CalculatorStorage:
    def __init__(self, path=None):
        self.path = Path(path or Path.home() / ".smartcalc-pro.json")

    def load(self):
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return data.get("history", []), data.get("memory", 0)
        except (OSError, ValueError, TypeError):
            return [], 0

    def save(self, history, memory):
        data = {"history": list(history)[-100:], "memory": memory}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")