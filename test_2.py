import openai

# Установите свой API-ключ
openai.api_key = 'API_KEY'

def get_gpt3_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-edit-001",  # Используем GPT-3.5 Turbo
        prompt=prompt,
        max_tokens=150,  # Максимальное количество токенов в ответе
        temperature=0.7,  # Параметр температуры для разнообразия ответов
    )
    return response.choices[0].text.strip()

# Пример использования
user_input = input("Введите ваш вопрос или запрос: ")
prompt = f"Пользователь: {user_input}\nCrewAI LLM:"
response = get_gpt3_response(prompt)

print(f"Ответ CrewAI LLM: {response}")