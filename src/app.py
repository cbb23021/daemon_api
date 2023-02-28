import redis
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
from flask_mail import Mail
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config.from_object('config.Config')
config = app.config

CORS(app, send_wildcard=True)  # 允許跨域請求
Compress(app)  # 壓縮

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
mail = Mail(app)

rs = redis.StrictRedis(
    host=config['REDIS_HOST'],
    password=config['REDIS_PASSWORD'],
    port=config['REDIS_PORT'],
    charset='utf-8',
    decode_responses=True,
)
rs_f_decode = redis.StrictRedis(
    host=config['REDIS_HOST'],
    password=config['REDIS_PASSWORD'],
    port=config['REDIS_PORT'],
    charset='utf-8',
    decode_responses=False,
)

""" 匯入 控制器 與 錯誤模板 """
from views import register_views
register_views()


def create_app():
    return app
