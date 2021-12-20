## 生成加密token(encoder)

#### 实现功能

根据user_id, terminal, 以及当前时间戳，生成加密后的token

选择自定义的key值，加密算法使用HS256
#### 传入参数

```python
user_id: str,
terminal: str
```

#### 返回值

```python
token: str
```

#### 函数声明

```python
def encoder(user_id: str, terminal: str) -> str
```

## 还原未加密token(decoder)

#### 实现功能

根据已加密的token还原user_id, terminal以及时间戳

#### 传入参数

```python
encoded_token: str
```

#### 返回值

```python
decoded: dict
```

#### 函数声明

```python
def decode(encoded_token: str) -> dict
```

## 验证加密token有效性(validator)(这段在auth里实现)

#### 实现功能

传入已加密的token，首先根据已加密的token还原user_id, terminal以及时间戳

接着依次进行以下判断：

验证user_id是否存在

验证token是否过期（时间戳之差大于3600，即时间超过一小时）

验证user表中的token属性与加密前的token是否相同

若通过以上验证则返回True，表示token有效，否则返回False，表示token无效

#### 传入参数

```python
encoded_token: str
```

#### 返回值

```python
result: bool
```

#### 函数声明

```python
def token_validator(encoded_token: str) -> bool
```

