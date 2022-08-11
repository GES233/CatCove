from wtforms.form import Form
from wtforms.fields import (
    StringField,
    PasswordField,
    BooleanField,
    )
from wtforms.validators import (
    DataRequired
)

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
            nickname=form.nickname.data,
            password=form.password.data,
            remember=form.remember.data
        )
    else:
        return form


def form_input(form: LoginForm) -> LoginForm:
    form.nickname.render_kw["aria-invalid"] = "true"
    form.nickname.render_kw["placeholder"] = "请填入昵称"
    form.password.render_kw["aria-invalid"] = "true"
    form.password.render_kw["placeholder"] = "请填入密码"
    return form


def user_not_exist_front(form: LoginForm) -> LoginForm:
    form.nickname.render_kw["aria-invalid"] = "true"
    form.nickname.render_kw["placeholder"] = "用户不存在！"
    return form


def password_not_match_front(form: LoginForm) -> LoginForm:
    form.password.render_kw["aria-invalid"] = "true"
    form.password.render_kw["placeholder"] = "一眼丁真，鉴定为假"
    return form
