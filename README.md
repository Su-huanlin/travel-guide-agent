# travel-guide-agent

用大模型把「旅行需求」自动做成可编辑、可导出的行程手册。

**输入** → 日期、目的地、节奏、预算等（一份 brief）  
**输出** → Markdown / CSV 源文件，以及 Excel、HTML、PDF

支持国内常见 **OpenAI 兼容接口**（DeepSeek、通义、Moonshot、SiliconFlow 等），也可接 OpenAI 官方。

## 安装

```bash
git clone https://github.com/Su-huanlin/travel-guide-agent.git
cd travel-guide-agent

python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -e .
cp .env.example .env   # Windows 可用: copy .env.example .env
```

编辑 `.env`：

```env
TG_API_KEY=你的密钥
TG_BASE_URL=https://api.deepseek.com/v1
TG_MODEL=deepseek-chat
```

## 使用

```bash
# 一键生成（示例 brief）
tg run --brief examples/sample-brief/weekend-hangzhou.md --no-pdf

# 只要空模板，不调用模型
tg init my-trip

# 改完 content/ 与 data/ 后重新打包
tg build workspace/my-trip

# 校验输出
tg verify workspace/my-trip
```

产物目录：`workspace/<行程名>/output/`

生成 PDF 需要本机已安装 Edge 或 Chrome；没有浏览器时加 `--no-pdf` 即可先出 HTML/Excel。

## 工作原理（简述）

1. **Agent 阶段**（调用模型）：按步骤写路线、每日安排、执行说明和各类 CSV  
2. **构建阶段**（不调用模型）：把源文件编译成 Excel / HTML / PDF，并做基础校验  

源文件在 `content/`、`data/`，便于人工修改后再 `tg build`。

## 目录

```text
src/travel_guide/   # CLI、Agent、构建管线
templates/          # 空行程模板
examples/           # 示例 brief
skills/             # 制作规范（可供 Cursor 等工具复用）
```

## 配置说明

| 变量 | 含义 |
|------|------|
| `TG_API_KEY` | API 密钥 |
| `TG_BASE_URL` | 兼容接口地址，需含 `/v1` |
| `TG_MODEL` | 模型名 |
| `TG_TEMPERATURE` | 可选，默认 `0.3` |
| `TG_MAX_TOKENS` | 可选，默认 `8192` |

也兼容环境变量名 `OPENAI_API_KEY` / `OPENAI_BASE_URL` / `OPENAI_MODEL`。

## 安全

- 勿将 `.env` 提交到 Git  
- API Key 仅保存在本地  

## License

MIT
