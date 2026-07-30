# Baseline Prompt for Custom Benchmark

> Use this prompt to run custom benchmark tasks on ordinary models (control group).
> This is the **B1 — Generic CoT** baseline. It does NOT use Agentic Method DSL.

---

## System Prompt

You are a helpful assistant solving technical tasks. Think step by step, explain your reasoning clearly, and provide a concrete, actionable answer.

Do not use any special markup tags like `(CTX)`, `(H)`, `(PREDICTION)`, or `(VERDICT)`. Just produce a natural-language response with clear sections.

---

## User Prompt Template

```markdown
# Task

{task_description}

## Question

{task_question}

---

Please solve this task step by step:

1. Briefly restate the problem in your own words.
2. Identify the key factors or constraints.
3. Reason through possible causes, solutions, or options.
4. State your final answer or recommendation clearly.

Keep your response focused and avoid unnecessary verbosity.
```

---

## Output Format

No strict format required. A good response should include:

- A short problem summary
- Step-by-step reasoning
- A clearly marked final answer or recommendation

---

## Example Usage

For `benchmarks/tasks/bug-diagnosis-01.md`, fill in:

- `{task_description}` = the Problem Description section
- `{task_question}` = the Question section

Then send to the model and record the output for scoring.
