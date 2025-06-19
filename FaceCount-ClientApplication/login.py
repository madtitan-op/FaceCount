import requests

def make_post_request(url, data, headers=None):
    try:
        if headers:
            response = requests.post(url, json=data, headers=headers)
        else:
            response = requests.post(url, json=data)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"POST request failed: {e}")
        return None

def get_token(userid, password):
    url = "http://localhost:8080/api/auth/login"
    data = {
        "userid": userid,
        "password": password
    }
    headers = {"Content-Type": "application/json"}

    response = make_post_request(url, data, headers)

    if response:
        print("POST request successful!")
        print("Response status code:", response.status_code)
        try:
            print("Response JSON:", response.json())
            return response.json().get('token')
        except requests.exceptions.JSONDecodeError:
            print("Response text:", response.text)
            return response.text
    else:
        print("POST request failed.")
        return None

