from functools import wraps

from flask import request
from schema import Optional, Regex, Schema


class PayloadUtils:

    @staticmethod
    def inspect_schema(schema):

        def real_decorator(method, **kwargs):

            @wraps(method)
            def wrapper(*args, **kwargs):
                payload = request.get_json(force=True)
                schema.validate(payload)
                return method(*args, **kwargs, payload=payload)

            return wrapper

        return real_decorator


class PayloadSchema:
    """

    password: 大小寫英文數字(底線、減號、井號) 8-30
    ifsc: 4字英文大小寫 + 7字英文大小寫數字
    """

    _PASSWORD_PATTERN = r'^[\w\d\-_#]{8,30}$'
    _EMAIL_PATTERN = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    _PHONE_PATTERN = r'^\+[\d]+$'
    # YYYY-MM-DD
    _DATE = '^(((?:19|20)[0-9]{2})[-](0?[1-9]|1[012])[-](0?[1-9]|[12][0-9]|3[01]))*$'
    _IFSC = '^[A-Za-z]{4}[a-zA-Z0-9]{7}$'
    _REFERRAL_CODE = '^[A-Z0-9]{6}$'
    _OTP_CODE = '^[0-9]{5}$'
    _NICKNAME_PATTERN = r'^[a-zA-Z0-9\-\_]{1,30}$'
    _TIMESTAMP_PATTERN = r'^[\d]{1,10}$'  # 0 - 1645511720
    """ AUTH """

    EMAIL_LOGIN = Schema({
        'email': Regex(_EMAIL_PATTERN),
        'password': Regex(_PASSWORD_PATTERN),
    })

    REFRESH_TOKEN = Schema({'refresh_token': str})
    """ REGISTER """

    REQUEST_REGISTER = Schema({'email': Regex(_EMAIL_PATTERN)})

    VERIFY_EMAIL_OTP = Schema({
        'email': Regex(_EMAIL_PATTERN),
        'otp': Regex(_OTP_CODE)
    })

    REGISTER = Schema({
        'email': Regex(_EMAIL_PATTERN),
        'password': Regex(_PASSWORD_PATTERN),
        'otp': Regex(_OTP_CODE),
    })
    """ FORGOT PASSWORD (email) """

    REQUEST_RESET_PASSWORD = Schema({
        'email': Regex(_EMAIL_PATTERN),
    })

    RESET_PASSWORD = Schema({
        'email': Regex(_EMAIL_PATTERN),
        'password': Regex(_PASSWORD_PATTERN),
        'otp': Regex(_OTP_CODE),
    })
    """ MEMBER """

    UPDATE_PASSWORD = Schema({
        'password': Regex(_PASSWORD_PATTERN),
        'new_password': Regex(_PASSWORD_PATTERN),
    })

    UPDATE_INFO = Schema({
        Optional('nickname'): Regex(_NICKNAME_PATTERN),
    })

    LOGIN_GAME = Schema({
        'provider_id': int,
    })
    """  FOLLOW  """

    FOLLOW_MEMBER = Schema({
        'member_id': int,
    })

    UNFOLLOW_MEMBER = Schema({
        'member_id': int,
    })
    """ REQUEST PAYMENT ORDER """

    REQUEST_DEPOSIT = Schema({
        'amount': int,
        'channel_id':
        int,  # TODO: need remove after paytm merge + frontend modify
    })

    REQUEST_WITHDRAW = Schema({
        'amount': int,
    })
    """ DAILY BONUS """
    GET_DAILY_BONUS = Schema({})
    """ BIRTHDAY PRIZE """
    GET_BIRTHDAY_PRIZE = Schema({})
    """ ACTIVE STATS """
    ACTIVE_STATS = Schema({
        'device_id': str,
        'referral_code': str,
    })

    LOTTO_NUMS = Schema({
        'a': int,
        'b': int,
        'c': int,
        'd': int,
        'e': int,
        'f': int,
        'g': int,
    })
