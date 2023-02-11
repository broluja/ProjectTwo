from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail
from pydantic import EmailStr
import asyncio

from app.config import settings


RESET_PASSWORD_TEMPLATE = '<h4>You requested password reset on Netflix.</h4><p>Please use this code: </p>'

USER_VERIFICATION_TEMPLATE = '''<h4>Welcome to Netflix,</h4><p>One more step is needed for full registration.</p>
                                <p>Please use this code for account verification: </p>'''


class EmailServices:

    conf = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False
    )

    @staticmethod
    def send_code_for_verification(email: EmailStr, code: int):
        html = USER_VERIFICATION_TEMPLATE + f"<strong>{str(code)}</strong>"

        message = MessageSchema(
            subject="Finish your registration on Netflix.",
            recipients=[email],
            body=html,
            subtype=MessageType.html,
        )

        fm = FastMail(EmailServices.conf)
        asyncio.run(fm.send_message(message))
        return

    @staticmethod
    def send_code_for_password_reset(email: EmailStr, code: int):
        html = RESET_PASSWORD_TEMPLATE + f"<strong>{str(code)}</strong>"

        message = MessageSchema(
            subject="Reset Password.",
            recipients=[email],
            body=html,
            subtype=MessageType.html,
        )

        fm = FastMail(EmailServices.conf)
        asyncio.run(fm.send_message(message))
        return
