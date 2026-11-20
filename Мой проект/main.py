import os
from dotenv import load_dotenv
from gigachat import GigaChat
from prompts import SYSTEM_PROMPT
from gigachat.models import ChatCompletionRequest, ChatMessage, ChatModelOptions

load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")

print("Помощник по уборке и домашним делам.")
print("Первым сообщением опишите задачу: что убрать, ограничения, результат.")
print("Доступные команды: «очистить» — забыть разговор, «история» — показать список сообщений, «выход» — завершить программу.")

messages = [ChatMessage(role="system", content=SYSTEM_PROMPT)]

# Задание 22: лимит изменён с трёх пар на две
max_pairs = 2

# Счётчик успешных обменов
exchange_count = 0

def write_log(role, content):
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(role + ": " + content + "\n")

def write_empty_line():
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write("\n")

with open("chat_history.txt", "a", encoding="utf-8") as f:
    f.write("Новый запуск\n")

with GigaChat(
    credentials=key,
    scope=scope,
    model="GigaChat-2",
    ca_bundle_file="certs/russian_trusted_root_ca_pem.crt",
    timeout=60,
) as client:

    while True:
        text = input("> ").strip()

        command = text.lower()

        if command == "выход":
            print("Диалог завершён.")
            print("Успешных обменов за запуск:", exchange_count)
            break

        if command == "очистить":
            system_message = messages[0]
            messages = [system_message]
            with open("chat_history.txt", "a", encoding="utf-8") as f:
                f.write("История текущего диалога очищена\n")
            print("История очищена. Начинаем новый разговор.")
            continue

        if command == "история":
            print("Сообщений в истории:", len(messages))
            for message in messages:
                print("-", message.role)
            continue

        if text == "":
            print("Введите текст сообщения.")
            continue

        messages.append(ChatMessage(role="user", content=text))
        write_log("user", text)

        request = ChatCompletionRequest(
            messages=messages,
            model="GigaChat-2",
            model_options=ChatModelOptions(
                temperature=0.2,
                max_tokens=400,
            ),
        )

        response = client.chat.create(request)
        answer = response.messages[0].content[0].text
        print("Помощник:", answer)

        messages.append(ChatMessage(role="assistant", content=answer))
        write_log("assistant", answer)
        write_empty_line()

        exchange_count = exchange_count + 1

        if len(messages) > 1 + 2 * max_pairs:
            messages = [messages[0]] + messages[-2 * max_pairs:]

        print("Сообщений в истории:", len(messages))
