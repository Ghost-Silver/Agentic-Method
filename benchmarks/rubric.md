# Benchmark Scoring Rubric

## Overview

Each benchmark output is evaluated across 6 dimensions on a 0-5 scale. The weighted sum produces a final score out of 5.

| Dimension | Weight | 5 (Excellent) | 3 (Acceptable) | 1 (Poor) | 0 (Missing) |
|-----------|--------|---------------|----------------|----------|-------------|
| Task Success | 25% | Fully achieves objective with actionable output. | Partially achieves objective; needs human refinement. | Misses main objective but contains some relevant content. | No relevant output. |
| DSL Compliance | 15% | All required tags present and correctly used. | Most tags present; minor misuse. | Some tags missing or misused. | No DSL structure. |
| Hypothesis Quality | 15% | Hypotheses are falsifiable, with predictions, controls, and alternatives. | Hypotheses stated but predictions or controls weak. | Hypotheses vague or non-falsifiable. | No explicit hypotheses. |
| Evidence Grounding | 15% | Every claim tied to explicit evidence; no hallucination. | Most claims grounded; minor unsupported assertions. | Several unsupported claims or fabrications. | Mostly hallucinated or ungrounded. |
| Logical Soundness | 15% | No circular reasoning, false dichotomies, or non-sequiturs. | Minor logical gaps. | Significant logical errors. | Argument is incoherent. |
| Efficiency | 15% | High signal-to-noise ratio; minimal token waste. | Some redundancy but acceptable. | Excessive verbosity or repetition. | Output is unusably long or short. |

## Hallucination Flags

Raters may flag specific hallucinations:

- `H-FACT`: Fabricated fact about code, paper, or system behavior.
- `H-CITATION`: Non-existent citation or reference.
- `H-CONF`: Overstated confidence without evidence.
- `H-CODE`: Invented API, function, or file path.

Each flag reduces the Evidence Grounding score by at least 1 point.

## Inter-Rater Reliability

- 20% of outputs are double-rated.
- Cohen's kappa target: ≥ 0.70.
- Disagreements are resolved by discussion and rubric refinement.

## Aggregated Metrics

For each baseline/task/model combination, report:

- Mean score
- Median score
- Standard deviation
- Task success rate (percentage of cases with Task Success ≥ 3)
- Hallucination rate (percentage of cases with ≥1 flag)
- Mean token usage
