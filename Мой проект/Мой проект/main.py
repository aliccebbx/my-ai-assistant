import os
from dotenv import load_dotenv
from gigachat import GigaChat
from prompts import SYSTEM_PROMPT
from gigachat.models import ChatCompletionRequest, ChatMessage, ChatModelOptions

load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")

rooms = input("Что нужно убрать? ").strip()
limitation = input("Какие ограничения? (время, техника, средства; можно пропустить) ").strip()
goal = input("Какой хотите результат? ").strip()
area = input("Площадь помещения в кв. м? (можно пропустить) ").strip()

if area == "":
    area = "не указана"
answer_format = input("Выберите формат ответа: 1 — краткий, 2 — пошаговый ").strip()

if limitation == "":
    limitation = "не указано"

if answer_format == "1":
    answer_format_text = "Краткий ответ: без длинных списков, в 3-5 предложениях."
elif answer_format == "2":
    answer_format_text = "Пошаговый ответ: пронумерованный список действий от первого шага до последнего, с разделами «План», «Порядок действий», «Советы»."
else:
    answer_format_text = "ОШИБКА_ФОРМАТА"

if rooms == "" or goal == "" or answer_format_text == "ОШИБКА_ФОРМАТА":
    print("Ошибка: поля «Что убрать» и «Результат» обязательны, формат — 1 или 2. Запрос не отправлен.")
else:
    user_prompt = f"""Помоги с уборкой и домашними делами.
Что нужно убрать: {rooms}
Ограничения: {limitation}
Желаемый результат: {goal}
Площадь помещения: {area}
Формат ответа: {answer_format_text}"""

    print("=== Запрос к модели ===")
    print(user_prompt)

    request = ChatCompletionRequest(
        messages=[
            ChatMessage(
                role="system",
                content=SYSTEM_PROMPT,
            ),
            ChatMessage(
                role="user",
                content=user_prompt,
            )
        ],
        model="GigaChat-2",
        model_options=ChatModelOptions(
            temperature=0.2,
            max_tokens=400,
        ),
    )

    print("Отправляем запрос....")
    with GigaChat(
        credenticals=key,
        scope=scope,
        model="GigaChat-2",
        ca_bundle_file="certs/russian_trusted_root_ca_pem.crt",
        timeout=60,
    ) as client:
        response = client.chat.create(request)

    answer = response.messages[0].content[0].text
    print("Ответ:")
    print(answer)

    with open("last_prompt.txt", "w", encoding="utf-8") as f:
        f.write(user_prompt)
    with open("last_answer.txt", "w", encoding="utf-8") as f:
        f.write(answer)
