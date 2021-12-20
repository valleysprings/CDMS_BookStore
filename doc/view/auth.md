## 注册用户(register)

#### URL：
POST http://$address$/auth/register

#### Request

Body:
```
{
    "user_id":"$user name$",
    "password":"$user password$"
}
```

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 用户名 | N
password | string | 登陆密码 | N

#### Response

Status Code:


码 | 描述
--- | ---
200 | 注册成功
508 | 注册失败，用户名重复
518 | 表单缺值（user_id或password） 

Body:
```
{
    "message":"$error message$"
}
```
变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
message | string | 返回错误消息，成功时为"ok" | N

## 注销用户(unregister)

#### URL：
POST http://$address$/auth/unregister

#### Request

Body:
```
{
    "user_id":"$user name$",
    "password":"$user password$"
}
```

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 用户名 | N
password | string | 登陆密码 | N

#### Response

Status Code:


码 | 描述
--- | ---
200 | 注销成功
401 | 注销失败，用户名不存在或密码不正确
518 | 表单缺值（user_id或password） 


Body:
```
{
    "message":"$error message$"
}
```
变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
message | string | 返回错误消息，成功时为"ok" | N

## 用户登录(login)

#### URL：
POST http://$address$/auth/login

#### Request

Body:
```
{
    "user_id":"$user name$",
    "password":"$user password$",
    "terminal":"$terminal code$"
}
```

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 用户名 | N
password | string | 登陆密码 | N
terminal | string | 终端代码 | N 

#### Response

Status Code:

码 | 描述
--- | ---
200 | 登录成功
401 | 登录失败，用户名或密码错误
518 | 表单缺值（user_id或password） 

Body:
```
{
    "message":"$error message$",
    "token":"$access token$"
}
```
变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
message | string | 返回错误消息，成功时为"ok" | N
token | string | 访问token，用户登录后每个需要授权的请求应在headers中传入这个token | 成功时不为空 

#### 说明 

1. terminal标识是哪个设备登录的，不同的设备拥有不同的ID，测试时可以随机生成。

2. token是登录后，在客户端中缓存的令牌，在用户登录时由服务端生成，用户在接下来的访问请求时不需要密码。token会定期地（每3600秒）失效，对于不同的设备，token是不同的。token只对特定的时期特定的设备是有效的。

3. 登录后现在用户的 id 已被储存在 session 中，可以被后续的请求使用。对每个请求，如果用户已登录，那么其用户信息会在请求之前被载入。

```python
@bp.before_app_request
def load_logged_in_user():
    pass
```

## 用户更改密码

#### URL：
POST http://$address$/auth/password

#### Request

Body:
```
{
    "user_id":"$user name$",
    "oldPassword":"$old password$",
    "newPassword":"$new password$"
}
```

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 用户名 | N
oldPassword | string | 旧的登陆密码 | N
newPassword | string | 新的登陆密码 | N

#### Response

Status Code:

码 | 描述
--- | ---
200 | 更改密码成功
401 | 更改密码失败
518 | 表单缺值（user_id或password） 

Body:
```
{
    "message":"$error message$",
}
```
变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
message | string | 返回错误消息，成功时为"ok" | N

## 用户登出(logout)

#### URL：
POST http://$address$/auth/logout

#### Request

Headers:

| key   | 类型   | 描述      |
| ----- | ------ | --------- |
| token | string | 访问token |

Body:
```
{
    "user_id":"$user name$"
}
```

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 用户名 | N

#### Response

Status Code:

码 | 描述
--- | ---
200 | 登出成功
401 | 用户token错误 
518 | 表单缺值（user_id） 

Body:
```
{
    "message":"$error message$"
}
```
变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
message | string | 返回错误消息，成功时为"ok" | N
