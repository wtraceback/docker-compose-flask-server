from flask import Flask, jsonify
from flask_redis import FlaskRedis
import time
import pymysql


app = Flask(__name__)


# flask-redis 的配置和初始化
# 说明：Redis 服务启动后默认有 16 个数据库，编号分别是从 0 到 15，这边连接的是 0 号数据库
# 这边的 REDIS_URL 中的主机名必须使用 redis，使用 localhost 或者是 127.0.0.1 的话都不能连接上 redis
# REDIS_URL = "redis://用户名:密码@主机:端口/Redis默认的n号数据库" --> 在 Redis 6.0 之前的版本中，登陆Redis Server只需要输入密码（前提配置了密码 requirepass ）即可，不需要输入用户名
app.config['REDIS_URL'] = 'redis://:123456@redis:6379/0'
app.config['JSON_AS_ASCII'] = False
redis_client = FlaskRedis(app)


@app.route('/')
def index():
    return 'Hello World'

@app.route('/redis/set_data/<int:id>')
def set_data(id):
    # 准备相关的数据
    user_id = str(id)
    data = 'dyn_data_{}'.format(user_id)
    data_key = 'dyn_key_{}'.format(user_id)
    # 设置超时时间为 60 秒，当动态数据超过 60 没有更新时，Redis 会自动清除该数据。
    expires = int (time.time()) + 60

    # 写入 redis 中
    # 通过管道 pipeline 来操作 redis，以减少客户端与 redis-server 的交互次数。
    p = redis_client.pipeline()
    p.set(data_key, data)
    p.expireat(data_key, expires)
    p.execute()

    return '设置成功'

@app.route('/redis/get_data/<int:id>')
def get_data(id):
    user_id = str(id)
    data_key = 'dyn_key_{}'.format(user_id)
    data = redis_client.get(data_key)

    print('data = {}'.format(data))

    if data:
        return jsonify(
            {
                'data': data.decode(),
            }
        )
    else:
        return jsonify({})

@app.route('/mysql/info')
def mysql_info():
    # 打开数据库连接；数据库、用户名、密码 要和 .env 配置文件中的配置保持一致
    db = pymysql.connect(host='mysql',
                        port=3306,
                        user='root',
                        password='whxcer123456',
                        database='whxcer_db')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    result = []
    try:
        # 使用 execute() 方法执行 SQL，如果表不存在，则创建一个
        sql = """create table if not exists testtable (
                    id   VARCHAR(20)  NOT NULL,
                    text VARCHAR(20)  NOT NULL,
                    PRIMARY KEY(id) )"""
        cursor.execute(sql)

        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("select * from testtable")
        # 使用 fetchall() 方法获取所有记录列表
        data = cursor.fetchall()

        if data:
            for row in data:
                d = {
                    'id': row[0],
                    'text': row[1],
                }
                result.append(d)

            print("result = {}".format(result))
            return jsonify(result)
        else:
            return jsonify({"msg": "数据库表为空"})
    except:
        print("======数据库查询出错======")

    # 关闭数据库连接
    db.close()
    return jsonify({"msg": "数据库操作报错"})
