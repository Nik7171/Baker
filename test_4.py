import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {'API_KEY'}",
    #"HTTP-Referer": f"{YOUR_SITE_URL}", # Optional, for including your app on openrouter.ai rankings.
    #"X-Title": f"{YOUR_APP_NAME}", # Optional. Shows in rankings on openrouter.ai.
  },
  data=json.dumps({
    "model": "nousresearch/nous-capybara-7b:free", # Optional
    "messages": [
      {"role": "user", "content": "Что такое ООП?"}
    ]
  })
)

if response.status_code == 200:
    # Получение текста из ответа
    response_json = response.json()
    print(response_json)  # Вывод содержимого ответа для анализа
else:
    print("Ошибка при запросе:", response.status_code) 