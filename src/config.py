import os


class Config:
    # --- Config --- #
    APP_NAME = os.environ['APP_NAME']
    SYSTEM_NAME = os.environ['SYSTEM_NAME']
    SYSTEM_VERSION = os.environ['SYSTEM_VERSION']
    ENVIRONMENT = os.environ['ENVIRONMENT']
    CONSTRAIN_VERSION = os.environ['CONSTRAIN_VERSION']

    # --- Salt --- #
    SALT = os.environ['SALT']
    SECRET_KEY = os.environ['SECRET_KEY']

    # --- Host --- #
    FRONTEND_HOST = os.environ['FRONTEND_HOST']  # 驗證信轉址用
    STATIC_HOST = os.environ['STATIC_HOST']
    API_HOST = os.environ['API_HOST']  # CALLBACK URL使用

    # --- Database --- #
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['MYSQL_USER']
    DB_PWD = os.environ['MYSQL_PASSWORD']
    DB_HOST = os.environ['MYSQL_HOST']
    DB_PORT = os.environ['MYSQL_PORT']

    SQLALCHEMY_BINDS = {
        DB_NAME:
        f'mysql+pymysql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Redis --- #
    REDIS_HOST = os.environ['REDIS_HOST']
    REDIS_PORT = os.environ['REDIS_PORT']
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)

    # --- K8S --- #
    K8S_PROBE_TOKEN = os.environ.get('K8S_PROBE_TOKEN', None)
    PROBE_OPEN = os.environ.get('PROBE_OPEN', None)

    # --- Expire Time --- #
    ACCESS_TOKEN_EXPIRE_TIME = 60 * 15
    REFRESH_TOKEN_EXPIRE_TIME = 60 * 60 * 24 * 7

    # --- upload --- #
    UPLOAD_FOLDER = 'static'

    #########################
    # === 3rd Party API === #
    #########################
    # --- email --- #
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_MAX_EMAILS = 10  # 有些郵件伺服器會限制一次連接中的發送郵件的上限。 你可以設置重連前的發送郵件的最大數
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    VERIFY_EMAIL_PATTERN = f'{FRONTEND_HOST}/email-verification-result/{{token}}'
