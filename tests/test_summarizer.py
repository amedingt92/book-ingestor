import sys
import os

# Dynamically add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import summarizer # type: ignore

def test_summarize_text_short_sample():
    text = (
        "The whale is a mammal that lives in the sea. It breathes air, "
        "gives birth to live young, and feeds them with milk. It is an "
        "incredibly large animal, some species growing over 80 feet long."
    )

    result = summarizer.summarize_text(text)
    assert isinstance(result, str)
    assert len(result) > 20
