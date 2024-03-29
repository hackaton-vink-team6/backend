import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


def gpt(auth_headers):

    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'

    with open('body.json', 'r', encoding='utf-8') as f:
        data = json.dumps(json.load(f))
    resp = requests.post(url, headers=auth_headers, data=data)

    if resp.status_code != 200:
        raise RuntimeError(
            'Invalid response received: code: {}, message: {}'.format(
                {resp.status_code}, {resp.text}
            )
        )

    return resp.text


if __name__ == "__main__":

    if os.getenv('YANDEX_API_KEY') is not None:
        yandex_api_key = os.getenv('YANDEX_API_KEY')
        folder_id = os.getenv('FOLDER_ID')
        headers = {
            'Authorization': f'Api-Key {yandex_api_key}',
            # "x-folder-id": folder_id,
        }
    else:
        print ('Please save either an IAM token or an API key into a corresponding `IAM_TOKEN` or `API_KEY` environment variable.')
        exit()

    print(gpt(headers))
