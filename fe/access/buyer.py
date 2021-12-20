import requests
import simplejson
from urllib.parse import urljoin
from fe.access.auth import Auth


class Buyer:
    def __init__(self, url_prefix, user_id, password):
        self.url_prefix = urljoin(url_prefix, "buyer/")
        self.user_id = user_id
        self.password = password
        self.token = ""
        self.terminal = "my terminal"
        self.auth = Auth(url_prefix)
        code, self.token = self.auth.login(self.user_id, self.password, self.terminal)
        assert code == 200

    def new_order(self, store_id: str, book_id_and_count: [(str, int)]) -> (int, str):
        books = []
        for id_count_pair in book_id_and_count:
            books.append({"id": id_count_pair[0], "count": id_count_pair[1]})
        json = {"user_id": self.user_id, "store_id": store_id, "books": books}
        #print(simplejson.dumps(json))
        url = urljoin(self.url_prefix, "new_order")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        response_json = r.json()
        return r.status_code, response_json.get("order_id")

    def payment(self,  order_id: str):
        json = {"user_id": self.user_id, "password": self.password, "order_id": order_id}
        url = urljoin(self.url_prefix, "payment")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def add_funds(self, add_value: str) -> int:
        json = {"user_id": self.user_id, "password": self.password, "add_value": add_value}
        url = urljoin(self.url_prefix, "add_funds")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def search_book(self, keywords: str, is_title: bool, is_content:bool
                    , is_author: bool, is_tag: bool) -> int:
        json = {
            "keywords": keywords,
            "params": {
                "is_title": is_title,
                "is_content": is_content,
                "is_author": is_author,
                "is_tag": is_tag
            }
        }
        url = urljoin(self.url_prefix, "search_book")
        r = requests.post(url, json = json)
        return r.status_code
    
    def cancel(self, user_id: str, order_id: int) -> int:
        json = {'user_id': user_id, 'order_id':order_id}
        url = urljoin(self.url_prefix, "cancel")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json = json)
        return r.status_code

    def delivery_confirmed(self, buyer_id: str, order_id: int) -> int:
        json = {'user_id': buyer_id, 'order_id': order_id}
        url = urljoin(self.url_prefix, "delivery_confirmed")
        r = requests.post(url, json = json)
        return r.status_code
    
    def comment(self, buyer_id, order_id, score, comment) -> int:
        json = {'buyer_id': buyer_id, 'order_id': order_id, 'score': score, 'comment': comment}
        url = urljoin(self.url_prefix, "comment")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code
    
    def search_comment(self, store_id) -> (int, list):
        json = {'store_id': store_id}
        url = urljoin(self.url_prefix, "search_comment")
        r = requests.post(url, json=json)
        return r.status_code, r.json().get("comment_list")

    def check_order_status(self, buyer_id, order_id) -> (int, int):
        json = {'buyer_id': buyer_id, 'order_id': order_id}
        url = urljoin(self.url_prefix, "check_order_status")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code, r.json().get("status")
    
    def check_order_history(self, buyer_id) -> (int, list):
        json = {'buyer_id': buyer_id}
        url = urljoin(self.url_prefix, "check_order_history")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code, r.json().get("history_order")
    
    def check_order_history_ongoing(self, buyer_id) -> (int, list):
        json = {'buyer_id': buyer_id}
        url = urljoin(self.url_prefix, "check_order_history_ongoing")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code, r.json().get("ongoing_order")