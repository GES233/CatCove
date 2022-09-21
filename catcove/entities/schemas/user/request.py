from pydantic import BaseModel, validator, ValidationError, EmailStr


class SignUpModel(BaseModel):
    nickname: str
    email: EmailStr
    password: str
    confirm: str
    auto_login: bool = False
    # Alyways false if using API.

    @validator("confirm")
    def passwd_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValidationError("Password not same!")


class UserLoginModel(BaseModel):
    nickname: str
    password: str
    remember: bool
