# 数据库访问对象
# 处理对user表的CRUD操作
# 为逻辑层提供数据库访问接口
from be.dao.db_conn import Dao
from be.dao.db_conn import connPool

class User(Dao):
    def __init__(self):
        self.conn = connPool.connection()
        self.cursor = self.get_cursor()

    def __del__(self):
        # connPool.release(self.conn)
        self.conn.close()
        self.close_cursor()

    def drop_table(self):
        cursor = self.cursor
        cursor.execute("DROP TABLE IF EXISTS user;")

    def create_table(self):
        cursor = self.cursor
        cursor.execute("CREATE TABLE IF NOT EXISTS user ( " 
            "user_id VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,"
            "user_password VARCHAR(255) NOT NULL,"
            "cash INT NOT NULL,"
            "token TEXT NOT NULL"
            ");"
        )
    
    def get_user_by_id(self, user_id):
        user = self.get_one("SELECT * FROM user WHERE user_id = %s;", (user_id,))
        return user
    
    def add_user(self, user_id, user_password):
        self.modify("INSERT INTO user (user_id, user_password, cash, token) VALUES (%s, %s, %s, %s);", (user_id, user_password, 0, ""))

    def delete_user(self, user_id):
        self.modify("DELETE FROM user WHERE user_id = %s;", (user_id,))

    def update_user_token(self, user_id, user_token):
        self.modify("UPDATE user SET token = %s WHERE user_id = %s;", (user_token, user_id))
    
    def update_user_password(self, user_id, user_password):
        self.modify("UPDATE user SET user_password = %s WHERE user_id = %s;", (user_password, user_id))

    def add_user_cash(self, user_id, cash):
        self.modify("UPDATE user SET cash = cash + %s WHERE user_id = %s;", (cash, user_id))
    
    def get_user_token(self, user_id):
        user = self.get_one("SELECT token FROM user WHERE user_id = %s;", (user_id,))
        return user['token']
    
    def get_user_cash(self, user_id):
        user = self.get_one("SELECT cash FROM user WHERE user_id = %s;", (user_id,))
        return user['cash']