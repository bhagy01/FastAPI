from fastapi_mail import FastMail,MessageSchema,ConnectionConfig
from app.schemas import EmailSchema

conf = ConnectionConfig(
    MAIL_USERNAME="bhag3747@plintron.com",
    MAIL_PASSWORD ="Ptpl@123",
    MAIL_FROM="bhagiyaraj.gp@plintron.com",
    MAIL_PORT=587,
    MAIL_SERVER = "smtp.office365.com",
    MAIL_FROM_NAME="Tesing",
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

