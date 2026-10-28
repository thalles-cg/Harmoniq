import os
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

if not JWT_SECRET_KEY:
  raise RuntimeError("A variável JWT_SECRET_KEY não foi definida.")

def criar_token_acesso(usuario_id: int) -> str:
  expiracao = datetime.now(timezone.utc) + timedelta(
    minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES
  )

  payload = {
    "sub": str(usuario_id),
    "exp": expiracao
  }

  return jwt.encode(
    payload,
    JWT_SECRET_KEY,
    algorithm=JWT_ALGORITHM
  )