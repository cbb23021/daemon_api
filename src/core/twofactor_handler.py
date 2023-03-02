import threading

from common.const import Const
from common.error_handler import ErrorCode, ValidationError
from common.text.text_handler import TextHandler
from common.utils.data_cache import DataCache
from common.utils.email_handler import EmailHandler
from common.utils.toolkit import Toolkit


class TwoFactorHandler:

    @classmethod
    def send_email_verification(cls, email, task):
        """
        阻擋短時間多次嘗試
        發送驗證信
        """
        attempt = DataCache.get_verify_email_attempt(email=email)
        if attempt and (attempt >=
                        Const.VerificationSystem.EMAIL_OTP_ATTEMPT_MAXIMUM):
            seconds = Const.VerificationSystem.EMAIL_OTP_RETRY_INTERVAL
            unit = 'minutes'
            interval = Toolkit.convert_seconds(seconds=seconds, unit=unit)
            message = f'Please try after {interval} {unit}'
            raise ValidationError(
                error_code=ErrorCode.REACHED_MAXIMUM_RETRY_ATTEMPTS,
                message=message)
            raise ValidationError(
                error_code=ErrorCode.REACHED_MAXIMUM_RETRY_ATTEMPTS)
        DataCache.increase_verify_email_attempt(email=email)

        thread = threading.Thread(
            target=EmailHandler.send_verification,
            args=(email, task),
        )
        thread.start()
        return True

    @staticmethod
    def _vaildate(email):
        attempts = DataCache.get_verify_email_attempt(email=email)
        if not attempts:
            raise ValidationError(error_code=ErrorCode.EMAIL_NOT_VERIFIED,
                                  message='email is incorrect')

    @classmethod
    def verify_email(cls, email, otp):
        """
        - 檢查token內容是否與信箱一致 並驗證
        """
        cls._vaildate(email=email)
        EmailHandler.verify_email(email=email, otp=otp)
        DataCache.set_verified_email(email=email, otp=otp)
        DataCache.del_verify_email_otp(email=email)
        return True

    @classmethod
    def verify_verified_email(cls, email, otp):
        """
        - 檢查token 驗證的信箱一致 等註冊
        """
        cls._vaildate(email=email)
        EmailHandler.verify_verified_email(email=email, otp=otp)
        return True

    @classmethod
    def verify_forgot_password(cls, email, otp):
        """
        - 檢查token 內容是否與信箱一致 並驗證
        """
        cls._vaildate(email=email)
        EmailHandler.verify_email(email=email, otp=otp)
        return True
