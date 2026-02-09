from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

from app.models.user import UserRole, AccountStatus


# Registration
class RegisterRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str
    role: UserRole = UserRole.CUSTOMER
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


class RegisterResponse(BaseModel):
    status: str = "success"
    message: str
    data: dict


# Email Verification
class VerifyEmailRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)


class VerifyEmailResponse(BaseModel):
    status: str = "success"
    message: str
    data: dict


# Resend OTP
class ResendOTPRequest(BaseModel):
    email: EmailStr
    type: str = "EMAIL_VERIFICATION"


# Login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    device_info: Optional[dict] = None


class LoginResponse(BaseModel):
    status: str = "success"
    message: str
    data: dict


# Refresh Token
class RefreshTokenRequest(BaseModel):
    refresh_token: str


# Forgot Password
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


# Verify Reset OTP
class VerifyResetOTPRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)
    reset_token: str


# Reset Password
class ResetPasswordRequest(BaseModel):
    password_reset_token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


# Change Password
class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v