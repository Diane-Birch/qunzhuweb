from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.app.core.config import get_settings


# Use pbkdf2_sha256 as the default hashing scheme to avoid bcrypt backend
# compatibility issues in Python 3.8 environments. Keep bcrypt for reading
# existing hashes if older seeded data already used it.
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],
    deprecated="auto",
)
settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against the stored password hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a secure password hash for the admin account."""
    return pwd_context.hash(password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT that the admin frontend can store and reuse."""
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload: Dict[str, Any] = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> Optional[str]:
    """Decode the JWT and return the login subject if the token is still valid."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError:
        return None
    return payload.get("sub")