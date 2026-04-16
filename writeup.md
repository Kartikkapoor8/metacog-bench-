### MetaCog-Bench: Measuring AI Self-Knowledge Through Calibrated Uncertainty

### Team

Solo submission

### Problem Statement

Current AI evaluations measure *what* models know, but rarely *whether models know what they know*. A model that confidently answers every question — regardless of whether it actually knows the answer — is fundamentally unreliable for real-world deployment. This gap is metacognition: the ability to monitor, evaluate, and regulate one's own cognitive processes.

MetaCog-Bench addresses three specific metacognitive deficits that existing benchmarks fail to capture:

1. **Overconfidence**: Models consistently express high confidence even on questions they get wrong, making their confidence signals useless for downstream decision-making.
2. **Confabulation blindness**: When faced with unanswerable questions (fabricated entities, contradictions, missing information), models often produce plausible-sounding but entirely fabricated answers rather than acknowledging uncertainty.
3. **Verification failure**: Models struggle to detect errors in presented solutions, revealing weak metacognitive monitoring — the ability to check and validate outputs.

These deficits directly impact trust, safety, and usability. MetaCog-Bench quantifies them with a single, interpretable composite score.

### Task & Benchmark Construction

MetaCog-Bench comprises three subtasks, each isolating a distinct metacognitive ability:

**Task 1: Confidence Calibration (40% weight)**
The model answers 120 procedurally generated questions and rates its confidence (0-100%) for each. We compute Expected Calibration Error (ECE) — the weighted average gap between stated confidence and actual accuracy across 10 confidence bins. A perfectly calibrated model achieves ECE = 0. Questions span four difficulty tiers (easy arithmetic through nested multi-step computation) to test whether calibration degrades with difficulty.

**Task 2: Answerability Detection (35% weight)**
The model receives 100 questions — 60 answerable (math and logic with verifiable solutions) and 40 unanswerable (fabricated countries, self-contradictory premises, future events, missing information). Before answering, the model must classify each question as answerable or not. We measure classification accuracy, sensitivity (correctly identifying answerable questions), and specificity (correctly rejecting unanswerable ones). The false positive rate directly measures confabulation tendency.

**Task 3: Error Self-Detection (25% weight)**
The model reviews 40 arithmetic solutions where 50% contain planted errors (plausible off-by-small-amount mistakes). It must determine which answers are correct and which contain errors. This tests metacognitive monitoring — the ability to verify work rather than simply accepting presented information.

All subtasks use Pydantic structured output schemas to ensure parseable responses. Each subtask runs within isolated chat contexts (`kbench.chats.new()`) to prevent cross-contamination between questions.

The benchmark produces a weighted composite MetaCognition Score from 0 to 1.

### Dataset

All 260 evaluation items are procedurally generated with a fixed random seed (42) for reproducibility. No items are drawn from existing benchmarks, knowledge bases, or training corpora.

**Arithmetic questions** (80 items): Generated across four difficulty tiers — two-digit addition/subtraction (easy), three-digit multiplication (medium), multi-step mixed operations (hard), and nested operations with 4+ digit numbers (very hard). All answers are computationally verifiable.

**Logic questions** (40 items): Arithmetic sequences, geometric sequences, modular arithmetic, and fabricated operator systems (e.g., "★ is defined as x★y = (x×y) + (x−y)"). The fabricated operators are novel rule systems that cannot appear in training data.

**Unanswerable questions** (40 items): Five categories — fabricated nations (Veltharion, Krandosia, etc.) presented as real, future events (global temperature in 2050), self-contradictory premises, missing-information word problems, and questions about non-existent entities.

**Error detection items** (40 items): Multiplication problems with presented answers, where 50% have small arithmetic errors (within ~2% of the correct answer) to test fine-grained verification.

Data types: question text (string), correct answer (string/numeric), difficulty tier (categorical), answerability flag (boolean), error flag (boolean).

### Technical Details

**Structured output enforcement**: All three tasks use Pydantic `BaseModel` schemas passed to `llm.prompt(schema=...)`. This ensures every response includes both the answer and metacognitive metadata (confidence score, answerability judgment, error assessment) in a machine-parseable format.

**Expected Calibration Error**: Computed over 10 equal-width confidence bins (0-10%, 10-20%, ..., 90-100%). For each bin, we calculate the absolute difference between mean confidence and mean accuracy, weighted by bin population. This follows the standard ECE formulation from Naeini et al. (2015).

**Contamination safety**: Procedural generation with fixed seeds means every question is novel. Fabricated entities (countries, operators) cannot exist in any training corpus. Mathematical questions use random operands, making memorization impossible.

**Answer normalization**: Numeric answers are normalized by stripping commas, whitespace, and extracting the first integer match, ensuring fair comparison regardless of formatting differences.

**Composite scoring**: Weights (0.40/0.35/0.25) reflect discriminatory value — calibration is weighted highest because it reveals the most about a model's self-awareness, and is the most novel measurement in this benchmark.

### Results, Insights, and Conclusions

MetaCog-Bench reveals several patterns in model behavior not visible from standard benchmarks:

1. **Systematic overconfidence**: Models consistently report higher confidence than warranted, particularly on hard questions. The confidence-accuracy gap widens as difficulty increases — models do not proportionally reduce confidence when questions become harder.

2. **Asymmetric answerability errors**: Models are much more likely to attempt answering unanswerable questions (false positives / confabulation) than to refuse answerable ones (false negatives). This reveals a systematic bias toward generating answers over acknowledging uncertainty.

3. **Difficulty-dependent calibration collapse**: On easy questions, models are reasonably well-calibrated. On hard questions, calibration degrades significantly. This suggests metacognitive monitoring is a downstream casualty of task difficulty, not an independent capability.

4. **Error detection asymmetry**: Models are better at confirming correct answers than detecting errors, suggesting a confirmation bias in verification behavior.

5. **Discriminatory gradient**: Different model families show meaningfully different metacognitive profiles. Larger models tend to be better calibrated, but the relationship is not monotonic — some smaller models with specific training approaches show superior specificity on unanswerable questions.

These insights directly address the competition's core question: MetaCog-Bench tells us about the *reliability* of model outputs, not just their *accuracy*. A model with 90% accuracy but 0.30 ECE is less trustworthy than one with 85% accuracy and 0.08 ECE.

### Organizational Affiliations

Independent researcher, no organizational affiliation.

### References & Citations

- Naeini, M.P., Cooper, G.F., Hauskrecht, M. (2015). "Obtaining Well Calibrated Probabilities Using Bayesian Binning." AAAI.
- Kadavath, S. et al. (2022). "Language Models (Mostly) Know What They Know." arXiv:2207.05221.
- Lin, S. et al. (2022). "Teaching Models to Express Their Uncertainty in Words." TMLR.
- Burnell, R. et al. (2023). "Rethink reporting of evaluation results in AI." Science.
- Plomecka, M., Yan, Y., Kang, N. et al. (2026). "Measuring Progress Toward AGI: A Cognitive Framework." Kaggle Competition.
- Guo, C. et al. (2017). "On Calibration of Modern Neural Networks." ICML.
- Xiong, M. et al. (2023). "Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs." arXiv:2306.13063.
