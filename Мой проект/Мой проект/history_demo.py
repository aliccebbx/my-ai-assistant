from gigachat.models import ChatMessage

max_pairs = 3

def trim(messages):
    return [messages[0]] + messages[-2 * max_pairs:]

messages = [
    ChatMessage(role="system", content="Ты — помощник по уборке."),
    ChatMessage(role="user", content="обмен 1: вопрос"),
    ChatMessage(role="assistant", content="обмен 1: ответ"),
    ChatMessage(role="user", content="обмен 2: вопрос"),
    ChatMessage(role="assistant", content="обмен 2: ответ"),
    ChatMessage(role="user", content="обмен 3: вопрос"),
    ChatMessage(role="assistant", content="обмен 3: ответ"),
    ChatMessage(role="user", content="обмен 4: вопрос"),
    ChatMessage(role="assistant", content="обмен 4: ответ"),
]

print("До сокращения:", len(messages))
messages = trim(messages)
print("После сокращения:", len(messages))

roles = [m.role for m in messages]
texts = [m.content for m in messages]
all_text = "".join(texts)

print("Первое сообщение — system:", roles[0] == "system")
print("Первая пара удалена:", "обмен 1" not in all_text)
print("Обмены 2-4 сохранены:", all(("обмен " + str(i)) in all_text for i in (2, 3, 4)))
print("Порядок ролей не нарушен:", all(roles[i] != roles[i + 1] for i in range(len(roles) - 1)))
