# agent.py —— P2 收官：带工具的 ReAct Agent（5 工具 + 错误恢复版）
import json
import os
from datetime import datetime
from chat import client, MODEL

# ===== 执行层：模型不会做的，代码替它做 =====
def calculator(expression):
    return str(eval(expression, {"__builtins__": {}}))   # 拔掉内置函数，防注入

def get_weather(city):
    return {"贵阳": "多云，18°C", "北京": "晴，25°C"}.get(city, f"未找到 {city} 的天气")

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def unit_convert(value, from_unit, to_unit):
    """单位换算：温度/长度"""
    if from_unit == "celsius" and to_unit == "fahrenheit":
        return str(value * 9 / 5 + 32)
    if from_unit == "fahrenheit" and to_unit == "celsius":
        return str((value - 32) * 5 / 9)
    if from_unit == "km" and to_unit == "m":
        return str(value * 1000)
    return "不支持的换算组合"

def search_files(keyword, path="D:/agent-learning"):
    """在目录下搜 .py/.md/.txt 中含关键词的文件"""
    hits = []
    for root, _, files in os.walk(path):
        if "venv" in root or "site-packages" in root:    # ← 新增：跳过第三方库目录
            continue                                     # ← 新增
        for f in files:
            if f.endswith((".py", ".md", ".txt")):
                fp = os.path.join(root, f)
                try:
                    if keyword in open(fp, encoding="utf-8", errors="ignore").read():
                        hits.append(fp)
                except Exception:
                    pass
    return "\n".join(hits[:5]) or "没找到"

# 工具名 → 真函数（加工具只改这里）
TOOLS = {
    "calculator": calculator,
    "get_weather": get_weather,
    "get_current_time": get_current_time,
    "unit_convert": unit_convert,
    "search_files": search_files,
}

# ===== 工具菜单：给模型看的「招聘启事」=====
TOOL_SCHEMAS = [
    {"type": "function", "function": {
        "name": "calculator",
        "description": "执行数学计算。需要算术、乘方、百分比等任何数值计算时使用。",
        "parameters": {"type": "object",
            "properties": {"expression": {"type": "string", "description": "数学表达式，如 '27 * 43'"}},
            "required": ["expression"]}}},
    {"type": "function", "function": {
        "name": "get_weather",
        "description": "查询指定城市的实时天气。当用户询问某地天气时使用。",
        "parameters": {"type": "object",
            "properties": {"city": {"type": "string", "description": "城市名，如：贵阳"}},
            "required": ["city"]}}},
    {"type": "function", "function": {
        "name": "get_current_time",
        "description": "获取当前日期和时间。当用户问现在几点、今天日期时使用。",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "unit_convert",
        "description": "单位换算。支持摄氏度↔华氏度、公里↔米。当用户需要换算单位时使用。",
        "parameters": {"type": "object",
            "properties": {
                "value": {"type": "number", "description": "数值"},
                "from_unit": {"type": "string", "description": "源单位：celsius/fahrenheit/km"},
                "to_unit": {"type": "string", "description": "目标单位：fahrenheit/celsius/m"}
            },
            "required": ["value", "from_unit", "to_unit"]}}},
    {"type": "function", "function": {
        "name": "search_files",
        "description": "在项目目录中搜索包含指定关键词的文件。当用户想找含某内容的代码或文档时使用。",
        "parameters": {"type": "object",
            "properties": {
                "keyword": {"type": "string", "description": "要搜索的关键词"},
                "path": {"type": "string", "description": "搜索目录，默认 D:/agent-learning"}
            },
            "required": ["keyword"]}}},
]

# ===== ReAct 循环：Agent 的本体 =====
def run_agent(question, max_steps=8):
    messages = [
        {"role": "system", "content": "你是会使用工具的智能助手。需要计算、查天气、查时间、换算单位、搜文件时调用对应工具，不要自己编造。"},
        {"role": "user", "content": question}
    ]

    for step in range(max_steps):
        resp = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SCHEMAS)
        msg = resp.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:                      # 停止条件：不点菜了 = 收工
            print(f"[第 {step + 1} 轮] 模型直接回答，收工")
            return msg.content

        print(f"[第 {step + 1} 轮] 模型点了 {len(msg.tool_calls)} 个菜")
        for call in msg.tool_calls:                 # 炒菜 + 上菜
            name = call.function.name
            args = json.loads(call.function.arguments)
            print(f"    → 调用 {name}({args})")
            try:
                result = TOOLS[name](**args)        # 炒菜
            except Exception as e:                  # 炒糊了也是经验
                result = f"工具执行出错：{e}"
            print(f"    ← 返回：{result}")          # 无论成败，日志要记
            messages.append({                        # 无论成败，结果要回传
                "role": "tool",
                "tool_call_id": call.id,
                "content": result
            })

    return "（达到最大轮次，强制收工）"              # 安全阀

# ===== CLI =====
print("=== Agent 已启动，quit 退出 ===")
while True:
    q = input("你: ")
    if q.strip().lower() == "quit":
        break
    print("助手:", run_agent(q))
