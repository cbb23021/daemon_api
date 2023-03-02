from app import config
from common.const import Const
from common.error_handler import ErrorCode, ValidationError
from common.models import Cash, Member, Ticket
from common.text.text_handler import TextHandler
from common.utils.data_cache import DataCache
from common.utils.encrypt_tool import Encrypt, KeyGenerator
from common.utils.orm_tool import ORMTool
from common.utils.task_tool import TaskTool
from core.twofactor_handler import TwoFactorHandler


class SystemHandler:
    _STATIC_HOST = config['STATIC_HOST']
    _DOWNLOAD_URL_PATTERN = f'{_STATIC_HOST}/download/{{filename}}'

    _REQUEST_TIMEOUT = 10

    _MEMBER_USERNAME_NUMBER_LENGTH = 7
    _MEMBER_USERNAME_PREFIX = 'M'

    @classmethod
    def request_register(cls, payload):
        """ 請求OTP 申請註冊 '必須不存在' """
        email = payload['email']
        user = Member.query.filter_by(email=email).first()
        if user:
            raise ValidationError(error_code=ErrorCode.EMAIL_IS_EXIST)
        TwoFactorHandler.send_email_verification(
            email=email, task=TextHandler._TASK_REGESTER)
        return True

    @classmethod
    def verify_email_otp(cls, payload):
        """
        payload = {
            'email': Regex(_EMAIL_PATTERN),
            'otp': Regex(_OTP_CODE)
        }
        """
        email = payload['email']
        otp = payload['otp']
        TwoFactorHandler.verify_email(email=email, otp=otp)
        return True

    @classmethod
    def _generate_username(cls):
        length = cls._MEMBER_USERNAME_NUMBER_LENGTH
        while True:
            username_number = KeyGenerator.get_random_code(
                number=length,
                has_digit=True,
                has_lower=False,
                has_upper=False,
                has_punctuation=False)
            username = f'{cls._MEMBER_USERNAME_PREFIX}{username_number}'
            if ORMTool.is_unique(model=Member, username=username):
                return username

    @classmethod
    def register(cls, payload):
        """
        payload = {
            'email': Regex(_EMAIL_PATTERN),
            'password': Regex(_PASSWORD_PATTERN),
            'otp': otp,
        }
        """
        email = payload['email']
        password = payload['password']
        otp = payload['otp']

        if Member.query.filter_by(email=email).first():
            raise ValidationError(error_code=ErrorCode.EMAIL_IS_EXIST)
        TwoFactorHandler.verify_verified_email(email=email, otp=otp)
        password = Encrypt.encrypt_password(password)
        username = cls._generate_username()
        data = {
            'username': username,
            'nickname': username,
            'password': password,
            'email': email,
            'role': Const.RoleType.MEMBER,
            'latest_login_info': {
                'login_address': None,
                'login_datetime': None,
                'platform': None,
                'browser': None,
                'is_app': None,
            },
        }
        # ---------- 增加新用戶 ---------- #
        new_user = ORMTool.insert(model=Member, is_flush=True, **data)
        new_user_cash = ORMTool.insert(model=Cash,
                                       is_flush=True,
                                       member_id=new_user.id)
        init_ticket = {'game': 0}
        new_user_ticket = ORMTool.insert(model=Ticket,
                                         is_flush=True,
                                         member_id=new_user.id,
                                         amount=init_ticket)
        # issue rewards for register
        TaskTool.issue_task_reward(user=new_user,
                                   type_=Const.Task.Type.REGISTER)
        ORMTool.commit()
        DataCache.del_verified_email(email=email)
        return True

    @classmethod
    def request_reset_password(cls, payload):
        """ 請求OTP 重置密碼 '必須存在' """
        email = payload['email']
        user = Member.query.filter_by(email=email).first()
        if not user:
            raise ValidationError(error_code=ErrorCode.EMAIL_IS_EXIST)
        TwoFactorHandler.send_email_verification(
            email=email, task=TextHandler._TASK_RESET_PASSWORD)
        return True

    @classmethod
    def reset_password(cls, payload):
        email = payload['email']
        otp = payload['otp']
        user = Member.query.filter_by(email=email).first()
        if not user:
            raise ValidationError(error_code=ErrorCode.USER_NOT_FOUND)
        TwoFactorHandler.verify_forgot_password(email=email, otp=otp)
        user.password = Encrypt.encrypt_password(password=payload['password'])
        ORMTool.commit()
        DataCache.del_verify_email_otp(email=email)
        return True
