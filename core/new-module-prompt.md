# NEW MODULE PROMPT：{PROJECT_NAME} 新模块 / 新算子开发协议

> 适用：新增算子、Node、Kernel、层、工具类、测试框架、CLI 等任何新增代码模块。

---

## 1. 阶段一：需求冻结与上下文阅读 (R)

### 1.1 (CTX) 复述模板

```markdown
(CTX) 新增模块：<名称>
(CTX) 功能目标：<一句话>
(CTX) 输入 / 输出契约：<形状、类型、设备、异常>
(CTX) 依赖模块：<列出相关现有模块>
(CTX) 约束：<性能、精度、设备支持、内存、线程安全>
(CTX) 验收标准：<测试、基准、文档>
```

### 1.2 必读清单 (R)

1. 项目 `main.md` skill 目录中与该模块相关的 skill。
2. 同类现有模块的实现（至少 2 个对照）。
3. 调度器 `{PROJECT_NAME}Scheduler.cpp` 对该类型模块的调用方式。
4. 已有单元测试的风格与覆盖率。
5. {BUILD_SCRIPT} / 构建脚本中的注册方式。

### 1.3 接口设计预检 (HITL)

在写任何实现代码前，必须先：
- 给出接口草案（头文件）。
- 列出与现有模块的关系图。
- 请求人类确认接口后再进入实现。

---

## 2. 阶段二：结构化设计 (T)

### 2.1 逻辑依赖图

```markdown
(T) 模块依赖图：
  [NewModule]
    ├── depends on [Storage/Tensor]
    ├── depends on [Scheduler]
    ├── used by [{DATASET_NAME}Test]
    └── uses [Kernel_X]

(T) 数据流：
  输入 → 预处理 → 计算 → 输出 → 后处理

(T) 状态机：
  初始化 → forward → backward → 更新 → 销毁
```

### 2.2 设计决策记录

对每个关键决策，使用 (CFC) 给出反事实对比，并标注置信度：

```markdown
| 决策 | 选择方案 | 备选方案 | 反事实 (CFC) | 理由 | 置信度 |
|---|---|---|---|---|---|
| 拷贝语义 | 浅拷贝 + clone() | 深拷贝 | 若深拷贝会在异步写入前触发，会导致旧值 | 浅拷贝 | high (F0×2, F1×1) |
| 调度方式 | 注册到 Scheduler | 独立执行 | 若独立执行会绕过优先级调度 | 统一调度 | high (F1×2) |
```

### 2.3 多分支方案对比

```markdown
(BRANCH) 方案 A：最小改动，仅新增独立 Kernel (CONF: medium, F1×1, F3×1)
(BRANCH) 方案 B：中等改动，新增 Node 并注册到 Scheduler (CONF: high, F1×2, F3×1)
(BRANCH) 方案 C：激进改动，重构 Scheduler 以支持新调度策略 (CONF: low, F4×1)
(MERGE) 推荐方案 B：证据最充分、风险可控、与现有架构一致。
```

### 2.4 实验模块 (EXP) 设计

新模块必须通过实验验证。至少设计：

```markdown
### EXP-1：功能正确性
- 方法：单元测试 + 与参考实现（PyTorch/NumPy/手写）对照
- 判断：误差 < 阈值

### EXP-2：梯度正确性
- 方法：数值梯度 vs 解析梯度
- 判断：相对误差 < 1e-5

### EXP-3：设备一致性（若涉及 {BACKEND_A}/GPU）
- 方法：CPU 结果 vs {BACKEND_A} 结果
- 判断：L2 误差 < 1e-5

### EXP-4：性能基线
- 方法：与同类现有模块或 CPU 基线对比
- 判断：不慢于基线或给出可接受原因

### EXP-5：内存与生命周期
- 方法：valgrind / AddressSanitizer / 显式释放检查
- 判断：无泄漏、无悬垂引用
```

每个实验结果必须标注 `(CONF: <level>, <证据统计>)`。

---

## 3. 阶段三：实现 (E)

### 3.1 实现顺序

1. 头文件与接口契约。
2. 单元测试（先写 fail）。
3. CPU 实现。
4. {CPU_ACCEL_A} / {CPU_ACCEL_B} 优化实现（如适用）。
5. {BACKEND_A} / GPU 实现（如适用）。
6. Scheduler 注册与调度逻辑。
7. 集成到现有测试或示例。

### 3.2 实现纪律

- **单一职责**：每个函数只做一件事。
- **错误处理**：使用 `{PROJECT_NAME}Error::throwException()`，禁止静默 fallback。
- **异步安全**：{BACKEND_A}/{BACKEND_B} 代码必须包裹 `@autoreleasepool`，并在读取前 `{BACKEND_A}_flush_wait(true)`。
- **内存安全**：RAII、`std::shared_ptr`、禁止裸 `new/delete`。
- **可复现**：所有随机输入使用固定种子。

### 3.3 代码审查自检 (ADV)

```markdown
(ADV) 该模块是否与现有模块存在重复？
(ADV) 接口是否足够通用以支持未来合理扩展？
(ADV) 是否存在更高效的算法或数据结构？
(ADV) 异常路径是否全部覆盖？
(ADV) 是否引入了新的隐藏假设？
```

---

## 4. 阶段四：验证与集成 (M)

### 4.1 测试金字塔

```markdown
- 单元测试：>= 3 个正向 + 3 个边界/异常用例
- 集成测试：与现有模块组合运行
- 端到端测试：{DATASET_NAME} 或对应完整流程
- 对照测试：与参考实现 / CPU gold standard 对比
```

### 4.2 验收检查清单

- [ ] 所有新增单元测试通过。
- [ ] 集成测试通过。
- [ ] 与参考实现 / CPU 对照误差在阈值内。
- [ ] 性能不劣化（或已记录可接受原因）。
- [ ] 无内存泄漏（ASan / 手动检查）。
- [ ] 代码符合项目风格。
- [ ] 文档 / 注释 / skill 已更新。

### 4.3 报告

写入 `{MEMORY_DIR}/reports/YYYY-MM-DD/module-<name>.md`：

```markdown
# 模块设计文档：<名称>

## 1. 目标与范围
## 2. 接口契约
## 3. 设计决策与反事实分析
## 4. 实验记录（EXP-1 ... EXP-N）
## 5. 性能数据
## 6. 已知限制与后续优化
## 7. 对抗思考 (ADV)
```

---

## 5. (HITL) 决策门

1. 接口设计完成前必须确认。
2. 新增依赖库或工具链前必须确认。
3. 修改公共基类或调度器行为前必须确认。
4. 性能不达标但决定合并前必须确认。
5. 主要设计决策置信度为 low 时必须确认。

### 5.1 HITL_REJECTED 记录

若人类否决了接口设计、模块划分、依赖引入或实现方案，必须立即记录 `(HITL_REJECTED)`：

```markdown
(HITL_REJECTED) [YYYY-MM-DD HH:MM:SS]
- 被否决方案: <Agent 原本提议>
- 人类理由: <逐条记录>
- Agent 隐藏假设: <未显式声明的假设>
- 表层优点: <为什么看起来合理>
- 深层缺陷: <为什么被否决>
- 替代方向: <人类建议>
- 假设更新: H<x>: <old> → <new>
- 应生成的 MEM: <标题>
```

- 写入当前 reasoning log。
- 若可迁移，额外生成 `{MEMORY_DIR}/memories/YYYY-MM-DD/hitl-rejected-<title>.md`。
- (M) 阶段输出：`(AUDIT) 已记录 HITL_REJECTED：<描述>`。
