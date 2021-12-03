from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.controllers.core.utils.mail.change_password_mail import format_html_mail_forgot_pass
from app.controllers.core.utils.mail.register_mail import format_html_mail_register


conf = ConnectionConfig(
    MAIL_USERNAME='abf05d464aef95',
    MAIL_PASSWORD='a51fe129402031',
    MAIL_FROM="your@email.com",
    MAIL_PORT=2525,
    MAIL_SERVER='smtp.mailtrap.io',
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def change_password_mail(record_staff, password):
    message = MessageSchema(
        subject="Change Password",
        recipients=[record_staff.email],
        body=format_html_mail_forgot_pass(record_staff.email, password),
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_password_mail(record_staff, password):
    email = record_staff.email
    message = MessageSchema(
        subject="Change Password",
        recipients=[email],
        body=format_html_mail_register(record_staff.email, password),
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
