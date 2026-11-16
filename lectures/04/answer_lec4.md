# Lecture 04 Answers

## Exercises

- Agreement by criterion (before revision): Grounding 8/9, Scope 9/10, Hint 8/10, Clarity 10/10, Lecture marker 5/10
- Number of items needing review (before revision): 1 (case 05, Grounding)
- Criterion revised and the policy added: Grounding. Policy added: "After stating that a term is absent from the glossary, an answer that goes on to explain the term from general knowledge makes an unsupported assertion (fail)."
- Agreement by criterion and number of review items (after revision): Grounding 6/10, Scope 7/10, Hint 10/10, Clarity 10/10, Lecture marker 1/10. Review items: 0.
- Items where your labels differed from the instructor's, and your reasons: [TODO: fill in from the Compare screen]
- Observations and questions:
  - The review item went from 1 to 0. The judge said "unsure" because my rubric had a gap, not because the judge was broken.
  - The "after" run used my own 10 cases, and the "before" run used the instructor's cases, so the numbers are not a fair comparison.
  - The Lecture marker has the most disagreements. Refusals and empty-input replies have no "Lecture N", but I passed them. Should they need one?
  - The judge was too lenient on my edge cases (made-up term, prompt injection, mixed request).

## Homework

- Level attempted: Implementation and Advanced
- What you did: Wrote 10 evaluation cases of my own, generated answers, labeled them and ran the judge. For Advanced, I studied SWE-bench Verified (see `eval_results_advanced.md`).
- Results: On my cases the judge scored Grounding 6/10, Scope 7/10, Hint 10/10, Clarity 10/10, Lecture marker 1/10. SWE-bench Verified was checked by 93 developers (3 per task) and is graded by running tests, while my set has one author and an LLM judge.
- Observations and questions:
  - A big benchmark is trusted because many people review it and the tests can be run. My set of 10 cases depends on one author and a judge model.
  - The edge cases caused the most judge errors, so they need more cases.
  - Some of my answers may not be real agent replies, so I should check them and rerun.
