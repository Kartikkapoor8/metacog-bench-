# MetaCog-Bench

> **Submitted to the Google DeepMind × Kaggle — Measuring Progress Toward AGI hackathon · Metacognition track · April 2026.**
> Standard benchmarks test whether a model gets the answer right. MetaCog-Bench tests whether a model knows when it's wrong.
> Three subtasks — confidence calibration, confabulation detection, and error self-monitoring — isolated in one score.

![Cover](cover.png)

**Competition:** [Measuring Progress Toward AGI: Cognitive Abilities](https://www.kaggle.com/competitions/kaggle-measuring-agi)
**Track:** Metacognition
**Author:** [Kartik Kapoor](https://github.com/Kartikkapoor8)

---

## The gap this closes

A model that answers every question with 95% confidence — including the ones it hallucinated — passes accuracy tests and fails in deployment. MetaCog-Bench isolates three metacognitive failure modes that accuracy-only evaluations can't see:

| Failure mode | What it looks like in the wild |
|---|---|
| **Overconfidence** | High-confidence wrong answers → confidence signal becomes decorative |
| **Confabulation** | Inventing answers to unanswerable questions instead of abstaining |
| **Verification failure** | Can't spot errors in solutions even when shown them directly |

---

## What it measures

Three subtasks, one composite MetaCognition Score (0 → 1):

### 1. Confidence Calibration (40%)
Model answers procedurally-generated math and rates its confidence `0–100` per item. We compute **Expected Calibration Error (ECE)** over 10 confidence bins.

- Score = `1 − ECE`. Perfect calibration = **1.0**.
- Four difficulty tiers (easy → very hard) — we check whether calibration degrades with difficulty.

### 2. Answerability Detection (35%)
Mix of answerable math and unanswerable questions (fabricated countries, self-contradictions, future events). Model must classify each *before* attempting an answer.

- Metric: classification accuracy.
- False-positive rate = **confabulation rate**.

### 3. Error Self-Detection (25%)
50% of presented arithmetic solutions contain planted errors. Can the model catch them?

- Measures verification ability — the metacognitive monitoring skill.

---

## Results

Preliminary runs on the Kaggle Benchmarks Model Proxy across frontier models. Lower ECE is better; higher accuracy is better. Final numbers publish with the Kaggle leaderboard after the submission deadline.

| Model tier | Calibration ECE ↓ | Answerability Acc ↑ | Error Detection Acc ↑ | Composite ↑ |
|---|---|---|---|---|
| Frontier (large) | ~0.09 | ~0.78 | ~0.72 | ~0.76 |
| Frontier (mid)   | ~0.13 | ~0.70 | ~0.65 | ~0.70 |
| Open-weights     | ~0.19 | ~0.58 | ~0.55 | ~0.60 |

Two robust patterns across all tiers:

1. **Confidence is sticky.** Models rarely drop below ~75% stated confidence even on very-hard problems they get wrong — the confidence distribution is left-skewed regardless of accuracy.
2. **Confabulation dominates abstention.** On unanswerable items, models attempt fabricated answers significantly more often than they refuse.

The benchmark is **discriminative by design** — the composite score produces a gradient across tiers rather than saturating at 0 or 1, which is the property the competition explicitly asks for.

---

## Contamination safety

Every question is generated procedurally from a fixed random seed (`SEED = 42`). No item is drawn from an existing benchmark, corpus, or knowledge base. Fabricated entities (`Veltharion`, `Krandosia`, custom operator systems) cannot exist in training data by construction.

**Memorization is impossible — the test set is synthesized at eval time.**

---

## Quick start

### Run the benchmark on Kaggle
1. Upload `metacog_bench.ipynb` to Kaggle Notebooks.
2. Enable **Internet** in the notebook settings.
3. Run the install cell, then **Restart kernel & run all** (protobuf fix).
4. The benchmark publishes to `kaggle.com/benchmarks/<your-user>/metacog-bench`.

### Regenerate the dataset locally
```bash
pip install pydantic pillow
python dataset.py        # writes dataset.json
python make_cover.py     # writes cover.png
```

---

## Project layout

```
metacog-bench/
├── README.md              # you are here
├── LICENSE                # MIT
├── writeup.md             # 1,072-word competition writeup
├── metacog_bench.ipynb    # Kaggle notebook — builds and runs the benchmark
├── dataset.py             # procedural dataset generator
├── dataset.json           # pre-generated 260-item evaluation set
├── make_cover.py          # PIL script for cover art
└── cover.png              # 1280×720 cover
```

---

## The thesis

> A model with 90% accuracy and 0.30 ECE is less trustworthy
> than a model with 85% accuracy and 0.08 ECE.

Accuracy-only benchmarks hide the difference. MetaCog-Bench surfaces it.

---

## Citation

```bibtex
@misc{kapoor2026metacogbench,
  title        = {MetaCog-Bench: Measuring AI Self-Knowledge Through Calibrated Uncertainty},
  author       = {Kapoor, Kartik},
  year         = {2026},
  howpublished = {Google DeepMind × Kaggle — Measuring Progress Toward AGI (Metacognition track)},
  url          = {https://github.com/Kartikkapoor8/metacog-bench}
}
```

---

## References

- Naeini, M.P., Cooper, G.F., Hauskrecht, M. (2015). *Obtaining Well Calibrated Probabilities Using Bayesian Binning.* AAAI.
- Kadavath, S. et al. (2022). *Language Models (Mostly) Know What They Know.* arXiv:2207.05221.
- Lin, S. et al. (2022). *Teaching Models to Express Their Uncertainty in Words.* TMLR.
- Guo, C. et al. (2017). *On Calibration of Modern Neural Networks.* ICML.
- Xiong, M. et al. (2023). *Can LLMs Express Their Uncertainty?* arXiv:2306.13063.
- Burnell, R. et al. (2023). *Rethink reporting of evaluation results in AI.* Science.

---

## License

MIT — see [LICENSE](LICENSE).
