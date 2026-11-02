"""Guideline training quiz for new annotators and raters.

Questions live in a JSON file, so a QA lead can write new ones without coding:
[
  {"topic": "relevance", "question": "...", "options": ["A", "B", "C"], "answer": 1,
   "why": "Short explanation shown when someone gets it wrong."}
]
`answer` is the 0-based index of the correct option.

Usage:
    python quiz.py questions.json                          # interactive quiz in the terminal
    python quiz.py questions.json --answers answers.txt    # grade an answer sheet (one letter per line)
    python quiz.py questions.json --pass-mark 0.8 --seed 1 --shuffle
"""
import argparse
import json
import random
import string
from collections import defaultdict

LETTERS = string.ascii_uppercase


def load(path):
    with open(path, encoding="utf-8") as f:
        qs = json.load(f)
    for i, q in enumerate(qs, 1):
        for key in ("topic", "question", "options", "answer"):
            if key not in q:
                raise ValueError(f"question {i} is missing '{key}'")
        if not 0 <= q["answer"] < len(q["options"]):
            raise ValueError(f"question {i}: answer index {q['answer']} out of range")
    return qs


def to_index(letter, n_options):
    """'b' -> 1. Returns None for blank or invalid input."""
    letter = (letter or "").strip().upper()
    if len(letter) == 1 and letter in LETTERS[:n_options]:
        return LETTERS.index(letter)
    return None


def grade(questions, choices):
    """choices: list of option indexes (or None). Returns a result dict."""
    if len(choices) != len(questions):
        raise ValueError(f"{len(choices)} answers for {len(questions)} questions")
    by_topic = defaultdict(lambda: [0, 0])
    wrong = []
    for n, (q, c) in enumerate(zip(questions, choices), 1):
        by_topic[q["topic"]][1] += 1
        if c == q["answer"]:
            by_topic[q["topic"]][0] += 1
        else:
            wrong.append((n, q, c))
    correct = len(questions) - len(wrong)
    return {"correct": correct, "total": len(questions), "score": correct / len(questions),
            "by_topic": dict(by_topic), "wrong": wrong}


def feedback(result, pass_mark=0.8):
    r = result
    status = "PASS" if r["score"] >= pass_mark else "NEEDS REVIEW"
    lines = [f"Score: {r['correct']}/{r['total']} ({r['score']:.0%}), {status} (pass mark {pass_mark:.0%})", "", "By topic:"]
    for topic, (ok, total) in sorted(r["by_topic"].items(), key=lambda kv: kv[1][0] / kv[1][1]):
        lines.append(f"  {topic:<14} {ok}/{total}")
    if r["wrong"]:
        lines += ["", "Review these:"]
        for n, q, c in r["wrong"]:
            given = q["options"][c] if c is not None else "(no answer)"
            lines.append(f"  Q{n}. {q['question']}")
            lines.append(f"      You chose: {given}")
            lines.append(f"      Correct:   {q['options'][q['answer']]}")
            if q.get("why"):
                lines.append(f"      Why:       {q['why']}")
    return "\n".join(lines)


def ask(questions):
    """Run the quiz interactively and return the chosen indexes."""
    choices = []
    for n, q in enumerate(questions, 1):
        print(f"\nQ{n} [{q['topic']}] {q['question']}")
        for i, opt in enumerate(q["options"]):
            print(f"   {LETTERS[i]}) {opt}")
        c = None
        while c is None:
            c = to_index(input("Your answer: "), len(q["options"]))
            if c is None:
                print(f"   Please type a letter A-{LETTERS[len(q['options']) - 1]}")
        choices.append(c)
    return choices


def main(argv=None):
    p = argparse.ArgumentParser(description="Annotator guideline quiz")
    p.add_argument("questions")
    p.add_argument("--answers", help="file with one answer letter per line (grades without asking)")
    p.add_argument("--pass-mark", type=float, default=0.8)
    p.add_argument("--shuffle", action="store_true", help="shuffle question order")
    p.add_argument("--seed", type=int, help="seed for --shuffle, so a sheet can be re-graded")
    a = p.parse_args(argv)
    qs = load(a.questions)
    if a.shuffle:
        random.Random(a.seed).shuffle(qs)
    if a.answers:
        with open(a.answers, encoding="utf-8") as f:
            letters = [line for line in f.read().splitlines() if line.strip()]
        choices = [to_index(x, len(q["options"])) for x, q in zip(letters, qs)]
        choices += [None] * (len(qs) - len(choices))
    else:
        choices = ask(qs)
    print(feedback(grade(qs, choices), a.pass_mark))


if __name__ == "__main__":
    main()
