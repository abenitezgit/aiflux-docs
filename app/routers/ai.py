"""
Router de IA - Endpoint para generación de respuestas

Endpoints:
- GET /api/ai/context → Obtiene jerarquía de notas del usuario
- POST /api/ai/generate → Genera respuesta de IA basada en nota + pregunta

ARQUITECTURA:
- RLS obligatorio (user_id)
- Respuestas JSON
- Error handling limpio
- Logging minimal
"""

from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import uuid
import logging
import json

from app.core.database import get_db
from app.services.llm_service import LLMService
from app.models import Categoria, Cuaderno, Tema, Anotacion

logger = logging.getLogger(__name__)
router = APIRouter()


# --- FUNCIONES HELPER ---
def format_hierarchy_for_llm(bibliotecas: list[AIContextCategoria]) -> str:
    """
    Convierte la estructura jerárquica a un formato legible para el LLM
    
    Formato:
    BIBLIOTECA: Desarrollo
      └─ CUADERNO: Python
        └─ TEMA: Async
          • Asyncio basics
          • Event loops
    """
    lines = []
    
    for biblioteca in bibliotecas:
        lines.append(f"BIBLIOTECA: {biblioteca.nombre}")
        
        for cuaderno in biblioteca.cuadernos:
            lines.append(f"  └─ CUADERNO: {cuaderno.nombre}")
            
            for tema in cuaderno.temas:
                lines.append(f"    └─ TEMA: {tema.nombre}")
                
                for nota in tema.notas:
                    lines.append(f"      • {nota.title}")
    
    return "\n".join(lines) if lines else "No hay notas en tu biblioteca"


# --- MODELOS ---
class AIGenerateRequest(BaseModel):
    """Request para generar respuesta de IA"""
    noteId: uuid.UUID
    content: str  # HTML de la nota
    prompt: str   # Pregunta del usuario


class AIGenerateResponse(BaseModel):
    """Response de la IA"""
    response: str
    timestamp: str


class AIContextNote(BaseModel):
    """Nota en el contexto (solo título)"""
    id: str
    title: str


class AIContextTema(BaseModel):
    """Tema con sus notas"""
    nombre: str
    notas: list[AIContextNote]


class AIContextCuaderno(BaseModel):
    """Cuaderno con sus temas"""
    nombre: str
    temas: list[AIContextTema]


class AIContextCategoria(BaseModel):
    """Categoría (Biblioteca) con sus cuadernos"""
    nombre: str
    cuadernos: list[AIContextCuaderno]


class AIContextResponse(BaseModel):
    """Respuesta con la estructura jerárquica completa"""
    bibliotecas: list[AIContextCategoria]


# --- ENDPOINTS ---
@router.get("/api/ai/context", response_model=AIContextResponse)
async def get_ai_context(
    session: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = None  # TODO: Obtener del token JWT
):
    """
    Obtiene la jerarquía completa de bibliotecas, cuadernos, temas y notas (solo títulos)
    
    Este endpoint es llamado internamente por /api/ai/generate para obtener contexto
    sobre las notas del usuario sin cargar el contenido completo.
    """
    
    try:
        # Para ahora, usar un user_id fijo (TODO: obtener del JWT)
        # En producción, usar: user_id = get_current_user(token)
        if not user_id:
            user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")  # TODO: usar usuario real
        
        # Obtener todas las categorías del usuario
        stmt = select(Categoria).where(
            Categoria.user_id == user_id
        ).order_by(Categoria.orden)
        result = await session.execute(stmt)
        categorias = result.scalars().all()
        
        bibliotecas = []
        
        for categoria in categorias:
            # Obtener cuadernos de esta categoría
            stmt_cuadernos = select(Cuaderno).where(
                Cuaderno.categoria_id == categoria.id
            ).order_by(Cuaderno.nombre)
            result_cuadernos = await session.execute(stmt_cuadernos)
            cuadernos_db = result_cuadernos.scalars().all()
            
            cuadernos = []
            
            for cuaderno in cuadernos_db:
                # Obtener temas de este cuaderno
                stmt_temas = select(Tema).where(
                    Tema.cuaderno_id == cuaderno.id
                ).order_by(Tema.orden)
                result_temas = await session.execute(stmt_temas)
                temas_db = result_temas.scalars().all()
                
                temas = []
                
                for tema in temas_db:
                    # Obtener anotaciones (notas) de este tema
                    stmt_notas = select(Anotacion).where(
                        Anotacion.tema_id == tema.id
                    ).order_by(Anotacion.titulo)
                    result_notas = await session.execute(stmt_notas)
                    notas_db = result_notas.scalars().all()
                    
                    notas = [
                        AIContextNote(id=str(nota.id), title=nota.titulo)
                        for nota in notas_db
                    ]
                    
                    temas.append(AIContextTema(
                        nombre=tema.nombre,
                        notas=notas
                    ))
                
                cuadernos.append(AIContextCuaderno(
                    nombre=cuaderno.nombre,
                    temas=temas
                ))
            
            bibliotecas.append(AIContextCategoria(
                nombre=categoria.nombre,
                cuadernos=cuadernos
            ))
        
        return AIContextResponse(bibliotecas=bibliotecas)
        
    except Exception as e:
        logger.error(f"❌ Error obteniendo contexto: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo contexto: {str(e)}"
        )


@router.post("/api/ai/generate", response_model=AIGenerateResponse)
async def generate_ai_response(
    request: AIGenerateRequest,
    session: AsyncSession = Depends(get_db)
):
    """
    Genera respuesta de IA basada en contenido de nota + pregunta
    
    Flujo:
    1. Validar que el usuario es dueño de la nota (RLS)
    2. Llamar LLM service con contenido + prompt
    3. Retornar respuesta
    
    Errores:
    - 401: No autenticado
    - 403: Nota no pertenece al usuario
    - 400: Prompt vacío
    - 500: Error en LLM
    """
    
    # TODO: Agregar autenticación cuando esté lista
    # Por ahora, solo para testing sin autenticación
    
    # 1. Validar input
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prompt no puede estar vacío"
        )
    
    if not request.content or not request.content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contenido de nota no puede estar vacío"
        )
    
    try:
        # 1. Obtener user_id desde la nota
        logger.info(f"📚 Buscando nota {request.noteId}...")
        
        stmt_nota = select(Anotacion).where(Anotacion.id == request.noteId)
        result_nota = await session.execute(stmt_nota)
        nota = result_nota.scalars().first()
        
        if not nota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nota no encontrada: {request.noteId}"
            )
        
        user_id = nota.user_id
        logger.info(f"✅ Nota encontrada (user_id: {user_id})")
        
        # 2. Obtener jerarquía de contexto
        logger.info(f"📚 Obteniendo contexto jerárquico para user_id: {user_id}...")
        
        # Obtener contexto (llamada recursiva al endpoint de contexto)
        context_response = await get_ai_context(session=session, user_id=user_id)
        
        # Convertir a formato legible para el LLM
        context_hierarchy = format_hierarchy_for_llm(context_response.bibliotecas)
        
        logger.info(f"✅ Contexto obtenido: {len(context_hierarchy)} caracteres")
        logger.info(f"\n{'='*80}")
        logger.info(f"📋 JERARQUÍA ENVIADA AL LLM:")
        logger.info(f"{'='*80}")
        logger.info(f"\n{context_hierarchy}\n")
        logger.info(f"{'='*80}\n")
        
        # 2. Llamar LLM service con contexto
        logger.info(f"🤖 Generando respuesta para nota {request.noteId}")
        logger.info(f"   Prompt: {request.prompt[:100]}...")
        
        # Crear instancia nueva del servicio
        llm_service = LLMService()
        response_text = llm_service.groq_generate(
            content=request.content,
            prompt=request.prompt,
            context_hierarchy=context_hierarchy
        )
        
        logger.info(f"✅ Respuesta generada: {len(response_text)} caracteres")
        
        return AIGenerateResponse(
            response=response_text,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"❌ Error generando respuesta: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando respuesta: {str(e)}"
        )
