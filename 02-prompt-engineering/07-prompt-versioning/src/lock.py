"""Record the hash of every prompt version in prompts/lock.json:  python -m src.lock"""
from .prompts import write_lock

if __name__ == "__main__":
    for ref, h in write_lock().items():
        print(f"{ref}: {h}")
