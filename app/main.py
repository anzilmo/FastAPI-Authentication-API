from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import re

# Create FastAPI app
app = FastAPI(
    title="Authentication API",
    description="Complete Authentication API with FastAPI",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Models
# ============================================

class RegisterRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str
    role: str = "CUSTOMER"
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class VerifyEmailRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)

# ============================================
# Endpoints
# ============================================

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "🔐 Authentication API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs"
    }

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}

@app.post("/api/auth/register", status_code=201, tags=["Auth"])
async def register(request: RegisterRequest):
    """Register new user"""
    return {
        "status": "success",
        "message": "Registration successful. Please check your email for OTP verification.",
        "data": {
            "user_id": f"usr_{int(datetime.utcnow().timestamp())}",
            "email": request.email,
            "account_status": "UNVERIFIED",
            "otp_sent": True,
            "otp_expires_at": datetime.utcnow().isoformat() + "Z"
        }
    }

@app.post("/api/auth/verify-email", tags=["Auth"])
async def verify_email(request: VerifyEmailRequest):
    """Verify email with OTP (demo: use 123456)"""
    if request.otp != "123456":
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "Invalid OTP.", "error_code": "INVALID_OTP"}
        )
    return {
        "status": "success",
        "message": "Email verified successfully.",
        "data": {
            "email": request.email,
            "account_status": "ACTIVE",
            "verified_at": datetime.utcnow().isoformat() + "Z"
        }
    }

@app.post("/api/auth/login", tags=["Auth"])
async def login(request: LoginRequest):
    """Login (demo: test@example.com / Test1234!)"""
    if request.email != "test@example.com" or request.password != "Test1234!":
        raise HTTPException(
            status_code=401,
            detail={"status": "error", "message": "Invalid credentials.", "error_code": "INVALID_CREDENTIALS"}
        )
    return {
        "status": "success",
        "message": "Login successful.",
        "data": {
            "user": {
                "user_id": "usr_demo123",
                "email": request.email,
                "first_name": "Test",
                "last_name": "User",
                "role": "CUSTOMER"
            },
            "tokens": {
                "access_token": "demo_access_token_123",
                "refresh_token": "demo_refresh_token_456",
                "token_type": "Bearer",
                "expires_in": 900
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)