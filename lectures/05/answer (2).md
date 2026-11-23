# Retrieval Homework Report (Lecture 2 materials)

## Level attempted
Implementation (adjacent pages) and Advanced (graph + distance gate), compared with Basic RAG.

## What I did (`app/retrieval.py`)
- **Implementation:** added `neighbors=False` to `search()`. After the top-5 vector hits, it adds the page before and after each hit (document → section → page order). It never crosses documents, never repeats a page, and labels each result `hit`, `before` or `after`. Added a `--neighbors` command-line flag.
- **Advanced:** kept the graph search (seeds from vector search, then expansion over `next_page` and `mentions` edges). Added a gate: an expanded page is kept only if its vector distance is within `MARGIN` (0.08 to start) of the best seed. Distances come from one extra `search(k=200)` call, so the query is embedded once.

## Comparison conditions
- Same materials (Lecture 2), embedding model and top-K (5) for all methods.
- Questions: (1) Compare pre-training, post-training and fine-tuning; (2) When to use RAG instead of fine-tuning to add knowledge; (3) What does 7B mean and how much memory does it need?
- Extra test for neighbors: "what is regularisation" (not in the materials).

## Results

Tokens are estimated as characters ÷ 4.

| Question | Method | Pages | Tokens | Time | Finding |
|---|---|---|---|---|---|
| 1 Compare | Basic | 5 | 1,451 | 2.72 s | No pre-training page |
| | Graph | 10 | 2,943 | 2.50 s | Adds the pre-training page |
| 2 RAG vs FT | Basic | 5 | 1,072 | 2.54 s | Core pages found |
| | Graph | 8 | 2,031 | 2.37 s | Same pages plus repeats |
| 3 7B | Basic | 5 | 1,005 | 1.85 s | Answer page found |
| | Graph | 10 | 2,488 | 1.74 s | 7 off-topic extras |

Neighbors on "what is regularisation": 5 pages became 15, and only 2 of the 10 added pages were useful.

Not yet available: `--trace` output, generated answers, and generation cost, because the agent has not run successfully. Cost = (input tokens × input price + output tokens × output price) ÷ 1,000,000.

## Improvements
- **Graph, Q1:** found the pre-training page that Basic missed, through a shared term.
- **Neighbors, RAG-vs-FT page:** added "Small-scale FT" and "Continued pre-training", which complete the argument.

## Failures and limits
- **Graph, Q3:** the answer was already in Basic, and the 7 extra pages were noise (2.5× tokens, no gain).
- **Graph, Q2:** the extras repeated pages Basic already had.
- **Neighbors:** 8 of 10 added pages were off-topic (title slide, news slide), and neighbors have no distance score.
- **Out-of-corpus queries:** every method still returns pages, never "not found."
- **Gate:** the seed distances were not printed, so `MARGIN = 0.08` is untested and probably too loose. Next test: 0.03.
- **Not measured:** neighbors on the three main questions, and the generated answers.

## Observations and questions
- Extra context helps only when the answer spans pages or concepts. For single-fact lookups, Basic is enough.
- Time is similar across methods. The cost difference comes from the extra tokens sent to the generator.
- Suggested use: Basic for lookups, neighbors for explanations, gated graph for comparisons, plus a distance cutoff for "not found."
- Which `MARGIN` keeps the pre-training page in Q1 but removes the 7B noise?
