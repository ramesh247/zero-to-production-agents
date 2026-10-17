"""Evaluate a prompt version on a ticket set, compare it with a baseline, and gate on the result.

    python -m src.evaluate triage@v3 --set test --mode replay
    python -m src.evaluate triage@v3 --set test --mode record
    python -m src.evaluate triage@v1 --set test --baseline triage@v3 --max-drop 0.05   # exits 1 if it drops too far

The baseline is always replayed from its recorded snapshots: you compare against what was released, not a fresh re-run.

Exit code 0 = gate passed, 1 = gate failed, 2 = snapshots missing in replay mode.
"""
import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from .llm import FIELDS, MissingSnapshot, classify
from .prompts import ROOT, load

TICKETS = json.loads((ROOT / "data" / "tickets.json").read_text())


def run_eval(ref: str, split: str = "test", runs: int = 3, mode: str = "replay") -> dict:
    prompt = load(ref)
    jobs = [(t, r) for t in TICKETS[split] for r in range(1, runs + 1)]
    t0 = time.perf_counter()
    with ThreadPoolExecutor(8) as ex:
        outs = list(ex.map(lambda j: (j, classify(prompt, j[0]["text"], j[1], mode)), jobs))
    seconds = time.perf_counter() - t0
    per_ticket: dict[int, list[bool]] = {}
    for (t, _), o in outs:
        per_ticket.setdefault(t["id"], []).append(o["labels"] == t["label"])
    right = sum(sum(v) for v in per_ticket.values())
    return {"ref": ref, "hash": prompt.hash, "split": split, "runs": runs, "mode": mode, "score": right / len(jobs),
            "right": right, "total": len(jobs), "per_ticket": {k: sum(v) / len(v) for k, v in per_ticket.items()},
            "cost": sum(o["cost"] for _, o in outs), "seconds": seconds}


def compare(new: dict, base: dict) -> dict:
    better = [k for k in new["per_ticket"] if new["per_ticket"][k] > base["per_ticket"][k]]
    worse = [k for k in new["per_ticket"] if new["per_ticket"][k] < base["per_ticket"][k]]
    return {"better": better, "worse": worse, "delta": new["score"] - base["score"]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompt", help="name@version, e.g. triage@v3")
    ap.add_argument("--set", default="test", choices=["dev", "validation", "test"])
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--mode", default="replay", choices=["live", "record", "replay"])
    ap.add_argument("--baseline", help="name@version to compare against (always replayed from its snapshots)")
    ap.add_argument("--min-score", type=float, help="fail if the score is below this (0-1)")
    ap.add_argument("--max-drop", type=float, help="fail if the score drops more than this below the baseline (0-1)")
    a = ap.parse_args(argv)
    try:
        new = run_eval(a.prompt, a.set, a.runs, a.mode)
        base = run_eval(a.baseline, a.set, a.runs, "replay") if a.baseline else None
    except MissingSnapshot as e:
        print(f"MISSING SNAPSHOT: {e}")
        return 2
    print(f"{new['ref']} (hash {new['hash']}) on {new['split']}: {new['score']:.0%} all 3 labels right "
          f"({new['right']}/{new['total']}) | mode {new['mode']} | ${new['cost']:.4f} | {new['seconds']:.2f} s")
    ok = True
    if a.min_score is not None and new["score"] < a.min_score:
        print(f"GATE FAILED: {new['score']:.0%} is below the minimum {a.min_score:.0%}")
        ok = False
    if base:
        c = compare(new, base)
        print(f"vs {base['ref']} (hash {base['hash']}): {base['score']:.0%} -> {new['score']:.0%} ({c['delta']:+.0%}) | "
              f"tickets better: {len(c['better'])} {c['better']} | worse: {len(c['worse'])} {c['worse']}")
        if a.max_drop is not None and c["delta"] < -a.max_drop:
            print(f"GATE FAILED: dropped {-c['delta']:.0%}, more than the allowed {a.max_drop:.0%}")
            ok = False
    if ok and (a.min_score is not None or a.max_drop is not None):
        print("GATE PASSED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
