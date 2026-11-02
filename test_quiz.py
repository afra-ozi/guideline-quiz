import json
import os
import tempfile
import unittest

from quiz import grade, load, to_index

QS = [
    {"topic": "a", "question": "q1", "options": ["x", "y"], "answer": 0},
    {"topic": "a", "question": "q2", "options": ["x", "y", "z"], "answer": 2},
    {"topic": "b", "question": "q3", "options": ["x", "y"], "answer": 1},
]


class TestQuiz(unittest.TestCase):
    def test_to_index(self):
        self.assertEqual(to_index("b", 3), 1)
        self.assertEqual(to_index(" C ", 3), 2)
        self.assertIsNone(to_index("d", 3))
        self.assertIsNone(to_index("", 3))

    def test_grade(self):
        r = grade(QS, [0, 1, 1])
        self.assertEqual(r["correct"], 2)
        self.assertAlmostEqual(r["score"], 2 / 3)
        self.assertEqual(r["by_topic"]["a"], [1, 2])
        self.assertEqual([n for n, _, _ in r["wrong"]], [2])

    def test_unanswered_counts_wrong(self):
        self.assertEqual(grade(QS, [None, None, None])["correct"], 0)

    def test_answer_count_must_match(self):
        with self.assertRaises(ValueError):
            grade(QS, [0])

    def test_load_rejects_bad_answer_index(self):
        bad = [{"topic": "a", "question": "q", "options": ["x"], "answer": 3}]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(bad, f)
        try:
            with self.assertRaises(ValueError):
                load(f.name)
        finally:
            os.remove(f.name)

    def test_sample_bank_is_valid(self):
        self.assertEqual(len(load(os.path.join(os.path.dirname(__file__), "questions.json"))), 10)


if __name__ == "__main__":
    unittest.main()
