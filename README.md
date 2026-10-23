# P1 · CLI 聊天机器人

基于 LLM API 的命令行聊天机器人。不依赖任何 Agent 框架，从裸 API 理解大模型应用的本质。

## 功能
- 多轮对话：messages 上下文累积（记忆由客户端维护）
- system prompt 人格切换：改一行字符串换一个产品
- 流式输出：打字机效果
- JSON 结构化输出模式（附 markdown 围栏防御）
- 历史窗口管理：防止 token 无限增长撑爆上下文

## 技术栈
Python 3.14 · OpenAI SDK · DeepSeek-V3（硅基流动平台）· python-dotenv

## 运行
1. `python -m venv venv` 并激活
2. `pip install openai python-dotenv`
3. 复制 `.env.example` 为 `.env`，填入你的 API key
4. `python main.py`（输入 `quit` 退出）

## 项目结构
chat.py        —— API 调用封装（单轮 + 流式）
main.py        —— 聊天机器人主循环
test_s2~s7.py  —— 各知识点的验证实验

## 已知不足（下一步方向）
- 历史窗口用「丢弃」策略，未做「摘要压缩」
- 对话无持久化，重启即丢失
- P2 计划：工具调用，让模型从「动嘴」到「动手」
## P2 · Agent 能力（2026-10-24）

- Function Calling：模型「点菜」、代码「炒菜」的决策-执行分离
- 5 个工具：计算器 / 天气（mock）/ 当前时间 / 单位换算 / 文件搜索（自动跳过 venv）
- ReAct 循环：模型自主决定是否调用、调用几轮，带停止条件与 max_steps 安全阀
- 错误恢复：工具异常转为 observation 回传，模型自我修正
- 执行层安全：eval 禁内置函数，不信任模型参数

## 踩坑记录

- 修复工具回传缩进 bug：`try` 误缩进在 `for` 循环外，导致 `print`/`messages.append` 掉进 except 分支——工具成功时结果不回传，模型重复点菜。教训：Python 缩进即逻辑；回传是协议动作，成败都必须执行。
