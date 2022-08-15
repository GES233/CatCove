from datetime import datetime, timedelta
from pydantic import BaseModel
from ...models.schemas.response.users import Status
from ...models.tables.users import Users

class UserSecurityPayload(BaseModel):
    id: int
    nickname: str
    status: Status
    exp: float


def user2payload(user: Users, exp_time: float) -> dict:
    dict = UserSecurityPayload(
        id = user.id,
        nickname = user.nickname,
        status = user.status,
        exp = exp_time,
    ).dict()
    """ 'UserMeta': 
        "{
            'id': 1,
            'nickname': '小地瓜123',
            'status': <Status.newbie: 'newbie'>,
            'exp': datetime.datetime(2022, 8, 21, 6, 25, 20, 863794)}"""
    # set dict.status -> str:
    dict["status"] = user.status
    return dict


def payload2user(dict: dict) -> Users:
    raise Exception("戳啦！")
