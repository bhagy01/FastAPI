from pydantic import BaseSettings, EmailStr

class Settings(BaseSettings):
    DATABASE_NAME: str
    DATABASE_PASSWORD:str
    DATABASE_USERNAME:str
    DATABASE_PORT:str
    DATABASE_HOSTNAME:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    MAIL_USERNAME:EmailStr
    MAIL_PASSWORD:str
    MAIL_FROM:EmailStr
    MAIL_SERVER:str

    class Config:
        env_file = ".env"

settings=Settings()
