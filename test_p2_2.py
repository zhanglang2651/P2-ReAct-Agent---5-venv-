# test_p2_2.py —— function calling 完整闭环：点菜→炒菜→上菜→客人点评
import json
from chat import client, MODEL

# 执行层：真函数（模型不会算，这是你替它算的地方）
def calculator(expression):
    return str(eval(expression, {"__builtins__": {}}))   # 禁掉内置函数，防恶意表达式

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "执行数学计算。当需要算术、乘方、百分比等任何数值计算时使用此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式，如 '27 * 43'"}
                },
                "required": ["expression"]
            }
        }
    }
]

# 第 1 步：带 tools 提问
messages = [{"role": "user", "content": "帮我算一下 27 乘以 43"}]
resp = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
msg = resp.choices[0].message

# 第 2 步：模型点了菜（tool_calls）——把它的「决定」原样存进历史
messages.append(msg)

# 第 3 步：你的代码炒菜
for call in msg.tool_calls:
    args = json.loads(call.function.arguments)     # 文本 → 字典
    result = calculator(args["expression"])        # 真算：1161
    # 第 4 步：把菜端回去——tool 消息必须带 tool_call_id 对号入座
    messages.append({
        "role": "tool",
        "tool_call_id": call.id,
        "content": result
    })

# 第 5 步：带着真实结果再问一次模型，生成最终回答
resp2 = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
print("最终回答：", resp2.choices[0].message.content)
