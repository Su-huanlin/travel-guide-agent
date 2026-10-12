# travel-guide-agent

把「多日旅行攻略制作」做成可复用的 **本地 CLI Agent**：

1. 你提供时间、目的地、节奏、排除项（`brief.md`）
2. Agent 分阶段调用 **OpenAI 兼容 API**（国内节点 / 国外均可）写出 Markdown + CSV
3. 本地确定性脚本生成 **Excel / HTML / PDF**，并自动校验

> 源自真实项目经验：2026 北疆舒适摄影自驾指南的制作流程。

## 仓库地址

https://github.com/Su-huanlin/travel-guide-agent

学习入口：[docs/00-START-HERE.md](docs/00-START-HERE.md)

## 5 分钟上手

```powershell
cd travel-guide-agent
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -3 -m pip install -e .
copy .env.example .env
# 编辑 .env 填入 TG_API_KEY / TG_BASE_URL / TG_MODEL

tg run --brief examples\sample-brief\weekend-hangzhou.md --no-pdf
```

详细步骤：[docs/03-setup-and-run.md](docs/03-setup-and-run.md)

## 学习路径（基础友好）

按顺序读：

1. [docs/PROCESS-LOG.md](docs/PROCESS-LOG.md) — **我们做了什么、为什么**（推荐先看）
2. [docs/01-what-is-an-agent.md](docs/01-what-is-an-agent.md) — Agent 是什么
3. [docs/02-architecture.md](docs/02-architecture.md) — 本仓库架构图
4. [docs/03-setup-and-run.md](docs/03-setup-and-run.md) — 安装运行
5. [skills/travel-guide-handbook/SKILL.md](skills/travel-guide-handbook/SKILL.md) — Cursor 里可调用的同款流程

## 命令一览

| 命令 | 作用 |
|---|---|
| `tg init <name>` | 复制空行程模板（不调用模型） |
| `tg run --brief <file>` | LLM 分阶段写作 + 构建 + 校验 |
| `tg build <trip>` | 仅构建（你手改 MD/CSV 后用） |
| `tg verify <trip>` | 仅校验 |

## 设计原则

- **源文件可审查**：`content/` + `data/` 才是真相；PDF 是编译结果
- **模型与构建分离**：写作可随机发挥，打包必须可重复
- **阶段式 Agent**：避免一次生成全书导致截断/格式崩坏
- **API 可替换**：`base_url` + `api_key` + `model` 兼容国内多数节点

## 目录速览

```text
src/travel_guide/
  agent/          # LLM 阶段编排
  pipeline/       # Excel/HTML/PDF/校验
  prompts/        # 各阶段提示词
templates/        # 空行程脚手架
skills/           # Cursor Skill 副本
docs/             # 学习文档
examples/         # 示例 brief
```

## 安全

- 不要把 `.env` 提交到 Git
- API Key 只放本地

## License

MIT
