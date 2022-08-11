from wtforms.form import Form
from wtforms.fields import (
    StringField,
    PasswordField,
    BooleanField
    )
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo
)

class SignUpForm(Form):
    nickname = StringField(
        "nickname",
        validators=[
            DataRequired()
        ],
        render_kw={
            "placeholder": "昵称",
            "aria-label": "昵称",
            "autocomplete": "username"
        }
    )
    email = StringField(
        "email",
        validators=[
            DataRequired(),
            Email()
        ],
        render_kw={
            "placeholder": "邮件地址",
            "aria-label": "邮件地址",
            "autocomplete": "email"
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
        }
    )
    confirm = PasswordField(
        "confirm",
        validators=[
            DataRequired(),
            EqualTo("password")
        ],
        render_kw={
            "placeholder": "确认密码",
            "aria-label": "确认密码",
        }
    )
    auto_login = BooleanField(
        render_kw={
            "role": "switch",
            "value": "n"
        }
    )

form = SignUpForm()

print(form.auto_login)