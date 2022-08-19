from wtforms.form import Form
from wtforms.fields import (
    StringField,
    PasswordField,
    BooleanField,
    )
from wtforms.validators import (
    DataRequired
)

from .....entities.schemas.user.request import UserLoginModel


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
            "checked": "checked"
        }
    )


def validate_login_form(form: LoginForm)-> UserLoginModel | LoginForm:
    if form.validate():
        return UserLoginModel(**form.data)
    else:
        if form.nickname.errors:
            form.nickname.render_kw["aria-invalid"] = "true"
            form.nickname.render_kw["placeholder"] = "请填入昵称"
        elif form.password.errors:
            form.password.render_kw["aria-invalid"] = "true"
            form.password.render_kw["placeholder"] = "请填入密码"
        return form


def user_not_exist(form: LoginForm) -> LoginForm:
    form.nickname.render_kw["aria-invalid"] = "true"
    form.nickname.render_kw["placeholder"] = "用户不存在！"
    return form


def password_not_match(form: LoginForm) -> LoginForm:
    form.password.render_kw["aria-invalid"] = "true"
    form.password.render_kw["placeholder"] = "一眼丁真，鉴定为假"
    return form