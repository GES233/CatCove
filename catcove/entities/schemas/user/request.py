from pydantic import BaseModel, validator, ValidationError

class SignUpModel(BaseModel):
    nickname: str
    email: str
    password: str
    confirm: str
    auto_login: bool = False
    # Alyways false if using API.

    @validator("confirm")
    def passwd_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValidationError("Password not same!")
    
    '''
    # Skip it until a real func.
    @validator("email")
    def email_match(cls, v, values, **kwargs):
        pass'''


class UserLoginModel(BaseModel):
    nickname: str
    password: str
