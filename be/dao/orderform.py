# 数据库访问对象
# 处理对orderform, orderform_history表的CRUD操作
# 为逻辑层提供数据库访问接口
from be.dao.db_conn import connPool
from be.dao.db_conn import Dao

class Orderform(Dao):
    def __init__(self):
        self.conn = connPool.connection()
        self.cursor = self.get_cursor()

    def __del__(self):
        # connPool.release(self.conn)
        self.conn.close()
        self.close_cursor()

    def drop_table(self):
        cursor = self.cursor
        cursor.execute("DROP TABLE IF EXISTS book_for_orderform;")
        cursor.execute("DROP TABLE IF EXISTS orderform;")
        cursor.execute("DROP TABLE IF EXISTS book_for_orderform_history;")
        cursor.execute("DROP TABLE IF EXISTS orderform_history;")

    def create_table(self):
        cursor = self.cursor
        cursor.execute("CREATE TABLE IF NOT EXISTS orderform ("
            "orderform_id BIGINT NOT NULL AUTO_INCREMENT,"
    		"buyer_id VARCHAR(255) NOT NULL,"
    		"store_id VARCHAR(255) NOT NULL,"
    		"purchased_price INT,"
            "transaction_start_time TIMESTAMP NOT NULL,"
            "status INT NOT NULL,"
    		"FOREIGN KEY(buyer_id) REFERENCES user(user_id),"
    		"FOREIGN KEY(store_id) REFERENCES store(store_id),"
    		"PRIMARY KEY (orderform_id)"
            ");"
        )

        cursor.execute("CREATE TABLE IF NOT EXISTS book_for_orderform ( " 
            "orderform_id BIGINT NOT NULL,"
            "book_for_orderform_id VARCHAR(255) NOT NULL,"
            "book_count INT NOT NULL,"
            "FOREIGN KEY(orderform_id) REFERENCES orderform(orderform_id),"
    		"FOREIGN KEY(book_for_orderform_id) REFERENCES book(book_id)"
            ");"
        )

        cursor.execute("CREATE TABLE IF NOT EXISTS orderform_history ( "
            "orderform_id BIGINT NOT NULL,"
    		"buyer_id VARCHAR(255) NOT NULL,"
    		"store_id VARCHAR(255) NOT NULL,"
    		"purchased_price INT NOT NULL,"
            "transaction_start_time TIMESTAMP NOT NULL,"
    		"transaction_end_time TIMESTAMP NOT NULL,"
            "status INT NOT NULL,"
    		"FOREIGN KEY(buyer_id) REFERENCES user(user_id),"
    		"FOREIGN KEY(store_id) REFERENCES store(store_id),"
    		"PRIMARY KEY (orderform_id)"
            ");"
        )

        cursor.execute("CREATE TABLE IF NOT EXISTS book_for_orderform_history ("
            "orderform_id BIGINT NOT NULL,"
            "book_for_orderform_id VARCHAR(255) NOT NULL,"
            "book_count INT NOT NULL,"
            "FOREIGN KEY(orderform_id) REFERENCES orderform_history(orderform_id),"
    		"FOREIGN KEY(book_for_orderform_id) REFERENCES book(book_id)"
            ");"
        )

    def create_index(self):
        cursor = self.cursor
        cursor.execute("CREATE INDEX index_buyer_id ON orderform(buyer_id);")
        cursor.execute("CREATE INDEX index_store_id ON orderform(store_id);")
        cursor.execute("CREATE INDEX index_book_for_orderform_id ON book_for_orderform(book_for_orderform_id);")
        cursor.execute("CREATE INDEX index_buyer_id ON orderform_history(buyer_id);")
        cursor.execute("CREATE INDEX index_store_id ON orderform_history(store_id);")
        cursor.execute("CREATE INDEX index_book_for_orderform_id ON book_for_orderform_history(book_for_orderform_id);")


    def add_book_for_orderform(self, orderform_id, books):
        for book in books:
            self.modify("INSERT INTO book_for_orderform (orderform_id, book_for_orderform_id, book_count) VALUES (%s, %s, %s)", (orderform_id, book[0], book[1]))
    
    def add_orderform(self, buyer_id, store_id, transaction_start_time, status):
        self.modify("INSERT INTO orderform (buyer_id, store_id, transaction_start_time, status) VALUES (%s, %s, %s, %s);", (buyer_id, store_id, transaction_start_time, status))
        return self.cursor.lastrowid

    def update_orderform_price(self, orderform_id, purchased_price):
        self.modify("UPDATE orderform SET purchased_price = %s WHERE orderform_id = %s", (purchased_price, orderform_id))

    def get_orderform_status(self, orderform_id):
        result = self.get_one("SELECT status FROM orderform WHERE orderform_id = %s", (orderform_id,))
        return result['status']

    def check_orderform_valid(self, buyer_id, order_id):
        result = self.get_one("SELECT * FROM orderform WHERE buyer_id = %s AND orderform_id = %s", (buyer_id, order_id))
        return result is not None

    def get_orderform_price(self, orderform_id):
        result = self.get_one("SELECT purchased_price FROM orderform WHERE orderform_id = %s", (orderform_id,))
        return result['purchased_price']

    def update_orderform_status(self, orderform_id, status):
        self.modify("UPDATE orderform SET status = %s WHERE orderform_id = %s", (status, orderform_id))
    
    
    def delete_invalid_orderform_book(self, orderform_id):
        self.modify("DELETE FROM orderform WHERE orderform_id = %s", (orderform_id,))
        return True

    def delete_invalid_orderform(self, orderform_id):
        self.modify("DELETE FROM book_for_orderform WHERE orderform_id = %s", (orderform_id,))
        return self.delete_invalid_orderform_book(orderform_id)

    def check_orderform_time(self, orderform_id):
        result = self.get_one("SELECT transaction_start_time FROM orderform WHERE orderform_id = %s", (orderform_id,))
        return result['transaction_start_time']

    def check_order_exists(self, order_id):
        result = self.get_one("SELECT * FROM orderform WHERE orderform_id = %s", (order_id,))
        return result is not None

    def check_order_for_store(self, store_id, order_id):
        result = self.get_one("SELECT * FROM orderform WHERE store_id = %s AND orderform_id = %s", (store_id, order_id))
        return result is not None
    
    def orderfrom_into_history(self, orderform_id, transaction_end_time):
        result = self.get_one("SELECT * FROM orderform WHERE orderform_id = %s", (orderform_id,))
        self.modify("INSERT INTO orderform_history (orderform_id, buyer_id, store_id, purchased_price, transaction_start_time, transaction_end_time, status) VALUES (%s, %s, %s, %s, %s, %s, %s);", (orderform_id, result['buyer_id'], result['store_id'], result['purchased_price'], result['transaction_start_time'], transaction_end_time, 4))
        result = self.get_list("SELECT * FROM book_for_orderform WHERE orderform_id = %s", (orderform_id,))
        for book in result:
            self.modify("INSERT INTO book_for_orderform_history (orderform_id, book_for_orderform_id, book_count) VALUES (%s, %s, %s);", (orderform_id, book['book_for_orderform_id'], book['book_count']))
        self.multi_modify("DELETE FROM book_for_orderform WHERE orderform_id = %s", (orderform_id,))
        self.modify("DELETE FROM orderform WHERE orderform_id = %s", (orderform_id,))
    
    def get_orderform_history_status(self, orderform_id):
        result = self.get_one("SELECT status FROM orderform_history WHERE orderform_id = %s", (orderform_id,))
        return result['status']

    def check_order_history_exists(self, order_id):
        result = self.get_one("SELECT * FROM orderform_history WHERE orderform_id = %s", (order_id,))
        return result is not None

    def update_orderform_history_status(self, orderform_id, status):
        self.modify("UPDATE orderform_history SET status = %s WHERE orderform_id = %s", (status, orderform_id))

    def get_orderform_history_store_id(self, orderform_id):
        result = self.get_one("SELECT store_id FROM orderform_history WHERE orderform_id = %s", (orderform_id,))
        return result['store_id']

    def get_orderform_store_id(self, orderform_id):
        result = self.get_one("SELECT store_id FROM orderform WHERE orderform_id = %s", (orderform_id,))
        return result['store_id']

    def get_orderform_order_id_books(self, orderform_id):
        result = self.get_list("SELECT * FROM book_for_orderform WHERE orderform_id = %s", (orderform_id,))
        return result

    def check_order_history_ongoing(self, buyer_id):
        result = self.get_list("SELECT orderform_id, status, purchased_price, transaction_start_time FROM orderform WHERE buyer_id = %s", (buyer_id,))
        return result

    def check_order_history(self, buyer_id):
        result = self.get_list("SELECT orderform_id, status, purchased_price, transaction_start_time, transaction_end_time  FROM orderform_history WHERE buyer_id = %s", (buyer_id,))
        return result
    
    def check_orderform_history_valid(self, buyer_id, order_id):
        result = self.get_one("SELECT * FROM orderform_history WHERE buyer_id = %s AND orderform_id = %s", (buyer_id, order_id))
        return result is not None