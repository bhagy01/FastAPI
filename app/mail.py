from fastapi_mail import FastMail,MessageSchema,ConnectionConfig
from app.schemas import EmailSchema

conf = ConnectionConfig(
    MAIL_USERNAME="bhagiyarajmahesh@gmail.com",
    MAIL_PASSWORD ="qsbkSjMPCzth52Y3",
    MAIL_FROM="bhagiyarajmahesh@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER = "smtp-relay.sendinblue.com",
    MAIL_FROM_NAME="Tesing",
    MAIL_TLS = True,
    MAIL_SSL = False,
)

Html = """ <p>Hi! user registration email</p> """


async def send_confirmation_email(email:EmailSchema):
    message=MessageSchema(

        subject="User Registration",
        recipients=[email],
        body=Html,
        subtype="html"
        
    )
    fm=FastMail(conf)
    await fm.send_message(message)
    return { "message": "Email sent successfully"}