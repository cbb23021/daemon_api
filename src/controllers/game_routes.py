from app import app
from common.const import Const
from common.utils.auth_tool import AuthTool
from common.utils.operation_recorder import OperationRecorder
from common.utils.response_handler import ResponseHandler
from common.utils.toolkit import Toolkit
from core.game_handler import LottoHandler
from core.payload_handler import PayloadSchema, PayloadUtils


@app.route('/game', methods=['POST'])
@Toolkit.inspect_version()
@AuthTool.login_required(Const.GroupType.USER)
@Toolkit.request_lock(ex=2)
@PayloadUtils.inspect_schema(PayloadSchema.LOTTO_NUMS)
@OperationRecorder.log()
def join_game(user, payload):
    """ 開始遊戲 """
    result = LottoHandler.join_game(user=user)
    return ResponseHandler.jsonify(result)
