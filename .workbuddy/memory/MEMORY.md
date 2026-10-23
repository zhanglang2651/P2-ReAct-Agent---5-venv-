# 项目长期记忆（p1-chatbot）

## 仓库与推送
- GitHub 远端（当前 origin）：`zhanglang2651/P2-ReAct-Agent---5-venv-`（public）；`gitee` remote 保留（gitee.com/zhanglang/p1-chatbot）
- 旧库 `zhanglang2651/P1-CLI-v1.0`（public）保留未动，内容与本地一致（2026-10-24 时 main=ebfa4dd）
- 换仓库推送的标准动作：`git remote set-url origin <新URL>` + `git update-ref -d refs/remotes/origin/main` + `auto_upload.py sync --api --force-repo --path D:\agent-learning\p1-chatbot`（注意 `--repo` 参数在 origin 已存在时无效）
- 本机只有 api.github.com 可达（git 直连 github.com schannel 失败、gitclone.com 502），推送一律走 API 模式
- Token 存于 `~/.workbuddy/github-auto-upload/config.json`（scope: repo+workflow，**无 delete_repo**，删库需用户网页操作）

## 安全
- `.env` = SILICONFLOW_API_KEY，已被 .gitignore 忽略；2026-10-24 曾随公开 zip 泄露约 8 小时，轮换事宜见当日日志
- 铁律：推送前确认 `.env`/`venv`/`__pycache__` 不在 `git ls-tree` 跟踪列表里

## 环境
- git 2.55.0 @ D:\DevTools\Git；python 3.13.12（managed，`~\.workbuddy\binaries\python\...`）
- Bash shim 缺 dirname/head/wc 等基础命令；PowerShell stdout 会被宿主吞，结果需落盘再读
