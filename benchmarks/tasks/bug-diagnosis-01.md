# Task: Bug Diagnosis — 01

**Task ID**: `bug-diagnosis-01`  
**Type**: Engineering reasoning  
**Difficulty**: Medium  
**Source**: Synthetic

---

## Problem Description

A user reports that after refactoring a memory allocator in a C++ tensor library, unit tests for `Tensor::clone()` start failing intermittently. The failures only happen when:

1. The tensor has `requires_grad == true`.
2. The clone is created and then both the original and clone receive gradient updates.
3. The test checks that `original.grad()` and `clone.grad()` are independent.

The test sometimes passes and sometimes fails, with the failure mode being that `clone.grad()` unexpectedly equals `original.grad()` after backward.

## Provided Code

```cpp
class Tensor {
public:
    Tensor(const Tensor& other);
    Tensor& operator=(const Tensor& other);
    Tensor clone() const;
    // ... other members ...
private:
    Storage _storage;
    AutogradMeta _autograd_meta;
    size_t _storage_offset = 0;
};

struct AutogradMeta {
    bool _requires_grad = false;
    std::shared_ptr<Tensor> _grad;
    std::shared_ptr<Node> _node;
    std::weak_ptr<Tensor> _self;
};

Tensor::Tensor(const Tensor& other)
    : _storage(other._storage),  // shallow copy
      _autograd_meta(other._autograd_meta),  // shares _grad shared_ptr
      _storage_offset(other._storage_offset) {}
```

## Question

Identify the root cause, explain why the failure is intermittent, and propose the minimal fix.

## Ground-Truth Rubric

| Criterion | Points | Expected Answer |
|-----------|--------|-----------------|
| Identifies `_autograd_meta` shallow copy | 2 | Should mention that `_grad` is a `shared_ptr` and is shared between original and clone. |
| Explains intermittent behavior | 2 | Race or order-dependence in gradient accumulation; if both tensors share the same `_grad` tensor, updates collide. |
| Proposes minimal fix | 1 | Deep-copy `_grad` in copy constructor, or ensure `clone()` creates independent AutogradMeta. |
| Avoids red herrings | 1 | Does not blame `Storage` shallow copy (which is fine because `clone()` deep-copies storage) or threading. |

**Max score: 6**
