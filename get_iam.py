import requests
# curl -d "{\"yandexPassportOauthToken\":\"<OAuth-токен>\"}" "https://iam.api.cloud.yandex.net/iam/v1/tokens"
import json
from config import oauth_token
import datetime as dt

url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"


def get_token():
    json_to_send = {
        "yandexPassportOauthToken": oauth_token
    }
    format_str = "%Y-%m-%dT%H:%M:%S"

    resp = json.loads(requests.post(url=url, json=json_to_send).text)
    date_str = resp['expiresAt']
    index = date_str.rfind('.')
    expire_date = dt.datetime.strptime(date_str[:index], format_str)
    resp['expiresAt'] = expire_date

    return resp


if __name__ == "__main__":
    # print(get_token())
    resp = get_token()
    # token = resp['iamToken']
    print(resp)

