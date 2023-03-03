import json
from datetime import datetime, timedelta

from flask import request

from app import app
from common.const import Const
from common.error_handler import ErrorCode, ValidationError
from common.models import LottoDraw
from common.utils.auth_tool import AuthTool
from common.utils.data_cache import DataCache
from common.utils.encrypt_tool import Encrypt
from common.utils.operation_recorder import OperationRecorder
from common.utils.orm_tool import ORMTool
from common.utils.response_handler import ResponseHandler
from core.game_handler import LottoHandler
from core.payload_handler import PayloadSchema, PayloadUtils


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


@app.route('/dev/test', methods=['GET'])
def test():
    from sqlalchemy.orm.attributes import flag_modified

    from common.models import Member, Ticket
    from common.utils.orm_tool import ORMTool
    user = Member.query.filter(Member.id == 3).first()
    print(user.email)
    user.ticket.amount['game'] += 10
    flag_modified(user.ticket, 'amount')
    ORMTool.flush()

    t = Ticket.query.filter(Ticket.member_id == 3).first()
    print(t.amount)
    ORMTool.commit()
    print(t.amount)

    return ResponseHandler.jsonify(True)


@app.route('/dev/draw', methods=['POST'])
@PayloadUtils.inspect_schema(schema=PayloadSchema.DRAW)
def create_draw(payload):
    data = {
        'name': payload['name'],
        'period': payload['period'],
        'number': {
            'numbers': LottoHandler.get_numbers(),
        },
        'open_dt': datetime.strptime(payload['open_dt'], "%Y%m%d"),
        'status': Const.DrawStatus.ACTIVATED,
        'fee': payload['fee'],
        'size': payload['size'],
    }
    draw = ORMTool.insert(model=LottoDraw, **data)
    DataCache.push_active_draw_ids(draw_ids=[draw.id])
    result = {
        'id': draw.id,
        'name': draw.name,
        'period': draw.period,
        'open_dt': draw.open_dt,
        'status': draw.status,
        'fee': draw.fee,
        'size': draw.size,
    }
    return ResponseHandler.jsonify(result)
