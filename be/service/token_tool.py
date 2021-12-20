from json import decoder
import time
import jwt
from be.dao import user
import logging

jwtkey = 'NdX2@d#oZ8cD'

def encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=jwtkey,
        algorithm="HS256",
    )
    return encoded

def decode(encoded_token: str) -> dict:
    decoded = jwt.decode(encoded_token, 
        key=jwtkey, 
        algorithms="HS256")
    return decoded


# 检查token是user_id的token
# 过时清除token
def check_token_validation(encoded_token: str, user_id: str) -> bool:
    try:
        if user.User().get_user_token(user_id) == '':
            return False
        if decode(encoded_token).get("timestamp") + 3600 < int(time.time()):
            user.User().update_user_token(user_id, user_token="")
            return False
        return True
    except:
        return False
