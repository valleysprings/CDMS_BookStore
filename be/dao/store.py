# 数据库访问对象
# 处理对store, book_for_store, comment_for_store表的CRUD操作
# 为逻辑层提供数据库访问接口
from be.dao.db_conn import Dao
from be.dao.db_conn import connPool

class Store(Dao):
    def __init__(self):
        self.conn = connPool.connection()
        self.cursor = self.get_cursor()

    def __del__(self):
        # connPool.release(self.conn)
        self.conn.close()
        self.close_cursor()


    def drop_table(self):
        cursor = self.cursor
        cursor.execute("DROP TABLE IF EXISTS comment_for_store;")
        cursor.execute("DROP TABLE IF EXISTS book_for_store;")
        cursor.execute("DROP TABLE IF EXISTS store;")

    def create_table(self):
        cursor = self.cursor
        cursor.execute("CREATE TABLE IF NOT EXISTS store ( " 
            "store_id VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,"
            "seller_id VARCHAR(255) NOT NULL,"
            "FOREIGN KEY(seller_id) REFERENCES user(user_id)"
            ");"
        )
        cursor.execute("CREATE TABLE IF NOT EXISTS book_for_store ( "
            "store_id VARCHAR(255) NOT NULL,"
            "book_id VARCHAR(255) NOT NULL,"
    		"book_count INT NOT NULL,"
            "FOREIGN KEY(store_id) REFERENCES store(store_id),"
    		"FOREIGN KEY(book_id) REFERENCES book(book_id)"
            ");"
        )
        cursor.execute("CREATE TABLE IF NOT EXISTS comment_for_store ( "
            "store_id VARCHAR(255) NOT NULL,"
            "user_id VARCHAR(255) NOT NULL,"
            "order_id VARCHAR(255) NOT NULL,"
    		"score INT NOT NULL,"
            "comment TEXT,"
            "FOREIGN KEY(store_id) REFERENCES store(store_id),"
            "FOREIGN KEY(user_id) REFERENCES user(user_id)"
            ");"
        )
    def create_index(self):
        cursor = self.cursor
        cursor.execute("CREATE INDEX index_title ON store(seller_id);")
        cursor.execute("CREATE INDEX index_store_book ON book_for_store(store_id,book_id);")

    def add_store(self, store_id, seller_id):
        self.modify("INSERT INTO store (store_id, seller_id) VALUES (%s, %s);", (store_id, seller_id))

    def add_book_for_store(self, store_id, book_id, stock_level):
        self.modify("INSERT INTO book_for_store (store_id, book_id, book_count) VALUES (%s, %s, %s);", (store_id, book_id, stock_level))
        
    def get_store_by_id(self, store_id):
        store = self.get_one("SELECT * FROM store WHERE store_id = %s;", (store_id,))
        return store

    def add_stock_level(self, store_id, book_id, stock_level):
        self.modify("UPDATE book_for_store SET book_count = book_count + %s WHERE store_id = %s AND book_id = %s;", (stock_level, store_id, book_id))

    def check_store_for_seller(self, seller_id, store_id):
        store = self.get_one("SELECT * FROM store WHERE store_id = %s AND seller_id = %s;", (store_id, seller_id))
        return store != None

    def check_store_exists(self, store_id):
        result = self.get_one("SELECT store_id FROM store WHERE store_id = %s;", (store_id, ))
        return result != None

    def check_book_store_exists(self, store_id, book_id):
        result = self.get_one("SELECT book_id FROM book_for_store WHERE store_id = %s AND book_id = %s;", (store_id, book_id))
        return result != None

    def get_stock_level(self, store_id, book_id):
        result = self.get_one("SELECT book_count FROM book_for_store WHERE store_id = %s AND book_id = %s;", (store_id, book_id))
        return result['book_count']
    
    def add_comment_for_store(self, store_id, user_id, order_id, score, comment):
        self.modify("INSERT INTO comment_for_store (store_id, user_id, order_id, score, comment) VALUES(%s, %s, %s, %s, %s);", (store_id, user_id, order_id, score, comment))
    
    def get_comment(self, store_id):
        result = self.get_list("SELECT user_id, order_id, score, comment FROM comment_for_store WHERE store_id = %s;", (store_id, ))
        return result