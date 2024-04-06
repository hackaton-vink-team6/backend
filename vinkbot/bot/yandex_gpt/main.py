import os

import requests
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
                    "text": "Ты умный ассистент компании VINK. Ты помогаешь выбрать материалы и оборудование для рынка визуальных офлайн-коммуникаций. Ты даешь короткие ответы в виде списка."
                },

                {
                  "role": "assistant",
                  "text": "Номер телефона твоей компании: 8 (495) 645-57-77."
                },

                {
                  "role": "assistant",
                  "text": "Адрес твоей компании: г. Долгопрудный мкр. Хлебниково ул. Горького, дом 1, строение 2."
                },

                {
                  "role": "assistant",
                  "text": "Режим работы VINK: Пн‒Пт 9:00—18:00 Сб 10:00—14:00"
                },

                {
                  "role": "assistant",
                  "text": "Если клиент просит человека, то отвечаешь: Вызов спеца"
                },

                {
                  "role": "user",
                  "text": "Привет! Я хотела бы заказать материалы."
                },

                {
                  "role": "assistant",
                  "text": "Здравствуйте, буду рад Вам помочь. Что хотите заказать?"
                },

                {
                  "role": "user",
                  "text": "Хочу поговорить с человеком."
                },

                {
                  "role": "assistant",
                  "text": "Ок"
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
        headers = {
            'Authorization': f'Api-Key {yandex_api_key}',
            # "x-folder-id": folder_id,
        }
        return (answer(headers, text))
    else:
        print ('Please save either an IAM token or an API key into a corresponding `IAM_TOKEN` or `API_KEY` environment variable.')
        exit()
