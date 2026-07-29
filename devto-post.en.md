# We Open-Sourced a Methodology That Teaches LLMs to Actually Think

> **Agentic Method** — not more prompts, but a workflow that makes model output observable, falsifiable, and evolvable.
>
> GitHub: https://github.com/Ghost-Silver/Agentic-Method

---

## The Problem Is Becoming Obvious

Today's LLMs — especially mid-range models — already have strong **instruction-following abilities**. Ask them to format output, follow steps, call tools: they mostly comply.

But as soon as the task gets complex — reviewing a multi-file code change, designing a controlled experiment, or reasoning about the root cause of a system bug — models tend to fail in two characteristic ways:

1. **Hallucination**: confidently stating conclusions with no grounding.
2. **Post-hoc rationalization**: jumping to an answer first, then fabricating a plausible chain of reasoning afterward (fake CoT).

The issue isn't that models aren't "smart enough." It's that their **decoding space is too unconstrained**. Without external scaffolding, nothing anchors them to the track of "correct reasoning."

---

## Our Approach: Constrain the Decoding Space with Methodology

**Agentic Method** is not a collection of prompts. It is a **meta-workflow** that externalizes, structures, and audits the model's reasoning process through four mechanisms:

### 1. Strict DSL Anchoring

Tags like `(CTX)`, `(H)`, `(PREDICTION)`, `(OBSERVATION)`, `(VERDICT)` force the model to declare at every critical step:

- What is the current context?
- What is the hypothesis?
- What is the falsifiable prediction?
- What was actually observed?
- What is the final verdict?

This turns output from free-form prose into structured scientific records — and hallucinations drop dramatically.

### 2. Forced Deep Reasoning

Every key conclusion must carry:

- Evidence grade (F0-F4)
- Confidence `(CONF: <level>, <evidence summary>)`
- At least one competing hypothesis `(BRANCH)`
- Explicit falsification conditions `(FALSIFICATION)`

No more surface-level answers.

### 3. Sub-Agent Cross-Review

Roles like `FORM_REVIEWER`, `HYPOTHESIS_VALIDATOR`, and `COUNTEREXAMPLE_REVIEWER` make agents audit each other. Circular reasoning, hidden assumptions, and post-hoc rationalizations get flagged explicitly.

### 4. Embedded Scientific Method

Bisection, ablation, controlled experiments, and counterfactual reasoning are not just suggestions in a document. They are **non-skippable steps** embedded in the prompts.

---

## 30 Core Prompts for High-Stakes Tasks

The repo includes 30 desensitized, reusable core prompts:

- `experimental-design-prompt.md` — design verifiable experiments
- `logical-inference-prompt.md` — rigorous logical reasoning and proof review
- `code-review-prompt.md` — systematic code review
- `debug-prompt.md` — causal diagnosis and repair
- `performance-optimization-prompt.md` — performance decision protocol
- `prompt-evolution-prompt.md` — **let prompts evolve themselves**
- `subagent-protocol.md` — protocol for 18 sub-agent roles
- ...and many more

All prompts share the same DSL and can be loaded on demand, composed, and evolved.

---

## Prompt Evolution Loop (PEL)

Perhaps the most interesting part is the **Prompt Evolution Loop (PEL)**.

The idea is simple: take a seed prompt, generate multiple mutated variants, evaluate them in parallel on the same set of real tasks, and keep the fittest ones.

Our example report shows one real PEL run:

- The `CONSTRAINT_ADD` mutation fixed a P0 protocol-consistency defect.
- The `ANTI_PATTERN_BLOCK` mutation had to be discarded because it contradicted existing rules.
- The `EXAMPLE_INJECT` mutation only worked when examples were bound to concrete checklist items.

These findings are themselves evidence that prompt engineering can move from alchemy to experimental science.

---

## Recommended Setup

This methodology is designed for high-stakes tasks and consumes more tokens and context. We believe it's worth it.

- **Main agent / orchestration**: 200B+ parameters, 200K+ context window
- **Sub-agent / review layer**: cheaper medium-sized models
- **How to run**: read `main.md` first, then load only the prompt matching your current task

---

## Where It Helps

- Complex code review and architecture decisions
- Root-cause bug diagnosis
- Performance optimization experiment design
- Scientific argumentation and technology surveys
- Any task where a wrong statement is expensive

---

## Open Source, MIT License

We want this methodology to be validated, improved, and applied across more domains.

If you:

- Apply it to a domain outside software engineering or research;
- Evolve a better prompt variant through PEL;
- Find a flaw in any prompt;

Please open an Issue or PR on GitHub. The community will accumulate domain-specific adapters and best practices together.

---

## Next Steps

1. Open the repo: https://github.com/Ghost-Silver/Agentic-Method
2. Start with `core/master-prompt.md`
3. Pick a hard task you're currently struggling with, and try `experimental-design-prompt.md` or `debug-prompt.md`
4. If it works, give us a ⭐ or share your use case

---

**This is not another prompt repo. This is a workflow that teaches LLMs to think like scientists.**

https://github.com/Ghost-Silver/Agentic-Method
