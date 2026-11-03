from sentiment_eval import accuracy, confusion, load_reviews, misses, recall_by_label


def row(reference, llm):
    return {"text": f"{reference}/{llm}", "reference": reference, "llm": llm}


def test_accuracy_is_share_of_exact_matches():
    rows = [row("positive", "positive"), row("neutral", "positive"), row("mixed", "mixed")]
    assert accuracy(rows) == 2 / 3


def test_confusion_counts_reference_llm_pairs():
    rows = [row("neutral", "positive"), row("neutral", "positive"), row("mixed", "mixed")]
    assert confusion(rows) == {("neutral", "positive"): 2, ("mixed", "mixed"): 1}


def test_recall_is_computed_per_reference_label():
    rows = [row("neutral", "neutral"), row("neutral", "positive"), row("mixed", "positive")]
    assert recall_by_label(rows) == {"neutral": 0.5, "mixed": 0.0}


def test_misses_returns_only_disagreements():
    wrong = row("neutral", "positive")
    assert misses([row("mixed", "mixed"), wrong]) == [wrong]


def test_assignment_labels_score_half():
    reviews = load_reviews()
    assert accuracy(reviews) == 0.5
    assert recall_by_label(reviews) == {
        "mixed": 0.0,
        "positive": 1.0,
        "negative": 1.0,
        "neutral": 0.0,
    }
