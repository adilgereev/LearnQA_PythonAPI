import requests
import time

url = 'https://playground.learnqa.ru/ajax/api/longtime_job'

# 1) создавал задачу
create_task = requests.get(url)

token = create_task.json()['token']
delay = create_task.json()['seconds']

print(create_task.text)

# 2) делал один запрос с token ДО того, как задача готова, убеждался в правильности поля status
response_before_ready_task = requests.get(url, params={'token': token})
print(response_before_ready_task.text)

# 3) ждал нужное количество секунд с помощью функции time.sleep() - для этого надо сделать import time
print(f'Ждем {delay} секунд')
time.sleep(delay)

# 4) делал бы один запрос c token ПОСЛЕ того, как задача готова, убеждался в правильности поля status и наличии поля result
response_after_ready_task = requests.get(url, params={'token': token})
print(response_after_ready_task.text)