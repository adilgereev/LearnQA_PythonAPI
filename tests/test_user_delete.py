from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_delete_main_user(self):
        # LOGIN
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id = self.get_json_value(response1, 'user_id')

        # DELETE
        response2 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response2, 400)
        Assertions.assert_json_value_by_name(
            response2,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            "Not error message after delete"
        )

    def test_delete_user(self):
        # REGISTER
        data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = data['email']
        password = data['password']
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

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response4, 404)
        assert response4.content.decode("utf-8") == "User not found"

    def test_delete_user_as_another_user(self):
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

        # DELETE
        response4 = MyRequests.delete(
            f"/user/{user_id1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response4, 400)
        Assertions.assert_json_value_by_name(
            response4,
            "error",
            "This user can only delete their own account.",
            "Not error message after delete"
        )