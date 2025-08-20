from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_status_code(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name})

        Assertions.assert_status_code(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit")

    # Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_edit_user_not_auth(self):
        # REGISTER
        data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # EDIT
        new_name = "Changed Name"
        response2 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name})

        Assertions.assert_status_code(response2, 400)
        Assertions.assert_json_value_by_name(
            response2,
            "error",
            "Auth token not supplied",
            "Not error message after edit")

    # Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_user_auth_as_another_user(self):
        # REGISTER 1 USER
        data_user1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=data_user1)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id1 = self.get_json_value(response1, "id")

        # REGISTER 2 USER
        data_user2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=data_user2)

        Assertions.assert_status_code(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        # LOGIN 2 USER
        login_data = {
            'email': data_user2['email'],
            'password': data_user2['password']
        }
        response3 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_status_code(response3, 200)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response4 = MyRequests.put(
            f"/user/{user_id1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name})

        Assertions.assert_status_code(response4, 200)
        Assertions.assert_json_value_by_name(
            response4,
            "success",
            '!',
            "Not success message after edit")

        # Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_user_email_without_at_sign(self):
        # REGISTER
        data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': data['email'],
            'password': data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_status_code(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = data['email'].replace('@', '')
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email})

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Invalid email format",
            "Not error message after edit")

    # Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_user_short_name(self):
        # REGISTER
        data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': data['email'],
            'password': data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_status_code(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = 'A'
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name})

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "The value for field `firstName` is too short",
            "Not error message after edit")
