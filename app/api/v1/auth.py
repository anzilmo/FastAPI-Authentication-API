from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    VerifyEmailRequest,
    LoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.services.auth_service import AuthService
from app.core.exceptions import AuthException, ValidationException

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user and send email OTP for verification.
    
    - **first_name**: User's first name
    - **last_name**: User's last name
    - **email**: User's email address
    - **password**: User's password (min 8 characters)
    - **confirm_password**: Password confirmation
    - **role**: User role (CUSTOMER, ADMIN, MODERATOR)
    """
    auth_service = AuthService(db)
    return await auth_service.register_user(request)


@router.post("/verify-email", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def verify_email(
    request: VerifyEmailRequest,
    db: Session = Depends(get_db)
):
    """
    Verify user email with OTP.
    
    - **email**: User's email address
    - **otp**: 6-digit OTP sent to email
    """
    auth_service = AuthService(db)
    return await auth_service.verify_email(request)


@router.post("/resend-otp", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
async def resend_otp(
    request: ResendOTPRequest,
    db: Session = Depends(get_db)
):
    """
    Resend OTP to user's email.
    
    - **email**: User's email address
    - **type**: OTP type (EMAIL_VERIFICATION, PASSWORD_RESET)
    """
    auth_service = AuthService(db)
    return await auth_service.resend_otp(request)


@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login user and return access and refresh tokens.
    
    - **email**: User's email address
    - **password**: User's password
    - **device_info**: Optional device information
    """
    auth_service = AuthService(db)
    return await auth_service.login(request)


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
@limiter.limit("3/hour")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Send password reset OTP to user's email.
    
    - **email**: User's email address
    """
    auth_service = AuthService(db)
    return await auth_service.forgot_password(request)


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Reset user password using verified OTP token.
    
    - **password_reset_token**: Token received after OTP verification
    - **new_password**: New password
    - **confirm_password**: Password confirmation
    """
    auth_service = AuthService(db)
    return await auth_service.reset_password(request)