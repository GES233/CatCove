from datetime import datetime, timedelta
from pydantic import BaseModel
from ...entities.tables.users import Users
from ...entities.schemas.auth import UserTokenPayload


def user2payload(user: Users, exp_time: float) -> dict:
    dict = UserTokenPayload(
        id=user.id,
        nickname=user.nickname,
        status=user.status,
        role="spectator" if user.is_spectator == True else "normal",
        exp=exp_time,
    ).dict()
    """ 'UserMeta': 
        "{
            'id': 1,
            'nickname': '小地瓜123',
            'status': <Status.newbie: 'newbie'>,
            'exp': timestamp}"""
    # set dict.status -> str:
    # dict["status"] = user.status
    return dict


def payload2user(dict: dict) -> Users:
    raise Exception("戳啦！")
