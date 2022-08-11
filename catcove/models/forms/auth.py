from wtforms.form import Form
from wtforms.fields import (
    StringField,
    PasswordField,
    BooleanField,
    )
from wtforms.validators import (
    DataRequired
)
from pydantic import ValidationError

from ..schemas.request import UserLoginModel

class LoginForm(Form):
    nickname = StringField(
        "nickname",
        validators=[
            DataRequired()
        ],
        render_kw={
            "placeholder": "昵称或邮件地址",
            "aria-label": "昵称或邮件地址",
            "autocomplete": "username"
        }
    )
    password = PasswordField(
        "password",
        validators=[
            DataRequired()
        ],
        render_kw={
            "placeholder": "密码",
            "aria-label": "密码",
            "autocomplete": "current-password"
        }
    )
    remember = BooleanField(
        render_kw={
            "role": "switch",
            "value": "n"
        }
    )

raw_form = LoginForm()


def validate_login_form(form: LoginForm)-> UserLoginModel | LoginForm:
    if form.validate():
        return UserLoginModel(
            nickname=form.data["nickname"][0],
            password=form.data["password"][0],
            remember=form.data["remember"]
        )
    else: return LoginForm()


def form_render() -> LoginForm:
    ...
    # Catch Error(s).

    # Create a raw-form Replace holderplace.
    if ...:
        raw_form.nickname.render_kw["aria-invalid"] = "true"
        raw_form.nickname.render_kw["placeholder"] = "用户不存在！"
    elif ...:
        raw_form.password.render_kw["aria-invalid"] = "true"
        raw_form.password.render_kw["placeholder"] = "一眼丁真，鉴定为假"
    ...

