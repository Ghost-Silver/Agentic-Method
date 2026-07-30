# Agentic Method Benchmark Plan

> Version: 0.1  
> Status: Draft — awaiting human review before execution  
> Goal: Quantify whether Agentic Method improves task success, reasoning quality, and hallucination resistance compared to baseline prompts.

---

## 1. Executive Summary

This plan proposes a three-phase benchmark for the `Agentic Method` prompt framework. We will measure its effectiveness across 5 representative high-stakes tasks, compare it against 4 baselines, and evaluate on multiple model backends.

The benchmark is designed to be **reproducible**, **version-controlled**, and **human-auditable**. All tasks, rubrics, and raw outputs will be committed to the repository.

---

## 2. Research Questions

1. **RQ1 — Value Proposition**: Does Agentic Method achieve higher task success and lower hallucination than zero-shot and generic CoT prompts?
2. **RQ2 — Model Scaling**: How sensitive is Agentic Method to model size/context length? At what point do medium models match larger models?
3. **RQ3 — Evolution Effectiveness**: Does Prompt Evolution Loop (PEL) consistently improve prompt quality over the seed version?
4. **RQ4 — Cost-Efficiency**: What is the token overhead, and is the quality gain worth the cost?

---

## 3. Benchmark Tasks

Each task has 3-5 test cases. Cases are stored in `benchmarks/tasks/`.

### Task 1: Bug Root-Cause Diagnosis

**Type**: Engineering reasoning  
**Difficulty**: High  
**Description**: Given a bug report and relevant code snippets, the model must identify the root cause, generate falsifiable hypotheses, and propose a minimal fix.  
**Evaluation**: Root-cause accuracy, hypothesis quality, fix correctness.

### Task 2: Code Review for Regressions

**Type**: Engineering review  
**Difficulty**: Medium  
**Description**: Given a diff, identify potential correctness, performance, or ABI issues.  
**Evaluation**: Precision/recall against a known issue list, false-positive rate.

### Task 3: Experimental Design

**Type**: Scientific method  
**Difficulty**: Medium  
**Description**: Given an ambiguous performance or behavior question, design a valid experiment with prediction, control group, and falsification criteria.  
**Evaluation**: Completeness of `(H)` → `(PREDICTION)` → `(EXP)` → `(OBSERVATION)` → `(VERDICT)` chain.

### Task 4: Logical Fallacy Detection

**Type**: Logical reasoning  
**Difficulty**: Medium  
**Description**: Given a technical argument, identify hidden assumptions, logical fallacies, and counterexamples.  
**Evaluation**: Number of valid fallacies/assumptions identified, absence of fabricated issues.

### Task 5: Architecture Trade-off Analysis

**Type**: Design reasoning  
**Difficulty**: High  
**Description**: Given competing architectural options, produce a structured comparison with decision criteria, risks, and explicit HITL gates.  
**Evaluation**: Coverage of decision dimensions, confidence calibration, risk disclosure.

---

## 4. Baselines

| Baseline ID | Description | Purpose |
|-------------|-------------|---------|
| B0 — Zero-shot | Task description only. | Measures model native capability without scaffolding. |
| B1 — Generic CoT | "Think step by step and explain your reasoning." | Measures simple reasoning scaffolding. |
| B2 — Agentic Method (seed) | Use raw `core/` prompts without PEL. | Measures core methodology value. |
| B3 — Agentic Method (PEL-v1) | Use prompts after one PEL iteration. | Measures evolution benefit. |

---

## 5. Models Under Test

We recommend testing on a spectrum of capability and cost:

| Tier | Example Models | Role |
|------|----------------|------|
| Top-tier | GPT-4o, Claude 3.5 Sonnet, DeepSeek-V3 | Main orchestrator / full protocol |
| Mid-tier | Claude 3 Haiku, GPT-4o-mini, Qwen2.5-72B | Sub-agent / abridged protocol |
| Open-weight | Llama-3.1-70B, Qwen2.5-32B, DeepSeek-V2.5 | Local / cost-sensitive evaluation |

**Note**: For Phase 1, we will test only 2 models to control cost.

---

## 6. Evaluation Rubric

Each output is scored on a 0-5 scale across 6 dimensions.

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Task Success | 25% | Did the model achieve the primary objective? |
| DSL Compliance | 15% | Did it follow required tags (CTX/H/PREDICTION/VERDICT/CONF)? |
| Hypothesis Quality | 15% | Are hypotheses falsifiable, with predictions and controls? |
| Evidence Grounding | 15% | Are claims tied to explicit evidence, not hallucination? |
| Logical Soundness | 15% | Any circular reasoning, non-sequiturs, or false dichotomies? |
| Efficiency | 15% | Token usage relative to output quality. |

Scoring is performed by a human rater, with a second rater auditing a 20% sample. Automated checks (regex tag presence, evidence grade format) run first.

---

## 7. Data Collection Format

Each run produces a JSON file:

```json
{
  "task_id": "bug-diagnosis-01",
  "baseline_id": "B2",
  "model_id": "claude-3-5-sonnet-20241022",
  "seed_prompt_version": "experimental-design-prompt.md@ae39385",
  "output": "...",
  "scores": {
    "task_success": 4,
    "dsl_compliance": 5,
    "hypothesis_quality": 4,
    "evidence_grounding": 4,
    "logical_soundness": 5,
    "efficiency": 3
  },
  "token_usage": {
    "input": 4200,
    "output": 3100
  },
  "hallucination_flags": [],
  "rater_notes": "..."
}
```

---

## 8. Execution Plan

### Phase 1 — Pilot (2 weeks)

**Scope**:
- Tasks: Bug Diagnosis + Experimental Design
- Baselines: B0, B1, B2
- Models: 2 (one top-tier, one mid-tier)
- Cases: 3 per task

**Deliverable**: `benchmarks/results/phase-1-report.md`

**Success Gate**: Agentic Method (B2) shows ≥15% improvement in average score over B1 on at least one task.

### Phase 2 — Breadth (3 weeks)

**Scope**:
- Tasks: All 5 tasks
- Baselines: B0, B1, B2
- Models: 4 (top-tier × 2, mid-tier × 2)
- Cases: 5 per task

**Deliverable**: `benchmarks/results/phase-2-report.md`

### Phase 3 — Evolution (3 weeks)

**Scope**:
- Tasks: All 5 tasks
- Baselines: B2 (seed) vs B3 (PEL-v1)
- Models: 2 top-tier models
- Cases: 5 per task

**Deliverable**: `benchmarks/results/phase-3-report.md` + updated `README.md` with benchmark highlights.

---

## 9. Expected Outputs

1. `benchmarks/tasks/*.md` — task definitions and ground-truth rubrics
2. `benchmarks/scripts/runner.py` — automated benchmark runner
3. `benchmarks/results/phase-{1,2,3}-report.md` — result reports
4. `benchmarks/rubric.md` — detailed scoring guide
5. Updated `README.md` badge: `Benchmarks`

---

## 10. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| High token cost | Medium | Start with 2 tasks × 3 cases; use cheaper models for B0/B1. |
| Subjective scoring | Medium | Two raters + inter-rater reliability check; publish rubric. |
| Model API drift | Low | Pin exact model versions in result files. |
| Prompt leakage in training data | Low | Use synthetic or already-public code snippets. |
| PEL iterations produce worse prompts | Medium | Archive all mutations; report negative results too. |

---

## 11. Open Questions for Review

1. Should we include a **human baseline** (expert engineer/researcher score) for calibration?
2. Should we publish raw outputs, or only aggregated scores?
3. Do we want a **leaderboard** format in the README?
4. Which two models should Phase 1 use?

---

## 12. Decision Gate

**(HITL)** This plan must be approved before execution. Once approved, the first step is to create 3 pilot task cases and the scoring rubric.
