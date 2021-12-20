# CDMS_PJ2_10195501437

## 部署方法

#### 安装依赖项
```shell
pip install -r requirements.txt
```
#### 安装模块
```shell
python3 setup.py install
```
#### 设置环境变量
```shell
export FLASK_APP=be (shell)
set FLASK_APP=be (cmd)
```
#### 配置mysql数据库连接方式
be/dao/db_conn.py
```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "passwd": "root",
    "db": "bookstore",
    "charset": "utf8"
}
```
#### 运行flask服务器
```shell
flask run
```
## 项目布局
```
├─be                后端实现
│  ├─dao            
│  ├─service        
│  ├─view           
├─doc               设计文档
│  ├─database
│  ├─service
│  └─view
├─fe                测试用例
│  ├─access
│  ├─bench
│  ├─data
│  ├─extended_test  附加功能测试
│  ├─test           基本功能测试
|  └─testTps        吞吐率测试
├─script            代码覆盖率测试脚本
├─README.md
├─setup.py
└─requirements.txt
```
## 其他方法

#### 测试覆盖率
```shell
script/test.sh
```

#### 测试吞吐量
```shell
flask run & (或用其他方法部署)
python3 fe/tps/testTps.py
```
使用gunicorn多线程部署
```shell
gunicorn -w 3 -b 0.0.0.0:5000 be:app
```

#### 数据库初始化
```shell
flask init-db
```