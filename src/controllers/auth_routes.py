from app import app
from common.utils.auth_tool import AuthTool
from common.utils.response_handler import ResponseHandler
from common.utils.toolkit import Toolkit
from core.payload_handler import PayloadSchema, PayloadUtils
from core.system_handler import SystemHandler

""" Register: [request register] -> [verify otp] -> [register] """


@app.route('/request/register', methods=['POST'])
@Toolkit.inspect_version()
@PayloadUtils.inspect_schema(PayloadSchema.REQUEST_REGISTER)
def member_request_register(payload):
    """ request register """
    result = SystemHandler.request_register(payload=payload)
    return ResponseHandler.jsonify(result)


@app.route('/verify/email/otp', methods=['POST'])
@Toolkit.inspect_version()
@PayloadUtils.inspect_schema(PayloadSchema.VERIFY_EMAIL_OTP)
def member_verify_email(payload):
    """ verify email """
    result = SystemHandler.verify_email_otp(payload=payload)
    return ResponseHandler.jsonify(result)


@app.route('/register', methods=['POST'])
@Toolkit.inspect_version()
@PayloadUtils.inspect_schema(PayloadSchema.REGISTER)
def member_register(payload):
    result = SystemHandler.register(payload=payload)
    return ResponseHandler.jsonify(result)


""" Authorization """


@app.route('/login/email', methods=['POST'])
@Toolkit.inspect_version()
@PayloadUtils.inspect_schema(PayloadSchema.EMAIL_LOGIN)
def login_by_email(payload):
    """ 會員 使用 email 登入 """
    result = AuthTool.member_login(
        email=payload['email'],
        password=payload['password'],
    )
    return ResponseHandler.jsonify(results=result)


@app.route('/refresh-token', methods=['POST'])
@Toolkit.inspect_version()
@PayloadUtils.inspect_schema(PayloadSchema.REFRESH_TOKEN)
def member_refresh_token(payload):
    """ 更新 Access Token """
    refresh_token = payload['refresh_token']
    result = AuthTool.member_refresh(refresh_token=refresh_token)
    return ResponseHandler.jsonify(results=result)


""" Reset Password: [request reset password] -> [verify otp] -> [reset password] """


@app.route('/request/reset-password', methods=['POST'])
@Toolkit.inspect_version()
@PayloadUtils.inspect_schema(PayloadSchema.REQUEST_RESET_PASSWORD)
def member_request_reset_password(payload):
    """ 請求 重設密碼 (忘記密碼) """
    result = SystemHandler.request_reset_password(payload=payload)
    return ResponseHandler.jsonify(result)


@app.route('/reset-password', methods=['POST'])
@Toolkit.inspect_version()
@PayloadUtils.inspect_schema(PayloadSchema.RESET_PASSWORD)
def member_reset_password(payload):
    result = SystemHandler.reset_password(payload=payload)
    return ResponseHandler.jsonify(result)
