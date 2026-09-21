# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
Most of my questions point to a single short post, but the Kestrel Commons one
also has a follow-up file, so 4 of 5 leaves room for the harder retrieval
without pretending every question is equally easy.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
These posts are short enough that a grounded answer should always be able to
say where it came from, and an answer without a source is not useful to a
student even if the fact happens to be right.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
The in-corpus questions cluster well below the off-topic ones, so the cutoff
can sit in the gap instead of forcing me to choose between refusing real
questions or letting unrelated ones through.

---

## 4. Something about your chunks

For at least 4 of my 5 sample chunks, the chunk reads as a complete thought
that stays on one topic and does not cut a sentence in half.

**Why this target:**
Most campus_life documents are short blurbs, so if the sample chunks look like
fragments or topic mashups, the chunker is cutting too aggressively for this
corpus.

---

## 5. Your choice

For at least 4 of my 5 answerable questions, the answer stays at three
sentences or fewer.

**Why this target:**
These are short factual questions, so longer answers usually mean the model is
adding filler or uncertainty instead of staying grounded in the retrieved
chunks.

---

<!-- ── UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
