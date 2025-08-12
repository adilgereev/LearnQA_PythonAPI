import requests

methods = ['GET', 'POST', 'PUT', 'DELETE']

url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'

# 1. Делает http-запрос любого типа без параметра method.
response1 = requests.post(url)

# 2. Делает http-запрос не из списка. Например, HEAD.
response2 = requests.patch(url, data={'method': 'PATCH'})

# 3. Делает запрос с правильным значением method.
response3 = requests.post(url, data={'method': 'POST'})

print(response1.text)
print(response2.text)
print(response3.text)

for real_method in methods:
    for param_method in methods:

        payload = {"method": param_method}

        if real_method == "GET":
            response = requests.get(url, params=payload)
        else:
            response = requests.request(real_method, url, data=payload)

        if response.status_code == 200:
            if response.text == '{"success":"!"}':
                if real_method != param_method:
                    print(
                        f"НАЙДЕНО! ✅ Несовпадение, но успех! Реальный метод: {real_method}, Параметр: {param_method}, Ответ: {response.text}")
                else:
                    print(
                        f"Ок. Реальный метод: {real_method}, Параметр: {param_method}, Ответ: {response.text}")
            elif response.text == 'Wrong method provided':
                if real_method == param_method:
                    print(
                        f"НАЙДЕНО! ❌ Совпадение, но ошибка! Реальный метод: {real_method}, Параметр: {param_method}, Ответ: {response.text}")
                else:
                    print(
                        f"Ожидаемая ошибка. Реальный метод: {real_method}, Параметр: {param_method}, Ответ: {response.text}")
            else:
                print(
                    f"Неожиданный ответ. Реальный метод: {real_method}, Параметр: {param_method}, Ответ: {response.text}")
