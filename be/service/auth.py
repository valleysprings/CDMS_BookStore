# 参考doc/service/auth文档，处理具体业务逻辑
# 实现基于be/dao/dao提供的接口
from be.dao.user import User
from be.service import token_tool

def register(user_id: str, password: str) -> tuple:
    if User().get_user_by_id(user_id) is not None:
        return 508, 'User ID already exists.'
    
    User().add_user(user_id, password)
    return 200, 'OK'


def check_user_valid(user_id: str, password: str) -> bool:
    user_info = User().get_user_by_id(user_id)
    if user_info is None:
        return False
    elif not user_info['user_password'] == password:
        return False
    return True


def unregister(user_id: str, password: str) -> tuple:
    if not check_user_valid(user_id, password):
        return 401, 'User ID or Password is incorrect.', None

    User().delete_user(user_id)
    return 200, 'OK'


def login(user_id: str, password: str, terminal: str) -> tuple:
    if not check_user_valid(user_id, password):
        return 401, 'User ID or Password is incorrect.', None
    
    token = token_tool.encode(user_id, terminal)
    User().update_user_token(user_id, token)
    return 200, 'OK', token


def change_password(user_id: str, oldPassword: str, newPassword: str) -> tuple:
    if not check_user_valid(user_id, oldPassword):
        return 401, 'User ID or Password is incorrect.', None

    User().update_user_password(user_id, newPassword)
    return 200, 'OK'


def logout(user_id: str, token: str):
    if not token_tool.check_token_validation(token, user_id):
        return 401, 'Token is invalid or User is not login.'
    logout_R(user_id)
    return 200, 'OK'

def logout_R(user_id: str):
    User().update_user_token(user_id, user_token="")


def get_user(user_id: str):
    user_info = User().get_user_by_id(user_id)
    return user_info