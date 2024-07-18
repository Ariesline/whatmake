import requests
import json


def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token
    """
    API_Key = 'mhfKtcstIBmsnJg0mN7ehmZY'
    Secret_Key = 'rZN7UMnz8zIsWUDKxpjAxWKrdvAsVVPA'

    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_Key}&client_secret={Secret_Key}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def main():
    access_token = get_access_token()
    if access_token is None:
        print("Failed to get access token.")
        return

    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-8k-0329?access_token={access_token}"

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "你好,请问今天星期几"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    print(response.text)


if __name__ == '__main__':
    main()
