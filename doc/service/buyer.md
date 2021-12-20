## 买家下单(new_order)

#### 实现功能

验证token有效性。

验证买家用户ID、商铺ID、购买的图书ID是否存在。

验证商品库存是否不足。

修改order表，增加订单，计算总价格，status属性设置为1（待付款）

修改book_for_store表，修改book_count属性，减少对应书在商铺中的库存

#### 传入参数

```python
buyer_id: str,
store_id: str,
books: [(str, int)]
token: str,
```

其中books为一个列表，列表的每一项为一个二元组(book_id, count)，即books=[(book_id1, count1), (book_id2, count2),...]

#### 返回值

```python
statusCode: int,
message: str,
order_id: int
```

200:成功

503:商铺ID不存在

509:买家ID不存在

510:购买的图书ID不存在

511:商品库存不足

401:token错误

#### 函数声明

```python
def new_order(buyer_id: str, store_id: str, books: [(str, int)], token: str) -> (int, str, int)
```





## 买家付款(payment)

#### 实现功能

验证用户是否存在，密码是否正确。

验证订单ID是否存在。

验证订单是否未支付（状态码为1）。（避免重复支付）

验证账户余额是否大于订单金额。

修改user表中买家的cash属性（扣钱），在order表中根据order_id查找store_id，并在store表中根据store_id查找seller_id，得到卖家id后修改user表中卖家的cash属性（加钱）

修改order表中的status属性，由1（待付款）修改为2（待发货）

#### 传入参数

```python
buyer_id: str,
order_id: int,
password: str
```

#### 返回值

```python
statusCode: int,
message: str
```

200:成功

401:用户名不存在或密码不正确

512:账户余额不足

513:订单ID不存在，或订单和买家关系不正确

514:订单已被支付

522:订单超时

#### 函数声明

```python
def payment(buyer_id: str, order_id: int, password: str) -> (int, str)
```





## 买家主动撤销订单(manual_cancel)

#### 实现功能

买家主动撤销订单。

#### 传入参数

```python
buyer_id: str,
order_id: int
```

#### 返回值

```python
statusCode: int,
message: str
```

200:成功

513:订单ID不存在，或订单和买家关系不正确

#### 函数声明

```python
def cancel(buyer_id: str, order_id: int) -> (int, str)
```





## 买家充值(add_funds)

#### 实现功能

验证用户是否存在，密码是否正确。

验证充值金额是否>0。

修改user表中的cash属性，增加余额

#### 传入参数

```python
user_id: str,
password: str,
add_value: int
```

#### 返回值

```python
statusCode: int
message: str
```

200:成功

401:用户名不存在或密码不正确

515:充值金额不合法

518:表单缺值

#### 函数声明

```python
def add_funds(user_id: str, password: str, add_value: int) -> (int, str)
```





## 买家通过关键词获取图书列表(search_book)

#### 实现功能

用户可以通过关键词，按照给定范围获得图书列表。

#### 传入参数

```python
keywords: str,
params: dict
```

#### 返回值

```python
statusCode: int,
message: str,
books_id: list
```

200:成功

518:表单缺值

520:搜索输入为空

521:范围参数非法，需要至少指定一个有效的查询范围

#### 函数声明

```python
def search_book(keywords: str, params: dict) -> (int, str, list)
```

注：错误时list为none。





## 买家评价订单(comment)

#### 实现功能

订单完成后，用户可以对订单进行评价，包括打分和评论，评价结果将记录在店铺信息中

#### 传入参数
```python
buyer_id: str,
store_id: str,
order_id: str,
score: int,
comment: str
```
#### 返回值
```python
statusCode: int,
message: str
```
#### 函数声明
```python
def comment(token: str, buyer_id: str, store_id: str, order_id: str, score: int, comment: str) -> (int, str)
```





## 买家查看店铺评价(search_comment)

#### 实现功能

订单完成后，用户可以对订单进行评价，包括打分和评论，评价结果将记录在店铺信息中

#### 传入参数
```python
store_id: str
```
#### 返回值
```python
statusCode: int,
message: str,
comment_list: list
```
#### 函数声明
```python
def search_comment(store_id: str) -> (int, str, list)
```





## 买家查看订单状态(check_order_status)

#### 实现功能

买家查看订单状态。

#### 传入参数

```python
buyer_id: str,
order_id: int
```

#### 返回值

```python
statusCode: int,
message: str,
status: int
```

200:成功

401:token有效性验证失败

513:订单ID不存在，或订单和买家关系不正确

#### 函数声明

```python
def check_order_status(token: str, buyer_id: str, order_id: int) -> (int, str)
```





