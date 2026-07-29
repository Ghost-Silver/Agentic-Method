# Adaptation Guide

This guide explains how to adapt `agentic-method` to your own project.

## 1. Fork or copy this repository

Do not edit files in place if you plan to pull future updates. Create your own adapter layer:

```
your-project/
├── agentic-method/          # submodule or copied from upstream
└── agentic-method-adapters/ # your project-specific prompts
    ├── code-review-adapter.md
    ├── debug-adapter.md
    └── architecture-adapter.md
```

## 2. Replace placeholders

Search and replace these placeholders in your adapted prompts:

| Placeholder | Replace with |
|-------------|--------------|
| `{PROJECT_NAME}` | Your project name |
| `{PROJECT_ROOT}` | Absolute or relative path to your project |
| `{MEMORY_DIR}` | Where agent memories/reports/logs are stored |
| `{BACKEND_A}` / `{BACKEND_B}` | Your primary compute backends (e.g., GPU, CUDA, Metal, WebGPU) |
| `{CPU_ACCEL_A}` / `{CPU_ACCEL_B}` | Your CPU acceleration targets (e.g., AVX-512, NEON, AMX) |
| `{CPU_FALLBACK}` | Your CPU fallback path name |
| `{LANGUAGE}` | Your primary implementation language |
| `{DOMAIN}` | Your domain (e.g., compilers, robotics, bioinformatics) |
| `{DATASET_NAME}` | Your canonical dataset or benchmark name |
| `{MODEL_FAMILY_A}` / `{MODEL_FAMILY_B}` | Example model families relevant to your domain |
| `{SCHEDULER}` | Your operator/kernel scheduler name |
| `{TENSOR_HEADER}` / `{STORAGE_HEADER}` / `{AUTOGARD_HEADER}` / `{KERNELS_HEADER}` | Your actual header file paths |
| `{TEST_FILE}` / `{TEST_EXAMPLE_FILE}` | Your actual test file names |
| `{ALLOCATOR_MANAGER}` / `{DEVICE_ALLOCATOR}` | Your memory allocator types |
| `{OP_NAME}` / `{OP_NS}` / `{OP_EXAMPLE}` | Example operator names and namespaces |

> 注意：部分 prompt 中可能还包含未列出的占位符。适配时请全局搜索 `{` 和 `}`，确保所有占位符都被替换为你的项目实际值。

## 3. Define your hard constraints

Every project has non-negotiable rules. In your adapter, explicitly list them. Examples:

- "All memory allocations must use `{ALLOCATOR}`."
- "All asynchronous operations must have explicit synchronization points."
- "All public API changes require human approval."
- "All performance claims must include statistical measurements."

## 4. Register your sub-agents

Edit `subagent-protocol.md` (or your adapter copy) to define project-specific sub-agent roles. Do not invent roles on the fly — if a role is not registered, the prompt should not invoke it.

## 5. Keep examples small

Include 2–3 concrete examples of how the prompt should behave on real tasks from your project. Examples are more useful than abstract rules.

## 6. Run a pilot

Before relying on any prompt for real work:

1. Pick a small, real task.
2. Run it with the prompt.
3. Score the output on: DSL compliance, hypothesis validation, evidence quality, usefulness.
4. Iterate.

## 7. Evolve

Use `prompt-evolution-prompt.md` to mutate your adapters and compare variants. Archive failures.

## Anti-patterns

- **Do not** copy all prompts verbatim without removing project-specific references.
- **Do not** add more rules before you have run a pilot.
- **Do not** skip the human-in-the-loop gates for irreversible actions.
