# 参考doc/service/buyer文档，处理具体业务逻辑
# 实现基于be/dao/dao提供的接口
from be.dao.user import User
from be.dao.store import Store
from be.dao.book import Book
from be.dao.orderform import Orderform
from be.service import auth
from be.service import token_tool
import time


def new_order(buyer_id: str, store_id: str, books: list, token: str) -> tuple:
    # 先验证Buyer是否存在（因为需要返回特殊状态码509）, 再验证token有效性
    if User().get_user_by_id(buyer_id) is None:
        return 509, 'User is not exist.', None
    if not token_tool.check_token_validation(token, buyer_id):
        return 401, 'Token is invalid', None
    # 验证商铺ID是否存在
    if Store().check_store_exists(store_id) == False:
        return 503, 'Store ID doesn\'t exist.', None

    for book in books:
        book_id = book[0]
        book_count = book[1]
        # 验证图书是否存在于商铺
        if Store().check_book_store_exists(store_id, book_id) == False:
            return 510, 'Book is not in the store.', None
        # 验证商品库存是否不足
        if Store().get_stock_level(store_id, book_id) < book_count:
            return 511, 'Book stock is not enough.', None

    # add order 修改orderform表，增加订单，计算总价格，status属性设置为1（待付款）
    # 获取当前时间
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    order_id = Orderform().add_orderform(buyer_id, store_id, now, 1)

    # 修改book_for_orderform表，将订单中的图书添加到book_for_orderform表中，
    Orderform().add_book_for_orderform(order_id, books)

    # 修改book_for_store表，修改book_count属性，减少对应书在商铺中的库存
    for book in books:
        book_id = book[0]
        book_count = book[1]
        Store().add_stock_level(store_id, book_id, -book_count)

    # 查找总价，更新总价
    purchased_price = 0
    for book in books:
        book_id = book[0]
        book_count = book[1]
        purchased_price += Book().get_book_price(book_id) * book_count
    Orderform().update_orderform_price(order_id, purchased_price)

    return 200, 'OK', order_id


def payment(buyer_id: str, order_id: int, password: str) -> tuple:
    if not auth.check_user_valid(buyer_id, password):
        return 401, 'User ID or Password is incorrect.'
    if Orderform().check_orderform_valid(buyer_id, order_id) == False:
        return 513, 'Order ID is invalid.'
    if Orderform().get_orderform_status(order_id) != 1:
        return 514, 'Order is already paid.'

    transaction_start_time = Orderform().check_orderform_time(order_id)

    if int(time.time()) - transaction_start_time.timestamp() > 900:
        # 修改book_for_store表，修改book_count属性，减少对应书在商铺中的库存
        store_id = Orderform().get_orderform_store_id(order_id)
        books = Orderform().get_orderform_order_id_books(order_id)
        for book in books:
            book_id = book["book_for_orderform_id"]
            book_count = book["book_count"]
            Store().add_stock_level(store_id, book_id, book_count)

        Orderform().delete_invalid_orderform(order_id)
        return 522, 'Order is due.'

    user_cash = User().get_user_cash(buyer_id)
    order_price = Orderform().get_orderform_price(order_id)
    if user_cash < order_price:
        return 512, 'User cash is not enough.'

    Orderform().update_orderform_status(order_id, 2)
    User().add_user_cash(buyer_id, -order_price)
    return 200, 'OK'


def add_funds(user_id: str, password: str, add_value: int) -> tuple:
    if not auth.check_user_valid(user_id, password):
        return 401, 'User ID or Password is incorrect.'
    User().add_user_cash(user_id, add_value)
    return 200, 'OK'


def manual_cancel(token: str, buyer_id: str, order_id: int) -> tuple:
    if User().get_user_by_id(buyer_id) is None:
        return 509, 'User is not exist.'
    if not token_tool.check_token_validation(token, buyer_id):
        return 401, 'Token is invalid'
    if Orderform().check_orderform_valid(buyer_id, order_id) == False:
        return 513, 'Order ID is invalid or relationship between buyer and order doesn\'t exist.'
    if Orderform().get_orderform_status(order_id) != 1:
        return 514, 'Order is already paid.'

    # 修改book_for_store表，修改book_count属性，减少对应书在商铺中的库存
    store_id = Orderform().get_orderform_store_id(order_id)
    books = Orderform().get_orderform_order_id_books(order_id)
    for book in books:
        book_id = book["book_for_orderform_id"]
        book_count = book["book_count"]
        Store().add_stock_level(store_id, book_id, book_count)

    Orderform().delete_invalid_orderform(order_id)
    return 200, 'OK'


def delivery_confirmed(buyer_id: str, order_id: int) -> tuple:
    if Orderform().check_orderform_valid(buyer_id, order_id) == False:
        return 513, 'Order ID is invalid or relationship between buyer and order doesn\'t exist.'
    if Orderform().get_orderform_status(order_id) != 3:
        return 524, 'Order is not delivered.'
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    Orderform().orderfrom_into_history(order_id, now)
    return 200, 'OK'


def search_book(keywords: str, is_title: bool, is_content: bool, is_author: bool, is_tag: bool) -> tuple:
    if keywords == "":
        return 520, 'keywords must contain at least one character.', None
    if is_title + is_content + is_author + is_tag == 0:
        return 521, "Params should not be all zeros, you should at least assign one variable to true.", None
    result = Book().search_book_by_keywords(keywords, is_title, is_content, is_author, is_tag)
    return 200, 'OK', result

def comment(token:str, buyer_id: str, order_id: str, score: int, comment: str) -> (int, str):
    if User().get_user_by_id(buyer_id) is None:
        return 509, 'User is not exist.'
    if not token_tool.check_token_validation(token, buyer_id):
        return 401, 'Token is invalid'
    if Orderform().check_order_history_exists(order_id) == False:
        return 513, 'Order ID doesn\'t exist.'
    if Orderform().get_orderform_history_status(order_id) != 4:
        return 524, 'Order status error.'

    if score < 0 or score > 10:
        return 525, 'Score range error.'
    
    store_id = Orderform().get_orderform_history_store_id(order_id)
    Orderform().update_orderform_history_status(order_id, 5)
    Store().add_comment_for_store(store_id, buyer_id, order_id, score, comment)
    return 200, 'OK'

def search_comment(store_id: str) -> (int, str, list):
    if Store().check_store_exists(store_id) == False:
        return 503, 'Store ID doesn\'t exist.', None

    comment_list = Store().get_comment(store_id)
    return 200, 'OK', comment_list


def check_order_status(token: str, buyer_id: str, order_id: int) -> tuple:
    if User().get_user_by_id(buyer_id) is None:
        return 509, 'User is not exist.', None
    if not token_tool.check_token_validation(token, buyer_id):
        return 401, 'Token is invalid', None
    if Orderform().check_orderform_valid(buyer_id, order_id) == True:
        status = Orderform().get_orderform_status(order_id)
    elif Orderform().check_orderform_history_valid(buyer_id, order_id) == True:
        status = Orderform().get_orderform_history_status(order_id)
    else:
        return 513, 'Order ID is invalid or relationship between buyer and order doesn\'t exist.', None

    return 200, 'OK', status


def check_order_history_ongoing(token: str, buyer_id: str) -> tuple:
    if User().get_user_by_id(buyer_id) is None:
        return 509, 'User is not exist.', None
    if not token_tool.check_token_validation(token, buyer_id):
        return 401, 'Token is invalid', None

    ongoing_order = Orderform().check_order_history_ongoing(buyer_id)
    return 200, 'OK', ongoing_order


def check_order_history(token: str, buyer_id: str) -> tuple:
    if User().get_user_by_id(buyer_id) is None:
        return 509, 'User is not exist.', None
    if not token_tool.check_token_validation(token, buyer_id):
        return 401, 'Token is invalid', None

    history_order = Orderform().check_order_history(buyer_id)
    return 200, 'OK', history_order