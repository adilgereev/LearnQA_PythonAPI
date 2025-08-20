from requests import Response
import datetime
import os


class Logger:
    file_name = f'logs/log_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'

    @classmethod
    def _write_log_to_file(cls, data: str):
        with open(cls.file_name, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, method: str):
        test_name = os.environ.get('PYTEST_CURRENT_TEST')

        data_to_write = f"\n----- Начало запроса -----\n"
        data_to_write += f"Test: {test_name}\n"
        data_to_write += f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        data_to_write += f"Request method: {method}\n"
        data_to_write += f"Request URL: {url}\n"
        data_to_write += f"Request headers: {headers}\n"
        data_to_write += f"Request cookies: {cookies}\n"
        data_to_write += f"Request data: {data}\n"
        data_to_write += "----- Конец запроса -----\n"

        cls._write_log_to_file(data_to_write)

    @classmethod
    def add_response(cls, response: Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_write = "\n----- Начало ответа -----\n"
        data_to_write += f"Response code: {response.status_code}\n"
        data_to_write += f"Response text: {response.text}\n"
        data_to_write += f"Response headers: {headers_as_dict}\n"
        data_to_write += f"Response cookies: {cookies_as_dict}\n"
        data_to_write += "----- Конец ответа -----\n"

        cls._write_log_to_file(data_to_write)

