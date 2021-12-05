from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi_mail import FastMail,MessageSchema,ConnectionConfig
from starlette import status
from app.schemas import EmailSchema
from .database import  engine
from . import models
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)
conf = ConnectionConfig(
    MAIL_USERNAME="BhagiyarajMahesh",
    MAIL_PASSWORD ="Bhagy@1398",
    MAIL_FROM="bhagiyarajmahesh@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Ding DOng2",
    MAIL_TLS = True,
    MAIL_SSL = False,
)

Html = """ <p>Hi this test mail, Please oombu</p> """



app = FastAPI()

origins= ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)  
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message" : "Vanthutan Bunda aatitu"}

@app.post("/mail",status_code=status.HTTP_201_CREATED)
async def send_email(email:EmailSchema):
    message=MessageSchema(
        subject="I am the king of the world",
        recipients=email.dict().get("email"),
        body=Html,
        subtype="html"
    )
    fm=FastMail(conf)
    await fm.send_message(message)
    return { "message": "Email sent successfully"}
