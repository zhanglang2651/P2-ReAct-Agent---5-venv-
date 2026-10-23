# 第一课：第一次调用大模型
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # 把 .env 里的变量加载进环境

client = OpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"),      # 从环境变量读 key
    base_url="https://api.siliconflow.cn/v1"        # 硅基流动服务器地址
)

resp = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3",               # 选模型
    messages=[
        {"role": "user", "content": "用一句话解释什么是 Python"}
    ]
)

print(resp.choices[0].message.content)
