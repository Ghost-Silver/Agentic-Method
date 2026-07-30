# Task: Experimental Design — 01

**Task ID**: `experimental-design-01`  
**Type**: Scientific method  
**Difficulty**: Medium  
**Source**: Synthetic

---

## Problem Description

A team observes that their model training throughput dropped by ~30% after a recent refactor that introduced explicit synchronization points between the GPU backend and the CPU thread pool. The team suspects the synchronization is the cause, but they are not sure which synchronization point is responsible, or whether the slowdown is actually due to the synchronization at all.

## Question

Design an experiment to determine whether the synchronization points are responsible for the throughput drop, and if so, identify which ones matter most.

## Ground-Truth Rubric

| Criterion | Points | Expected Answer |
|-----------|--------|-----------------|
| States falsifiable hypothesis | 2 | e.g., "Removing synchronization point X restores throughput to within 5% of baseline." |
| Includes control/baseline | 1 | Compare against pre-refactor version or a synthetic baseline with no synchronization. |
| Uses single-variable changes | 2 | Remove one synchronization point at a time, not all at once. |
| Defines measurable metric | 1 | Throughput in samples/sec, wall-clock time per epoch, etc. |
| Includes falsification condition | 1 | "If removing X does not change throughput by >5%, X is not the bottleneck." |

**Max score: 7**
