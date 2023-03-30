# 指定下载 python 版本，说明该镜像以哪个镜像为基础
FROM python:3.8.5

# 构建者的基本信息
MAINTAINER whxcer

# 创建 server 文件夹
RUN mkdir -p /var/www/html/server

# 将 server 文件夹作为工作目录，并且进入 server 目录
WORKDIR /var/www/html/server

# 将 linux 系统当前目录下的内容拷贝到容器的 /var/www/html/server 目录下
ADD . /var/www/html/server

# 在容器内部执行的命令，利用 pip 安装依赖
# RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple/
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/

# 使用 Gunicorn 服务器启动 Flask 应用
CMD ["gunicorn", "-c", "gunicorn_config.py", "wsgi:application"]
