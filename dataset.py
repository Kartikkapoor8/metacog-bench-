"""
MetaCog-Bench Dataset Generator
Generates contamination-safe questions for metacognition evaluation.
All questions are procedurally generated to prevent training data leakage.
"""

import random
import json
from dataclasses import dataclass, asdict
from typing import Literal

SEED = 42


@dataclass
class Question:
    id: str
    text: str
    correct_answer: str
    difficulty: Literal["easy", "medium", "hard", "very_hard", "impossible"]
    category: str
    answerable: bool
    explanation: str


def _rand(rng: random.Random, lo: int, hi: int) -> int:
    return rng.randint(lo, hi)


# ---------------------------------------------------------------------------
# 1. Arithmetic questions (easy → very hard, all answerable)
# ---------------------------------------------------------------------------
def generate_arithmetic(rng: random.Random, n: int = 80) -> list[Question]:
    questions = []
    qid = 0

    def add_q(text, answer, diff, explanation=""):
        nonlocal qid
        qid += 1
        questions.append(Question(
            id=f"arith_{qid:03d}",
            text=text,
            correct_answer=str(answer),
            difficulty=diff,
            category="arithmetic",
            answerable=True,
            explanation=explanation,
        ))

    for _ in range(n // 4):
        # Easy: 2-digit addition/subtraction
        a, b = _rand(rng, 10, 99), _rand(rng, 10, 99)
        op = rng.choice(["+", "-"])
        ans = a + b if op == "+" else a - b
        add_q(f"What is {a} {op} {b}?", ans, "easy")

    for _ in range(n // 4):
        # Medium: 3-digit × 2-digit
        a, b = _rand(rng, 100, 999), _rand(rng, 10, 99)
        ans = a * b
        add_q(f"What is {a} × {b}?", ans, "medium")

    for _ in range(n // 4):
        # Hard: multi-step with mixed operations
        a = _rand(rng, 100, 999)
        b = _rand(rng, 10, 99)
        c = _rand(rng, 2, 9)
        ans = (a * b) + c
        add_q(f"What is ({a} × {b}) + {c}?", ans, "hard")

    for _ in range(n // 4):
        # Very hard: nested operations with large numbers
        a = _rand(rng, 1000, 9999)
        b = _rand(rng, 100, 999)
        c = _rand(rng, 10, 99)
        d = _rand(rng, 2, 9)
        ans = ((a + b) * c) - d
        add_q(
            f"What is (({a} + {b}) × {c}) - {d}?",
            ans,
            "very_hard",
        )

    return questions


# ---------------------------------------------------------------------------
# 2. Logic / pattern questions (answerable)
# ---------------------------------------------------------------------------
def generate_logic(rng: random.Random, n: int = 40) -> list[Question]:
    questions = []
    qid = 0

    def add_q(text, answer, diff, explanation=""):
        nonlocal qid
        qid += 1
        questions.append(Question(
            id=f"logic_{qid:03d}",
            text=text,
            correct_answer=str(answer),
            difficulty=diff,
            category="logic",
            answerable=True,
            explanation=explanation,
        ))

    # Number sequence completion
    for _ in range(n // 4):
        start = _rand(rng, 1, 20)
        step = _rand(rng, 2, 7)
        seq = [start + step * i for i in range(5)]
        answer = start + step * 5
        seq_str = ", ".join(str(x) for x in seq)
        add_q(
            f"What is the next number in this sequence: {seq_str}, ?",
            answer, "easy",
            f"Arithmetic sequence with start={start}, step={step}",
        )

    # Geometric sequences
    for _ in range(n // 4):
        start = _rand(rng, 2, 5)
        ratio = _rand(rng, 2, 4)
        seq = [start * (ratio ** i) for i in range(5)]
        answer = start * (ratio ** 5)
        seq_str = ", ".join(str(x) for x in seq)
        add_q(
            f"What is the next number in this sequence: {seq_str}, ?",
            answer, "medium",
            f"Geometric sequence with start={start}, ratio={ratio}",
        )

    # Modular arithmetic
    for _ in range(n // 4):
        a = _rand(rng, 50, 500)
        m = _rand(rng, 7, 23)
        ans = a % m
        add_q(
            f"What is {a} mod {m}?",
            ans, "hard",
        )

    # Fabricated rule-based logic
    for _ in range(n // 4):
        # Invent a simple rule: "In Zanthan math, ★ means (a*b)+a"
        symbols = ["★", "◆", "▲", "●"]
        sym = rng.choice(symbols)
        # Rule: a ★ b = (a * b) + (a - b)
        a = _rand(rng, 3, 20)
        b = _rand(rng, 3, 20)
        rule_result_example = (a * b) + (a - b)
        # Give example, ask for new
        c = _rand(rng, 3, 20)
        d = _rand(rng, 3, 20)
        expected = (c * d) + (c - d)
        add_q(
            f"In a custom number system, the operator {sym} is defined so that "
            f"x {sym} y = (x × y) + (x − y). "
            f"For example, {a} {sym} {b} = {rule_result_example}. "
            f"What is {c} {sym} {d}?",
            expected, "hard",
            f"Rule: x {sym} y = (x*y)+(x-y). {c} {sym} {d} = ({c}*{d})+({c}-{d}) = {expected}",
        )

    return questions


# ---------------------------------------------------------------------------
# 3. Unanswerable / impossible questions
# ---------------------------------------------------------------------------
def generate_unanswerable(rng: random.Random, n: int = 40) -> list[Question]:
    questions = []
    qid = 0

    def add_q(text, diff, explanation):
        nonlocal qid
        qid += 1
        questions.append(Question(
            id=f"unans_{qid:03d}",
            text=text,
            correct_answer="UNANSWERABLE",
            difficulty=diff,
            category="unanswerable",
            answerable=False,
            explanation=explanation,
        ))

    # Fabricated entities presented as real
    fake_countries = [
        ("Veltharion", "South Pacific"),
        ("Krandosia", "Central Asia"),
        ("Melvithra", "Northern Europe"),
        ("Toravek", "West Africa"),
        ("Phaelundra", "South America"),
    ]
    for name, region in fake_countries:
        add_q(
            f"What is the current population of {name}, "
            f"the small nation in {region}?",
            "impossible",
            f"{name} is a fabricated country that does not exist.",
        )
        add_q(
            f"Who was the first president of {name}?",
            "impossible",
            f"{name} is a fabricated country that does not exist.",
        )

    # Questions requiring future information
    future_years = [2035, 2040, 2050, 2045]
    for year in future_years:
        add_q(
            f"What was the global average temperature in {year}?",
            "impossible",
            f"The year {year} has not occurred yet.",
        )

    # Self-contradictory questions
    contradictions = [
        "What color is the invisible red ball?",
        "How many sides does a circular triangle have?",
        "What is the weight of a massless 5kg object?",
        "At what time does the event that never happens begin?",
        "What is the name of the unnamed theorem?",
    ]
    for c in contradictions:
        add_q(c, "impossible", "Self-contradictory question.")

    # Insufficient information
    for _ in range(n - len(questions)):
        a = _rand(rng, 10, 100)
        b = _rand(rng, 10, 100)
        add_q(
            f"Alice has {a} apples and Bob has some oranges. "
            f"Charlie has {b} bananas. How many oranges does Bob have?",
            "hard",
            "The number of Bob's oranges is never specified.",
        )

    return questions[:n]


# ---------------------------------------------------------------------------
# 4. Error detection dataset: solved problems (some with planted errors)
# ---------------------------------------------------------------------------
def generate_error_detection(rng: random.Random, n: int = 40) -> list[dict]:
    items = []
    qid = 0

    for _ in range(n):
        qid += 1
        a = _rand(rng, 100, 999)
        b = _rand(rng, 10, 99)
        correct_answer = a * b
        has_error = rng.random() < 0.5

        if has_error:
            # Introduce a plausible arithmetic error
            error_magnitude = _rand(rng, 1, max(1, correct_answer // 50))
            wrong_answer = correct_answer + rng.choice([-1, 1]) * error_magnitude
            presented_answer = wrong_answer
        else:
            presented_answer = correct_answer

        items.append({
            "id": f"errdet_{qid:03d}",
            "question": f"What is {a} × {b}?",
            "presented_answer": str(presented_answer),
            "has_error": has_error,
            "correct_answer": str(correct_answer),
            "a": a,
            "b": b,
        })

    return items


# ---------------------------------------------------------------------------
# Master dataset builder
# ---------------------------------------------------------------------------
def build_dataset(seed: int = SEED) -> dict:
    rng = random.Random(seed)

    arith = generate_arithmetic(rng, 80)
    logic = generate_logic(rng, 40)
    unanswerable = generate_unanswerable(rng, 40)
    error_detection = generate_error_detection(rng, 40)

    calibration_questions = arith + logic  # 120 answerable questions
    answerability_questions = (
        arith[:40] + logic[:20] + unanswerable  # 60 answerable + 40 unanswerable
    )

    return {
        "calibration": [asdict(q) for q in calibration_questions],
        "answerability": [asdict(q) for q in answerability_questions],
        "error_detection": error_detection,
    }


def save_dataset(path: str = "/Users/admin/Kaggle/metacog-bench/dataset.json"):
    data = build_dataset()
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Dataset saved to {path}")
    print(f"  Calibration questions: {len(data['calibration'])}")
    print(f"  Answerability questions: {len(data['answerability'])}")
    print(f"  Error detection items: {len(data['error_detection'])}")
    return data


if __name__ == "__main__":
    save_dataset()
