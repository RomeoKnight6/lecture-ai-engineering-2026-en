"""Lecture 01: a script that asks a bare LLM a single question.

Usage:
    uv run python -m app.ask "What is LoRA?"
    uv run python -m app.ask            # Ask a course-specific question if none is supplied

A "bare" call with no tools or conversation history.
Check that, when asked about course-specific information, it either says "I don't know"
or gives a plausible general answer (which differs from the actual course).
(In Lecture 03, improve it by making an agent that can search the glossary.)
"""

import argparse
import os, time, csv
from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# A course-specific question. The correct answer is in homework-levels in data/glossary.json
DEFAULT_QUESTION = "What are the 3 homework levels in the AIE2026 course?"


def ask():
    MODELS = ["gemini-3.5-flash-lite", "gemini-3.8-flash"]
    QUESTIONS = ["What is LoRA?", "Explain overfitting in two sentences."]
    client = genai.Client(api_key=get_api_key())
    rows = []
    for model in MODELS:
        for question in QUESTIONS:
            t0 = time.perf_counter()
            response = client.models.generate_content(model=modeL, contents=question)
            dt = time.perf_counter() - t0
            u = response.usage_metadata
            rows.append([model, q, round(dt, 2), u.prompt_token_count,
                         u.candidates_token_count, u.total_token_count, "ok"])

    # TODO(Lecture 01 exercise): use response.usage_metadata to
    #   display input and output token counts (you may ask Copilot)
    with open("results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "question", "seconds", "prompt_tok", "output_tok", "total_tok", "status"])
        w.writerows(rows)
    return "analysis generated"


def main() -> None:
    try:
        print(ask())
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
