# PERFORMANCE TEST PROMPT：{PROJECT_NAME} 性能测试与优化协议

> 适用：性能回归排查、性能优化、吞吐/延迟基准测试、瓶颈分析、kernel 调度优化等。

---

## 1. 阶段一：测试目标与基线建立 (R)

### 1.1 (CTX) 复述模板

```markdown
(CTX) 测试目标：<延迟 / 吞吐 / 内存 / 能耗 / 扩展性>
(CTX) 测试对象：<模型 / 算子 / 调度路径>
(CTX) 设备 / 后端：<CPU / {CPU_ACCEL_A} / {CPU_ACCEL_B} / {BACKEND_A} / GPU>
(CTX) 输入规模：<batch size / 序列长度 / 维度>
(CTX) 基线来源：<历史数据 / 竞品 / 理论上限>
```

### 1.2 环境冻结

```markdown
- 操作系统版本：
- 编译器版本：
- CMake 配置：
- 编译选项：
- 运行设备：
- 电源模式：
- 后台进程控制：
```

### 1.3 基线测试

在改动前运行基线测试，至少 3 次取中位数，记录：

```markdown
| 指标 | Run 1 | Run 2 | Run 3 | 中位数 | 标准差 |
|---|---|---|---|---|---|
| 总时间 (ms) | | | | | |
| 吞吐 (samples/s) | | | | | |
| 内存峰值 (MB) | | | | | |
```

---

## 2. 阶段二：性能假设与实验设计 (T)

### 2.1 瓶颈假设树

```markdown
(BRANCH) H1：瓶颈在 forward MatMul (CONF: low, F4×1)
  (H1.1) {BACKEND_A} kernel 提交开销高
  (H1.2) buffer 分配频繁
(BRANCH) H2：瓶颈在 backward 同步 (CONF: medium, F1×2, F3×1)
  (H2.1) MatMulNode::backward 显式 waitUntilCompleted
  (H2.2) 多个 command buffer 串行
(BRANCH) H3：瓶颈在 update 阶段 (CONF: medium, F1×1, F3×1)
  (H3.1) zero_grad 同步点过多
  (H3.2) CPU {CPU_ACCEL_B} 未启用
(MERGE) 优先验证 H2 与 H3，因为已有代码证据支持；H1 目前仅基于先验。
```

### 2.1.1 子 Agent 假设扩展（可选但推荐）

瓶颈假设特别容易受"采样占比 = 根因"误导。生成初始假设后，调用 **HYPOTHESIS_EXPANDER**：

```markdown
(SUB) [YYYY-MM-DD HH:MM:SS] HYPOTHESIS_EXPANDER | 挑战瓶颈归因
输入: 当前瓶颈假设 H1, H2, H3 及阶段拆解数据
约束: 新假设必须指向"耗时最长阶段不一定是根因"的替代解释；必须提供证伪方式

(SUB-OUTPUT) [YYYY-MM-DD HH:MM:SS]
- H4: <同步开销被误归为计算开销的假设>
- H5: <采样工具本身引入偏差的假设>

(SUB-VERDICT) [YYYY-MM-DD HH:MM:SS]
- 采纳: ...
- 拒绝: ...
- 是否增加额外验证实验: 是/否
```

### 2.2 阶段拆解实验

必须将端到端流程拆解为可独立测量阶段：

```markdown
| 阶段 | 测量方式 | 占比 | 优化优先级 |
|---|---|---|---|
| Forward | 代码插桩 | | |
| Backward | 代码插桩 | | |
| Update | 代码插桩 | | |
| Data / Other | 代码插桩 | | |
```

### 2.3 实验矩阵 (EXP)

```markdown
### EXP-1：Batch size 扫描
- 变量：batch size ∈ {32, 64, 128, 256, 512}
- 指标：吞吐、准确率（若相关）
- 目的：找到最佳 batch size

### EXP-2：设备 / 后端对比
- 变量：CPU({CPU_ACCEL_A}+{CPU_ACCEL_B}) vs {BACKEND_A}
- 指标：吞吐、延迟、内存
- 目的：量化后端差异

### EXP-3：消融实验
- 变量：移除 / 替换某个 kernel / 同步点
- 指标：吞吐变化
- 目的：定位瓶颈

### EXP-4：同步点影响
- 变量：增加 / 减少 {BACKEND_A}_flush_wait 调用
- 指标：正确性与性能
- 目的：验证同步开销
```

---

## 3. 阶段三：性能数据采集 (E)

### 3.1 采集工具

优先使用：
- `sample` / `xctrace` 进行运行时采样。
- `otool` / `nm` 检查编译产物。
- 代码插桩获取阶段耗时。
- `ps` / 系统监控获取内存。

### 3.2 数据记录规范

```markdown
| 实验 | 配置 | 总时间 | 吞吐 | Forward | Backward | Update | Other | 备注 |
|---|---|---|---|---|---|---|---|---|
| Baseline | CPU, BS=128 | | | | | | | |
| E1 | {BACKEND_A}, BS=128 | | | | | | | |
```

### 3.3 统计纪律

1. 至少 3 次重复，取中位数或均值±标准差。
2. 排除冷启动与缓存影响。
3. 记录异常值并分析原因。

---

## 4. 阶段四：分析、优化与验证 (M)

### 4.1 瓶颈判定

```markdown
- 主要瓶颈：<阶段 / 函数 / kernel>
- 证据：<采样占比 / 阶段耗时 / 对比数据>
- 根因：<为什么>
```

#### 4.1.1 子 Agent 混淆变量审查（强制）

性能归因特别容易把"相关性"当"因果性"。完成瓶颈判定后，必须调用 **CONFUSION_HUNTER**：

```markdown
(SUB) [YYYY-MM-DD HH:MM:SS] CONFUSION_HUNTER | 审查瓶颈归因
输入: 当前瓶颈结论、前提假设、阶段拆解数据、实验矩阵结果
约束: 必须提出 ≥2 个未在主 Agent 输出中出现的混淆变量；每个变量必须说明如何影响当前结论

(SUB-OUTPUT) [YYYY-MM-DD HH:MM:SS]
(SUB-CONFUSION)
- 隐藏变量 1: <例如：系统后台进程、电源模式、缓存状态>
  - 若此变量变化，结论是否仍成立？
- 隐藏变量 2: <例如：编译器版本差异、测试顺序效应>
  - 若此变量变化，结论是否仍成立？
- 最小验证实验: <验证或排除这些混淆变量的最小实验>

(SUB-VERDICT) [YYYY-MM-DD HH:MM:SS]
- 采纳: ...
- 拒绝: ...
- 是否补充实验: 是/否
```

### 4.2 优化实施

1. 一次只做一个优化。
2. 每个优化后重新跑完整测试。
3. 若优化无效或负优化，记录并回滚。

### 4.3 正确性验证

性能优化必须同时验证：
- 单元测试通过。
- 梯度 / loss 与优化前一致（误差 < 阈值）。
- 训练准确率无衰退。

### 4.4 报告

写入 `{MEMORY_DIR}/reports/YYYY-MM-DD/perf-<YYYYMMDD>-<title>.md`：

```markdown
# 性能测试报告：<标题>

## 1. 测试目标与环境
## 2. 基线数据
## 3. 阶段拆解
## 4. 实验矩阵与结果
## 5. 瓶颈分析
## 6. 优化实施与收益
## 7. 正确性验证
## 8. 对抗思考 (ADV)
## 9. 下一步优化建议
```

### 4.5 对抗思考 (ADV)

```markdown
(ADV) 是否还有未测量的瓶颈？
(ADV) 当前优化是否在更大规模输入下仍然有效？
(ADV) 是否牺牲了正确性或可维护性换取性能？
(ADV) 同类优化是否适用于其他模块？
```

#### 4.5.1 子 Agent 对抗对（强制）

完成 ADV 后，调用 **ADVERSARIAL_PAIR**：

```markdown
(SUB) [YYYY-MM-DD HH:MM:SS] ADVERSARIAL_PAIR | 性能结论对抗审查
输入: 当前性能结论、瓶颈归因、优化方案、已执行实验
约束: 攻击者必须找到至少一个能推翻"当前瓶颈/优化"结论的致命假设；拥护者必须辩护最强证据

(SUB-OUTPUT) [YYYY-MM-DD HH:MM:SS]
(ADV-PRO) 拥护者辩护:
- <最强证据 1>
- <最强证据 2>

(ADV-CON) 攻击者反驳:
- <致命缺陷 1>
- <致命缺陷 2>
- 若结论错误，最不起眼的初始假设是：...

(SUB-VERDICT) [YYYY-MM-DD HH:MM:SS]
- 采纳: ...
- 拒绝: ...
- 是否调整结论/优化方案: 是/否
```

---

## 5. 正反面示例 (Bad vs Good)

### 5.1 瓶颈归因示例

**Bad**（把现象当根因）：
```markdown
(M) 瓶颈是 backward 太慢，因为 backward 占了 53%。
```

**Good**（细分到可优化动作）：
```markdown
(M) 主要瓶颈是 MatMulNode::backward 中的 waitUntilCompleted (CONF: high, F0×3)
(M) 证据：sample 显示 53% 时间花在 {BACKEND_A}CommandBuffer::waitUntilCompleted；
        消融实验移除该 wait 后吞吐提升 2.1×（需验证正确性）。
(M) 次瓶颈是 buffer 分配，占比 18% (CONF: medium, F0×2)。
```

### 5.2 阶段拆解示例

**Bad**（只给总时间）：
```markdown
(E) {BACKEND_A} 总时间 4867 ms。
```

**Good**（拆解到阶段）：
```markdown
(E) {BACKEND_A}, BS=128, 中位数 (n=3)：
  - Forward:  1023 ms (21.0%)
  - Backward: 2587 ms (53.2%)
  - Update:    730 ms (15.0%)
  - Other:     527 ms (10.8%)
```

### 5.3 正确性验证示例

**Bad**（只看速度）：
```markdown
(M) 优化后吞吐提升 30%，完成。
```

**Good**（速度与正确性并重）：
```markdown
(M) 优化后吞吐提升 30% (CONF: high, F0×3)
(M) 正确性：test_{DATASET_NAME}_step 通过；梯度 L2 误差 < 1e-6；15 epoch 准确率 99.28% vs 基线 99.31% (CONF: high, F0×2)
```

## 6. (HITL) 决策门

1. 编译选项变更（如关闭 LTO、改变 -O 级别）必须确认。
2. 性能优化导致代码可读性显著下降时必须确认。
3. 采样或插桩涉及修改生产代码路径时必须确认。
4. 性能收益无法解释或违反物理直觉时必须确认。
5. 优化后正确性验证未通过但决定继续时必须确认。

### 6.1 HITL_REJECTED 记录

若人类否决了优化方案、采样策略、编译选项变更或性能结论，必须立即记录 `(HITL_REJECTED)`：

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
