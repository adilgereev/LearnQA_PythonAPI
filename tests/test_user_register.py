import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

fields_of_reg_data = ['firstName', 'lastName', 'email', 'password']

class TestUserRegister(BaseCase):
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email=email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.text == f"Users with email '{email}' already exists", f"Expected error message, but got {response.text}"

    # Создание пользователя с некорретным email - без символа @
    def test_create_user_without_at_sign(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.text == 'Invalid email format', f"Expected error message, but got {response.text}"


    # Создание пользователя без указания одного из полей - с помощью @parametrize необходимо проверить, что отсутствие любого параметра не дает зарегистрировать пользователя
    @pytest.mark.parametrize('field', fields_of_reg_data)
    def test_create_user_without_one_of_field(self, field):
        data = self.prepare_registration_data()
        data.pop(field)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.text == f"The following required params are missed: {field}", f"Expected error message, but got {response.text}"

    # Создание пользователя с очень коротким именем в один символ
    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'A'

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.text == 'The value of \'firstName\' field is too short', f"Expected error message, but got {response.text}"

    # Создание пользователя с очень длинным именем - длиннее 250 символов
    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'A' * 251

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.text == 'The value of \'firstName\' field is too long', f"Expected error message, but got {response.text}"