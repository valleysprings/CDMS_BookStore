# 数据库访问对象
# 处理对book, tag_for_book, pic_for_book表的CRUD操作
# 为逻辑层提供数据库访问接口
from be.dao.db_conn import Dao
from be.dao.db_conn import connPool

class Book(Dao):        
    def __init__(self):
        self.conn = connPool.connection()
        self.cursor = self.get_cursor()

    def __del__(self):
        # connPool.release(self.conn)
        self.conn.close()
        self.close_cursor()


    def drop_table(self):
        cursor = self.get_cursor()
        cursor.execute("DROP TABLE IF EXISTS tag_for_book;")
        cursor.execute("DROP TABLE IF EXISTS pic_for_book;")
        cursor.execute("DROP TABLE IF EXISTS book;")
        
    def create_table(self):
        cursor = self.get_cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS book ("
            "book_id VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,"
            "title VARCHAR(255),"
            "author VARCHAR(255),"
            "publisher VARCHAR(255),"
            "original_title VARCHAR(255),"
            "translator VARCHAR(255),"
            "pub_year VARCHAR(255),"
            "pages INT,"
            "price INT,"
            "binding VARCHAR(255),"
            "ISBN VARCHAR(20),"
            "author_intro TEXT,"
            "book_intro TEXT,"
            "content TEXT"
            ");"
        )
        cursor.execute("CREATE TABLE IF NOT EXISTS tag_for_book ("
            "book_id VARCHAR(255) NOT NULL,"
    		"book_tag VARCHAR(255) NOT NULL,"
    		"FOREIGN KEY(book_id) REFERENCES book(book_id)"
            ");"
        )
        cursor.execute("CREATE TABLE IF NOT EXISTS pic_for_book ("
            "book_id VARCHAR(255) NOT NULL,"
    		"book_pic LONGBLOB NOT NULL,"
    		"FOREIGN KEY(book_id) REFERENCES book(book_id)"
            ");"
        )

    def create_index(self):
        cursor = self.get_cursor()
        cursor.execute("CREATE INDEX index_title ON book(title);")
        cursor.execute("CREATE INDEX index_author ON book(author);")
        cursor.execute("CREATE INDEX index_tag ON tag_for_book(book_tag);")
    
    def add_book(self, book_info, store_id):
        book_id = book_info["id"]
        title = book_info["title"]
        author = book_info["author"]
        publisher = book_info["publisher"]
        original_title = book_info["original_title"]
        translator = book_info["translator"]
        pub_year = book_info["pub_year"]
        pages = book_info["pages"]
        price = book_info["price"]
        binding = book_info["binding"]
        ISBN = book_info["isbn"]
        author_intro = book_info["author_intro"]
        book_intro = book_info["book_intro"]
        content = book_info["content"]
        self.modify("INSERT INTO book"
            "(book_id, title, author, publisher, original_title, translator, pub_year,"
            "pages, price, binding, ISBN, author_intro, book_intro, content)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", 
            (book_id, title, author, publisher, original_title, translator, pub_year,
            pages, price, binding, ISBN, author_intro, book_intro, content))

        tags = book_info["tags"]
        pictures = book_info["pictures"]
        args = [[book_id, tags[i]] for i in range(len(tags))]
        self.multi_modify("INSERT INTO tag_for_book"
            "(book_id, book_tag)"
            "VALUES (%s, %s);",
            args)
        args = [(book_id, pictures[i]) for i in range(len(pictures))]
        self.multi_modify("INSERT INTO pic_for_book"
            "(book_id, book_pic)"
            "VALUES (%s, %s);",
            args)

    def get_book_by_id(self, book_id):
        book = self.get_one("SELECT * FROM book WHERE book_id = %s;", (book_id,))
        return book

    def get_book_price(self, book_id):
        price = self.get_one("SELECT price FROM book WHERE book_id = %s;", (book_id,))
        return price["price"]

    def check_book_exists(self, book_id):
        result = self.get_one("SELECT * FROM book WHERE book_id = %s;", (book_id,))
        return result != None

    def search_book_by_keywords(self, keywords, is_title, is_content, is_author, is_tag):
        result = []
        if is_title:
            result.append(self.get_list("SELECT distinct title,author,price FROM book WHERE title like %s;", (keywords,)))
        if is_content:
            result.append(self.get_list("SELECT distinct title,author,price FROM book WHERE content like %s;", (keywords,)))
        if is_author:
            result.append(self.get_list("SELECT distinct title,author,price FROM book WHERE author like %s;", (keywords,)))
        if is_tag:
            result.append(self.get_list("SELECT distinct title,author,price FROM tag_for_book,book WHERE book_tag like %s and book.book_id = tag_for_book.book_id;", (keywords,)))
        return result