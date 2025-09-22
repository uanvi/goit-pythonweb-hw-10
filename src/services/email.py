from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from src.core.config import settings

# Конфігурація email
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_verification_email(email: str, user_id: int):
    """Відправити лист для верифікації email"""
    
    # HTML шаблон листа
    html = f"""
    <h2>Verify your email address</h2>
    <p>Hello! Please verify your email address by clicking the link below:</p>
    <p>
        <a href="http://localhost:8000/auth/verify/{user_id}">
            Verify Email
        </a>
    </p>
    <p>If you didn't create an account, please ignore this email.</p>
    """
    
    message = MessageSchema(
        subject="Email Verification - Contacts API",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)