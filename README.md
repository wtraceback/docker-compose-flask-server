# docker-compose-flask-server

使用 docker-compose 完整的运行一个 Flask 应用（ nginx + gunicorn + flask + mysql + redis ）


## 项目运行
```bash
# 1. 拉取 nginx、mysql、redis 镜像
docker pull nginx
docker pull mysql
docker pull redis

# 2. 克隆项目到服务器中
$ git clone https://github.com/wtraceback/docker-compose-flask-server.git

# 3. 切换至目录中
$ cd docker-compose-flask-server

# 4. 运行 docker-compose
docker-compose up -d

# 5. 查看运行的状态
docker-compose ps
```

## 测试
在浏览器中输入 ```http://服务器的ip:80``` 即可访问刚刚启动的 flask 应用
