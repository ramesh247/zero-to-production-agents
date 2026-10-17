"""Prompts live in files, one file per version: prompts/<name>/<version>.md.

A prompt is referred to as "name@version" (e.g. "triage@v3"). Its hash covers everything the model sees,
so any edit, even a comma, produces a new hash. prompts/lock.json records the hash of every released version.
"""
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"
LOCK = PROMPTS / "lock.json"


@dataclass(frozen=True)
class Prompt:
    name: str
    version: str
    system: str
    body: str
    description: str

    @property
    def ref(self) -> str:
        return f"{self.name}@{self.version}"

    @property
    def hash(self) -> str:
        return hashlib.sha256(f"{self.system}\n---\n{self.body}".encode()).hexdigest()[:12]


def load(ref: str) -> Prompt:
    name, version = ref.split("@")
    text = (PROMPTS / name / f"{version}.md").read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{ref}: missing front matter")
    meta = dict(line.split(": ", 1) for line in m.group(1).splitlines() if ": " in line)
    return Prompt(name, version, meta["system"], m.group(2).strip(), meta.get("description", ""))


def all_refs() -> list[str]:
    return sorted(f"{d.name}@{f.stem}" for d in PROMPTS.iterdir() if d.is_dir() for f in d.glob("*.md"))


def read_lock() -> dict[str, str]:
    return json.loads(LOCK.read_text()) if LOCK.exists() else {}


def write_lock() -> dict[str, str]:
    """Record the current hash of every prompt file. Run this when you release a new version."""
    lock = {ref: load(ref).hash for ref in all_refs()}
    LOCK.write_text(json.dumps(lock, indent=2) + "\n")
    return lock
