<div align="center">

# Agentic Method

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Prompts](https://img.shields.io/badge/Prompts-30%20core-green)](./core)
[![Examples](https://img.shields.io/badge/Examples-12-orange)](./examples)
[![Methodology](https://img.shields.io/badge/Methodology-OHEOU--KU-purple)]()

**A rigorous, evidence-driven methodology for autonomous agents.**  
**Battle-tested as CTorch Agent, now open-sourced.**

<p align="center">
  <b>Observation → Hypothesis → Experiment → Observation Update → Knowledge Update</b><br/>
  <b>观察 → 假设 → 实验 → 观测更新 → 知识更新</b>
</p>

[中文版本](./README.md)

</div>

---

## What is this?

`Agentic Method` is a collection of meta-prompts and sub-agent protocols designed for high-stakes engineering, research, and decision-making tasks. It is not a lightweight chat prompt library — it is a workflow system that forces agents to:

1. **Freeze context** before acting.
2. Generate **competing hypotheses**, not single answers.
3. Make **falsifiable, quantitative predictions** before experiments.
4. Report **observations and verdicts**, not just conclusions.
5. **Archive failures** and update world models honestly.
6. **Evolve their own prompts** through controlled parallel evaluation.

## Design Principles

Today's mid-range and low-end models already possess strong **instruction-following capabilities**. Where they truly lag behind top-tier models is **zero-shot reasoning**. Yet even high-end models are prone to logical fallacies and hallucinations when tackling large-scale code development or complex scientific problems.

`Agentic Method` addresses this through the following mechanisms:

- **Strict DSL anchoring**: Tags like `(CTX)`, `(H)`, `(EXP)`, `(PREDICTION)`, `(OBSERVATION)`, `(VERDICT)` constrain the model's decoding space to the target task region, significantly reducing hallucinations.
- **Forced deep reasoning**: Every key conclusion must include `(CONF)` confidence and evidence grade; models cannot stop at surface-level answers.
- **Sub-agent cross-review**: Roles such as `FORM_REVIEWER`, `HYPOTHESIS_VALIDATOR`, and `COUNTEREXAMPLE_REVIEWER` catch circular reasoning, hidden assumptions, and post-hoc rationalizations.
- **Scientific methodology**: Counterfactual reasoning, bisection, ablation studies, controlled experiments, and thought experiments are explicitly embedded into the workflow, forcing high-order thinking.

Essentially, we are not making the model "smarter"; we are making its reasoning process **more observable, falsifiable, and auditable**.

## Model Requirements and Cost Strategy

### Recommended Configuration

For complex tasks in this protocol — especially multi-file code review, architecture decisions, and long-chain causal reasoning — we recommend:

- **Parameters**: 200B+
- **Context window**: 200K+
- **Capabilities**: Strong instruction following, stable long-context handling, tool-use support (for sub-agents)

### Cost-Reduction Strategy

This protocol consumes significant tokens and context, but the quality gains justify the cost. The best practice is **on-demand loading + model routing**:

- **Main Agent / Orchestration**: Use the strongest model for task decomposition, hypothesis generation, and final verdicts.
- **Sub-agent / Review layer**: Use cheaper models for format review, hypothesis validation, counterexample construction, and similar sub-tasks.
- **On-demand loading**: Do not load all prompts at once. Let the Agent read `main.md` first, then load only the core prompt matching the current task.
- **Scheduled evolution**: Run `prompt-evolution-prompt.md` during idle time to iteratively improve prompts via PEL.

With well-designed prompts, a medium-sized model can approach or even match larger models on specific sub-tasks.

## Recommended Workflow

```
Step 1: Agent reads main.md to understand global protocol and available prompts
        ↓
Step 2: User tells Agent the current environment (project type, preferences, hard constraints, goals)
        ↓
Step 3: Agent automatically selects and fills the adapted prompt
        ↓
Step 4: Execute task, invoke sub-agents when necessary
        ↓
Step 5: After task completion, Agent organizes materials, summarizes insights, generates MEMs
        ↓
Step 6: During idle time, run PEL to iterate and optimize prompts (at least 2 rounds recommended)
```

## Applicable Domains

`Agentic Method` was originally designed for **software development** and **scientific reasoning**, especially suited for:

- Code review and refactoring
- Complex bug diagnosis
- Performance optimization and experiment design
- Architecture decisions and technology surveys
- Causal argumentation in papers and research reports

For other domains, please refer to `ADAPTATION_GUIDE.md` for customization, and consider contributing your adapted use cases.

## Origin

`Agentic Method` was originally designed as the internal workflow for **CTorch Agent**, used to constrain agent reasoning during code review, bug diagnosis, performance optimization, and architecture decisions for the CTorch deep-learning framework. After multiple rounds of battle-testing, we abstracted the project-agnostic methodology, desensitized it, and open-sourced it.

CTorch Agent remains a **reference implementation** of Agentic Method: it has proven the value of this methodology in high-stakes domains such as systems programming, HPC backends, and automatic differentiation. If you work in similar engineering fields, the desensitized cases in `examples/mems/` and `examples/reports/` are a good starting point.

## Repository Structure

```
agentic-method/
├── core/                        # 30 universal protocol prompts
│   ├── master-prompt.md         # Top-level protocol
│   ├── meta-data-generation-prompt.md
│   ├── prompt-evolution-prompt.md
│   ├── experimental-design-prompt.md
│   ├── logical-inference-prompt.md
│   ├── subagent-protocol.md
│   ├── prompt-review-prompt.md
│   ├── reflection-prompt.md
│   ├── code-review-prompt.md
│   ├── cpp-code-review-prompt.md
│   ├── debug-prompt.md
│   ├── performance-optimization-prompt.md
│   ├── algorithm-correctness-prompt.md
│   ├── semantic-regression-test-prompt.md
│   ├── semantic-change-regression-prompt.md
│   ├── world-model-learning-prompt.md
│   └── ... and 30 core prompts total
├── main.md                      # Auto-generated prompt directory index
├── examples/                    # 12 examples (adapters + MEMs + reports)
│   ├── software-engineering-review-example.md
│   ├── research-survey-example.md
│   ├── large-model-inference-gap-example.md
│   ├── mems/                    # 6 desensitized transferable knowledge examples
│   │   ├── counterfactual-single-variable-principle.md
│   │   ├── semantic-change-full-regression.md
│   │   ├── prompt-evolution-failures.md
│   │   ├── operator-addition-abi-checklist.md
│   │   ├── backend-dtype-constraint.md
│   │   └── inplace-memory-overlap.md
│   └── reports/                 # 3 desensitized review/evolution report examples
│       ├── prompt-evolution-daily-report-example.md
│       ├── new-prompts-reflection-example.md
│       └── large-model-inference-gap-analysis.md
├── .github/                     # Issue / PR templates
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
├── ADAPTATION_GUIDE.md          # How to adapt to your project
├── CONTRIBUTING.md              # Contribution guide
├── .gitignore
└── LICENSE                      # MIT
```

For the full prompt list, see [`main.md`](./main.md).

## Quick Start

1. Read `core/master-prompt.md` to understand the DSL tags and global rules.
2. Pick a task-type prompt from `core/` (e.g., `experimental-design-prompt.md`).
3. Adapt it to your project using `ADAPTATION_GUIDE.md`.
4. Run a small pilot task. Inspect whether the output follows the DSL.
5. Use `prompt-evolution-prompt.md` to mutate and improve prompts over time.

## Automation & Continuous Evolution

`prompt-evolution-prompt.md` should not be a manually-run luxury. To truly realize the value of PEL, we strongly recommend **automating** it:

- **GitHub Actions**: Use `schedule` events to trigger PEL workflows daily or weekly, automatically evaluating mutations, generating daily reports, and submitting Draft PRs.
- **Self-hosted cron**: Set up scheduled tasks on a local server or workstation to run evolution experiments during idle GPU/CPU time.
- **No-code platforms**: Use n8n, Make, or Zapier to orchestrate flows like "read main.md → select seed prompt → call LLM to generate mutations → evaluate in parallel → write report."
- **Agent frameworks**: Implement a reusable PEL Runner with LangChain, LangGraph, or AutoGen, supporting multi-model routing, result persistence, and human approval nodes.

The goal of automation is not to replace human judgment, but to delegate the filtering of "which prompt variants are worth reviewing" to machines, so humans can focus on the final decision of "whether to integrate into core."

## Tested Environments

This protocol has been tested in integrated development environments such as **TRAE CN** with good results.

## Contributing

The project is in its early stages; prompt types and generalization capabilities still have much room to grow. We will continue to provide more **domain-specific examples** and **community prompts**, and warmly welcome your contributions:

- Successfully apply `Agentic Method` to a new domain (e.g., hardware design, biomedicine, legal research, game development);
- Submit adapter prompts for specific tasks or domains;
- Share high-quality prompt variants evolved through PEL;
- Provide real-world success or failure case studies;
- Have any suggestions, criticisms, or improvement ideas.

Please open an Issue describing your use case, or submit a Pull Request with a new `examples/<domain>-adapter.md` or `core/<task>-prompt.md`. With the community's help, we can build an increasingly rich collection of prompts and best practices.

## License

[MIT License](./LICENSE)

---

<div align="center">

**This is the power of open source. Enjoy!**

</div>
