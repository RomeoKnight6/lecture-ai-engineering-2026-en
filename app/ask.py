"""Lecture 01: ask a bare LLM questions.

Usage:
    uv run python -m app.ask advanced   # Advanced: time + tokens, 2 models x 2 questions -> results.csv
    uv run python -m app.ask basic     # Basic: same question 3 times on each model -> basic.txt
    uv run python -m app.ask implementation      # Implementation: follow-up questions with history
"""

import csv
import sys
import time

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

DEFAULT_QUESTION = "What are the 3 homework levels in the AIE2026 course?"
MODELS = ["gemini-3.5-flash-lite", "gemini-3.8-flash"]
QUESTIONS = ["What is LoRA?", "Explain overfitting in two sentences."]


def advanced(client):
    """Advanced: response time and token counts per model and question."""
    rows = []
    for model in MODELS:
        for question in QUESTIONS:
            t0 = time.perf_counter()
            try:
                response = client.models.generate_content(model=model, contents=question)
                u = response.usage_metadata
                row = [model, question, round(time.perf_counter() - t0, 2),
                       u.prompt_token_count, u.candidates_token_count,
                       u.total_token_count, "ok"]
            except errors.APIError as e:
                row = [model, question, round(time.perf_counter() - t0, 2),
                       "", "", "", f"error {e.code}"]
            print(row)
            rows.append(row)
            time.sleep(13)  # stay under 5/min on the stronger model
    with open("results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "question", "seconds", "prompt_tok", "output_tok", "total_tok", "status"])
        w.writerows(rows)
    return "saved results.csv"


def basic(client):
    """Basic: same question 3 times on each model; read the answers and compare."""
    question = QUESTIONS[0]
    out = []
    for model in MODELS:
        for i in range(1, 4):
            try:
                text = client.models.generate_content(model=model, contents=question).text
            except errors.APIError as e:
                text = f"[error {e.code}]"
            out.append(f"=== {model} run {i} ===\n{text}\n")
            print(out[-1])
            time.sleep(13)
    with open("basic.txt", "w") as f:
        f.write("\n".join(out))
    return "saved basic.txt"


def implementation(client):
    """Implementation: the chat object keeps the history between questions."""
    session = client.chats.create(model=MODEL)
    question = " ".join(sys.argv[2:]) or input("You: ")
    while question.strip():
        response = session.send_message(question)
        u = response.usage_metadata
        print(f"\n{response.text}\n[tokens] input={u.prompt_token_count} output={u.candidates_token_count}\n")
        question = input("You (blank to quit): ")
    return "bye"


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "advanced"
    modes = {"advanced": advanced, "basic": basic, "implementation": implementation}
    if mode not in modes:
        raise SystemExit("Usage: python -m app.ask [advanced|basic|implementation]")
    try:
        print(modes[mode](genai.Client(api_key=get_api_key())))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
