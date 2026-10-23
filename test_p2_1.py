# test_p2_1.py —— 从「模型多蠢」到「给它工具」
from chat import client, MODEL, chat

print("=== 第一幕：不动手的模型 ===")
for q in ["27 乘以 43 等于多少？直接说数字", "1000 的阶乘等于多少？"]:
    print("问：", q)
    print("答：", chat([{"role": "user", "content": q}]))
    print()

print("=== 第二幕：递给它一个计算器 ===")
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "执行数学计算。当需要算术、乘方、百分比等任何数值计算时使用此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式，如 '27 * 43' 或 '2 ** 10'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

resp = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "帮我算一下 27 乘以 43"}],
    tools=tools
)

msg = resp.choices[0].message
print("模型的回答内容：", msg.content)        # 很可能是 None
print("模型想调用的工具：", msg.tool_calls)   # 重点看这个！
