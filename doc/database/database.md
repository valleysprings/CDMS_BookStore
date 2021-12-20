# 数据库设计

若无特别说明，默认设置第一行属性为PRIMARY KEY



## user
记录user的单值属性
NAME|TYPE|UNIQUE|FORENIGN KEY|NOT NULL
----|----|---|---|---
user_id| VARCHAR(255) |Y|N|Y
user_password| VARCHAR(255) |N|N|Y
cash| INT          |N|N|Y
token|VARCHAR(255)|N|N|Y



创建表代码

```sql
CREATE TABLE IF NOT EXISTS user (  
            user_id VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
            user_password VARCHAR(255) NOT NULL,
            cash INT NOT NULL,
            token VARCHAR(255) NOT NULL
);
```



## orderform

记录还在执行中（已下单（未付款）/已付款（未发货）/已发货（未收货）状态）的订单
 NAME                   | TYPE         | UNIQUE | FORENIGN KEY    | NOT NULL 
----|----|---|---|---
 orderform_id           | BIGINT       | Y      | N               | Y        
 buyer_id               | VARCHAR(255) | N      | user(user_id)   | Y        
 store_id               | VARCHAR(255) | N      | store(store_id) | Y        
 purchased_price        | INT          | N      | N               | Y        
 transaction_start_time | TIMESTAMP    | N      | N               | Y        
 transaction_end_time   | TIMESTAMP    | N      | N               | Y        
 status                 | INT          | N      | N               |Y

status状态码: 1：待付款，2：待发货，3：待收货



创建表代码

```sql
CREATE TABLE IF NOT EXISTS orderform (
            orderform_id BIGINT NOT NULL AUTO_INCREMENT,
    		buyer_id VARCHAR(255) NOT NULL,
    		store_id VARCHAR(255) NOT NULL,
    		purchased_price INT,
            transaction_start_time TIMESTAMP NOT NULL,
            status INT NOT NULL,
    		FOREIGN KEY(buyer_id) REFERENCES user(user_id),
    		FOREIGN KEY(store_id) REFERENCES store(store_id),
    		PRIMARY KEY (orderform_id)
);
```



## book_for_orderform

记录还在执行中（已下单（未付款）/已付款（未发货）/已发货（未收货）状态）的订单

| NAME                  | TYPE         | UNIQUE | FORENIGN KEY            | NOT NULL |
| --------------------- | ------------ | ------ | ----------------------- | -------- |
| orderform_id          | BIGINT       | N      | orderform(orderform_id) | Y        |
| book_for_orderform_id | VARCHAR(255) | N      | book(book_id)           | Y        |
| book_count            | INT          | N      | N                       | Y        |



创建表代码

```sql
CREATE TABLE IF NOT EXISTS book_for_orderform ( 
            orderform_id BIGINT NOT NULL,
            book_for_orderform_id VARCHAR(255) NOT NULL,
            book_count INT NOT NULL,
            FOREIGN KEY(orderform_id) REFERENCES orderform(orderform_id),
    		FOREIGN KEY(book_for_orderform_id) REFERENCES book(book_id)
);
```





## orderform_history

记录已完成（或取消）的历史订单
NAME|TYPE|UNIQUE|FORENIGN KEY|NOT NULL
:--:|:--:|---|---|---
orderform_id| BIGINT |Y|N|Y
 buyer_id         | VARCHAR(255) | N      | user(user_id) | Y        
 store_id         | VARCHAR(255) | N      | store(store_id) | Y        
 purchased_price | INT          | N      | N | Y        
 transaction_start_time |TIMESTAMP|N|N|Y
 transaction_end_time |TIMESTAMP|N|N|Y
 status |INT|N|N|Y



创建表代码

```sql
CREATE TABLE IF NOT EXISTS orderform_history (  
            orderform_id BIGINT NOT NULL,
    		buyer_id VARCHAR(255) NOT NULL,
    		store_id VARCHAR(255) NOT NULL,
    		purchased_price INT NOT NULL,
            transaction_start_time TIMESTAMP NOT NULL,
    		transaction_end_time TIMESTAMP NOT NULL,
            status INT NOT NULL,
    		FOREIGN KEY(buyer_id) REFERENCES user(user_id),
    		FOREIGN KEY(store_id) REFERENCES store(store_id),
    		PRIMARY KEY (orderform_id)
);
```





## book_for_orderform_history

记录已完成（或取消）的历史订单

| NAME                  | TYPE         | UNIQUE | FORENIGN KEY            | NOT NULL |
| --------------------- | ------------ | ------ | ----------------------- | -------- |
| orderform_id          | BIGINT       | N      | orderform(orderform_id) | Y        |
| book_for_orderform_id | VARCHAR(255) | N      | book(book_id)           | Y        |
| book_count            | INT          | N      | N                       | Y        |



创建表代码

```sql
CREATE TABLE IF NOT EXISTS book_for_orderform_history ( 
            orderform_id BIGINT NOT NULL,
            book_for_orderform_id VARCHAR(255) NOT NULL,
            book_count INT NOT NULL,
            FOREIGN KEY(orderform_id) REFERENCES orderform(orderform_id),
    		FOREIGN KEY(book_for_orderform_id) REFERENCES book(book_id)
);
```





## book

记录book的单值属性

NAME|TYPE|UNIQUE|FORENIGN KEY|NOT NULL
:--:|----|---|---|---
book_id|VARCHAR(255)|Y|N|Y
title|VARCHAR(255)|N|N|N
author|VARCHAR(255)|N|N|N
publisher|VARCHAR(255)|N|N|N
original_title|VARCHAR(255)|N|N|N
translator|VARCHAR(255)|N|N|N
pub_year|YEAR|N|N|N
pages|INT|N|N|N
price|INT|N|N|N
biding|VARCHAR(255)|N|N|N
ISBN|VARCHAR(20)|N|N|N
author_intro|TEXT|N|N|N
book_intro|TEXT|N|N|N
content|TEXT|N|N|N



创建表代码

```sql
CREATE TABLE IF NOT EXISTS book (
            book_id VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255),
            publisher VARCHAR(255),
            original_title VARCHAR(255),
            pub_year YEAR,
            pages INT,
            price INT,
            biding VARCHAR(255),
            ISBN VARCHAR(20),
            author_intro TEXT,
            book_intro TEXT,
            content TEXT
);
```





## store

记录store的单值属性

NAME|TYPE|UNIQUE|FORENIGN KEY|NOT NULL
----|----|---|---|---
store_id|VARCHAR(255)|Y|N|Y
seller_id|VARCHAR(255)|N|user(user_id)|Y



创建表代码

```sql
CREATE TABLE IF NOT EXISTS store (  
            store_id VARCHAR(255) UNIQUE NOT NULL,
            seller_id VARCHAR(255) NOT NULL,
            FOREIGN KEY(seller_id) REFERENCES user(user_id)
);
```





## book_for_store

记录store和book的拥有关系

设置联合主键或由系统生成默认主键
NAME|TYPE|UNIQUE|FORENIGN KEY|NOT NULL
----|----|---|---|---
store_id|VARCHAR(255)|N|store(store_id)|Y
book_id|VARCHAR(255)|N|book(book_id)|
 book_count | INT          | N      | N               | Y        



创建表代码

```sql
CREATE TABLE IF NOT EXISTS book_for_store (  
            store_id VARCHAR(255) NOT NULL,
            book_id VARCHAR(255) NOT NULL,
    		book_count INT NOT NULL,
            FOREIGN KEY(store_id) REFERENCES store(store_id),
    		FOREIGN KEY(book_id) REFERENCES book(book_id)
);
```





## tag_for_book

记录book的多值属性tag

设置联合主键或由系统生成默认主键
NAME|TYPE|UNIQUE|FORENIGN KEY|NOT NULL
----|----|---|---|---
book_id|VARCHAR(255)|N|book(book_id)|Y
book_tag|VARCHAR(255)|N|N|Y



创建表代码

```sql
CREATE TABLE IF NOT EXISTS tag_for_book (  
            book_id VARCHAR(255) NOT NULL,
    		book_tag VARCHAR(255) NOT NULL,
    		FOREIGN KEY(book_id) REFERENCES book(book_id)
);
```





## pic_for_book

记录book的多值属性pic

设置联合主键或由系统生成默认主键
NAME|TYPE|UNIQUE|FORENIGN KEY|NOT NULL
----|----|---|---|---
book_id|VARCHAR(255)|N|book(book_id)|Y
book_pic|LONGBLOB|N|N|Y



创建表代码

```sql
CREATE TABLE IF NOT EXISTS pic_for_book (  
            book_id VARCHAR(255) NOT NULL,
    		book_pic LONGBLOB NOT NULL,
    		FOREIGN KEY(book_id) REFERENCES book(book_id)
);
```





## comment_for_store

记录用户对历史记录的评价

设置联合主键或由系统生成默认主键

| NAME     | TYPE         | UNIQUE | FORENIGN KEY                    | NOT NULL |
| -------- | ------------ | ------ | ------------------------------- | -------- |
| store_id | VARCHAR(255) | N      | store(store_id)                 | Y        |
| user_id  | VARCHAR(255) | N      | user(user_id)                   | Y        |
| order_id | BIGINT       | N      | orderform_history(orderform_id) | Y        |
| score    | INT          | N      | N                               | Y        |
| comment  | TEXT         | N      | N                               | N        |



创建表代码

```sql
CREATE TABLE IF NOT EXISTS comment_for_store ( 
            store_id VARCHAR(255) NOT NULL,
            user_id VARCHAR(255) NOT NULL,
            order_id VARCHAR(255) NOT NULL,
    		score INT NOT NULL,
            comment TEXT,
            FOREIGN KEY(store_id) REFERENCES store(store_id),
            FOREIGN KEY(user_id) REFERENCES user(user_id),
            FOREIGN KEY(order_id) REFERENCES orderform_history(orderform_id),    
 );
```

