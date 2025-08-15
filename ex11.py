import requests

def test_cookie():
    url = 'https://playground.learnqa.ru/api/homework_cookie'
    response = requests.get(url)

    cookie_value = response.cookies['HomeWork']

    assert cookie_value == 'hw_value', f"Cookie value is not correct. Expected 'hw_value', but got {cookie_value}"