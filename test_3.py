import openai

# Установка вашего ключа API
openai.api_key = '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'

# Текст, для которого нужно получить продолжение
prompt_text = "Какие суть основные принципы ООП?"

# Запрос продолжения текста у GPT-3.5 Turbo
response = openai.Completion.create(
  engine="gpt-3.5-turbo-0613",
  prompt=prompt_text,
  temperature=0.7,
  max_tokens=100
)

# Вывод полученного текста
print(response.choices[0].text.strip())
