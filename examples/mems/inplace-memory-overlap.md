# In-place Unary Kernel 的内存重叠修复记录

**创建日期**：2026-07-29  
**更新日期**：2026-07-29  
**关联问题**：全局代码审查 P1-3

## Rule

调度器的 `supports_unary_memory_overlap(DeviceType dev, op op_type)` 按算子粒度返回：

- 对已实现并验证的 **11 个逐元素 unary 算子**（如 Neg、Cos、Sin、ReLU、Tanh、Sigmoid、GELU、LReLU、Log、Exp、Abs）在 GPU 与 CPU 通用后端上返回 `true`；
- 对未实现 in-place kernel、含规约/二元语义（如 Softmax、Sum、Min、Max）或尚未验证的算子返回 `false`；
- 对 `requires_grad == true` 的张量，即使算子在白名单内，也禁止执行 in-place 操作。

> 历史版本：在方案 B 落地前，GPU 上所有 unary 算子统一返回 `false`，作为保守临时方案。

## When

- 调用公开 in-place API（如 `relu_`、`leaky_relu_`、`neg_`、`abs_` 等）；
- 调度器或上层 API 判断能否复用输入 buffer 作为输出 buffer；
- 新增 GPU/CPU 通用后端 unary in-place kernel 或扩展白名单时；
- 在 GPU 设备上做前向内存优化时。

## Because

1. 原 GPU unary kernel 假设输入/输出为不同设备 buffer；当 `input_buffer == output_buffer` 时，异步 command encoder 可能出现 read-after-write hazard，导致结果未定义。
2. 方案 B 为上述 11 个算子实现了 CPU 通用后端与 GPU 后端的 in-place kernel，GPU 路径在同一 buffer 上通过合适的 command buffer 调度完成读写。
3. `supports_unary_memory_overlap` 不再一刀切返回 `false`，而是按算子白名单开放；未验证的算子继续保守返回 `false`，避免未经验证的 in-place 路径被调度。
4. `requires_grad == true` 时禁止 in-place，防止覆盖反向图所需的中间值，避免梯度错误。

## Verification

- **F1**：静态检查调度器头文件，仅 11 个算子返回 `true`。
- **F0**：in-place unary 单元测试 16/16 通过，覆盖：
  - CPU/GPU 完全重叠（`input.data() == output.data()`）；
  - 连续调用多个 in-place unary 算子；
  - 共享 storage 的视图；
  - `requires_grad == true` 时正确抛异常。
- **F0**：自动微分测试 256/256 通过，确认未破坏梯度语义（呼应 `semantic-change-full-regression.md`）。
- **F3**：partial overlap / stride / non-contiguous 路径尚未被显式单测覆盖。

## Failure cases & Limitations

- **Partial overlap / stride 未覆盖**：当前白名单仅保证完全重叠且连续的场景；部分重叠、非连续 stride 仍可能触发 hazard，需继续返回 `false` 或额外验证。
- **LReLU_ 参数固定**：`leaky_relu_` 的 negative_slope 固定为 `0.01f`，未暴露用户可配置参数。
- **算子范围有限**：仅 11 个算子开放；其他 unary 算子若未实现 in-place kernel 或未验证，必须保持 `false`。
- **requires_grad 禁止**：训练场景下对需要梯度的张量无法使用 in-place；未来若放宽必须验证反向图一致性。

## Next steps

- [x] 已记录为修复不完全
- [x] 已补充 GPU in-place 单元测试
- [x] 已按算子粒度开启 in-place 支持
- [ ] 补充 partial overlap / stride / non-contiguous 的 GPU in-place 单测。
- [ ] 评估 `leaky_relu_` 的 negative_slope 可配置化。
- [ ] 按相同流程逐步开放其余 unary 算子。

## Related MEMs

- `semantic-change-full-regression.md` — 本次已执行自动微分完整语义回归。
