"""Part B.1: score the LLM sentiment labels against the reference labels."""
import json
from collections import Counter
from pathlib import Path

REVIEWS_PATH = Path(__file__).parent / "data" / "reviews.json"


def load_reviews(path=REVIEWS_PATH):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def accuracy(rows):
    return sum(r["reference"] == r["llm"] for r in rows) / len(rows)


def confusion(rows):
    return dict(Counter((r["reference"], r["llm"]) for r in rows))


def recall_by_label(rows):
    totals = Counter(r["reference"] for r in rows)
    hits = Counter(r["reference"] for r in rows if r["reference"] == r["llm"])
    return {label: hits[label] / total for label, total in totals.items()}


def misses(rows):
    return [r for r in rows if r["reference"] != r["llm"]]


def main():
    reviews = load_reviews()

    print(f"Accuracy: {accuracy(reviews):.0%} ({len(reviews) - len(misses(reviews))}/{len(reviews)})")

    print("Recall per reference label")
    for label, recall in recall_by_label(reviews).items():
        print(f"  {label}: {recall:.0%}")

    print("Misses")
    for r in misses(reviews):
        print(f'  "{r["text"]}" reference={r["reference"]} llm={r["llm"]}')


if __name__ == "__main__":
    main()
