from pydantic import BaseModel, validator, ValidationError

class SignUpModel(BaseModel):
    nickname: int | str
    email: str
    password: str
    confirm: str
    auto_login: bool | None = None
    # from App, may not have this item.

    @validator("confirm")
    def passwd_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValidationError("Password not same!")


class UserLoginModel(BaseModel):
    nickname: str | int
    password: str | int
    remember: bool
