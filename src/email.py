from src.config import RESET_CODE_EXPIRE_SECONDS, redis_client, settings
import secrets
import aiosmtplib
import os
from email.message import EmailMessage


async def send_reset_email(email: str):
    code = secrets.token_hex(3).upper()
    key = f"reset_code:{email}"
    await redis_client.set(key, code, ex=RESET_CODE_EXPIRE_SECONDS)
    message = EmailMessage()
    message['From'] = settings.SMTP_USER
    message['To'] = email
    message['Subject'] = 'Reset password code'
    message.set_content(f'Your reset code: {code}')
    await aiosmtplib.send(
        message, 
        hostname=settings.SMTP_SERVER, 
        port=settings.SMTP_PORT, 
        username=settings.SMTP_USER, 
        password=settings.SMTP_PASSWORD,
        use_tls = True
    )
    
async def send_userinfo_email(email: str, password: str):
    message = EmailMessage()
    message['From'] = settings.SMTP_USER
    message['To'] = email
    message['Subject'] = 'User info for Tasker'
    message.set_content(f"Use your email as login\nYour password is {password}\nLink to Tasker: http://127.0.0.1:8080/docs")
    await aiosmtplib.send(
        message, 
        hostname=settings.SMTP_SERVER, 
        port=settings.SMTP_PORT, 
        username=settings.SMTP_USER, 
        password=settings.SMTP_PASSWORD,
        use_tls = True
    )
    
#fdgddffdf@yandex.ru