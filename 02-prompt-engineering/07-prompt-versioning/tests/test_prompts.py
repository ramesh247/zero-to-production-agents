"""Prompt tests. They run in replay mode: no API key, no cost, a few seconds.

1. Every prompt file matches its hash in prompts/lock.json, so editing a released version in place fails.
2. Golden tickets: specific tickets must keep specific labels under the current prompt.
3. Score gate: the current prompt must stay at or above its released test score.
"""
import json

import pytest

from src.evaluate import TICKETS, run_eval
from src.llm import classify
from src.prompts import all_refs, load, read_lock

CURRENT = "triage@v3"
MIN_TEST_SCORE = 0.85

BY_ID = {t["id"]: t for split in ("dev", "validation", "test") for t in TICKETS[split]}
GOLDEN = [
    1,    # "charged twice for order ORD-48213": billing, high, neutral
    2,    # "YOUR CHECKOUT PAGE IS DOWN": bug, urgent, negative
    408,  # "Someone changed my password and my email address": account, urgent, negative
    413,  # "Charged three times for ORD-51290!!": billing, high, negative
]


@pytest.mark.parametrize("ref", all_refs())
def test_prompt_matches_lockfile(ref):
    lock = read_lock()
    assert ref in lock, f"{ref} is not in prompts/lock.json. New version? Run: python -m src.lock"
    assert load(ref).hash == lock[ref], (
        f"{ref} was edited after release (hash {load(ref).hash}, locked {lock[ref]}). "
        "Released prompts are immutable: copy it to a new version file instead.")


@pytest.mark.parametrize("ticket_id", GOLDEN)
def test_golden_ticket(ticket_id):
    t = BY_ID[ticket_id]
    for run in (1, 2, 3):
        got = classify(load(CURRENT), t["text"], run, mode="replay")["labels"]
        assert got == t["label"], f"ticket {ticket_id} run {run}: got {got}, expected {t['label']}"


def test_score_gate():
    result = run_eval(CURRENT, "test", runs=3, mode="replay")
    assert result["score"] >= MIN_TEST_SCORE, f"{CURRENT} scored {result['score']:.0%} on test, below {MIN_TEST_SCORE:.0%}"
