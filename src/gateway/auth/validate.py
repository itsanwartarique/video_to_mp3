import os, requests


def token(token):
    if not token:
        return None, ("missing credentials", 401)

    response = requests.post(
        f"http://localhost:8000/validate",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)