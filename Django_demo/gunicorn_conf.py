# gunicorn/django  服务监听地址、端口 bind本机的gunicorn
bind = '127.0.0.1:8000'

# gunicorn worker 进程个数，建议为： CPU核心个数 * 2 + 1
workers =  3

# gunicorn worker 类型， 使用异步的event类型IO效率比较高
worker_class =  "gevent" #协程模式的

# 日志文件路径
errorlog = "/home/linouhan/gunicorn.log"
loglevel = "info"

import sys,os

cwd = os.getcwd()
sys.path.append(cwd)