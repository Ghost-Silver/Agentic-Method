#!/usr/bin/env python3
"""
Agentic Method Benchmark Runner — Template

This is a scaffold. To run actual benchmarks, integrate your LLM client
(OpenAI, Anthropic, local vLLM, etc.) and fill in the call_model() function.
"""

import json
import os
import time
from pathlib import Path
from typing import Any

BENCHMARK_DIR = Path(__file__).resolve().parent.parent
TASKS_DIR = BENCHMARK_DIR / "tasks"
RESULTS_DIR = BENCHMARK_DIR / "results"


def load_task(task_path: Path) -> dict[str, Any]:
    """Parse a markdown task file into structured fields."""
    content = task_path.read_text(encoding="utf-8")
    # Simple parser: extract sections between markdown headers.
    sections: dict[str, list[str]] = {}
    current = "metadata"
    sections[current] = []
    for line in content.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower().replace(" ", "_")
            sections[current] = []
        else:
            sections.setdefault(current, []).append(line)

    return {
        "id": task_path.stem,
        "description": "\n".join(sections.get("problem_description", [])).strip(),
        "question": "\n".join(sections.get("question", [])).strip(),
    }


def call_model(prompt: str, model_id: str, system_prompt: str | None = None) -> dict[str, Any]:
    """
    Placeholder for LLM inference.

    Returns:
        {
            "output": str,
            "input_tokens": int,
            "output_tokens": int,
            "latency_ms": int,
        }
    """
    raise NotImplementedError("Integrate your LLM client here.")


def run_benchmark(
    task_files: list[Path],
    baselines: list[dict[str, Any]],
    models: list[str],
) -> list[dict[str, Any]]:
    """Run all task/baseline/model combinations."""
    results = []
    for task_path in task_files:
        task = load_task(task_path)
        for baseline in baselines:
            for model_id in models:
                prompt = baseline["render"](task)
                system = baseline.get("system_prompt")
                print(f"Running {task['id']} | {baseline['id']} | {model_id}")
                try:
                    response = call_model(prompt, model_id, system)
                except NotImplementedError:
                    print("  Skipped: call_model() not implemented.")
                    continue
                results.append({
                    "task_id": task["id"],
                    "baseline_id": baseline["id"],
                    "model_id": model_id,
                    "output": response["output"],
                    "token_usage": {
                        "input": response["input_tokens"],
                        "output": response["output_tokens"],
                    },
                    "latency_ms": response["latency_ms"],
                    "scores": {},  # filled by human rater or auto-rater
                    "hallucination_flags": [],
                })
                time.sleep(0.5)  # be nice to the API
    return results


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)

    task_files = sorted(TASKS_DIR.glob("*.md"))

    baselines = [
        {
            "id": "B0-zero-shot",
            "render": lambda t: f"{t['description']}\n\n{t['question']}",
        },
        {
            "id": "B1-generic-cot",
            "render": lambda t: (
                f"{t['description']}\n\n{t['question']}\n\n"
                "Think step by step and explain your reasoning."
            ),
        },
        # Add Agentic Method baselines here by loading core/ prompts.
    ]

    models = [
        # "claude-3-5-sonnet-20241022",
        # "gpt-4o-2024-08-06",
    ]

    results = run_benchmark(task_files, baselines, models)

    output_path = RESULTS_DIR / f"run-{int(time.time())}.jsonl"
    with output_path.open("w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Saved {len(results)} results to {output_path}")


if __name__ == "__main__":
    main()
