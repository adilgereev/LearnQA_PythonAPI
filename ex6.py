import requests

url = 'https://playground.learnqa.ru/api/long_redirect'

response = requests.get(url)

print(len(response.history))
print(response.url)