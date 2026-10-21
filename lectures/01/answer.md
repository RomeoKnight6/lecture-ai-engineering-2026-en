# Lecture 01 Answers

## Exercises

- Model's answer to the course-specific question:
  It said it doesn't know the AIE2026 course and asked for more context.
- What you noticed when comparing it with the correct meaning in the glossary:
  The glossary says the levels are Basic, Implementation, Advanced. The model gave none of them.
- Token counts you displayed (input / output):
  18 / 50 for the AIE2026 homework-levels question (gemini-3.5-flash-lite).

## Homework

- Level attempted: Advanced
- What you did:
  Changed `app/ask.py` to time each call and print token counts for 2 questions on 2 models. Saved in `results.csv`.
- Results:

| model | question | seconds | input tok | output tok | total tok |
|---|---|---|---|---|---|
| gemini-3.5-flash-lite | What is LoRA? | 3.37 | 6 | 748 | 754 |
| gemini-3.5-flash-lite | Explain overfitting in two sentences. | 0.95 | 7 | 54 | 61 |
| gemini-3.8-flash | What is LoRA? | 49.03 | 6 | 834 | 1718 |
| gemini-3.8-flash | Explain overfitting in two sentences. | 17.68 | 7 | 47 | 407 |

  - gemini-3.8-flash was much slower (18-49 s vs 1-3 s).
  - For 3.8-flash, total tokens are much higher than input + output (not verified why).
  - Rate limits: 3.8-flash is slow and has a small daily limit (10-20), so the daily limit is the problem. Flash-lite is fast, so the per-minute limit (15) is reached first. (My reasoning, not tested.)
- Observations and questions:
  - gemini-3.8-flash took 18-49 s per call; gemini-3.5-flash-lite took 1-3 s.
  - Output length was similar on both models, so the time difference is not from output length.
  - The short "two sentences" question used far fewer output tokens than the LoRA question on both models.
  - 3.8-flash total tokens (1718, 407) are much higher than input + output (840, 54). Why?
  - Only one run per combination, so the 49 s result may be an outlier.
