# 过程记录：我们做了什么、为什么

> 面向基础较弱的读者。按时间顺序记录本仓库从 0 到可运行的搭建过程。

---

## 第 0 步：先想清楚要做成什么

北疆那次攻略的经验是：

- **聊天里改来改去很容易乱**
- **真正可靠的是文件**：Markdown + CSV → 再生成 PDF/Excel
- **模型擅长规划与写作**，不擅长每次可靠地「排 Excel / 打 PDF」

所以目标不是「又一个聊天机器人」，而是：

```text
用户 brief
   ↓（模型多阶段写作）
content/*.md + data/*.csv
   ↓（确定性脚本，不调用模型）
output/*.xlsx + *.html + *.pdf
```

这叫 **Agent = 模型决策 + 工具执行**。

---

## 第 1 步：先沉淀 Cursor Skill（已完成）

在你本机：

`C:\Users\10129\.cursor\skills\travel-guide-handbook\`

Skill 是给 Cursor 看的操作手册。本仓库又复制了一份到：

`skills/travel-guide-handbook/`

**为什么两边都有？**

- Cursor 个人库：你在任意项目里说「按 travel-guide-handbook 做」就能触发
- GitHub 仓库：别人 clone 后也能看到同一套流程，避免两套文档漂移

---

## 第 2 步：选择「阶段 A+B」而不是直接做网站

| 方案 | 含义 | 为何先不做 |
|---|---|---|
| 只要 Skill | 仍靠 Cursor 人工驱动 | 自动化不足 |
| A 模板仓库 | 只有脚手架 + build | 还不能一键生成内容 |
| **A+B CLI Agent** | 模板 + 本地命令调用模型 | **当前选择** |
| C Web 服务 | 上传 brief 下载 zip | 要登录、部署、计费，后面再加 |

本地 CLI 的好处：密钥留在你电脑的 `.env`，不先公开到服务器。

---

## 第 3 步：搭仓库目录（脚手架）

关键目录：

| 路径 | 作用 |
|---|---|
| `src/travel_guide/pipeline/` | 确定性构建：CSV→Excel、MD→HTML、HTML→PDF、校验 |
| `src/travel_guide/agent/` | Agent：读 brief、分阶段调模型、写文件 |
| `src/travel_guide/prompts/` | 每阶段给模型的说明书 |
| `templates/trip-scaffold/` | 新行程空白模板 |
| `skills/` | 与 Cursor skill 同步的流程说明 |
| `docs/` | 学习文档（你正在看的） |
| `examples/` | 示例 brief |
| `.env.example` | API 配置样例（不含真密钥） |

**知识点：为什么用 `src/` 布局？**

Python 包放在 `src/travel_guide`，用 `pip install -e .` 安装后，命令行才能找到 `tg` 入口，也避免「在错误目录 import 到半成品」。

---

## 第 4 步：确定性管线（Pipeline）先于 Agent

顺序很重要：**先保证「有手写好的 MD/CSV 也能出 PDF」**，再让模型去写 MD/CSV。

否则你会分不清：是模型写错了，还是打包脚本坏了。

管线模块：

1. `meta.py`：读 `meta.json`（标题、输出文件名、校验关键词）
2. `build.py`：生成 xlsx/html，必要时补地图占位 SVG
3. `pdf.py`：用本机 Edge/Chrome headless 打印 PDF
4. `verify.py`：检查文件是否存在、Excel 表是否空、预算合计、禁用词

**知识点：确定性 vs 非确定性**

- 确定性：同样输入 → 同样输出（build/verify）
- 非确定性：模型每次措辞可能不同（agent 写作）

工程上要把二者拆开，Agent 才好调试。

---

## 第 5 步：Agent 做成「状态机」而不是一次生成全书

一次让模型「写出全部手册 + 全部 CSV」容易：

- 超长输出被截断
- CSV 格式崩溃
- 前后矛盾（路线表和日报不一致）

因此拆成阶段：

```text
0 复制模板
1 生成 meta.json
2 写 01-route-design.md
3 写 02-daily-guide.md（带着路线上下文）
4 写 03-execution-guide.md
5 写 data/*.csv
6 build（无模型）
7 verify（无模型）
```

每一阶段的提示词在 `src/travel_guide/prompts/`。

**知识点：这就是最简单的 Agent 形态**

不是神秘黑科技，而是：

1. 系统提示（角色 + 硬规则）
2. 阶段提示（本步交付物格式）
3. 用户材料（brief + 上一步产物）
4. 工具（写文件、build、verify）
5. 循环到下一阶段

更复杂的 Agent 会加入「工具调用（function calling）」「记忆」「并行子代理」。本项目先用**固定阶段流水线**，最适合学习。

---

## 第 6 步：API 兼容国内与国外

使用官方 `openai` Python SDK，但配置：

- `base_url`（接口根地址）
- `api_key`
- `model`

因为国内很多厂商提供 **OpenAI 兼容模式**：路径仍是 `/v1/chat/completions`，只是换域名和模型名。

见 `.env.example`：DeepSeek / 通义 / Moonshot / SiliconFlow / OpenAI。

**知识点：兼容接口**

只要厂商实现了相近的 Chat Completions JSON 协议，同一套代码就能换「大脑」，不必为每个厂商重写客户端。

---

## 第 7 步：CLI 入口

安装后命令：

```bash
tg init my-trip
tg run --brief examples/sample-brief/weekend-hangzhou.md
tg build workspace/xxx
tg verify workspace/xxx
```

用 Typer 做命令行解析，Rich 做彩色日志。

---

## 第 8 步：GitHub 建仓与推送

1. 本机原先没有 `gh`，从 GitHub CLI release 下载便携版
2. Cursor 的 GitHub 连接已登录账号 `Su-huanlin`
3. 创建公开/私有仓库并 `git push`

（具体仓库 URL 见 README「仓库地址」一节，以推送结果为准。）

---

## 第 9 步：你之后怎么用

1. 复制 `.env.example` → `.env`，填国内兼容节点的 key
2. `pip install -e .`
3. 写一份 brief（可参考 `examples/`）
4. `tg run --brief your.md`
5. 打开 `workspace/<name>/output/`

若模型某阶段 CSV 解析失败：先看该阶段原始回复，或改为手改 CSV 后只跑 `tg build`。

---

## 常见坑

| 现象 | 原因 | 处理 |
|---|---|---|
| Missing TG_API_KEY | 没配 `.env` | 复制 example 并填写 |
| PDF 失败 | 没装 Edge/Chrome | `tg run --no-pdf` 先出 HTML/XLSX |
| budget 校验失败 | 小计不等于分项和 | 改 CSV 或让模型重跑 stage 5 |
| 禁用词出现在 HTML | 模型又写回已删除地点 | 在 meta.forbidden_terms 加强，并重跑 |
| 一次输出太长被截断 | max_tokens 不够 | 调大 `TG_MAX_TOKENS` 或缩短 brief |
