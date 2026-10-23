# test_s2.py —— 对照实验：大模型到底有没有记忆？
from chat import chat

print("=== 实验1：不累积历史（每次只发当前问题）===")
chat([{"role": "user", "content": "我最喜欢的城市是贵阳"}])
r1 = chat([{"role": "user", "content": "我最喜欢的城市是哪座？"}])
print("模型答：" + r1)

print()
print("=== 实验2：累积历史（每轮对话都带上）===")
messages = []
# 第 1 轮
messages.append({"role": "user", "content": "我最喜欢的城市是贵阳"})
answer = chat(messages)
messages.append({"role": "assistant", "content": answer})  # 模型的回答也要存！
# 第 2 轮
messages.append({"role": "user", "content": "我最喜欢的城市是哪座？"})
r2 = chat(messages)
print("模型答：" + r2)
