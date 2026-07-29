# 存储原始访问与后端 kernel 的数据类型约束

**更新日期**：2026-07-29

## Rule

1. **禁止对存储调用 `data<char>()` 进行字节级访问**：若存储实现内部使用强类型检查（`checkDType<T>()`），仅支持注册过的具体类型。`char` 通常不在支持列表中，调用 `data<char>()` 可能在运行时抛出类型不匹配异常。
2. **跨 dtype 或字节级拷贝必须按实际 dtype 取指针**：需要原始字节指针时，先通过 `data<float>()` / `data<double>()` 等获取类型化指针，再 `reinterpret_cast<char*>()`。
3. **后端 kernel 若硬编码 `data<float>()`，只能用于 float32 张量**：通用初始化/调度路径必须在进入 GPU kernel 前检查数据类型是否为 float32，否则非 float32 张量会触发类型不匹配。
4. **非 float32 初始化应回退到 host 侧 memset**：若后端分配器使用 host 可访问的共享内存模式，通用初始化可直接在 CPU 侧 `memset`。

## When

- 修改涉及张量设备迁移、清零、广播等需要原始指针或字节级拷贝的函数时。
- 新增或修改后端 kernel，且 kernel 内部硬编码 `data<float>()` 时。
- 在后端设备上支持非 float32 dtype（如 double、int32、bool）时。

## Because

- 强类型检查不识别 `char`，字节级操作不能绕开它。
- 后端 kernel 目前大多只实现了 float32 版本，调度器/调用方必须负责 dtype 前置检查，不能假设所有 dtype 都走后端。
- 直接在 host 侧 memset 共享 buffer 可以避免为非 float32 dtype 单独写后端 shader，同时保证正确性。

## Verification

- 修复后运行对应单元测试，CPU/SIMD/专用指令集/GPU 四个后端全部通过 338/0。
- 具体触发场景：GPU + 张量转换为 double 类型时，构造 double 张量会调用 `zero()`，旧实现无条件调用 `Zero_GPU_kernel`，其内部 `data<float>()` 与 double dtype 不匹配导致崩溃。

## Failure cases

- 不要假设 `data<char>()` 可以像原始指针一样使用。
- 不要假设后端 kernel 能自动处理所有 dtype；若 kernel 只支持 float32，调用方必须显式检查或降级。
- host memset 路径仅适用于 host 可访问的共享内存模式；若未来改为私有存储模式，需要重新设计同步。

## Related MEMs

- `backend-inplace-memory-overlap.md`
- `backend-flush-not-just-sync.md`
- `semantic-change-full-regression.md`
