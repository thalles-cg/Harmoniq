import os

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from src.database.dependencies import get_db
from src.model.usuario import Usuario

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

security = HTTPBearer()

if not JWT_SECRET_KEY:
  raise RuntimeError("A variável JWT_SECRET_KEY não foi definida.")

def get_usuario_atual(credenciais: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> Usuario:
  token = credenciais.credentials

  try:
    payload = jwt.decode(
      token,
      JWT_SECRET_KEY,
      algorithms=[JWT_ALGORITHM]
    )

    usuario_id = payload.get("sub")

    if usuario_id is None:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido"
      )

    usuario_id = int(usuario_id)

  except (jwt.InvalidTokenError, ValueError):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Token inválido"
    )

  usuario = db.scalar(
    select(Usuario).where(Usuario.id == usuario_id)
  )

  if usuario is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Usuário não encontrado"
    )

  return usuario