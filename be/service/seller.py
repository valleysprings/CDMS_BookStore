# 参考doc/service/seller文档，处理具体业务逻辑
# 实现基于be/dao/seller提供的接口
from be.dao.orderform import Orderform
from be.dao.store import Store
from be.dao.user import User
from be.dao.book import Book
from be.service import token_tool

def create_store(token: str, seller_id: str, store_id: str) -> tuple:
    store_info = Store().get_store_by_id(store_id)
    seller_info = User().get_user_by_id(seller_id)
    if store_info != None:
        return 501, 'Store ID already exists.'
    if seller_info == None:
        return 401, 'User doesn\'t not exist.'
    if not token_tool.check_token_validation(token, seller_id):
        return 401, 'Token is invalid or User is not login.'
    
    Store().add_store(store_id, seller_id)
    return 200, 'OK'


def add_book(token: str, seller_id: str, store_id: str, book_info: dict, stock_level: int) -> tuple:
    if not token_tool.check_token_validation(token, seller_id):
        return 401, 'Token is invalid or User is not login.'

    book_id = book_info["id"]

    if Store().check_store_exists(store_id) == False:
        return 503, 'Store ID doesn\'t exist.'
    if Book().check_book_exists(book_id) == True:
        return 504, 'Book ID already exists.'
    if Store().check_store_for_seller(seller_id, store_id) == False:
        return 506, 'Relationship between seller and store doesn\'t exist.'
    
    Book().add_book(book_info, store_id)
    Store().add_book_for_store(store_id, book_id, stock_level)
    return 200, 'OK'


def add_stock_level(token: str, seller_id: str, store_id: str, book_id: str, add_stock_level: int) -> tuple:
    if not token_tool.check_token_validation(token, seller_id):
        return 401, 'Token is invalid or User is not login.'

    if Store().check_store_exists(store_id) == False:
        return 503, 'Store ID doesn\'t exist.'
    if Book().check_book_exists(book_id) == False:
        return 519, 'Book ID doesn\'t exist.'
    if Store().check_store_for_seller(seller_id, store_id) == False:
        return 506, 'Relationship between seller and store doesn\'t exist.'

    Store().add_stock_level(store_id, book_id, add_stock_level)
    return 200, 'OK'


def delivery(token: str, seller_id: str, store_id: str, order_id: str) -> tuple:
    if not token_tool.check_token_validation(token, seller_id):
        return 401, 'Token is invalid or User is not login.'

    if Store().check_store_exists(store_id) == False:
        return 502, 'Store ID doesn\'t exist.'
    if Store().check_store_for_seller(seller_id, store_id) == False:
        return 506, 'Relationship between seller and store doesn\'t exist.'
    if Orderform().check_order_exists(order_id) == False:
        return 518, 'Order ID doesn\'t exist.'
    if Orderform().check_order_for_store(store_id, order_id) == False:
        return 523, 'Order ID doesn\'t belong to this store.'
    if Orderform().get_orderform_status(order_id) != 2:
        return 524, 'Order is not paid or has been delivered.'

    Orderform().update_orderform_status(order_id, 3)
    return 200, 'OK'