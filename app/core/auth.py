from typing import Optional
from fastapi import Request, Depends, HTTPException, status
from jose import jwt, JWTError
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.config import settings
from app.core.database import get_db
from app.core.security import verify_password
from app.models import UsuarioDB

# Dependencia para obtener el usuario desde la Cookie
async def get_current_user(
    request: Request, 
    session: AsyncSession = Depends(get_db)
) -> Optional[UsuarioDB]:
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    # Limpieza del token (Bearer ...)
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None

    # Buscar usuario en DB
    try:
        u_uuid = uuid.UUID(user_id)
        result = await session.exec(select(UsuarioDB).where(UsuarioDB.id == u_uuid))
        user = result.first()
        return user
    except (ValueError, Exception):
        return None

# Dependencia estricta (lanza error si no hay usuario)
async def get_authenticated_user(user: Optional[UsuarioDB] = Depends(get_current_user)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Función de Login
async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[UsuarioDB]:
    statement = select(UsuarioDB).where(UsuarioDB.email == email)
    result = await session.exec(statement)
    user = result.first()
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user