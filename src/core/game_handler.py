import json
from datetime import datetime

from sqlalchemy.orm.attributes import flag_modified

from common.error_handler import ErrorCode, ValidationError
from common.models import LottoDraw
from common.utils.data_cache import DataCache
from common.utils.orm_tool import ORMTool


class LottoHandler:

    @classmethod
    def _get_spare_order_id(cls, draw):
        """ 檢查 是否還有空缺 """
        order_id = DataCache.get_spare_order_id(draw_id=draw.id)
        if not order_id:
            message = f'Draw: {draw.id} Reached Limitation {draw.size}'
            raise ValidationError(error_code=ErrorCode.INVALID_OPERATION,
                                  message=message)
        return order_id

    @classmethod
    def join_game(cls, user, payload):
        """
        zone
        (1, 2, 3, 4, 5, 6, 7)
        (a, b, c, d, e, f, g)

        each 0-30

        """
        is_ticket = payload['is_ticket']
        draw = {
            'a': payload['a'],
            'b': payload['b'],
            'c': payload['c'],
            'd': payload['d'],
            'e': payload['e'],
            'f': payload['f'],
            'g': payload['g'],
        }
        draw_set = {v for _, v in draw.items()}
        if len(draw_set) < 7:
            raise ValidationError(error_code=ErrorCode.INVALID_OPERATION,
                                  message='Number Can Not Duliplate')
        for _ in draw_set:
            if _ > 30:
                raise ValidationError(error_code=ErrorCode.INVALID_OPERATION,
                                      message=f'<Number:{_}> Over then 30')
        # get latest draw
        draw = LottoDraw.query.filter_by(
            LottoDraw.is_archive.is_(False)).order_by(
                LottoDraw.id.desc()).first()
        if not draw:
            raise ValidationError(error_code=ErrorCode.INVALID_OPERATION,
                                  message='Did Not release New Lotto Draw')

        # get fee
        ticket = user.ticket.amount['game']
        if is_ticket and ticket <= 0:
            raise ValidationError(error_code=ErrorCode.AMOUNT_INSUFFICIENT,
                                  message='Ticket Is Not Enough')
        fee = draw.fee

        # charge fee
        charge_fee = {
            'cash': 0,
            'ticket': 0,
        }
        remark = None
        if is_ticket:
            remark = f'save {fee} for 1 ticket.'
            charge_fee.update({'ticket': 1})
            user.ticket.amount['game'] -= 1
            flag_modified(user.ticket, 'amount')
            ORMTool.flush()

        else:
            charge_fee.update({'cash': fee})
            user.cash.amount -= fee
            ORMTool.flush()

        # create order
        order_id = cls._get_spare_order_id(draw=draw)
        DataCache.push_order_data_to_used(
            draw_id=draw.id,
            order_id=order_id,
            member_id=user.id,
            cash=charge_fee['cash'],
            ticket=charge_fee['ticket'],
            number=json.dumps(draw_set),
            join_dt=datetime.now().strftime("%Y-%m-%dT%H-%M-%S"),
            remark=remark,
        )

        ORMTool.commit()
        return
