# 安装与运行

## 环境要求

- Windows / macOS / Linux
- Python 3.10+
- 本机 Edge 或 Chrome（用于 PDF；没有也可 `--no-pdf`）
- 任一 OpenAI 兼容 API Key（DeepSeek / 通义 / Moonshot / OpenAI 等）

## 安装

在仓库根目录：

```powershell
cd d:\travel\travel-guide-agent
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -3 -m pip install -e .
copy .env.example .env
```

编辑 `.env`，至少填写：

```env
TG_API_KEY=你的密钥
TG_BASE_URL=https://api.deepseek.com/v1
TG_MODEL=deepseek-chat
```

## 命令

### 只初始化空行程（不花 API）

```powershell
tg init demo-trip
```

### 一键：LLM 写作 + 构建 + 校验

```powershell
tg run --brief examples\sample-brief\weekend-hangzhou.md
```

产物默认在：

`workspace/weekend-hangzhou/output/`

只要 HTML/Excel、不要 PDF：

```powershell
tg run --brief examples\sample-brief\weekend-hangzhou.md --no-pdf
```

### 手改内容后重建

```powershell
tg build workspace\weekend-hangzhou
```

### 只校验

```powershell
tg verify workspace\weekend-hangzhou
```

## 和 Cursor Skill 一起用

1. 本地 Agent：适合「一键出稿」
2. Cursor Skill：适合「边聊边改、中途按实时位置重排」

推荐工作流：

1. `tg run` 生成初稿  
2. 在 Cursor 打开 `workspace/...`，说「按 travel-guide-handbook 修订」  
3. `tg build` 重新出 PDF  

## 费用意识

每次 `tg run` 大约 5 次较长的模型调用（meta/route/daily/execution/csv）。  
先用便宜模型（如 deepseek-chat / qwen-plus）跑通，再换更强模型精修。
