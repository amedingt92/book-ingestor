"""Summarizes long texts using Hugging Face transformers (BART model).
"""
from tqdm import tqdm
from transformers import pipeline, AutoTokenizer
import textwrap
import math

# Load the summarization pipeline once globally for reuse
summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

def chunk_by_tokens(text: str, max_tokens: int = 1024, overlap: int = 100) -> list[str]:
    tokens = tokenizer.tokenize(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk = tokenizer.convert_tokens_to_string(tokens[start:end])
        chunks.append(chunk)
        start = end - overlap  # Slide window
    return chunks

def summarize_text(text, max_length=200, min_length=80):
    prompt = f"Summarize this literary passage:\n{text.strip()}"
    return summarizer_pipeline(
        prompt,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )[0]["summary_text"]

def refine_summary(summary):
    """Optional second pass if needed later with another model."""
    return summary.strip()  # placeholder for GPT-based refinement



def summarize_long_text(text: str, tokenizer=None, summarizer=None, target_tokens_per_chunk=400) -> str:
    """
    Dynamically chunk text by token count, summarize each chunk, and combine summaries.
    """
    if not text.strip():
        return ""

    # --- Setup tokenizer and summarizer if not provided ---
    from transformers import pipeline, AutoTokenizer
    if tokenizer is None:
        tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
    if summarizer is None:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # --- Token-based chunking ---
    inputs = tokenizer(text, return_tensors="pt", truncation=False)
    input_ids = inputs["input_ids"][0]
    total_tokens = len(input_ids)

    # Auto-determine number of chunks
    num_chunks = max(1, total_tokens // target_tokens_per_chunk)
    chunk_size = total_tokens // num_chunks

    chunks = []
    for i in range(num_chunks):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        chunk_ids = input_ids[start:end]
        chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True)
        chunks.append(chunk_text)

    # --- Summarize each chunk ---
    from tqdm import tqdm
    partial_summaries = []
    for chunk in tqdm(chunks, desc="⏳ Summarizing chunks", unit="chunk", leave=False):
        try:
            token_len = len(tokenizer(chunk)["input_ids"])
            max_len = max(80, int(token_len * 0.6))  # scale max_length
            summary = summarizer(chunk, max_length=max_len, min_length=60, do_sample=False)[0]["summary_text"]
            partial_summaries.append(summary)
        except Exception as e:
            print("❌ Error summarizing chunk:", e)

    # --- Final summary if needed ---
    combined_summary_input = " ".join(partial_summaries)
    if len(tokenizer(combined_summary_input)["input_ids"]) < 512:
        return combined_summary_input.strip()
    
    try:
        final_max_len = min(300, int(len(tokenizer(combined_summary_input)["input_ids"]) * 0.6))
        final_summary = summarizer(
            combined_summary_input,
            max_length=final_max_len,
            min_length=100,
            do_sample=False
        )[0]["summary_text"]
        return final_summary.strip()
    except Exception as e:
        print("❌ Error during final summary refinement:", e)
        return combined_summary_input.strip()



    
def refine_summary(summary_text: str) -> str:
    """Rewrite the summary into clear, expanded narrative prose."""
    prompt = (
        "Rewrite the following chapter summary into clear, expanded narrative prose "
        "that preserves key events, character motivations, and emotional tone:\n\n"
        + summary_text.strip()
    )

    refined = summarizer_pipeline(
        prompt,
        max_length=300,
        min_length=150,
        do_sample=False
    )
    return refined[0]["summary_text"]


def save_summaries(chapter_summaries, output_path):
    """Save a list of (chapter_title, summary) tuples to a markdown file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for chapter_title, summary in chapter_summaries:
            f.write(f"## {chapter_title}\n\n")
            f.write(textwrap.fill(summary, width=100))
            f.write("\n\n")
