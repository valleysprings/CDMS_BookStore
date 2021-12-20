## 注册用户(register)

#### 实现功能

验证user_id是否已存在。

根据user_id和password修改user表。

#### 传入参数
```python
user_id: str,
password: str
```
#### 返回值
```python
statusCode: int
message: str
```
200:成功

508:注册失败，用户名重复

518:表单缺值（user_id或password）

#### 函数声明
```python
def register(user_id: str, password: str) -> (int, str)
```

## 注销用户(unregister)

#### 实现功能

验证用户是否存在，密码是否正确

++验证是否有未完成的购买订单

++验证该用户的商铺是否有未完成的出售订单

根据user_id和password修改user表，检查该用户是否有商铺，有则依次删除以下数据

1. book表中在该商铺中的所有书籍

2. book_for_store表中包含该商铺的数据

3. store表中的该商铺

4. user表中的用户

#### 传入参数
```python
user_id: str,
password: str
```
#### 返回值
```python
statusCode: int
```
200:成功

401:用户名不存在或密码不正确

++516:有未完成的购买订单

++517:有未完成的出售订单

#### 函数声明
```python
def unregister(user_id: str, password: str) -> (int, str)
```

## 用户登录(login)

#### 实现功能

验证用户是否存在，以及密码是否正确

session用于储存横跨请求的值。验证成功后，用户的 `id` 被储存于一个新的session中，被储存到一个 向浏览器发送的 *cookie* 中，在后继请求中，浏览器会返回它。 Flask 有签名机制防数据被篡改。

#### 传入参数
```python
user_id: str,
password: str，
terminal: str
```
#### 返回值
```python
statusCode: int
message: str
```
200:成功

401:登录失败，用户名或密码错误

518:表单缺值（user_id或password）

#### 函数声明
```python
def login(user_id: str, password: str, terminal: str) -> (int, str)
```


## 用户修改密码(change_password)

#### 实现功能

验证用户是否存在，密码是否正确

修改user表中的password属性


#### 传入参数
```python
user_id: str,
oldPassword: str,
newPassword: str
```
#### 返回值
```python
statusCode: int
message: str
```
200:成功

401:用户名不存在或密码不正确

518:表单缺值（user_id或password）

#### 函数声明
```python
def password(user_id: str, oldPassword: str, newPassword: str) -> (int, str)
```
