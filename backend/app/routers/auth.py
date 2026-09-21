from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.models.models import User
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Autenticação"])
bearer = HTTPBearer()
ALGORITHM = "HS256"

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not user.active or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos.")
    token = create_access_token(str(user.id))
    return {"access_token": token, "user": user}

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada.")

    user = db.get(User, user_id)
    if not user or not user.active:
        raise HTTPException(status_code=401, detail="Usuário não encontrado ou inativo.")
    return user

@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return user
