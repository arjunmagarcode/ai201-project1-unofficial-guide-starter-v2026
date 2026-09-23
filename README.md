# The Unofficial Guide

Arjun Pun Magar — campus_life

---

# Unit 1

## What This Does

This system answers questions about the campus_life corpus: housing, dining,
courses, transit, and other student-life details. It loads the documents,
chunks them into searchable pieces, retrieves the closest matches to a
question, and then writes a grounded answer from those chunks. If the best
chunk is too far away, the gate refuses instead of making something up.

## Chunking Strategy

**Chunk size:** 400 characters
**Overlap:** 80 characters

The corpus is mostly short, self-contained posts, but the longest documents are
still only about 550 characters, so a 400-character cap splits the outliers
without chopping up the common case. The 80-character overlap keeps adjacent
chunks from losing the tail end of a sentence when a longer post needs to be
split. I started with the starter's 800-character windows, then switched to a
paragraph-aware chunker after measuring that the default left the corpus almost
entirely unsplit.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt` — produced by:
`chunker.py::split_documents`

```text
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer
window — through the end of week six — but a drop after week two shows as a W
on your transcript. Nothing anywhere on the registrar's site says this
plainly, and students find out from each other.
```

**Chunk 2** — source: `admin_campus_jobs_and_financial_aid.txt` — produced by:
`chunker.py::split_documents`

```text
On the campus jobs and financial aid

Work-study earnings don't count against your financial aid the way ordinary
income does. Non-work-study campus jobs pay the same and do count, which is a
difference worth understanding before you take the first job offered.
```

**Chunk 3** — source: `admin_declaring_a_major.txt` — produced by:
`chunker.py::split_documents`

```text
On the declaring a major

You declare at the end of your second semester, or later if you need to.
There's no penalty for declaring late and no advantage to declaring early
except that it assigns you a departmental adviser, who is generally more useful
than the general one.
```

**Chunk 4** — source: `admin_dining_dollars.txt` — produced by:
`chunker.py::split_documents`

```text
On the dining dollars

Declining balance — what everyone calls dining dollars — rolls over from the
autumn semester to the spring, but not from spring to the following autumn.
Whatever is left in May disappears.
```

**Chunk 5** — source: `admin_grade_appeals.txt` — produced by:
`chunker.py::split_documents`

```text
On the grade appeals

A grade appeal starts with the instructor and has to be raised within fifteen
days of the grade posting. Only after that does it go to the department.
Skipping the instructor step gets the appeal returned, which wastes most of
the fifteen days.
```

## Sample Answer

**Question:** Is the housing lottery random?

**Answer:**

```text
No. Rising sophomores get a number drawn at random, but juniors and seniors
are ordered by accumulated credit hours first, with random tie-breaks.
Source: admin_housing_lottery.txt.
```

**My relevance cutoff:**

0.6

The covered questions clustered between 0.168 and 0.425. The out-of-scope
questions clustered between 0.825 and 0.934. A cutoff of 0.6 sits cleanly in
the gap between those two groups, so it refuses the unrelated questions
without blocking the ones the corpus actually answers.

| Question | In corpus? | Best distance |
|---|---|---|
| Is the housing lottery random? | Yes | 0.254 |
| When can I declare pass/fail for a course outside my major? | Yes | 0.234 |
| How long are wait times at Kestrel Commons during lunch? | Yes | 0.168 |
| What are the library hours during term? | Yes | 0.391 |
| How often does the campus shuttle run on weekdays? | Yes | 0.425 |
| What is the capital of Mongolia? | No | 0.825 |
| How do I change the oil in a diesel engine? | No | 0.934 |
| Who won the 1994 World Cup? | No | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.844 |
| How do I write a for loop in Rust? | No | 0.891 |

## How I Used AI

**1.** I asked for help diagnosing why `python3 app.py` failed, and the answer
pointed out that the CLI requires a subcommand. I used that to confirm the bug
was the invocation, not the app itself.

**2.** I asked for a chunking approach that fit this corpus, then changed it
after measuring the document lengths and seeing that 800-character windows left
almost everything unsplit. I kept the paragraph-aware idea but tuned it down to
400 characters with 80 characters of overlap.

---

# Unit 2

I ran `python3 run_eval.py --label before`. The complete evidence is in
`results/run_2026-09-23_1819_before.md`, produced by
`run_eval.py::main`. It contains three uncached generated answers for each of
the five answerable questions. The later attempts returned a temporary Gemini
503 error and are not part of this run log.

## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Something about your chunks | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Your choice | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

The answer-dependent criteria were stable across all three uncached runs. The
housing question was the one scored as a failure in criterion 1 because
`scorer.py::judge` required the exact phrase `not random`, while the generated
answer said `not entirely random`. The relevant source was still retrieved.
Criterion 3 is identical in all three columns because
`run_eval.py::check_out_of_scope` performs deterministic retrieval and gate
checks once; refused questions do not call the model.

## Real Output

The following is copied from `results/run_2026-09-23_1819_before.md`, rather
than summarized. Generated answers came from `run_eval.py::run_once`, which
calls `generate.py::answer_from_chunks`; pass/fail marks came from
`scorer.py::judge`.

### Criterion 1 — Retrieved answers

```text
The housing lottery is not entirely random for everyone. While rising sophomores get a number drawn at random, juniors and seniors are ordered by accumulated credit hours first, with random selection used only as a tie-breaker.

Source: `admin_housing_lottery.txt`
```

```text
You can declare a course outside your major as pass/fail as late as week eight, after you've seen your midterm. (Source: admin_pass_fail_option.txt)
```

```text
Based on the documents, wait times at Kestrel Commons are 20 to 25 minutes between 12:15 and 1:00, and under 5 minutes before 11:45.

Source: `dining_kestrel_commons.txt`
```

```text
The library is open until 2am during term.

Source: study_library_hours.txt
```

```text
The campus shuttle runs a loop every 20 minutes on weekdays (transit_shuttle.txt).
```

### Criterion 2 — Source names

```text
Source: `admin_housing_lottery.txt`
Source: admin_pass_fail_option.txt
Source: `dining_kestrel_commons.txt`
Source: study_library_hours.txt
(transit_shuttle.txt)
```

### Criterion 3 — Out-of-corpus gate output

Produced by `run_eval.py::check_out_of_scope`:

```text
refused  (best distance 0.825)  What is the capital of Mongolia?
refused  (best distance 0.934)  How do I change the oil in a diesel engine?
refused  (best distance 0.886)  Who won the 1994 World Cup?
refused  (best distance 0.844)  What is the recommended dosage of ibuprofen for a headache?
refused  (best distance 0.891)  How do I write a for loop in Rust?
-> gate refused 5 of 5
```

### Criterion 4 — Sample chunks

Produced by `chunker.py::split_documents`:

```text
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer
window — through the end of week six — but a drop after week two shows as a W
on your transcript.
```

```text
On the campus jobs and financial aid

Work-study earnings don't count against your financial aid the way ordinary
income does. Non-work-study campus jobs pay the same and do count.
```

```text
On the declaring a major

You declare at the end of your second semester, or later if you need to.
There's no penalty for declaring late and no advantage to declaring early.
```

```text
On the dining dollars

Declining balance — what everyone calls dining dollars — rolls over from the
autumn semester to the spring, but not from spring to the following autumn.
```

```text
On the grade appeals

A grade appeal starts with the instructor and has to be raised within fifteen
days of the grade posting. Only after that does it go to the department.
```

### Criterion 5 — Answer length

Produced by `run_eval.py::run_once` and `generate.py::answer_from_chunks`:

```text
The housing lottery is not entirely random for everyone. While rising sophomores get a number drawn at random, juniors and seniors are ordered by accumulated credit hours first, with random selection used only as a tie-breaker. Source: `admin_housing_lottery.txt`
```

```text
You can declare a course outside your major as pass/fail as late as week eight, after you've seen your midterm. (Source: admin_pass_fail_option.txt)
```

All five answerable responses were three sentences or fewer in each of the
three runs.
