from datetime import datetime
from passlib.context import CryptContext
import pyotp
import qrcode
TOTP_KEY='ZZXL7ZVUETHFG7NNDDOJAEIBNAW75QJ7'

# print(pyotp.random_base32())
#added TOTP-2FA functpionality
# mytimezone= Time Zone: (UTC+05:30)
# totp_uri='otpauth://totp/FastAPI%20App:bhagiyarajmahesh1%40gmail.com?secret=ZZXL7ZVUETHFG7NNDDOJAEIBNAW75QJ7&issuer=FastAPI%20App'
# otp = pyotp.parse_uri(totp_uri)
# print(otp.now())

totp = pyotp.TOTP(TOTP_KEY)
print(totp.now())
y = TOTP_KEY
with open("otp-sekrit.txt", "a") as f: 
    f.write(y) 

print(f"SAVE THIS : {y}")

x = pyotp.totp.TOTP(y).provisioning_uri(name="FastAPI", issuer_name="FastAPI app") 

img = qrcode.make(x) 
img.save("nerd.png")

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def hash(password:str):
 return pwd_context.hash(password)

def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def verify_totp(otp):
    return totp.verify(otp)