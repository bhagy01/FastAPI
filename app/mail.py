from fastapi_mail import FastMail,MessageSchema,ConnectionConfig
from app.schemas import EmailSchema
from .config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD =settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER =settings.MAIL_SERVER,
    MAIL_FROM_NAME="USER REGISTRATION",
    MAIL_TLS = True,
    MAIL_SSL = False,
)


# Html = """ <p>Hi! user registration email</p> """

async def send_confirmation_email(token:str,email:EmailSchema):
    confirmation_url=f'http://localhost:8000/users/verify/{token}'
    message=MessageSchema(

        subject="User Registration",
        recipients=[email],
        body='''Hi! Please confirm your registration: {}'''.format(confirmation_url), 
    )
    fm=FastMail(conf)
    await fm.send_message(message)
    return { "message": "Email sent successfully"}

