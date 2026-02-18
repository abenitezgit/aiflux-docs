# Guidance for AI coding agents — proyecto-docs

Este archivo contiene instrucciones focalizadas para que IAs (Copilot, Claude, Gemini, etc.) sean productivas en este repositorio sin introducir bugs arquitectónicos.

## Visión General

- **Stack:** FastAPI (backend) + Jinja2 + HTMX + Alpine.js + Tailwind CSS
- **Estructura:** Sidebar de navegación (Zona 1) + Sidebar contextual (Zona 2) + Editor (Zona 3) + Inspector (Zona 4)
- **Base de datos:** PostgreSQL con SQLAlchemy ORM + Alembic migrations
- **Componentes clave:**
  - `sidebar_dashboard.html` - Biblioteca de categorías y cuadernos
  - `sidebar_notebook.html` - Vista de temas y notas dentro de un cuaderno
  - `sidebar_inbox.html` - Triaje de notas
  - `base.html` - Master layout con estado compartido (Alpine.js)

---

## 🚨 ARQUITECTURA HTMX: PATRÓN CRÍTICO

**⚠️ ESTO ES LO MÁS IMPORTANTE. LEE COMPLETAMENTE ANTES DE TOCAR HTMX.**

Tu código tiene DOS patrones de HTMX legítimos que UNA IA PUEDE CONFUNDIR:

### Patrón 1: Navegación Principal (innerHTML)

**Qué es:** Cambiar entre vistas principales (Dashboard → Notebook → Inbox)

**Dónde:** Target `#contextual-sidebar` (el contenedor WRAPPER)

**Estrategia:** `hx-swap="innerHTML"` - Reemplaza SOLO el contenido

**Por qué:** El contenedor `#contextual-sidebar` es permanente. Queremos que desaparezca sidebar_dashboard y aparezca sidebar_notebook, pero el wrapper sigue existiendo.

```html
<!-- Correcto: sidebar_dashboard.html -->
<button hx-get="/partial/sidebar/notebook/{{ cuaderno.id }}"
        hx-target="#contextual-sidebar"
        hx-swap="innerHTML">
    Abrir Cuaderno
</button>

<!-- Correcto: sidebar_notebook.html (botón atrás) -->
<button hx-get="/partial/sidebar/dashboard"
        hx-target="#contextual-sidebar"
        hx-swap="innerHTML">
    Atrás
</button>
```

**❌ NUNCA HAGAS:** 
- `hx-swap="outerHTML"` para navegación principal
- El wrapper desaparecería y confundiría a HTMX

---

### Patrón 2: Actualizaciones Internas (outerHTML)

**Qué es:** Refrescar o editar contenido DENTRO de una vista (crear tema, editar nota)

**Dónde:** Target `#notebook-sidebar-container` (el componente mismo)

**Estrategia:** `hx-swap="outerHTML"` - Reemplaza el elemento COMPLETO

**Por qué:** Necesitamos reinicializar el componente (listeners de Alpine, scroll, estado interno)

```html
<!-- Correcto: modal_tema.html -->
<form hx-post="/partial/sidebar/notebook/crear-tema"
      hx-target="#notebook-sidebar-container"
      hx-swap="outerHTML">
    Crear Tema
</form>
```

**✅ SIEMPRE HACES:**
- `outerHTML` para ediciones/creaciones internas
- El servidor devuelve el componente COMPLETO renovado

---

### La Confusión Común

Una IA ve:
1. `sidebar_notebook.html` tiene `<div id="notebook-sidebar-container">`
2. Algunas operaciones usan `hx-target="#notebook-sidebar-container" hx-swap="outerHTML"`
3. Piensa: "Ah, este componente se reemplaza por completo"
4. Extrapolación errónea: "Entonces la navegación también debe usar outerHTML"
5. ❌ **RESULTADO:** Bug en navegación

**Cómo identificar que una IA lo entiende:** 
- Dile explícitamente: "NO cambies los atributos `hx-swap` existentes"
- Si insiste en cambiar, rechaza y explica este documento

---

## Archivos Clave

### Backend
- `app/routers/dashboard.py` - Endpoints de navegación y datos
  - `/partial/sidebar/dashboard` - Retorna `sidebar_dashboard.html`
  - `/partial/sidebar/notebook/{id}` - Retorna `sidebar_notebook.html`
  - `/partial/sidebar/inbox` - Retorna `sidebar_inbox.html`
  
- `app/models.py` - SQLAlchemy models (Cuaderno, Tema, Anotacion, Categoria)
- `app/database.py` - Conexión a PostgreSQL, session factory

### Frontend
- `templates/layouts/base.html` - Master layout con Alpine `appShell()`, zona 1-4
- `templates/modules/sidebar_*.html` - Componentes intercambiables de Zona 2
- `templates/modules/sidebar_notebook.html` - **CRÍTICA**: Contiene el patrón outerHTML interno
- `templates/static/js/editor.js` - Editor Tiptap, manejo de notas

### Migraciones
- `alembic/` - Cambios de schema. Usar: `alembic upgrade head`

---

## Patrones de Código

### 1. Crear un Endpoint de Navigación (Nivel 1)

Si necesitas una nueva vista principal (ej: Búsqueda Global):

```python
# app/routers/dashboard.py
@router.get("/partial/sidebar/search", response_class=HTMLResponse)
async def get_sidebar_search(request: Request, user: UsuarioDB = Depends(get_authenticated_user)):
    return templates.TemplateResponse("modules/sidebar_search.html", {
        "request": request
    })
```

```html
<!-- templates/modules/sidebar_search.html -->
<div id="sidebar-search-container" class="flex flex-col h-full">
    <!-- Contenido -->
    <!-- Botones para volver SIEMPRE usan innerHTML a #contextual-sidebar -->
    <button hx-get="/partial/sidebar/dashboard"
            hx-target="#contextual-sidebar"
            hx-swap="innerHTML">
        Atrás
    </button>
</div>
```

### 2. Actualizar Contenido Dentro de una Vista (Nivel 2)

Si necesitas editar/crear algo DENTRO de sidebar_notebook:

```python
# app/routers/dashboard.py
@router.post("/partial/sidebar/notebook/crear-tema", response_class=HTMLResponse)
async def crear_tema(tema_nombre: str, notebook_id: uuid.UUID, ...):
    # ... lógica de BD
    return templates.TemplateResponse("modules/sidebar_notebook.html", {
        "request": request,
        "cuaderno": cuaderno,  # Nuevo estado
        "categoria": cuaderno.categoria
    })
```

```html
<!-- templates/partials/modal_tema.html o dentro de sidebar_notebook.html -->
<button hx-post="/partial/sidebar/notebook/crear-tema"
        hx-target="#notebook-sidebar-container"
        hx-swap="outerHTML">
    Guardar Tema
</button>
```

---

## Errores Comunes

### ❌ Cambiar `hx-swap` sin entender la arquitectura

```html
<!-- MALO: Alguien cambió a outerHTML -->
<button hx-get="/partial/sidebar/notebook/{{ cuaderno.id }}"
        hx-target="#contextual-sidebar"
        hx-swap="outerHTML">  <!-- ← BUG: Rompe navegación -->
```

**Síntoma:** Segunda selección de cuaderno no funciona

**Solución:** Revisar este documento, revertir a `innerHTML`

---

### ❌ Agregar atributos HTMX redundantes

```html
<!-- MALO: sidebar_notebook.html tiene HTMX que no debería -->
<div id="notebook-sidebar-container" 
     hx-get="/partial/sidebar/notebook/..."  <!-- ← REDUNDANTE -->
     hx-swap="outerHTML">                     <!-- ← REDUNDANTE -->
```

**Síntoma:** Comportamientos extraños, múltiples requests

**Solución:** El componente no debería auto-actualizarse. Solo responde a eventos externos.

---

## Flujo de Navegación (Para Referencia)

```
Usuario hace click en Biblioteca (base.html)
  ↓
hx-get="/partial/sidebar/dashboard"
hx-target="#contextual-sidebar"
hx-swap="innerHTML"
  ↓
Servidor retorna: sidebar_dashboard.html con categorías y cuadernos
  ↓
#contextual-sidebar innerHTML = sidebar_dashboard.html
  ↓
Alpine procesa @click listeners en sidebar_dashboard
  ↓
Usuario hace click en Cuaderno
  ↓
hx-get="/partial/sidebar/notebook/{{ cuaderno.id }}"
hx-target="#contextual-sidebar"
hx-swap="innerHTML"
  ↓
Servidor retorna: sidebar_notebook.html con temas y notas
  ↓
#contextual-sidebar innerHTML = sidebar_notebook.html
  ↓
Alpine procesa x-init y @scroll listeners
  ↓
Usuario hace click en Atrás
  ↓
hx-get="/partial/sidebar/dashboard"
hx-target="#contextual-sidebar"
hx-swap="innerHTML"
  ↓
Volvemos al paso anterior
```

---

## Checklist: Antes de Hacer Cambios HTMX

Si una IA (o tú) necesita modificar componentes con HTMX:

- [ ] ¿Es una navegación principal (Dashboard/Notebook/Inbox)? → usa `innerHTML` a `#contextual-sidebar`
- [ ] ¿Es una edición dentro de una vista? → usa `outerHTML` al ID del componente
- [ ] ¿Cambié algún `hx-swap` existente? → Si sí, **DETENTE y revisa este documento**
- [ ] ¿El endpoint backend retorna el HTML correcto?
- [ ] ¿Testé navegando 2+ veces para verificar no hay conflictos?

---

## Para IAs: Prompts Seguros

Si pides cambios, especifica explícitamente:

```
Modifica sidebar_notebook.html para mostrar notas en tarjetas en lugar de lista.

IMPORTANTE:
- Solo HTML y CSS, SIN cambiar JavaScript
- NO MODIFICAR estos atributos HTMX:
  * hx-target="#notebook-sidebar-container" (línea X)
  * hx-swap="outerHTML" (línea Y)
  
Estos atributos son arquitectónicos. Cambiarlos rompe navegación.

Si necesitas cambiar algo relacionado con HTMX, pregunta primero.
```

---

## Contacto / Preguntas

Si encuentras un bug de navegación:

1. Revisa que `hx-swap` coincida con el patrón (innerHTML para navegación, outerHTML para edición)
2. Verifica que `hx-target` sea correcto
3. Comprueba el endpoint backend retorna HTML válido
4. Lee este documento completamente antes de cambiar nada

---

**Última actualización:** 10 de febrero de 2026
**Status:** 🔒 CRÍTICO - NO CAMBIAR SIN ENTENDER ARQUITECTURA HTMX
