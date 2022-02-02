from datetime import datetime
from passlib.context import CryptContext
import pyotp
# print(pyotp.random_base32())
#added TOTP-2FA functionality
# mytimezone= Time Zone: (UTC+05:30)
TOTP_KEY='ZZXL7ZVUETHFG7NNDDOJAEIBNAW75QJ7'
# totp_uri='otpauth://totp/FastAPI%20App:bhagiyarajmahesh1%40gmail.com?secret=ZZXL7ZVUETHFG7NNDDOJAEIBNAW75QJ7&issuer=FastAPI%20App'
# otp = pyotp.parse_uri(totp_uri)
# print(otp.now())
totp = pyotp.TOTP(TOTP_KEY)
print(totp.now())
URI=pyotp.totp.TOTP(TOTP_KEY).provisioning_uri(
name='bhagiyarajmahesh1@gmail.com', issuer_name='FastAPI App')
# print(URI)


pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def hash(password:str):
 return pwd_context.hash(password)

def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def verify(otp):
    return totp.verify(otp)