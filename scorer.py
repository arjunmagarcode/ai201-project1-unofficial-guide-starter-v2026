"""Score individual evaluation questions for run_eval.py.

The judge is intentionally simple: the answer has to be a real answer, it has
 to include the expected phrase, and it has to name at least one retrieved
source document.
"""

from __future__ import annotations

import re

import gate


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _source_names(results) -> set[str]:
    return {str(result.source).strip().lower() for result in results}


def judge(question, expects, answer, results) -> bool:
    if not answer or _normalize(answer) == _normalize(gate.REFUSAL):
        return False

    if expects and _normalize(expects) not in _normalize(answer):
        return False

    answer_text = _normalize(answer)
    if not any(source and source in answer_text for source in _source_names(results)):
        return False

    return True
