# 🔐 Authentication API - FastAPI

Complete authentication and authorization API built with FastAPI, PostgreSQL, and Redis.

## Features

✅ User Registration with Email OTP Verification  
✅ Login with JWT (Access & Refresh Tokens)  
✅ Password Reset with OTP  
✅ Two-Factor Authentication (2FA)  
✅ Session Management  
✅ Rate Limiting  
✅ Account Security (Login attempts, account locking)  
✅ Activity Logging  
✅ Password Strength Validation  

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **PostgreSQL** - Primary database
- **Redis** - Caching and rate limiting
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **JWT** - Token-based authentication
- **SMTP** - Email sending

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/authentication-api.git
cd authentication-api
```

### 2. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your configuration
```

### 3. Run with Docker

```bash
docker-compose up -d
```

### 4. Run Migrations

```bash
alembic upgrade head
```

### 5. Start Server

```bash
uvicorn app.main:app --reload
```

API will be available at: `http://localhost:8000`  
API Documentation: `http://localhost:8000/api/docs`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/verify-email` - Verify email with OTP
- `POST /api/auth/resend-otp` - Resend OTP
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh-token` - Refresh access token
- `POST /api/auth/logout` - Logout current session
- `POST /api/auth/logout-all` - Logout all sessions

### Password Management
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/verify-reset-otp` - Verify reset OTP
- `POST /api/auth/reset-password` - Reset password
- `POST /api/auth/change-password` - Change password (authenticated)

### User Profile
- `GET /api/auth/me` - Get current user
- `PUT /api/auth/me` - Update profile
- `DELETE /api/auth/me` - Delete account

### Security
- `GET /api/auth/sessions` - Get active sessions
- `DELETE /api/auth/sessions/:id` - Revoke session
- `GET /api/auth/activity-log` - Get login history

## Environment Variables

See `.env.example` for all configuration options.

## Testing

```bash
pytest
```

## License

MIT License