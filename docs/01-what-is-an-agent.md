# 什么是 Agent？（用本项目理解）

## 1. 聊天机器人 vs Agent

| | 聊天机器人 | Agent |
|---|---|---|
| 输入 | 一句话 | 目标 + 材料 |
| 输出 | 一段话 | **改世界**：写文件、跑命令、出 PDF |
| 步骤 | 通常一步 | 多步，可检查、可回退 |
| 工具 | 基本没有 | 有（文件系统、构建、校验） |

本项目的 Agent 会：

1. 读你的 `brief.md`
2. 分阶段调用大模型写手册源文件
3. 调用本地脚本生成 Excel/HTML/PDF
4. 自动检查预算合计和「不该再出现的地名」

---

## 2. 最小 Agent 公式

```text
Agent ≈ 模型（大脑） + 提示词（任务说明书） + 工具（手） + 状态（做到哪一步）
```

本仓库对应关系：

| 零件 | 文件 |
|---|---|
| 大脑 | `agent/llm.py`（OpenAI 兼容 API） |
| 说明书 | `prompts/*.md` |
| 手 | `agent/tools.py` + `pipeline/*` |
| 状态 | `runner.py` 里的 Stage 0→7 |

---

## 3. 为什么要「工具」？

如果只让模型「直接输出 PDF 二进制」——不现实且不可控。

正确做法：

- 模型输出 **人类可审查的中间格式**（MD/CSV）
- 工具把中间格式 **编译** 成交付物

这和程序员「写源码 → 编译器 → 程序」是同一思想。

---

## 4. 两种常见 Agent 架构

### A. 流水线（本项目）

```text
Stage1 → Stage2 → Stage3 → ... → Build
```

优点：好懂、好测、成本可控  
缺点：不灵活（不能中途自己决定「我要先去搜网页」）

### B. 工具循环（ReAct / function calling）

```text
思考 → 选工具 → 看结果 → 再思考 → ... → 结束
```

优点：灵活  
缺点：更难控、费用更高、更容易乱跑

**学习建议**：先掌握 A，再学 B。

---

## 5. OpenAI 兼容 API 到底在传什么？

一次聊天请求本质是 JSON：

```json
{
  "model": "deepseek-chat",
  "messages": [
    {"role": "system", "content": "你是..."},
    {"role": "user", "content": "根据 brief..."}
  ]
}
```

国内兼容节点只是把这个 JSON POST 到不同的 `base_url`。

---

## 6. 安全提醒

- API Key 只放 `.env`，永远不要提交到 GitHub
- `.gitignore` 已忽略 `.env`
- 公开仓库里只保留 `.env.example`
