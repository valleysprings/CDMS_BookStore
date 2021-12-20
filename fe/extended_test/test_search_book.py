import pytest
import uuid

from fe.access.new_seller import register_new_seller
from fe.access.new_buyer import register_new_buyer
from fe.test.gen_book_data import GenBook
from fe.access import book

class TestSearchBook:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        # do before test
        self.user_id = "test_search_book_level1_user_{}".format(str(uuid.uuid1()))
        self.store_id = "test_search_book_level1_store_{}".format(str(uuid.uuid1()))
        self.password = self.user_id
        self.seller = register_new_seller(self.user_id, self.password)
        
        self.buyer_id = "test_search_book_level1_user_{}".format(str(uuid.uuid1()))
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        
        code = self.seller.create_store(self.store_id)
        assert code == 200
        book_db = book.BookDB()
        self.books = book_db.get_book_info(0, 5)
        
        yield
        # do after test

    def test_ok(self):
        for book in self.books:
            title = book.title
            content = book.content
            author = book.author
            tag = book.tags[0]
            if title != '':
                code = self.buyer.search_book(title, 1, 1, 1, 1)
                assert code == 200
            if content != '':
                code = self.buyer.search_book(content, 1, 1, 1, 1)
                assert code == 200
            if author != '':
                code = self.buyer.search_book(author, 1, 1, 1, 1)
                assert code == 200
            if tag != '':
                code = self.buyer.search_book(tag, 1, 1, 1, 1)
                assert code == 200

    def test_error_empty_input(self):
        code = self.buyer.search_book('', 1, 1, 1, 1)
        assert code != 200

    def test_error_wrong_search_method(self):
        for book in self.books:
            title = book.title
            content = book.content
            author = book.author
            tag = book.tags[0]
            code = self.buyer.search_book(title, 0, 0, 0, 0)
            assert code != 200
