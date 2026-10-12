# 架构说明

```text
                   ┌─────────────────────────┐
                   │   brief.md（用户输入）    │
                   └───────────┬─────────────┘
                               │
                   ┌───────────▼─────────────┐
                   │  Agent runner（分阶段）   │
                   │  llm.py + prompts/*.md  │
                   └───────────┬─────────────┘
                               │ 写文件
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
   content/*.md           data/*.csv            meta.json
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               ▼
                   ┌───────────────────────┐
                   │ Pipeline（确定性构建）  │
                   │ build / pdf / verify  │
                   └───────────┬───────────┘
                               ▼
                         output/*
```

## 模块职责

### `travel_guide.agent`

- `llm.py`：加载环境变量，调用 Chat Completions
- `tools.py`：复制模板、写文件、从模型回复里抠代码块
- `runner.py`：阶段编排（核心教学文件）

### `travel_guide.pipeline`

- 不依赖 API Key
- 可单独用 `tg build` 运行——方便你手改内容后重建

### `templates/trip-scaffold`

新行程的「空项目」。Agent 开始时先复制它，避免每次从零创建目录。

## 数据流为什么是 MD + CSV？

| 格式 | 适合 |
|---|---|
| Markdown | 叙述、时间轴、原则 |
| CSV | 表格、预算、清单、点位 |
| JSON meta | 构建配置与校验词 |

Excel/PDF 是 **制品**，不是源。源可 diff、可 git、可审查。

## 扩展方向（以后）

1. 给 runner 加「网页检索工具」（查景区开放时间）
2. 把 Stage 5 CSV 再拆成每个文件一次调用，降低截断风险
3. FastAPI 包一层变成 Web（阶段 C）
4. 与 Cursor Skill 共用同一份 prompts（现已接近）
