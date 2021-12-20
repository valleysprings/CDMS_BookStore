import pytest

from fe.access.buyer import Buyer
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
import uuid


class TestCheckOrderStatus:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_payment_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_payment_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_payment_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        gen_book = GenBook(self.seller_id, self.store_id)
        self.seller = gen_book.seller
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        self.total_price = 0
        for item in self.buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num
        code = self.buyer.add_funds(self.total_price)
        yield

    def test_status_ok(self):
        code, status = self.buyer.check_order_status(self.buyer_id, self.order_id)
        assert code == 200
        assert status == 1

        code = self.buyer.payment(self.order_id)
        assert code == 200

        code, status = self.buyer.check_order_status(self.buyer_id, self.order_id)
        assert code == 200
        assert status == 2

        code = self.seller.delivery(self.seller_id, self.store_id, self.order_id)
        assert code == 200

        code, status = self.buyer.check_order_status(self.buyer_id, self.order_id)
        assert code == 200
        assert status == 3

        code = self.buyer.delivery_confirmed(self.buyer_id, self.order_id)
        assert code == 200

        code, status = self.buyer.check_order_status(self.buyer_id, self.order_id)
        assert code == 200
        assert status == 4

        code = self.buyer.comment(self.buyer_id, self.order_id, 5, 'comment')
        assert code == 200
        
        code, status = self.buyer.check_order_status(self.buyer_id, self.order_id)
        assert code == 200
        assert status == 5
    
    def test_buyer_id_error(self):
        code, status = self.buyer.check_order_status(self.buyer_id + '_x', self.order_id)
        assert code != 200

    def test_order_id_error(self):
        code, status = self.buyer.check_order_status(self.buyer_id + '_x', -1)
        assert code != 200