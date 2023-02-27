"""Mail Service module"""
import asyncio

from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail
from pydantic import EmailStr

from app.config import settings


RESET_PASSWORD_TEMPLATE = """<h4>You requested password reset on Netflix.</h4>
                            <p>Please use this verification code in next ten minutes: </p>"""

USER_VERIFICATION_TEMPLATE = """<h4>Welcome to Netflix,</h4><p>One more step is needed for full registration.</p>
                                <p>Please use this code for account verification: </p>"""


class EmailServices:
    """Service for mail operations"""
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
        """
        Function sends a verification code to the user's email address.
        The function takes in an email and a code as parameters, and uses them to create an HTML message
        that contains the code. The function then sends this message via FastMail.

        Param email:EmailStr: Store the email address of the user
        Param code:int: Send the verification code to the user.
        Return: The message that was sent to the user.
        """
        html = f"{USER_VERIFICATION_TEMPLATE}<strong>{code}</strong>"
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
        """
        The send_code_for_password_reset function sends a code to the user's email address.
        The function takes in an email and a code as parameters, and uses them to send the user
        an HTML message containing their password reset code.

        Param email:EmailStr: Specify the email address of the user who is requesting a password reset
        Param code:int: Send the code to the user.
        Return: A future object.
        """
        html = f"{RESET_PASSWORD_TEMPLATE}<strong>{code}</strong>"
        message = MessageSchema(
            subject="Reset Password.",
            recipients=[email],
            body=html,
            subtype=MessageType.html,
        )
        fm = FastMail(EmailServices.conf)
        asyncio.run(fm.send_message(message))
        return
