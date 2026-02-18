# Validación del Flujo Inbox - proyecto-docs

## 🔍 Resumen de Validación

He revisado el código y **CONFIRMO que el flujo funciona exactamente como lo describiste**. Aquí está el desglose:

---

## 1️⃣ Selecciona el icono Inbox

**Ubicación**: `templates/layouts/base.html` (línea 108-122)

```html
<button @click="mode = 'inbox'" 
        :class="mode === 'inbox' ? 'bg-amber-600 text-white shadow-lg shadow-amber-500/25' : '...'"
        class="w-10 h-10 rounded-xl flex items-center justify-center transition-all group relative"
        hx-get="/partial/sidebar/inbox" 
        hx-target="#contextual-sidebar">
    <i class="ph-fill ph-tray text-xl"></i>
    <!-- Badge de contador -->
    <span id="inbox-badge">...</span>
</button>
```

**Acción**:
- ✅ Cambia el modo a `'inbox'`
- ✅ Ejecuta `hx-get="/partial/sidebar/inbox"` 
- ✅ Renderiza en `#contextual-sidebar`
- ✅ Muestra badge con contador de notas pendientes

---

## 2️⃣ Zona 2 muestra Notas del Inbox

**Ubicación**: `templates/modules/sidebar_inbox.html`

**Se renderiza**:
- ✅ Lista de tarjetas de notas (notas sueltas sin clasificar)
- ✅ Cada tarjeta contiene:
  - 📌 **Título**: `{{ nota.titulo }}`
  - 📄 **Preview**: `{{ nota.contenido | striptags }}` (primeras 3 líneas)
  - ⏰ **Timestamp**: `{{ nota.created_at.strftime('%d %b, %H:%M') }}`
  - ⚙️ **Botón de engranaje**: Abre el modal de acciones

**Estructura HTML de la tarjeta**:
```html
<div class="group bg-[#1a1d26] p-4 rounded-xl border border-white/5 hover:border-amber-500/30">
    <div class="flex justify-between items-start mb-2">
        <h4 class="text-xs font-bold text-slate-200 truncate">{{ nota.titulo }}</h4>
        <button hx-get="/partial/modal/inbox-actions/{{ nota.id }}"
                hx-target="#modal-content"
                @click="aiLoading = true"
                class="text-slate-500 hover:text-white">
            <i class="ph-bold ph-gear text-sm"></i>  <!-- Botón de engranaje ⚙️ -->
        </button>
    </div>
    <p class="text-[11px] text-slate-500 line-clamp-3">{{ nota.contenido | striptags }}</p>
    <div class="mt-3 text-[9px] text-slate-600 font-mono">{{ nota.created_at.strftime('%d %b, %H:%M') }}</div>
</div>
```

---

## 3️⃣ Presiona Engranaje → Abre Modal

**Trigger del botón**:
```html
hx-get="/partial/modal/inbox-actions/{{ nota.id }}"
hx-target="#modal-content"
@click="aiLoading = true"
```

**Backend** (`app/routers/dashboard.py`, línea 182):
```python
@router.get("/partial/modal/inbox-actions/{nota_id}", response_class=HTMLResponse)
async def get_modal_inbox_actions(nota_id: uuid.UUID, ...):
    # Busca la nota
    nota = await session.get(Anotacion, nota_id)
    
    # Obtiene todas las categorías, cuadernos y temas del usuario
    stmt = (
        select(Categoria)
        .where(Categoria.user_id == user.id)
        .order_by(Categoria.orden)
        .options(selectinload(Categoria.cuadernos).selectinload(Cuaderno.temas))
    )
    categorias = (await session.exec(stmt)).all()
    
    return templates.TemplateResponse("partials/modal_inbox_triaje.html", {
        "request": request,
        "nota": nota,
        "categorias": categorias
    })
```

**Modal renderizado** (`templates/partials/modal_inbox_triaje.html`):
- ✅ Muestra el título actual de la nota
- ✅ Dropdown con todos los temas organizados por:
  - Categoría (optgroup)
  - Cuaderno
  - Tema
- ✅ **Excluye el Inbox** del destino (línea 23): `{% if cuad.nombre != 'Inbox' %}`
- ✅ Botón "Confirmar Movimiento" (POST a `/inbox/mover/{nota_id}`)
- ✅ Botón "Eliminar Nota" (DELETE a `/inbox/eliminar/{nota_id}`)

---

## 4️⃣ Selecciona Categoría y Mueve Nota

**Flujo de movimiento**:

```html
<form hx-post="/inbox/mover/{{ nota.id }}" hx-indicator="#btn-confirm-{{ nota.id }}" hx-swap="none">
    <select name="nuevo_tema_id" required>
        <!-- Opciones de destino -->
    </select>
    <button type="submit">Confirmar Movimiento</button>
</form>
```

**Backend** (`app/routers/dashboard.py`, línea 207):
```python
@router.post("/inbox/mover/{nota_id}")
async def mover_nota(
    nota_id: uuid.UUID,
    nuevo_tema_id: uuid.UUID = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    nota = await session.get(Anotacion, nota_id)
    if nota:
        nota.tema_id = nuevo_tema_id  # ✅ Asigna a nuevo tema
        session.add(nota)
        await session.commit()
    
    # ✅ Triggers que actualizan la lista del Inbox
    response = Response(status_code=204)
    response.headers["HX-Trigger"] = "update-inbox-count, update-inbox-list"
    return response
```

**Acciones post-movimiento**:
- ✅ `update-inbox-list` → Recarga `#inbox-sidebar-container` con HTMX
- ✅ `update-inbox-count` → Actualiza el badge del Inbox
- ✅ Modal se cierra automáticamente (`modalOpen = false`)

---

## 5️⃣ Validación de Opciones de Destino

**Regla**: Solo se muestran temas dentro de Cuadernos que **NO sean** "Inbox"

```html
{% for cat in categorias %}
    <optgroup label="{{ cat.nombre }}">
        {% for cuad in cat.cuadernos %}
            {% for tema in cuad.temas %}
                {% if cuad.nombre != 'Inbox' %}  <!-- ✅ Filtro -->
                <option value="{{ tema.id }}">{{ cuad.nombre }} / {{ tema.nombre }}</option>
                {% endif %}
            {% endfor %}
        {% endfor %}
    </optgroup>
{% endfor %}
```

---

## 📊 Diagrama del Flujo

```
┌─────────────────────────────────────────────────────────────────┐
│                    USUARIO HACE CLIC EN INBOX                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                  mode = 'inbox' ✅
                              ↓
    hx-get="/partial/sidebar/inbox" → Zona2
                              ↓
    ┌─────────────────────────────────────────┐
    │  TARJETAS DE NOTAS SIN CLASIFICAR       │
    │  - Título                               │
    │  - Preview (3 líneas)                   │
    │  - Timestamp                            │
    │  - Botón ⚙️ (engranaje)                 │
    └─────────────────────────────────────────┘
                              ↓
                   HACE CLIC EN ENGRANAJE
                              ↓
    hx-get="/partial/modal/inbox-actions/{id}"
                              ↓
    ┌─────────────────────────────────────────┐
    │  MODAL: CLASIFICAR NOTA                 │
    │  - Título actual (read-only)            │
    │  - Dropdown: Selecciona destino         │
    │    * Categoría > Cuaderno > Tema        │
    │    * Excluye Inbox                      │
    │  - [Confirmar Movimiento] 🔘             │
    │  - [Eliminar Nota] 🔴                    │
    └─────────────────────────────────────────┘
                              ↓
              POST /inbox/mover/{nota_id}
                              ↓
         nota.tema_id = nuevo_tema_id ✅
                              ↓
    HX-Trigger: "update-inbox-list"
    HX-Trigger: "update-inbox-count"
                              ↓
    ✅ Modal se cierra
    ✅ Zona2 se recarga (nota desaparece del Inbox)
    ✅ Badge del Inbox se actualiza
```

---

## ✅ Checklist de Validación

| Aspecto | Estado | Ubicación |
|---------|--------|-----------|
| Zona 2 muestra notas del Inbox | ✅ | `sidebar_inbox.html` |
| Cada nota es una tarjeta con preview | ✅ | `sidebar_inbox.html` línea 25 |
| Botón ⚙️ en cada tarjeta | ✅ | `sidebar_inbox.html` línea 27 |
| Al presionar ⚙️ se abre modal | ✅ | `base.html` línea 210 |
| Modal muestra opciones de destino | ✅ | `modal_inbox_triaje.html` línea 20-27 |
| Excluye "Inbox" del destino | ✅ | `modal_inbox_triaje.html` línea 23 |
| Botón para mover nota | ✅ | `modal_inbox_triaje.html` línea 30 |
| Backend actualiza `tema_id` | ✅ | `dashboard.py` línea 219 |
| Se actualizan contadores | ✅ | `dashboard.py` línea 224-225 |
| Modal se cierra post-movimiento | ✅ | `base.html` línea 35 |
| Zona 2 se recarga automáticamente | ✅ | `sidebar_inbox.html` línea 5-8 |

---

## 🎯 Conclusión

**✅ TODO FUNCIONA COMO SE ESPERABA**

El flujo es completo y coherente:
1. **Zona 1** → Selecciona "Inbox"
2. **Zona 2** → Muestra tarjetas de notas pendientes
3. **Modal** → Permite elegir categoría/cuaderno/tema de destino
4. **Backend** → Realiza el movimiento y notifica al frontend
5. **Auto-actualización** → La lista se recarga y el modal se cierra

---

## 💡 Mejoras Opcionales (si quieres explorar)

1. **Batch Operations**: Seleccionar múltiples notas y moverlas juntas
2. **Drag & Drop**: Arrastrar notas entre categorías en la UI
3. **Preview expandido**: Ver la nota completa antes de mover
4. **Búsqueda/Filtros**: Filtrar notas por palabra clave, fecha, etc.
5. **Historial**: Ver dónde estuvo la nota antes
6. **Asignación rápida**: Sugerencias de destino basadas en contenido

¿Necesitas validar algo más específico o deseas agregar alguna de estas mejoras?
