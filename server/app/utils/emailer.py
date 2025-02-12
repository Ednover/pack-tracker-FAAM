from typing import List, Text
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr

from app.config import settings

class EmailSchema(BaseModel):
    email: List[EmailStr]
    subject: str
    body: Text

conf = ConnectionConfig(
    MAIL_USERNAME =settings.mail_username,
    MAIL_PASSWORD = settings.mail_password,
    MAIL_FROM = settings.mail_username,
    MAIL_PORT = settings.mail_port,
    MAIL_SERVER = settings.mail_server,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True
)

async def send_mail(email: EmailSchema):
    message = MessageSchema(
        subject=email.subject,
        recipients=email.email,
        body=email.body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "email has been sent"}