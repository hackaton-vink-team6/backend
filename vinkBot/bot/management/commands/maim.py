import requests
import os
from dotenv import load_dotenv

load_dotenv()



def answer(headers, text):
    prompt = {
            "modelUri": "gpt://b1gmpi9290kot8n714bk/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "2000"
            },
            "messages": [
  {
      "role": "system",
      "text": "Ты умный ассистент. Ты даешь ответы на вопросы, но они небольшие. Ты отвечаешь просто."
    },
    {
      "role": "user",
      "text": "Привет! Я хотел бы заказать материалы для наружной рекламы."
    },
    {
      "role": "assistant",
      "text": "Здравствуйте, буду рад Вам помочь. Как можно к Вас обращаться?"
    },
    {
      "role": "user",
      "text": "Елена"
    },
    {
      "role": "assistant",
      "text": "Елена, Вы ищете что-то конкретное или нужно помочь определиться с выбором?"
    },
    {
      "role": "user",
      "text": "Нужно помочь подобрать пленку."
    },
    {
      "role": "assistant",
      "text": "Елена, какая пленка Вам нужна? Может, Вы ищете определенного производителя?"
    },
                {
                    "role": "user",
                    "text": f'{text}'
                },
            ]
        }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    resp = requests.post(url, headers=headers, json=prompt)

    if resp.status_code != 200:
        raise RuntimeError(
                'Invalid response received: code: {}, message: {}'.format(
                    {resp.status_code}, {resp.text}
                )
            )

    return resp.json()['result']['alternatives'][0]['message']['text']


def start(text):
    if os.getenv('YANDEX_API_KEY') is not None:
        yandex_api_key = os.getenv('YANDEX_API_KEY')
        folder_id = os.getenv('FOLDER_ID')
        headers = {
            'Authorization': f'Api-Key {yandex_api_key}',
            # "x-folder-id": folder_id,
        }
        return (answer(headers, text))
    else:
        print ('Please save either an IAM token or an API key into a corresponding `IAM_TOKEN` or `API_KEY` environment variable.')
        exit()

