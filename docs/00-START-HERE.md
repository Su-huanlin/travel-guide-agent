# 从这里开始读

如果你基础比较弱，按这个顺序即可：

1. **[PROCESS-LOG.md](PROCESS-LOG.md)**  
   我们实际做了哪些事、为什么这么拆（最重要）

2. **[01-what-is-an-agent.md](01-what-is-an-agent.md)**  
   Agent 和普通聊天有什么区别

3. **[02-architecture.md](02-architecture.md)**  
   本仓库模块怎么串起来

4. **[03-setup-and-run.md](03-setup-and-run.md)**  
   如何安装、填 `.env`、运行 `tg`

5. 回头打开根目录 `README.md` 当速查表

动手最小闭环：

```powershell
copy .env.example .env
# 填 TG_API_KEY
py -3 -m pip install -e .
tg run --brief examples\sample-brief\weekend-hangzhou.md --no-pdf
```
