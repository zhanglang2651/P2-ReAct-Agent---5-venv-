# test_s7.py —— 窗口实验：裁剪生效时，模型会「忘记」
from chat import chat

messages = [{"role": "system", "content": "你是简洁的助手"}]

# 第 1 轮：告诉它名字
messages.append({"role": "user", "content": "我叫张浪"})
messages.append({"role": "assistant", "content": chat(messages)})

# 中间聊 3 轮无关的，把「张浪」挤出窗口
for q in ["1+1等于几", "地球是什么形状", "一年有多少天"]:
    messages.append({"role": "user", "content": q})
    messages.append({"role": "assistant", "content": chat(messages)})

# 考它：但只带最近 4 条进窗口——「张浪」已被裁掉
windowed = [messages[0]] + messages[-4:]
print("窗口内的消息：", [m["content"][:8] for m in windowed])
print("模型答：", chat([{"role": "user", "content": "我叫什么名字？"}] if False else windowed + [{"role": "user", "content": "我叫什么名字？"}]))
