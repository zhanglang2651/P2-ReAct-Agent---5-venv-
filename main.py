# main.py —— P1 主体：命令行聊天机器人
from chat import chat, chat_stream


# system prompt：机器人的「人格设定」，永远放在记忆的第一位
messages = [
    {"role": "system", "content": "你是一个毒舌的程序设计大赛评委，说话一针见血但专业"}

]

print("=== 聊天机器人已启动，输入 quit 退出 ===")

while True:
    user_input = input("你: ")                              # 1. 等你输入（程序停在这里）

    if user_input.strip().lower() == "quit":                # 2. 退出机制
        print("助手: 再见！")
        break

    messages.append({"role": "user", "content": user_input})    # 3. 用户的话进记忆

    print("助手:", end="")                        # 前缀先打印，不换行           
        # S7：历史窗口——system 永驻，对话只留最近 10 条
    if len(messages) > 11:                     # 1 条 system + 10 条对话 = 11
        messages = [messages[0]] + messages[-10:]

    answer = chat_stream(messages)

    messages.append({"role": "assistant", "content": answer})
