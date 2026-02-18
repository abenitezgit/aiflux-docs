# app/routers/dashboard.py
from fastapi import APIRouter, Depends, Request, Form, Response, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select, desc, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from datetime import date, datetime
from pydantic import BaseModel
import mimetypes
import os

from app.core.database import get_db, init_rls
from app.core.auth import get_authenticated_user
from app.models import UsuarioDB, Categoria, Cuaderno, Anotacion, Tarea, Tema, Adjunto
from app.core.database import supabase
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    # RLS OBLIGATORIO
    await init_rls(session, str(user.id))

    # 1. Cargar Bibliotecas/Categorías
    stmt_cat = (
        select(Categoria)
        .where(Categoria.user_id == user.id)
        .order_by(Categoria.orden)
        .options(selectinload(Categoria.cuadernos))
    )
    categorias = (await session.exec(stmt_cat)).all()

    # 2. Tareas de hoy
    stmt_tareas = (
        select(Tarea)
        .where(Tarea.user_id == user.id, Tarea.hecho == False)
        .order_by(Tarea.fecha_objetivo.asc().nullslast())
        .limit(5)
    )
    agenda = (await session.exec(stmt_tareas)).all()

    # 3. Proyectos
    stmt_proy = (
        select(Cuaderno)
        .where(Cuaderno.user_id == user.id, Cuaderno.tipo == 'proyecto')
    )
    proyectos = (await session.exec(stmt_proy)).all()

    # 4. Notas Recientes
    stmt_recientes = (
        select(Anotacion)
        .where(Anotacion.user_id == user.id)
        .order_by(desc(Anotacion.updated_at))
        .limit(4)
        .options(selectinload(Anotacion.tema).selectinload(Tema.cuaderno))
    )
    recientes = (await session.exec(stmt_recientes)).all()

    return templates.TemplateResponse("layouts/base.html", {
        "request": request,
        "user": user,
        "view_mode": "dashboard",
        "categorias": categorias,
        "agenda": agenda,
        "proyectos": proyectos,
        "recientes": recientes,
        "today": date.today()
    })

@router.post("/inbox/captura")
async def captura_inbox(
    contenido: str = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    # Buscamos directamente el ID del tema inmutable
    stmt = (
        select(Tema.id)
        .join(Cuaderno)
        .where(
            Cuaderno.user_id == user.id,
            Cuaderno.nombre == "Inbox",
            Tema.nombre == "Capturas Rápidas"
        )
    )
    tema_id = (await session.exec(stmt)).first()

    if not tema_id:
        # Fallback de seguridad por si el usuario es antiguo y no tiene la estructura
        return Response(status_code=400) # O podrías llamar a una función de reparación

    nueva_nota = Anotacion(
        titulo=f"Nota {datetime.now().strftime('%H:%M')}",
        contenido=contenido,
        user_id=user.id,
        tema_id=tema_id
    )
    session.add(nueva_nota)
    await session.commit()

    resp = Response(status_code=204)
    resp.headers["HX-Trigger"] = "update-inbox-count, update-inbox-list"
    return resp

@router.get("/inbox/count")
async def get_inbox_count(
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    stmt = (
            select(func.count(Anotacion.id))
            .join(Tema, Anotacion.tema_id == Tema.id)
            .join(Cuaderno, Tema.cuaderno_id == Cuaderno.id)
            .where(
                Cuaderno.user_id == user.id,
                Cuaderno.nombre == "Inbox",
                Tema.nombre == "Capturas Rápidas"
            )
        )
        
    count = (await session.exec(stmt)).one()
        
    # Retornamos el número puro como texto plano
    return PlainTextResponse(str(count))

@router.get("/partial/sidebar/inbox", response_class=HTMLResponse)
async def get_sidebar_inbox(
    request: Request,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    # Buscamos las notas en la ruta GENERAL -> Inbox -> Capturas Rápidas
    stmt = (
        select(Anotacion)
        .join(Tema)
        .join(Cuaderno)
        .where(
            Cuaderno.user_id == user.id,
            Cuaderno.nombre == "Inbox",
            Tema.nombre == "Capturas Rápidas"
        )
        .order_by(desc(Anotacion.created_at))
    )
    notas = (await session.exec(stmt)).all()

    return templates.TemplateResponse("modules/sidebar_inbox.html", {
        "request": request,
        "notas": notas
    })

# También necesitamos el endpoint para restaurar la sidebar del dashboard
@router.get("/partial/sidebar/dashboard", response_class=HTMLResponse)
async def get_sidebar_dashboard(
    request: Request,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    stmt_cat = (
        select(Categoria)
        .where(Categoria.user_id == user.id)
        .order_by(Categoria.orden)
        .options(selectinload(Categoria.cuadernos))
    )
    categorias = (await session.exec(stmt_cat)).all()
    
    # Reutilizamos el partial que ya teníamos
    return templates.TemplateResponse("modules/sidebar_dashboard.html", {
        "request": request,
        "categorias": categorias
    })

@router.get("/partial/modal/inbox-actions/{nota_id}", response_class=HTMLResponse)
async def get_modal_inbox_actions(
    nota_id: uuid.UUID,
    request: Request,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    # Buscamos la nota (SQLModel/SQLAlchemy)
    # Al ser una sesión nueva por cada request, no hay caché de objeto.
    nota = await session.get(Anotacion, nota_id)
    
    stmt = (
        select(Categoria)
        .where(Categoria.user_id == user.id)
        .order_by(Categoria.orden)
        .options(selectinload(Categoria.cuadernos).selectinload(Cuaderno.temas))
    )
    categorias = (await session.exec(stmt)).all()

    response = templates.TemplateResponse("partials/modal_inbox_triaje.html", {
        "request": request,
        "nota": nota,
        "categorias": categorias
    })
    
    # Headers de hierro para evitar caché del navegador
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response

@router.get("/partial/modal/inbox-mover/{nota_id}", response_class=HTMLResponse)
async def get_modal_inbox_mover(
    nota_id: uuid.UUID,
    request: Request,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    """Retorna el nuevo modal de triaje con buscador y jerarquía completa"""
    await init_rls(session, str(user.id))
    
    # 1. Obtener la nota
    nota = await session.get(Anotacion, nota_id)
    if not nota:
        return PlainTextResponse("Nota no encontrada", status_code=404)
    
    # 2. Obtener toda la jerarquía (Biblioteca > Cuaderno > Tema)
    # Excluimos el cuaderno 'Inbox' de los destinos posibles
    stmt = (
        select(Categoria)
        .where(Categoria.user_id == user.id)
        .options(
            selectinload(Categoria.cuadernos)
            .selectinload(Cuaderno.temas)
        )
        .order_by(Categoria.orden)
    )
    result = await session.exec(stmt)
    categorias = result.all()
    
    return templates.TemplateResponse("partials/modal_inbox_triaje.html", {
        "request": request,
        "nota": nota,
        "categorias": categorias
    })

@router.post("/inbox/mover/{nota_id}")
async def mover_nota(
    nota_id: uuid.UUID,
    nuevo_tema_id: uuid.UUID = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    """Mueve la nota y dispara los triggers de actualización total"""
    await init_rls(session, str(user.id))
    
    nota = await session.get(Anotacion, nota_id)
    if not nota:
        raise HTTPException(status_code=404)

    # Actualizar destino
    nota.tema_id = nuevo_tema_id
    session.add(nota)
    await session.commit()
    
    # RESPUESTA AXIOMÁTICA: Triple Trigger para actualización en línea
    response = Response(status_code=204)
    # 1. Actualiza contador | 2. Limpia lista inbox | 3. Refresca sidebar de cuaderno (si está abierta)
    response.headers["HX-Trigger"] = "update-inbox-count, update-inbox-list, refresh-notebook-sidebar"
    return response

@router.delete("/inbox/eliminar/{nota_id}")
async def eliminar_nota(
    nota_id: uuid.UUID,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    nota = await session.get(Anotacion, nota_id)
    
    if nota:
        await session.delete(nota)
        await session.commit()
    
    # Respuesta 204 (Sin contenido) pero con Triggers para refrescar AMBAS sidebars
    # así funciona sea cual sea la vista donde estés.
    response = Response(status_code=204)
    response.headers["HX-Trigger"] = "update-inbox-count, update-inbox-list, refresh-notebook-sidebar"
    return response

# --- VISTA DE NAVEGACIÓN DENTRO DE UN CUADERNO (ZONA 2) ---
@router.get("/partial/sidebar/notebook/{notebook_id}", response_class=HTMLResponse)
async def get_sidebar_notebook(
    notebook_id: uuid.UUID,
    request: Request,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    # 1. Seguridad RLS
    await init_rls(session, str(user.id))
    
    # 2. Obtener el cuaderno con sus temas y la categoría a la que pertenece
    # Usamos selectinload para cargar los temas y las notas de forma eficiente
    stmt = (
        select(Cuaderno)
        .where(Cuaderno.id == notebook_id, Cuaderno.user_id == user.id)
        .options(
            selectinload(Cuaderno.categoria),
            selectinload(Cuaderno.temas).selectinload(Tema.anotaciones)
        )
    )
    result = await session.exec(stmt)
    cuaderno = result.first()

    if not cuaderno:
        return PlainTextResponse("Cuaderno no encontrado", status_code=404)

    # 3. Renderizar el nuevo partial que crearemos en el siguiente paso
    return templates.TemplateResponse("modules/sidebar_notebook.html", {
        "request": request,
        "cuaderno": cuaderno,
        "categoria": cuaderno.categoria
    })

@router.get("/api/notes/{note_id}")
async def get_note_data(
    note_id: uuid.UUID,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    # Seguridad RLS Obligatoria
    await init_rls(session, str(user.id))
    
    # Buscamos la nota con sus relaciones para el Inspector (Zona 4)
    stmt = (
        select(Anotacion)
        .where(Anotacion.id == note_id, Anotacion.user_id == user.id)
        .options(
            selectinload(Anotacion.tema).selectinload(Tema.cuaderno),
            selectinload(Anotacion.adjuntos)
        )
    )
    result = await session.exec(stmt)
    nota = result.first()

    if not nota:
        return Response(status_code=404)

    # Devolvemos un objeto JSON completo para que el JS lo procese
    return {
        "id": str(nota.id),
        "titulo": nota.titulo,
        "contenido": nota.contenido, # Aquí vendrá el HTML o JSON de TipTap
        "tags": nota.tags,
        "tema_nombre": nota.tema.nombre,
        "cuaderno_nombre": nota.tema.cuaderno.nombre,
        "adjuntos": [
            {"id": str(a.id), "nombre": a.nombre_original, "url": a.url, "tipo": a.tipo_archivo} 
            for a in nota.adjuntos
        ]
    }

@router.get("/note/{note_id}", response_class=HTMLResponse)
async def note_view(
    note_id: uuid.UUID,
    request: Request,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    # 1. RLS Obligatorio
    await init_rls(session, str(user.id))

    # 2. Cargar los datos básicos para la Sidebar (Igual que en /dashboard)
    stmt_cat = (
        select(Categoria)
        .where(Categoria.user_id == user.id)
        .order_by(Categoria.orden)
        .options(selectinload(Categoria.cuadernos))
    )
    categorias = (await session.exec(stmt_cat)).all()

    # 3. Cargar la nota específica para el "Escenario"
    stmt_nota = (
        select(Anotacion)
        .where(Anotacion.id == note_id, Anotacion.user_id == user.id)
        .options(
            selectinload(Anotacion.tema).selectinload(Tema.cuaderno)
        )
    )
    result_nota = await session.exec(stmt_nota)
    nota_activa = result_nota.first()

    if not nota_activa:
        # Si la nota no existe, redirigimos al dashboard
        return RedirectResponse(url="/dashboard")

    # 4. Renderizar base.html con el contexto de la nota
    return templates.TemplateResponse("layouts/base.html", {
        "request": request,
        "user": user,
        "view_mode": "notebook", # Forzamos modo notebook
        "categorias": categorias,
        "active_note": nota_activa, # Pasamos el objeto nota
        "active_note_id": str(nota_activa.id),
        "today": date.today()
    })

@router.post("/api/upload/image")
async def upload_editor_image(
    file: UploadFile = File(...),
    user: UsuarioDB = Depends(get_authenticated_user)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo no es una imagen")
    
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase no configurado")

    # Generar nombre único basado en el usuario (orden tipo Legacy)
    ext = mimetypes.guess_extension(file.content_type) or ".png"
    filename = f"inline_{user.id}/{uuid.uuid4().hex}{ext}"
    
    try:
        content = await file.read()
        # Subir al bucket configurado en el Legacy
        supabase.storage.from_("docs_assets").upload(
            path=filename,
            file=content,
            file_options={"content-type": file.content_type}
        )
        
        # Obtener la URL pública para el editor
        response = supabase.storage.from_("docs_assets").get_public_url(filename)
        return {"url": response}
        
    except Exception as e:
        print(f"Error subiendo a Supabase: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al subir la imagen")
    

# Clase para recibir actualizaciones parciales
class NoteUpdate(BaseModel):
    titulo: str | None = None
    contenido: str | None = None

@router.patch("/api/notes/{note_id}")
async def patch_note(
    note_id: uuid.UUID,
    note_data: NoteUpdate,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    # 1. Convertimos el modelo a un diccionario, ignorando los valores que no se enviaron
    update_values = note_data.dict(exclude_unset=True)
    
    if not update_values:
        return {"status": "no updates provided"}

    # 2. Ejecutamos una actualización quirúrgica en la DB
    # Esto solo toca las columnas titulo/contenido y no afecta a los adjuntos
    stmt = (
        update(Anotacion)
        .where(Anotacion.id == note_id, Anotacion.user_id == user.id)
        .values(**update_values)
    )
    
    await session.execute(stmt)
    await session.commit()
    
    return {"status": "success"}

@router.post("/api/notes/upload-attachment")
async def upload_attachment(
    request: Request,
    note_id: uuid.UUID = Form(...),
    file: UploadFile = File(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase no configurado")

    # 1. Subir a Supabase Storage
    ext = os.path.splitext(file.filename)[1]
    filename = f"att_{user.id}/{uuid.uuid4().hex}{ext}"
    content = await file.read()
    
    supabase.storage.from_("docs_assets").upload(
        path=filename,
        file=content,
        file_options={"content-type": file.content_type}
    )
    
    # 2. Obtener URL y guardar en DB
    public_url = supabase.storage.from_("docs_assets").get_public_url(filename)
    
    nuevo_adjunto = Adjunto(
        url=public_url,
        nombre_original=file.filename,
        tipo_archivo=file.content_type,
        anotacion_id=note_id,
        user_id=user.id
    )
    session.add(nuevo_adjunto)
    await session.commit()

    await init_rls(session, str(user.id))

    # 3. Recuperar todos los adjuntos de esta nota para devolver el partial actualizado
    stmt = select(Adjunto).where(Adjunto.anotacion_id == note_id)
    result = await session.exec(stmt)
    adjuntos = result.all()

    # Devolvemos el fragmento HTML (Partial)
    return templates.TemplateResponse("partials/attachments_list.html", {
        "request": request,
        "adjuntos": adjuntos
    })

# app/routers/dashboard.py

@router.delete("/api/notes/attachment/{attachment_id}")
async def delete_attachment(
    attachment_id: uuid.UUID,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    # 1. Obtener el adjunto para saber a qué nota pertenece
    adjunto = await session.get(Adjunto, attachment_id)
    if not adjunto:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    note_id = adjunto.anotacion_id
    
    # 2. Borrar de la DB (Supabase Storage se podría borrar aquí también, 
    # pero por seguridad de momento solo quitamos la referencia)
    await session.delete(adjunto)
    await session.commit()
    
    await init_rls(session, str(user.id))

    # 3. Devolver la lista actualizada de la nota
    stmt = select(Adjunto).where(Adjunto.anotacion_id == note_id)
    result = await session.exec(stmt)
    adjuntos = result.all()
    
    return templates.TemplateResponse("partials/attachments_list.html", {
        "request": {}, # HTMX no necesita el request completo aquí
        "adjuntos": adjuntos
    })

# --- CREAR TEMA (MODAL) ---
@router.get("/partial/modal/nuevo-tema/{cuaderno_id}", response_class=HTMLResponse)
async def get_modal_nuevo_tema(cuaderno_id: uuid.UUID, request: Request):
    """Sirve el modal de creación de tema con el ID del cuaderno inyectado"""
    return templates.TemplateResponse("partials/modal_tema.html", {
        "request": request,
        "cuaderno_id": cuaderno_id
    })

@router.post("/api/temas/create")
async def create_tema(
    request: Request,
    cuaderno_id: uuid.UUID = Form(...),
    nombre: str = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    # 1. Obtener el orden máximo actual para poner el nuevo al final
    stmt_max = select(func.max(Tema.orden)).where(Tema.cuaderno_id == cuaderno_id)
    max_orden = (await session.exec(stmt_max)).first() or 0

    nuevo_tema = Tema(
        nombre=nombre,
        cuaderno_id=cuaderno_id,
        user_id=user.id,
        orden=max_orden + 1
    )
    session.add(nuevo_tema)
    await session.commit()

    # 2. Devolver la sidebar completa del cuaderno para refrescar la lista
    # Reutilizamos la lógica de la sidebar_notebook
    return await get_sidebar_notebook(cuaderno_id, request, user, session)

# --- CREAR NOTA (DENTRO DE UN TEMA) ---
@router.post("/api/notes/create")
async def create_note(
    request: Request,
    tema_id: uuid.UUID = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    # 1. Crear la nota lo más rápido posible
    nueva_nota = Anotacion(
        titulo="Sin título",
        contenido='{"type":"doc","content":[{"type":"paragraph"}]}',
        tema_id=tema_id,
        user_id=user.id
    )
    session.add(nueva_nota)
    await session.commit()
    
    # IMPORTANTE: Re-inyectar RLS inmediatamente para la siguiente consulta
    await init_rls(session, str(user.id))
    
    # 2. Solo necesitamos saber a qué cuaderno pertenece para refrescar la sidebar
    res = await session.execute(select(Tema.cuaderno_id).where(Tema.id == tema_id))
    cuaderno_id = res.scalar()

    # 3. Respuesta con refresco de Sidebar
    response = await get_sidebar_notebook(cuaderno_id, request, user, session)
    
    nota_id_str = str(nueva_nota.id)
    response.headers["HX-Trigger"] = f'{{"note-selected": {{"id": "{nota_id_str}"}} }}'
    return response

# --- GESTIÓN DE CATEGORÍAS (MODALES) ---

@router.get("/partial/modal/nueva-categoria", response_class=HTMLResponse)
async def get_modal_nueva_categoria(request: Request):
    """Retorna el modal para crear una nueva biblioteca/categoría"""
    return templates.TemplateResponse("partials/modal_categoria.html", {
        "request": request
    })

@router.post("/api/categorias/create")
async def create_categoria(
    request: Request,
    nombre: str = Form(...),
    icono: str = Form("folder"),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    """Crea una categoría y refresca la sidebar del dashboard"""
    await init_rls(session, str(user.id))
    
    # Obtener el orden máximo para ponerla al final
    stmt_max = select(func.max(Categoria.orden)).where(Categoria.user_id == user.id)
    max_orden = (await session.exec(stmt_max)).first() or 0

    nueva_cat = Categoria(
        nombre=nombre,
        icono=icono,
        user_id=user.id,
        orden=max_orden + 1
    )
    session.add(nueva_cat)
    await session.commit()

    # Refrescar la sidebar del dashboard para mostrar la nueva categoría
    return await get_sidebar_dashboard(request, user, session)

# --- EDICIÓN Y BORRADO DE CATEGORÍAS ---

@router.get("/partial/modal/edit-categoria/{cat_id}", response_class=HTMLResponse)
async def get_modal_edit_categoria(cat_id: uuid.UUID, request: Request, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db)):
    await init_rls(session, str(user.id))
    categoria = await session.get(Categoria, cat_id)
    return templates.TemplateResponse("partials/modal_edit_categoria.html", {
        "request": request,
        "categoria": categoria
    })

@router.patch("/api/categorias/{cat_id}")
async def patch_categoria(
    cat_id: uuid.UUID,
    nombre: str = Form(...),
    icono: str = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db),
    request: Request = None
):
    await init_rls(session, str(user.id))
    categoria = await session.get(Categoria, cat_id)
    if categoria:
        categoria.nombre = nombre
        categoria.icono = icono
        session.add(categoria)
        await session.commit()
    return await get_sidebar_dashboard(request, user, session)

@router.delete("/api/categorias/{cat_id}")
async def delete_categoria(cat_id: uuid.UUID, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db), request: Request = None):
    await init_rls(session, str(user.id))
    categoria = await session.get(Categoria, cat_id)
    if categoria:
        await session.delete(categoria)
        await session.commit()
    return await get_sidebar_dashboard(request, user, session)

# --- MODALES DE SEGURIDAD (DANGER ZONE) ---

@router.get("/partial/modal/confirm-delete-categoria/{cat_id}", response_class=HTMLResponse)
async def get_modal_confirm_delete_categoria(cat_id: uuid.UUID, request: Request, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db)):
    await init_rls(session, str(user.id))
    categoria = await session.get(Categoria, cat_id)
    return templates.TemplateResponse("partials/modal_confirm_delete.html", {
        "request": request,
        "obj_id": cat_id,
        "obj_name": categoria.nombre,
        "type": "biblioteca",
        "warning": "Se eliminarán permanentemente todos los cuadernos, temas y notas dentro de esta biblioteca.",
        "delete_url": f"/api/categorias/{cat_id}"
    })

@router.get("/partial/modal/confirm-delete-cuaderno/{notebook_id}", response_class=HTMLResponse)
async def get_modal_confirm_delete_cuaderno(notebook_id: uuid.UUID, request: Request, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db)):
    await init_rls(session, str(user.id))
    cuaderno = await session.get(Cuaderno, notebook_id)
    return templates.TemplateResponse("partials/modal_confirm_delete.html", {
        "request": request,
        "obj_id": notebook_id,
        "obj_name": cuaderno.nombre,
        "type": "cuaderno",
        "warning": "Se eliminarán permanentemente todos los temas y notas dentro de este cuaderno.",
        "delete_url": f"/api/cuadernos/{notebook_id}" # El endpoint de borrado de cuaderno lo crearemos en la siguiente etapa
    })

# --- GESTIÓN DE CUADERNOS (NOTEBOOKS) ---

@router.get("/partial/modal/nuevo-cuaderno/{cat_id}", response_class=HTMLResponse)
async def get_modal_nuevo_cuaderno(cat_id: uuid.UUID, request: Request):
    return templates.TemplateResponse("partials/modal_cuaderno.html", {
        "request": request,
        "cat_id": cat_id
    })

@router.post("/api/cuadernos/create")
async def create_cuaderno(
    request: Request,
    nombre: str = Form(...),
    cat_id: uuid.UUID = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    nuevo_nb = Cuaderno(nombre=nombre, categoria_id=cat_id, user_id=user.id, tipo="cuaderno")
    session.add(nuevo_nb)
    await session.commit()
    return await get_sidebar_dashboard(request, user, session)

@router.get("/partial/modal/edit-cuaderno/{nb_id}", response_class=HTMLResponse)
async def get_modal_edit_cuaderno(nb_id: uuid.UUID, request: Request, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db)):
    await init_rls(session, str(user.id))
    cuaderno = await session.get(Cuaderno, nb_id)
    return templates.TemplateResponse("partials/modal_edit_cuaderno.html", {
        "request": request,
        "cuaderno": cuaderno
    })

@router.patch("/api/cuadernos/{nb_id}")
async def patch_cuaderno(
    nb_id: uuid.UUID,
    nombre: str = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db),
    request: Request = None
):
    await init_rls(session, str(user.id))
    cuaderno = await session.get(Cuaderno, nb_id)
    if cuaderno:
        cuaderno.nombre = nombre
        session.add(cuaderno)
        await session.commit()
    return await get_sidebar_dashboard(request, user, session)

@router.delete("/api/cuadernos/{nb_id}")
async def delete_cuaderno(nb_id: uuid.UUID, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db), request: Request = None):
    await init_rls(session, str(user.id))
    cuaderno = await session.get(Cuaderno, nb_id)
    if cuaderno:
        await session.delete(cuaderno)
        await session.commit()
    return await get_sidebar_dashboard(request, user, session)

# --- GESTIÓN DE TEMAS (NOTEBOOK) ---

@router.get("/partial/modal/edit-tema/{tema_id}", response_class=HTMLResponse)
async def get_modal_edit_tema(tema_id: uuid.UUID, request: Request, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db)):
    await init_rls(session, str(user.id))
    tema = await session.get(Tema, tema_id)
    return templates.TemplateResponse("partials/modal_edit_tema.html", {
        "request": request,
        "tema": tema
    })

@router.patch("/api/temas/{tema_id}")
async def patch_tema(
    tema_id: uuid.UUID,
    nombre: str = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db),
    request: Request = None
):
    await init_rls(session, str(user.id))
    tema = await session.get(Tema, tema_id)
    if tema:
        tema.nombre = nombre
        session.add(tema)
        await session.commit()
    return await get_sidebar_notebook(tema.cuaderno_id, request, user, session)

@router.get("/partial/modal/confirm-delete-tema/{tema_id}", response_class=HTMLResponse)
async def get_modal_confirm_delete_tema(tema_id: uuid.UUID, request: Request, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db)):
    await init_rls(session, str(user.id))
    
    # CORRECCIÓN: Carga explícita de anotaciones para evitar el error MissingGreenlet
    stmt = select(Tema).where(Tema.id == tema_id).options(selectinload(Tema.anotaciones))
    result = await session.exec(stmt)
    tema = result.first()
    
    if not tema:
        return Response(status_code=404)

    return templates.TemplateResponse("partials/modal_confirm_delete.html", {
        "request": request,
        "obj_id": tema_id,
        "obj_name": tema.nombre,
        "type": "tema",
        "warning": f"Se eliminarán permanentemente todas las notas ({len(tema.anotaciones)}) dentro de este tema.",
        "delete_url": f"/api/temas/{tema_id}"
    })

@router.delete("/api/temas/{tema_id}")
async def delete_tema(tema_id: uuid.UUID, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db), request: Request = None):
    await init_rls(session, str(user.id))
    tema = await session.get(Tema, tema_id)
    cuaderno_id = tema.cuaderno_id
    if tema:
        await session.delete(tema)
        await session.commit()
    return await get_sidebar_notebook(cuaderno_id, request, user, session)

@router.get("/partial/modal/confirm-edit/{nota_id}", response_class=HTMLResponse)
async def get_modal_confirm_edit(nota_id: uuid.UUID, request: Request):
    return templates.TemplateResponse("partials/modal_confirm_edit.html", {
        "request": request,
        "nota_id": nota_id
    })

@router.get("/partial/modal/eliminar-nota/{nota_id}", response_class=HTMLResponse)
async def get_modal_eliminar_nota(nota_id: uuid.UUID, request: Request, session: AsyncSession = Depends(get_db), user: UsuarioDB = Depends(get_authenticated_user)):
    await init_rls(session, str(user.id))
    nota = await session.get(Anotacion, nota_id)
    return templates.TemplateResponse("partials/modal_eliminar_nota.html", {
        "request": request,
        "nota": nota
    })