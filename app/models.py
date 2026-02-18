import uuid
import json
import re
from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Column, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy import text

# --- USUARIO ---
class UsuarioDB(SQLModel, table=True):
    __tablename__ = "usuarios"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    email: str = Field(unique=True, index=True)
    hashed_password: str
    nombre: str
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )

# --- CATEGORÍA (Biblioteca) ---
class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    nombre: str
    icono: str = Field(default="folder")
    color: str = Field(default="#3b82f6")
    orden: int = Field(default=0)
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    # Relaciones
    cuadernos: List["Cuaderno"] = Relationship(
        back_populates="categoria",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

# --- CUADERNO / PROYECTO ---
class Cuaderno(SQLModel, table=True):
    __tablename__ = "cuadernos"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    nombre: str
    descripcion: Optional[str] = None
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    categoria_id: Optional[uuid.UUID] = Field(default=None, foreign_key="categorias.id")
    
    # Campos específicos de Proyecto
    tipo: str = Field(default="cuaderno")  # 'cuaderno' | 'proyecto'
    estado: str = Field(default="activo")
    fecha_limite: Optional[datetime] = None
    progreso: int = Field(default=0)

    # Relaciones
    categoria: Optional[Categoria] = Relationship(back_populates="cuadernos")
    temas: List["Tema"] = Relationship(
        back_populates="cuaderno",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    tareas: List["Tarea"] = Relationship(
        back_populates="cuaderno",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

# --- TAREA ---
class Tarea(SQLModel, table=True):
    __tablename__ = "tareas"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    titulo: str
    hecho: bool = Field(default=False)
    cuaderno_id: Optional[uuid.UUID] = Field(default=None, foreign_key="cuadernos.id")
    fecha_objetivo: Optional[datetime] = None
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    cuaderno: Optional[Cuaderno] = Relationship(back_populates="tareas")

# --- TEMA ---
class Tema(SQLModel, table=True):
    __tablename__ = "temas"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    nombre: str
    orden: int = Field(default=0)
    cuaderno_id: uuid.UUID = Field(foreign_key="cuadernos.id")
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    cuaderno: Optional[Cuaderno] = Relationship(back_populates="temas")
    anotaciones: List["Anotacion"] = Relationship(
        back_populates="tema",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

# --- ANOTACION ---
class Anotacion(SQLModel, table=True):
    __tablename__ = "anotaciones"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    titulo: str
    contenido: Optional[str] = None
    tags: List[str] = Field(default=[], sa_column=Column(ARRAY(String)))
    tema_id: uuid.UUID = Field(foreign_key="temas.id")
    created_at: Optional[datetime] = Field(default=None, sa_column_kwargs={"server_default": text("now()")})
    updated_at: Optional[datetime] = Field(default=None, sa_column_kwargs={"server_default": text("now()"), "onupdate": text("now()")})
    
    tema: Optional["Tema"] = Relationship(back_populates="anotaciones")
    adjuntos: List["Adjunto"] = Relationship(back_populates="anotacion", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    @property
    def resumen_texto(self) -> str:
        """Extrae texto plano de forma ultra-rápida usando Regex"""
        if not self.contenido or len(self.contenido) < 5:
            return ""
        
        content = self.contenido.strip()
        
        # Caso 1: Es JSON de TipTap (Empieza con {)
        if content.startswith('{'):
            # Usamos Regex para capturar solo lo que está dentro de "text":"..."
            # Es 100 veces más rápido que parsear el JSON completo
            textos = re.findall(r'"text"\s*:\s*"([^"]+)"', content)
            return " ".join(textos) if textos else ""
            
        # Caso 2: Es HTML Legacy
        # Limpiamos etiquetas <...> y devolvemos el texto
        return re.sub(r'<[^<]+?>', '', content)
    
# --- ADJUNTO ---
class Adjunto(SQLModel, table=True):
    __tablename__ = "adjuntos"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    url: str
    nombre_original: Optional[str] = None
    tipo_archivo: Optional[str] = None
    anotacion_id: uuid.UUID = Field(foreign_key="anotaciones.id")
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    anotacion: Optional[Anotacion] = Relationship(back_populates="adjuntos")