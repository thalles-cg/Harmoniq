from collections.abc import Generator
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.service import token as token_service

def get_db() -> Generator[Session, None, None]:
  db = SessionLocal()

  try:
    yield db
  finally:
    db.close()

security = HTTPBearer()

def obter_usuario_id(credenciais: HTTPAuthorizationCredentials = Depends(security)) -> int:
  token = credenciais.credentials

  try:
    payload = jwt.decode(
      token,
      token_service.JWT_SECRET_KEY,
      algorithms=[token_service.JWT_ALGORITHM],
    )

    usuario_id = payload.get("sub")

    if usuario_id is None:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
      )

    return int(usuario_id)

  except (jwt.InvalidTokenError, ValueError):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Token inválido ou expirado",
    )