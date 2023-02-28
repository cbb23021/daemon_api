from common.const import Const
from common.error_handler import ErrorCode, ValidationError
from common.utils.auth_tool import AuthTool
from common.utils.encrypt_tool import Encrypt
from common.utils.operation_recorder import OperationRecorder
from common.utils.response_handler import ResponseHandler
from flask import request

from app import app


@app.route('/dev/info', methods=['GET', 'POST', 'PUT', 'DELETE'])
# @AuthTool.blacklist_inspect(update_address=True)
@AuthTool.whitelist_inspect(update_address=True)
def dev_info():
    result = {
        'method': request.method,
        'user_agent': {
            'user-agent': request.user_agent.string,
            'platform': request.user_agent.platform,
            'browser': request.user_agent.browser,
            'language': request.user_agent.language,
            'version': request.user_agent.version,
        },
        'host': request.environ['HTTP_HOST'],
        'accept': request.environ['HTTP_ACCEPT'],
        'real_ip': request.environ.get('HTTP_X_REAL_IP'),
        'remote_addr': request.remote_addr,
        'url': request.url,
        'args': dict(request.args),
        'payload': request.get_json(),
    }
    return ResponseHandler.jsonify(result)


@app.route('/dev/encrypt', methods=['GET'])
@AuthTool.login_required(Const.GroupType.ADMIN, update_address=True)
@OperationRecorder.log(debug=True)
def dev_encrypt(user):
    key = request.args.get('key')
    result = {
        'key': key,
        'encrypt': Encrypt.encrypt_password(key) if key else None,
    }
    return ResponseHandler.jsonify(result)


@app.route('/dev/error', methods=['GET'])
def dev_error():
    return ErrorCode.to_dict()


@app.route('/dev/hi', methods=['GET'])
def dev_hi():
    print('hello world')
    return ResponseHandler.jsonify(True)
