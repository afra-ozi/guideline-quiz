# 📝 Guideline Training Quiz

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white) ![No dependencies](https://img.shields.io/badge/dependencies-none-2ea44f?style=flat-square) ![Tests](https://img.shields.io/badge/tests-unittest-2ea44f?style=flat-square) ![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

A terminal quiz that trains new annotators and raters on guideline edge cases, with a score per topic and an explanation for every wrong answer.

## Why this exists

Most quality problems on a new project come from a handful of guideline edge cases. A short quiz with explanations fixes them before they reach real tasks. Questions live in a JSON file, so a QA lead can add new ones without touching code.

## Features

- **Interactive mode**: answer A/B/C in the terminal
- **Answer-sheet mode**: grade a file of letters (`--answers`)
- **Score by topic**, weakest topic first
- **Review section** with the correct answer and the reason
- **Shuffle** with a seed, and a configurable **pass mark**
- Includes 10 sample questions on search relevance, LLM rating, safety and annotation

## Quick start

No installs needed, just Python 3.9+.

```bash
git clone https://github.com/afra-ozi/guideline-quiz.git
cd guideline-quiz
python quiz.py questions.json --answers sample_answers.txt
```

## Input

`questions.json`: a list of `{topic, question, options, answer, why}` where `answer` is the 0-based index of the correct option.

## Sample output

Running `python quiz.py questions.json --answers sample_answers.txt` on the included sample data:

```text
Score: 8/10 (80%), PASS (pass mark 80%)

By topic:
  llm-rating     2/3
  annotation     2/3
  relevance      3/3
  safety         1/1

Review these:
  Q4. Response A is longer and well written but states one wrong date. Response B is short and fully correct. Which is better?
      You chose: A, because it is more detailed
      Correct:   B, because accuracy comes first
      Why:       A factual error outweighs style and length.
  Q9. Review: 'Great phone, but the battery dies by noon.' Overall sentiment?
      You chose: Positive
      Correct:   Mixed / neutral
      Why:       It has clear positive and negative parts with no dominant overall tone.
```

## Tests

```bash
python -m unittest -v test_quiz
```

## License

MIT
