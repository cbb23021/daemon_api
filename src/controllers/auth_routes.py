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
