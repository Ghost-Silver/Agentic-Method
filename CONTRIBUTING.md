# Contributing to Agentic Method

感谢你对 `Agentic Method` 的兴趣。本指南帮助你高效地参与贡献。

## 贡献类型

我们欢迎以下形式的贡献：

1. **Bug 报告**：某个 prompt 导致 DSL 违规、逻辑漏洞或不良输出。
2. **功能提议**：新增核心 prompt、子 Agent 角色或方法论改进。
3. **领域适配**：将方法论应用到新领域，并提交 `examples/<domain>-adapter.md`。
4. **文档改进**：修复错误、提升可读性、补充示例。
5. **PEL 结果分享**：分享你通过自动进化得到的高质量 prompt 变体。

## 贡献流程

### 1. 先开 Issue 讨论（推荐）

对于以下情况，请先开 Issue：

- 新增核心 prompt
- 修改现有核心 prompt 的 DSL 或全局规则
- 引入新的子 Agent 角色
- 重大结构调整

这能避免你投入大量时间后才发现与项目方向不一致。

### 2. Fork 并创建分支

```bash
git clone https://github.com/yourname/agentic-method.git
cd agentic-method
git checkout -b feat/your-feature-name
```

### 3. 遵循以下原则

- **脱敏**：任何贡献中不得包含项目特定的路径、人名、commit hash、私有代码细节。
- **占位符**：使用 `{PROJECT_NAME}`、`{BACKEND_A}`、`{MEMORY_DIR}` 等占位符，而不是真实值。
- **DSL 一致性**：新增 prompt 必须兼容 `master-prompt.md` 中定义的核心标签体系。
- **子 Agent 注册**：不要在 prompt 中调用未在 `subagent-protocol.md` 中注册的角色。
- **验证优先**：修改现有 prompt 前，请先运行一个试点任务，并记录输出对比。

### 4. 更新索引

- 新增 prompt 后，请在 `main.md` 中添加对应条目。
- 新增示例后，请在 `README.md` 和 `README.en.md` 的仓库结构节中补充。

### 5. 提交 PR

请使用 PR 模板，填写变更类型、摘要、理由、验证方式和证据。

## 核心 prompt 的准入标准

想要进入 `core/` 的 prompt 需要满足：

1. **通用性**：不依赖特定项目、框架或硬件。
2. **可验证性**：包含明确的 DSL 标签、假设验证闭环或实验设计流程。
3. **差异性**：与现有 prompt 有清晰区分，不重复。
4. **已审查**：建议通过 `PROMPT_REVIEWER` 或至少一个真实任务验证。

## 示例 / adapter 的准入标准

`examples/` 中的适配案例需要满足：

1. 说明目标领域和用户。
2. 列出从核心 prompt 到领域适配的具体修改。
3. 提供至少一个运行示例或输出片段。
4. 已脱敏，无项目特定信息。

## 代码行为例

```markdown
## 变更摘要

在 `core/debug-prompt.md` 第 3.2 节新增“异步读取前同步”检查项，修复 {BACKEND_A}/CUDA 场景下未 flush 导致的调试偏差。

## 验证方式

- 在 {PROJECT_NAME} 项目中运行了一个跨设备梯度调试任务。
- 对比基线与修改后 prompt 的输出，修改后版本明确输出了 `(SYNC)` 标签。

## 证据

```text
(OBSERVATION) 修改前：Agent 未在读取 buffer 前调用同步点。
(OBSERVATION) 修改后：Agent 在读取前输出 (SYNC) 并等待 command buffer 完成。
```
```

## 行为准则

- 对事不对人，聚焦 prompt 和方法论本身。
- 分享失败案例与成功案例同等重要。
- 保持谦逊：一个 prompt 的有效性与模型、任务、领域都相关，避免绝对化断言。

## 提问

如果你不确定某个想法是否适合贡献，欢迎在 Issue 中先讨论。
