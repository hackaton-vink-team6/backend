import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


def get_gpt_response(input_data):
    yandex_api_key = os.getenv('YANDEX_API_KEY')
    folder_id = os.getenv('FOLDER_ID')

    with open('bot/yandex_gpt/body.json', 'r', encoding='utf-8') as f:
        data = json.dumps(json.load(f))
    response = requests.post(
        url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
        headers = {
            'Authorization': f'Api-Key {yandex_api_key}',
        },
        data = data + f'"role": "user", "text": {input_data}',
        )

    if response.status_code != 200:
        raise RuntimeError(
            'Invalid response received: code: {}, message: {}'.format(
                {response.status_code}, {response.text}
            )
        )

    return response.json()['result']['alternatives'][0]['message']['text']
