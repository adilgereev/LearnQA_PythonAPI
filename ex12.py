import requests

def test_cookie():
    url = 'https://playground.learnqa.ru/api/homework_header'
    response = requests.get(url)

    header_value = response.headers['x-secret-homework-header']

    expected_value = 'Some secret value'
    assert header_value == expected_value, f"Header value is not correct. Expected '{expected_value}', but got {header_value}"

