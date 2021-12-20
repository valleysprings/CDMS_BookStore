# 说明文档：view层的buyer

若无特别说明，默认response返回的body为status code对应的描述。

## 买家下单

#### URL：
POST http://[address]/buyer/new_order

#### Request

##### Header:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

##### Body:
```json
{
  "user_id": "buyer_id",
  "store_id": "store_id",
  "books": [
    {
      "id": "1000067",
      "count": 1
    },
    {
      "id": "1000134",
      "count": 4
    }
  ]
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
store_id | string | 商铺ID | N
books | class | 书籍购买列表 | N

books数组：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
id | string | 书籍的ID | N
count | string | 购买数量 | N


#### Response

Status Code:

码 | 描述
--- | ---
200 | 下单成功
509 | 买家用户ID不存在
503 | 商铺ID不存在
510 | 购买的图书不存在
511 | 商品库存不足

##### Body:
```json
{
  "order_id": "uuid"
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
order_id | int | 订单号，只有返回200时才有效 | N





## 买家取消订单

#### URL：

POST http://[address]/buyer/cancel

#### Request

##### Header:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

##### Body:

```json
{
  "user_id": "buyer_id",
  "order_id": "order_id"
}
```

##### 属性说明：

| 变量名   | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 买家用户ID | N          |
| order_id | int    | 订单号     | N          |

#### Response

Status Code:

| 码   | 描述                                 |
| ---- | ------------------------------------ |
| 200  | 取消成功                             |
| 513  | 订单ID不存在，或订单和买家关系不正确 |
| 514  | 订单已被支付                         |





## 买家付款

#### URL：
POST http://[address]/buyer/payment

#### Request

##### Body:
```json
{
  "user_id": "buyer_id",
  "order_id": "order_id",
  "password": "password"
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
order_id | int | 订单ID | N
password | string | 买家用户密码 | N 


#### Response

Status Code:

码 | 描述
--- | ---
200 | 付款成功
512 | 账户余额不足
513 | 订单ID不存在，或订单和买家关系不正确 
401 | 用户名不存在或密码不正确 
514 | 订单已被支付 
522 | 订单超时 





## 买家充值

#### URL：
POST http://[address]/buyer/add_funds

#### Request

##### Body:
```json
{
  "user_id": "user_id",
  "password": "password",
  "add_value": 10
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
password | string | 用户密码 | N
add_value | int | 充值金额，以分为单位 | N

#### Response

Status Code:

码 | 描述
--- | ---
200 | 充值成功
401 | 用户名不存在或密码不正确 
515 | 充值金额不合法 
518 | 表单缺值 





## 买家确认收货

#### URL：

POST http://[address]/buyer/delivery_confirmed

#### Request

##### Body:

```json
{
  "user_id": "user_id",
  "order_id": "order_id"
}
```

##### 属性说明：

| 变量名   | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 买家用户ID | N          |
| order_id | int    | 订单号     | N          |

#### Response

Status Code:

| 码   | 描述                                |
| ---- | ----------------------------------- |
| 200  | 查询成功                            |
| 524 | 订单状态有误               |
| 513 | 订单ID不存在，或订单和买家关系不正确 |





## 买家通过关键词获取图书列表

#### URL：

POST http://[address]/buyer/search_book

#### Request

##### Body:

```json
{
  "keywords": "keywords",
  "params": {
      "is_title": "is_title",
      "is_content": "is_content",
      "is_author": "is_author",
      "is_tag": "is_tag"
  }
}
```

##### 属性说明：

| 变量名   | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| keywords | string | 搜索关键词 | N          |
| params   | dict   | 用户密码   | N          |

params字典

| 变量名     | 类型 | 描述                 | 是否可为空 |
| ---------- | ---- | -------------------- | ---------- |
| is_title   | bool | 搜索范围是否包括标题 | N          |
| is_content | bool | 搜索范围是否包括内容 | N          |
| is_author  | bool | 搜索范围是否包括作者 | N          |
| is_tag     | bool | 搜索范围是否包括标签 | N          |

#### Response

Status Code:

| 码   | 描述                                         |
| ---- | -------------------------------------------- |
| 200  | 查询成功                                     |
| 518  | 表单缺值                                     |
| 520  | 搜索输入为空                                 |
| 521  | 范围参数非法，需要至少指定一个有效的查询范围 |

##### Body:

```json
{
    "book_list": [
        [book_list_title],
        [book_list_content],
        [book_list_author],
        [book_list_tag]
    ],
    "message": "msg"
}
```

注：

1. 当status code不为200时，book_list为none。
2. book_list含有多少个list取决于你勾选了多少范围的数据。

##### 属性说明：

| 变量名    | 类型 | 描述             | 是否可为空 |
| --------- | ---- | ---------------- | ---------- |
| book_list | list | 返回各项搜索结果 | Y          |





## 买家评价已完成订单

#### URL:

POST http://[address]/buyer/comment
#### Request

##### Header:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

##### Body:

```json
{
  "user_id": "user_id",
  "order_id": "order_id",
  "score": 5,
  "comment": "comment"
}
```

##### 属性说明：

| 变量名    | 类型 | 描述             | 是否可为空 |
| --------- | ---- | ---------------- | ---------- |
| user_id  | str | 买家id   | N      |
| order_id | int | 订单id   | N      |
| score    | int | 评价分数 |  N     |
| comment  | str | 评价内容 |  Y     |

#### Response

Status Code:

| 码   | 描述                                         |
| ---- | -------------------------------------------- |
| 200  | 查询成功  |
| 401  | 用户名不存在或密码不正确 |
| 503  | 商铺ID不存在|
| 513  | 订单ID不存在，或订单和买家关系不正确 |
| 518  | 表单缺值    |
| 524  | 订单状态有误| 
| 525  | 评价分数不合法|





## 买家查看店铺评价(search_comment)

#### URL：

POST http://[address]/buyer/search_comment

#### Request

##### Body:

```json
{
  "store_id": "store_id"
}
```

##### 属性说明：

| 变量名   | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| store_id | str | 店铺id | N          |

#### Response

Status Code:

| 码   | 描述                                         |
| ---- | -------------------------------------------- |
| 200  | 查询成功        |
| 503  | 商铺ID不存在    |

##### Body:

```json
{
    "comment_list": [
        {
          "user_id": "user_id",
          "order_id": "order_id",
          "score": 5,
          "comment": "comment"
        }
    ],
    "message": "msg"
}
```

注：

##### 属性说明：

| 变量名    | 类型 | 描述             | 是否可为空 |
| --------- | ---- | ---------------- | ---------- |
| comment_list | list | 返回评价结果 | Y          |
| user_id | str | 评价用户id | N          |
| order_id | int | 订单id | N          |
| score | int | 评价分数 | N          |
| comment | str | 评价内容 | Y          |





## 买家查看订单状态(check_order_status)

#### URL：

POST http://[address]/buyer/check_order_status

#### Request

##### Header:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

##### Body:

```json
{
  "user_id": "buyer_id",
  "order_id": "order_id"
}
```

##### 属性说明：

| 变量名   | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 买家用户ID | N          |
| order_id | int    | 订单号     | N          |

#### Response

Status Code:

| 码   | 描述                                 |
| ---- | ------------------------------------ |
| 200  | 查询状态成功                         |
| 513  | 订单ID不存在，或订单和买家关系不正确 |

##### Body:

```json
{
  "status": "status",
  "message": "msg"
}
```

##### 属性说明：

| 变量名 | 类型 | 描述     | 是否可为空 |
| ------ | ---- | -------- | ---------- |
| status | int  | 订单状态 | Y          |

注：当status code不为200时，status为none。





## 买家查看所有进行中的订单(check_order_history_ongoing)

#### URL：

POST http://[address]/buyer/check_order_history_ongoing

#### Request

##### Header:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

##### Body:

```json
{
  "user_id": "buyer_id",
}
```

##### 属性说明：

| 变量名   | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 买家用户ID | N          |
| order_id | int    | 订单号     | N          |

#### Response

Status Code:

| 码   | 描述                                 |
| ---- | ------------------------------------ |
| 200  | 查询状态成功                         |
| 513  | 订单ID不存在，或订单和买家关系不正确 |

##### Body:

```json
{
  "history": [
        {
          "order_id": "order_id",
          "status": "status",
          "purchased_price": "purchased_price",
          "transaction_start_time": "transaction_start_time",
          "books": [books],
            
        }
    ],
  "message": "msg"
}
```

##### 属性说明：

| 变量名  | 类型 | 描述             | 是否可为空 |
| ------- | ---- | ---------------- | ---------- |
| history | list | 返回用户订单历史 | Y          |

history内部字典

| 变量名                 | 类型      | 描述           | 是否可为空 |
| ---------------------- | --------- | -------------- | ---------- |
| order_id               | int       | 返回用户订单号 | N          |
| status                 | int       | 订单状态       | N          |
| purchased_price        | int       | 订单价格       | N          |
| transaction_start_time | timestamp | 订单创建时间   | N          |

注：当status code不为200时，history为none。







## 买家查看所有交易完成订单(check_order_history)

#### URL：

POST http://[address]/buyer/check_order_history

#### Request

##### Header:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

##### Body:

```json
{
  "user_id": "buyer_id",
}
```

##### 属性说明：

| 变量名   | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 买家用户ID | N          |
| order_id | int    | 订单号     | N          |

#### Response

Status Code:

| 码   | 描述                                 |
| ---- | ------------------------------------ |
| 200  | 查询状态成功                         |
| 513  | 订单ID不存在，或订单和买家关系不正确 |

##### Body:

```json
{
  "history": [
        {
          "order_id": "order_id",
          "status": "status",
          "purchased_price": "purchased_price",
          "transaction_start_time": "transaction_start_time",
          "books": [books],
            
        }
    ],
  "message": "msg"
}
```

##### 属性说明：

| 变量名  | 类型 | 描述             | 是否可为空 |
| ------- | ---- | ---------------- | ---------- |
| history | list | 返回用户订单历史 | Y          |

history内部字典

| 变量名                 | 类型      | 描述           | 是否可为空 |
| ---------------------- | --------- | -------------- | ---------- |
| order_id               | int       | 返回用户订单号 | N          |
| status                 | int       | 订单状态       | N          |
| purchased_price        | int       | 订单价格       | N          |
| transaction_start_time | timestamp | 订单创建时间   | N          |
| transaction_end_time   | timestamp | 订单关闭时间   | N          |

注：当status code不为200时，history为none。

