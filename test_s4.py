# test_s4.py —— 对照实验：同一个问题，三种人格
from chat import chat

question = "我学了一整天 Python，感觉好累"

personas = [
    "你是一个热情鼓励型的学习伙伴，语气温暖，多给安慰",
    "你是一个说话毒舌但专业的严师，专挑毛病、不留情面",
    "你是一个极度简洁的机器人，每次回答绝不超过 15 个字"
]

for persona in personas:
    messages = [
        {"role": "system", "content": persona},
        {"role": "user", "content": question}
    ]
    print("【人格】", persona)
    print("【回答】", chat(messages))
    print()
