# test_s6.py —— JSON 模式：提取结构化信息
import json
import re
from chat import chat

text = "明天下午三点和张三在星巴克开会，聊项目进度"

messages = [
    {"role": "system", "content": "你是日程提取助手。只输出 JSON，不要输出任何其他文字，不要用 markdown 代码块。格式：{\"date\": \"日期\", \"time\": \"时间\", \"person\": \"人物\", \"location\": \"地点\", \"event\": \"事件\"}"},
    {"role": "user", "content": text}
]

answer = chat(messages)
print("原始输出：", answer)

# 从回答中抠出 {...} 部分（不管模型包了多少废话和围栏）
match = re.search(r"\{.*\}", answer, re.S)   # re.S 让 . 匹配换行符——JSON 是多行的
if match is None:
    raise ValueError("模型没有输出 JSON：" + answer)
data = json.loads(match.group())

print()
print("解析成功：")
print("时间：", data["time"])
print("事件：", data["event"])
