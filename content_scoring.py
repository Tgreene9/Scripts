#!/usr/bin/env python3
import requests
from random import randint


class MusicShopCheck:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.result = Result()

    @classmethod
    def generate_cart(cls):
        price_lookup_table = {
            1: "120.00",
            2: "70.00",
            3: "50.00",
            4: "25.00",
            5: "100.00",
            6: "10.00",
            7: "8.00",
            8: "15.00",
            9: "20.00",
            10: "45.00",
            11: "30.00",
            12: "12.00",
            13: "22.00",
            14: "5.00",
            15: "40.00",
        }
        item_id = randint(1, 15)
        return f'[{{"id":{item_id},"price":{price_lookup_table[item_id]},"quantity":1}}]'

    def checking_failed_orders(self):
        try:
            self.session.cookies.set(
                "cart",
                f'[{{"id": "{randint(9000,99999)}","price": {randint(1,100)}, "quantity": {randint(1,20)}}}]',
                domain=self.url,
            )
            order_result = self.session.get(f"{self.url}/purchase", allow_redirects=True, timeout=5)
            if order_result.status_code != 500:
                self.result.warn(feedback="Invalid order successfully processed")
            self.session.cookies.clear(name="cart", domain=self.url, path="/")
        except requests.exceptions.RequestException as e:
            self.result.warn(feedback="Error occurred while checking failed orders", details=str(e))

    def checking_orders(self):
        try:
            self.session.cookies.set("cart", self.generate_cart(), domain=self.url)
            order_result = self.session.get(f"{self.url}/purchase", allow_redirects=True, timeout=5)
            if order_result.status_code != 200:
                self.result.warn(feedback="Error occurred while checking out", details=f"Status code: {order_result.status_code}")
            if self.session.cookies.get("cart") != "[]":
                self.result.warn(feedback="Error clearing cart cookie on website")
        except requests.exceptions.RequestException as e:
            self.result.warn(feedback="Error occurred while checking orders", details=str(e))

    def music_shop_login(self):
        try:
            login_info = {
                "username": self.username,
                "password": self.password,
            }
            login_result = self.session.post(f"{self.url}/login.html", data=login_info, allow_redirects=True, timeout=5)
            if "session_id" not in self.session.cookies:
                self.result.fail(feedback="Unable to login", details=f"Status code: {login_result.status_code}")
        except requests.exceptions.RequestException as e:
            self.result.fail(feedback="Error occurred while logging in", details=str(e))

    def content_check(self):
        try:
            result = self.session.get(f"{self.url}/index.html", timeout=5)
            if "The Music Shop © 2023" not in result.text:
                self.result.fail(feedback="Correct content not found on the page")
        except requests.exceptions.RequestException as e:
            self.result.fail(feedback="Error occurred while checking content", details=str(e))

    def execute(self):
        try:
            self.content_check()
            self.music_shop_login()
            self.checking_failed_orders()
            self.checking_orders()
            self.result.success(feedback="Music shop checks passed")
        except requests.exceptions.RequestException as e:
            self.result.fail(feedback="Web server is inaccessible", details=str(e))


class Result:
    def __init__(self):
        self.status = "unknown"
        self.feedback = ""

    def fail(self, feedback, details=None):
        self.status = "fail"
        self.feedback = feedback
        print(f"FAIL: {feedback}")
        if details:
            print(f"Details: {details}")

    def warn(self, feedback, details=None):
        self.status = "warn"
        self.feedback = feedback
        print(f"WARN: {feedback}")
        if details:
            print(f"Details: {details}")

    def success(self, feedback):
        self.status = "success"
        self.feedback = feedback
        print(f"SUCCESS: {feedback}")


if __name__ == "__main__":
    web_server_url = "http://192.168.1.5"
    scoring_username = "scoreuser"
    scoring_password = "Score123!"

    check = MusicShopCheck(url=web_server_url, username=scoring_username, password=scoring_password)
    check.execute()
