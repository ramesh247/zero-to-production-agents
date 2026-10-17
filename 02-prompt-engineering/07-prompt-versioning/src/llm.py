"""Calls the model, with record/replay snapshots so tests can run offline and for free.

mode="live":   call the API, don't save anything
mode="record": call the API and save the reply to snapshots/
mode="replay": read the saved reply; raise MissingSnapshot if this exact (model, prompt hash, ticket, run) was never recorded
"""
import hashlib
import json
import os
import re
from pathlib import Path

from .prompts import ROOT, Prompt

MODEL = "claude-haiku-5-5"
PRICE = {"input": 0.10, "output": 0.50}   # $ per 1M tokens (prompts up to 100K tokens)
SNAPSHOTS = ROOT / "snapshots"
FIELDS = {"category": ["billing", "bug", "account", "shipping", "feature_request"],
          "priority": ["low", "medium", "high", "urgent"],
          "sentiment": ["negative", "neutral", "positive"]}
SCHEMA = ('{"category": one of ' + json.dumps(FIELDS["category"]) + ', "priority": one of ' + json.dumps(FIELDS["priority"])
          + ', "sentiment": one of ' + json.dumps(FIELDS["sentiment"]) + "}")


class MissingSnapshot(Exception):
    pass


def _client():
    from dotenv import load_dotenv
    import anthropic
    load_dotenv(ROOT / ".env") or load_dotenv(ROOT.parents[1] / ".env")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY is not set (needed for live/record mode)")
    return anthropic.Anthropic().with_options(max_retries=6)


def snapshot_key(prompt: Prompt, ticket: str, run: int) -> str:
    return hashlib.sha256(f"{MODEL}|{prompt.hash}|{ticket}|{run}".encode()).hexdigest()[:16]


def user_message(prompt: Prompt, ticket: str) -> str:
    return (f"{prompt.body}\n\nTriage this support ticket: give its category, priority and sentiment.\n\n"
            f"<ticket>\n{ticket}\n</ticket>\n\nReply with only a JSON object, no other text:\n{SCHEMA}")


def parse(text: str) -> dict | None:
    m = re.search(r"\{.*?\}", text, re.S)
    try:
        d = json.loads(m.group(0)) if m else {}
    except json.JSONDecodeError:
        return None
    out = {f: str(d.get(f, "")).strip().lower() for f in FIELDS}
    return out if all(out[f] in FIELDS[f] for f in FIELDS) else None


_client_cache = {}


def classify(prompt: Prompt, ticket: str, run: int = 1, mode: str = "replay") -> dict:
    """Returns {"labels": {...} or None, "cost": float, "from_snapshot": bool}."""
    path = SNAPSHOTS / f"{snapshot_key(prompt, ticket, run)}.json"
    if mode == "replay":
        if not path.exists():
            raise MissingSnapshot(f"{prompt.ref} (hash {prompt.hash}) was never recorded for this ticket/run. "
                                  "Run the eval with --mode record.")
        snap = json.loads(path.read_text())
        return {"labels": parse(snap["text"]), "cost": 0.0, "from_snapshot": True}
    if "c" not in _client_cache:
        _client_cache["c"] = _client()
    r = _client_cache["c"].messages.create(model=MODEL, max_tokens=300, thinking={"type": "disabled"}, system=prompt.system,
                                           messages=[{"role": "user", "content": user_message(prompt, ticket)}])
    text = "".join(b.text for b in r.content if b.type == "text")
    cost = (r.usage.input_tokens * PRICE["input"] + r.usage.output_tokens * PRICE["output"]) / 1e6
    if mode == "record":
        SNAPSHOTS.mkdir(exist_ok=True)
        path.write_text(json.dumps({"model": MODEL, "prompt": prompt.ref, "prompt_hash": prompt.hash, "run": run,
                                    "text": text, "cost": cost}, indent=1) + "\n")
    return {"labels": parse(text), "cost": cost, "from_snapshot": False}
