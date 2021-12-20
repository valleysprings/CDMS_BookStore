## 创建商铺(create_store)

#### 实现功能

验证store_id是否已存在

验证token, seller_id是否有效

根据传入的加密前的token和seller_id验证seller是否具有创建店铺的权限。

根据seller_id和store_id修改表store，即创建店铺。

#### 传入参数

```python
token: str
seller_id
store_id
```

#### 返回值
```python
statusCode: int
message: str
```
200:成功

501:店铺id已存在

507:token有效性验证失败
#### 函数声明

```python
def create_store(token: str, seller_id: str, store_id: str) -> (int, str)
```

## 商家添加书籍信息(add_book)

#### 实现功能

验证卖家ID是否存在、商铺ID是否存在、图书ID是否存在、seller_id与store_id的关系是否存在

验证token有效性

根据store_id和book_info修改表book，添加书籍信息。

同时根据store_id和stock_level修改表book_for_store。

#### 传入参数
```python
token: str
seller_id: str
store_id: str
book_info: str
stock_level: int
```
book_info为序列化后的json字符串，其反序列化后的json数据格式为

```json
"book_info": {
    "tags": [
        "tags1",
        "tags2",
        "tags3",
        "..."
    ],
    "pictures": [
        "$Base 64 encoded bytes array1$",
        "$Base 64 encoded bytes array2$",
        "$Base 64 encoded bytes array3$",
        "..."
    ],
    "id": "$book id$",
    "title": "$book title$",
    "author": "$book author$",
    "publisher": "$book publisher$",
    "original_title": "$original title$",
    "translator": "translater",
    "pub_year": "$pub year$",
    "pages": 10,
    "price": 10,
    "binding": "平装",
    "isbn": "$isbn$",
    "author_intro": "$author introduction$",
    "book_intro": "$book introduction$",
    "content": "$chapter1 ...$"
}
```
#### 返回值
```python
statusCode: int
```
200:成功

502:卖家ID不存在

503:商铺ID不存在

504:图书ID已存在

505:seller_id与store_id关系已存在

507:token有效性验证失败

#### 函数声明
```python
def add_book(token: str, seller_id: str, store_id: str, book_info: str, stock_level: int) -> int
```

## 商家添加书籍库存(add_stock_level)

#### 实现功能
验证商铺ID、图书ID、seller_id与store_id关系是否存在

验证token有效性

根据store_id和stock_level修改表book_for_store。

#### 传入参数
```python
token: str
seller_id: str
store_id: str
book_id: str
add_stock_level: int
```
#### 返回值
```python
statusCode: int
```
200:成功

503:商铺ID不存在

504:图书ID已存在

506:seller_id与store_id关系不存在

507:token有效性验证失败

#### 函数声明

```python
def add_stock_level(token: str, seller_id: str, store_id: str, book_id: str, add_stock_level: int) -> int
```