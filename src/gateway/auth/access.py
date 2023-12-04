import requests

def login(request):
    data = {
        "username" : request.username,
        "password" : request.password
     }

    response = requests.post(
        f"http://localhost:8000/login", json=data
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)