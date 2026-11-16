# Advanced Level: Investigating One Benchmark Dataset

## 1. Dataset

**SWE-bench Verified** (500 coding tasks built from real GitHub issues)

- Dataset: https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified
- Creation and validation write-up (OpenAI): https://openai.com/index/introducing-swe-bench-verified/
- Independent analysis (Epoch AI): https://epoch.ai/blog/what-skills-does-swe-bench-verified-evaluate
- Original benchmark paper: "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" (arXiv 2310.06770)

Each task gives the model an issue text (`problem_statement`) and a repository at a fixed commit (`base_commit`). The model must edit the code to resolve the issue. The hidden tests and the real fix come from the pull request that originally closed the issue.

## 2. Problems I read (summaries, not copies)

### django__django-11099 (Django)
- **Asks:** Django's username validators use a regex ending in `$`, which in Python also matches a trailing newline, so a username like `"name\n"` is accepted. The reporter says the validators should reject it.
- **Hidden check:** the test patch adds a trailing-newline username to the list of invalid usernames for both the ASCII and Unicode validators.
- **Could I solve it?** _(fill in your own answer)_ The issue itself suggests the fix (anchor with `\A` and `\Z`), so a person who knows the regex quirk can solve it quickly.
- **Difficulty for an LLM:** low. The issue names the cause and the fix. The bigger concern is that this is a famous task, so a model may have seen it in training (Epoch rates SWE-bench Verified's contamination risk as high).

### astropy__astropy-12907 (Astropy)
- **Asks:** `separability_matrix` gives the wrong answer for nested compound models (a compound model joined with `&` inside another one). Outputs that should be independent are reported as dependent.
- **Hidden check:** two parametrized cases in `test_separable.py` (nested compound models) must go from failing to passing, while the other tests in that file must keep passing. The reference fix is a one-line change in the `_cstack` helper in `separable.py`.
- **Could I solve it?** _(fill in your own answer)_ I would need to read how the matrix is built from left and right parts, so more than a quick fix. The dataset labels it "15 min - 1 hour".
- **Difficulty for an LLM:** medium. The issue gives a reproduction but not the location. The model must find `_cstack`, understand how it builds the right-hand block, and change it without breaking the other tests.

### scikit-learn__scikit-learn-14520 (OpenAI's example of a bad task)
- **Asks:** an issue in scikit-learn's TF-IDF vectorizer. The reference test checks that a specific deprecation warning is raised.
- **Why it matters:** OpenAI uses it to show an unfair task. The agent only sees the issue text, not the test, so the exact warning the test expects cannot be derived from the issue. They call it nearly impossible to solve as specified.
- **Difficulty for an LLM:** the model could write a sensible fix and still fail, because the grader checks behavior the issue never describes. This is the kind of task the human screening was meant to remove.

## 3. Contributors, validation and grading

**Creation (original SWE-bench):** tasks were collected automatically from resolved issues and merged pull requests in 12 popular open-source Python repositories (2,294 tasks in the full set). Each task includes tests that fail before the PR's fix and pass after (`FAIL_TO_PASS`), plus tests that should keep passing (`PASS_TO_PASS`).

**Verification (SWE-bench Verified, 2024):**
- **Contributors:** 93 software developers experienced in Python, working with OpenAI and the SWE-bench authors. They were not necessarily experts in the specific codebases but were given time to learn each one.
- **Scale:** 1,699 randomly selected tasks were annotated.
- **Reviewers per task:** 3 independent annotators.
- **What they judged:** whether the issue is well specified, whether the `FAIL_TO_PASS` tests could reject valid solutions, and other major problems, each on a severity scale of 0 to 3. They also estimated how long an experienced engineer would need to fix the issue.
- **Combining labels:** conservatively, by taking the highest severity among the 3 annotators, so one annotator's concern was enough to drop a task.
- **Rejections:** reported figures are about 38.3% flagged as underspecified, about 61.1% flagged for tests that could unfairly reject valid solutions, and 68.3% removed overall, leaving 500 tasks. (The categories overlap. I took these numbers from secondary summaries of the OpenAI post, so check them against the post itself.)
- **Remaining flaws:** Epoch estimates 5 to 10% of the 500 still have problems.

**Grading:** automatic and execution-based. The model's patch is applied in a Docker environment, and the task counts as solved only if both the `FAIL_TO_PASS` and `PASS_TO_PASS` tests pass. No LLM is involved in grading, and the model never sees the tests.

**Other facts:** per Epoch's analysis, about 39% of tasks are rated under 15 minutes for a human, 52% take 15 minutes to 1 hour, and only 3 are estimated at over 4 hours. About 87% are bug fixes.

## 4. Differences from today's evaluation set

| | SWE-bench Verified | My evaluation set |
|---|---|---|
| Size | 500 tasks | 10 cases |
| Authors | Real issues and PRs written by many open-source contributors | One author (me) |
| Validation | 93 developers, 3 independent labels per task, highest-severity rule, about two-thirds of candidates dropped | One person's judgment, plus comparison with the instructor's labels |
| Grading | Deterministic unit tests, no judge model | Rubric with an LLM judge, checked against human labels |
| What it tests | Editing real code to fix issues | Answering glossary questions, refusing out-of-scope requests |
| Correct answer | Objective (tests pass or fail) | Partly subjective (e.g. "clear", "stays in scope") |
| Known weaknesses | Contamination, skew toward small bug fixes, some flawed tasks remain | Tiny sample, one author's blind spots, judge errors |

**Main takeaway:** the large benchmark gets its trustworthiness from independent human review of every item and from tests that can be run, while my set depends on one author and a model's judgment. With 10 cases, one changed verdict moves the score by 10 points, so my results show behavior on specific cases and are not a reliable score.
