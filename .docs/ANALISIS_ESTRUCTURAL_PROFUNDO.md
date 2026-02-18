# 🏗️ ANÁLISIS ESTRUCTURAL PROFUNDO: Arquitectura del Sistema

## I. VISIÓN GENERAL DE LA ARQUITECTURA

El proyecto "Smart Knowledge OS" es una aplicación fullstack moderna que combina:

- **Backend:** Python (FastAPI/similar framework web)
- **Frontend:** HTML5 + Tailwind CSS + Alpine.js + HTMX + Tiptap
- **Base de Datos:** Estructura relacional (Biblioteca > Cuaderno > Tema > Nota)
- **Patrón UI:** Dashboard central + Editor en 3 columnas + Modales dinámicos

**Principio Arquitectónico Clave:** Fluidez sobre jerarquía — el usuario navega por "Modos" (Inicio, Escritura, Proyectos, Inbox) no por carpetas.

---

## II. ESTRUCTURA DE CAPAS

### **Capa 1: Backend (Python)**
```
backend/
├── main.py              ← Punto de entrada, routers registrados
├── models.py            ← Modelos SQLAlchemy (Biblioteca, Cuaderno, Tema, Nota, Etiqueta)
├── database.py          ← Configuración DB, SessionLocal
├── alembic/             ← Migraciones
├── routes/
│   ├── notas.py         ← CRUD notas
│   ├── modales.py       ← Endpoints que devuelven HTML parcial
│   ├── inbox.py         ← Gestión de inbox
│   ├── search.py        ← Búsqueda y RAG
│   └── ai.py            ← Endpoints IA (sugerencias, análisis)
└── services/
    ├── note_service.py  ← Lógica de negocio notas
    ├── ai_service.py    ← Integración con LLM
    └── search_service.py ← RAG, búsqueda semántica
```

**Responsabilidades:**
- Gestión de datos (CRUD con ORM)
- Autenticación / Autorización (si aplica)
- Migraciones de DB (Alembic)
- APIs REST que devuelven JSON o HTML parcial (templates Jinja2)

### **Capa 2: Frontend (HTML/CSS/JS)**
```
frontend/ (o templates/)
├── base.html            ← Layout principal con appShell() Alpine
├── dashboard/
│   └── index.html       ← Vista inicial, Omnibar central
├── editor/
│   └── index.html       ← Tiptap + Columnas (contexto | editor | IA)
├── modales/
│   ├── modal_inbox_triaje.html
│   ├── modal_crear_nota.html
│   └── modal_editar_etiqueta.html
├── includes/
│   ├── sidebar.html     ← Navegación izquierda
│   ├── header.html      ← Barra superior
│   └── floating_indicators.html ← Puntitos de IA
└── static/
    ├── css/             ← Tailwind compilado
    ├── js/
    │   ├── alpine_init.js ← appShell() y contexto global Alpine
    │   ├── htmx_config.js ← Configuración HTMX
    │   ├── editor_tiptap.js ← Lógica editor
    │   └── search_handler.js ← Búsqueda
    └── icons/           ← SVGs
```

**Responsabilidades:**
- Renderizado de HTML con Jinja2
- Estilos con Tailwind (responsive, tema Zen)
- Interactividad con Alpine.js (estado reactivo)
- Peticiones asincrónicas con HTMX
- Edición rica con Tiptap

---

## III. FLUJOS DE DATOS PRINCIPALES

### **Flujo A: Dashboard → Editor (Carga de Nota)**
```
1. Usuario hace click en una nota en el Dashboard
   ↓
2. Alpine: @click="navigateToNote(id)" 
   - Actualiza appShell.currentView = 'editor'
   - Actualiza appShell.currentNoteId = id
   ↓
3. HTMX: hx-get="/editor/{{ noteId }}" hx-target="main#editor"
   - Backend carga la nota desde DB
   - Devuelve template editor/index.html con datos
   ↓
4. Frontend: Tiptap inicializa con el contenido
   - JavaScript activa los event listeners del editor
   - Alpine.js sincroniza estado local
   ↓
5. Usuario ve editor listo para escribir ✅
```

### **Flujo B: Editor → Guardar Nota**
```javascript
// Estructura global del estado en Alpine.js
function appShell() {
  return {
    // ===== VISTAS/NAVEGACIÓN =====
    currentView: 'dashboard',      // 'dashboard', 'editor', 'projects', 'inbox'
    currentNoteId: null,           // ID de nota en editor
    currentProjectId: null,        // ID de proyecto activo
    
    // ===== ESTADO DE MODALES =====
    modalOpen: false,              // ¿Modal visible?
    modalType: null,               // 'triaje', 'crear_nota', 'editar_etiqueta'
    modalData: {},                 // Datos dinámicos del modal (nota_id, etc)
    
    // ===== INDICADORES DE CARGA =====
    aiLoading: false,              // ¿IA procesando? (muestra puntitos)
    isSaving: false,               // ¿Guardando nota?
    isSearching: false,            // ¿Buscando?
    
    // ===== ESTADO DEL EDITOR =====
    unsavedChanges: false,         // ¿Hay cambios sin guardar?
    lastSaved: null,               // Timestamp último guardado
    editorContent: '',             // Contenido de Tiptap (sincronizado)
    
    // ===== ESTADO UI =====
    sidebarOpen: true,             // ¿Sidebar visible?
    themeMode: 'light',            // 'light', 'dark'
    notificationQueue: [],         // Notificaciones toast
    
    // ===== MÉTODOS DE ESTADO =====
    openModal(type, data = {}) {
      this.modalType = type;
      this.modalData = data;
      this.modalOpen = true;
    },
    
    closeModal() {
      this.modalOpen = false;
      setTimeout(() => {
        this.modalType = null;
        this.modalData = {};
      }, 300); // Después de transición
    },
    
    navigateToEditor(noteId) {
      this.currentView = 'editor';
      this.currentNoteId = noteId;
    },
    
    addNotification(message, type = 'info') {
      this.notificationQueue.push({
        id: Date.now(),
        message,
        type
      });
      setTimeout(() => this.notificationQueue.shift(), 3000);
    }
  };
}
```

### **Componentes de Estado Específicos:**

1. **`currentView`** — Controla qué se muestra (dashboard, editor, proyectos, inbox)
2. **`modalOpen` / `modalType`** — Dictan si modal es visible y qué tipo es
3. **`aiLoading`** — Controla visibilidad de puntitos de IA
4. **`unsavedChanges`** — Indicador de cambios sin guardar
5. **`editorContent`** — Sincroniza Tiptap ↔ Alpine

---

## V. SINCRONIZACIÓN: Alpine ↔ HTMX ↔ Backend

### **Patrón de Comunicación (Event-Driven)**

```
┌─────────────────────────────────────────────────┐
│ USER EVENT                                      │
│ (Click, Input, Scroll)                          │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ ALPINE.JS HANDLER (@click, @input, etc)         │
│ - Actualiza estado local                        │
│ - Opcionalmente llama HTMX                      │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ HTMX REQUEST (hx-get, hx-post)                  │
│ - HTMX prepara petición HTTP                    │
│ - @htmx:before-request (pre-procesamiento)      │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ BACKEND (Python/API)                            │
│ - Procesa lógica de negocio                     │
│ - Lee/escribe en DB                            │
│ - Devuelve JSON o HTML                         │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ HTMX RESPONSE                                   │
│ - Inserta HTML en DOM (@htmx:after-swap)        │
│ - @htmx:after-settle (post-procesamiento)       │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ ALPINE.JS REACTIVITY                            │
│ - Detecta cambios de estado                     │
│ - Re-renderiza UI (x-show, x-if, etc)          │
│ - Ejecuta @htmx handlers                        │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ USER SEES UPDATE                                │
└─────────────────────────────────────────────────┘
```

### **Ejemplo Concreto: Guardar Nota**

```html
<!-- Template HTML (editor.html) -->
<button @click="saveNote()" 
        :disabled="!unsavedChanges">
  💾 Guardar
</button>

<!-- Contenedor con Tiptap -->
<div id="editor-tiptap"
     x-ref="tiptapContainer"
     @input="editorContent = $event.target.innerText; unsavedChanges = true">
</div>
```

```javascript
// En appShell()
async saveNote() {
  this.isSaving = true;
  
  try {
    const response = await fetch(`/api/notes/${this.currentNoteId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: this.noteTitle,
        content: this.editorContent,
        tags: this.noteTags
      })
    });
    
    if (!response.ok) throw new Error('Save failed');
    
    this.unsavedChanges = false;
    this.lastSaved = new Date().toISOString();
    this.addNotification('Nota guardada ✅', 'success');
  } catch (error) {
    this.addNotification('Error guardando ❌', 'error');
  } finally {
    this.isSaving = false;
  }
}
```

---

## VI. PATRONES DE INTEGRACIÓN CLAVE

### **Patrón 1: Modales Dinámicos (HTMX + Alpine)**

```html
<!-- Botón que abre modal -->
<button hx-get="/partial/modal/{{ type }}/{{ id }}"
        hx-target="#modal-content"
        @htmx:before-request="aiLoading = true"
        @htmx:after-settle="aiLoading = false; modalOpen = true"
        @htmx:on-error="aiLoading = false; addNotification('Error cargando modal', 'error')">
  ⚙️ Acciones
</button>

<!-- Contenedor del modal (siempre en el DOM, pero oculto) -->
<div id="modal-container"
     x-show="modalOpen"
     x-cloak
     @click.outside="closeModal()"
     x-transition.opacity>
  
  <div id="modal-content" class="bg-white rounded-lg shadow-lg p-6">
    <!-- HTMX inserta HTML aquí -->
  </div>
</div>
```

**Flujo:**
1. Usuario hace click → `@htmx:before-request` → `aiLoading = true`
2. HTMX GET → Backend devuelve modal_triaje.html
3. HTMX inserta en #modal-content
4. `@htmx:after-settle` → `modalOpen = true`
5. Alpine detecta cambio → `x-show="true"` → Modal visible ✅

---

### **Patrón 2: Búsqueda en Vivo (RAG + HTMX)**

```html
<!-- Campo de búsqueda -->
<input type="text"
       x-model="searchQuery"
       @input="isSearching = true"
       hx-post="/api/search"
       hx-trigger="input changed delay:300ms"
       hx-target="#search-results"
       @htmx:after-settle="isSearching = false"
       placeholder="Buscar notas...">

<!-- Resultados (dinámicos) -->
<div id="search-results"
     x-show="searchQuery.length > 0"
     class="absolute z-10 bg-white border rounded">
  <!-- HTMX inserta resultados aquí -->
</div>

<!-- Indicador de carga -->
<div x-show="isSearching" class="text-gray-500 text-sm">
  🔄 Buscando...
</div>
```

---

### **Patrón 3: Formularios con Validación en Tiempo Real**

```html
<form hx-post="/api/notes"
      @htmx:before-request="validateForm()"
      @htmx:response-error="addNotification('Error en servidor', 'error')">
  
  <input name="title"
         x-model="formData.title"
         @change="validateTitle()"
         required>
  
  <span x-show="formErrors.title" class="text-red-500 text-sm">
    {{ formErrors.title }}
  </span>
  
  <button type="submit"
          :disabled="!isFormValid() || isSaving">
    Crear Nota
  </button>
</form>
```

---

## VII. ESTRUCTURA DE TEMPLATES RECOMENDADA

```
templates/
├── base.html                    ← Base con appShell()
├── dashboard/
│   ├── index.html              ← Vista dashboard
│   ├── card_nota.html          ← Tarjeta individual
│   └── omnibar.html            ← Campo búsqueda central
├── editor/
│   ├── index.html              ← Estructura editor
│   ├── tiptap_editor.html      ← Zona de edición
│   ├── sidebar_contexto.html   ← Columna izquierda
│   └── sidebar_ia.html         ← Columna derecha (sugerencias IA)
├── modales/
│   ├── modal_inbox_triaje.html      ← Triaje de inbox
│   ├── modal_crear_nota.html        ← Crear nueva nota
│   ├── modal_editar_etiqueta.html   ← Editar tags
│   └── modal_confirmacion.html      ← Confirmaciones genéricas
├── includes/
│   ├── header.html             ← Barra superior
│   ├── sidebar.html            ← Navegación izquierda
│   ├── floating_ai.html        ← Indicador IA
│   └── toast_notifications.html ← Sistema de notificaciones
└── static/
    ├── css/
    │   ├── main.css            ← Tailwind compilado
    │   └── custom.css          ← Estilos personalizados
    └── js/
        ├── alpine_init.js      ← Función appShell()
        ├── htmx_config.js      ← Config HTMX
        ├── editor_tiptap.js    ← Lógica Tiptap
        └── utils.js            ← Funciones helpers
```

---

## VIII. CONSIDERACIONES DE RENDIMIENTO

### **Frontend Optimization**
- **Lazy Loading:** Cargar componentes grandes solo cuando se necesitan
- **HTMX Morphdom:** Usar `hx-swap="morph"` para actualizaciones DOM mínimas
- **Alpine Reactivity:** Usar `x-ref` para acceso a elementos sin DOM query
- **Debouncing:** Búsqueda, autoguardado con `delay:500ms` en HTMX

### **Backend Optimization**
- **Caching:** Cache HTTP para assets estáticos
- **DB Queries:** Usar índices en campos de búsqueda/filtrado
- **Async:** Tasks de IA/procesamiento en background (Celery/APScheduler)
- **Pagination:** Limitar resultados en búsquedas grandes

### **Network Optimization**
- **Compresión:** Gzip para responses HTML/JSON
- **Bundling:** Minify CSS/JS en producción
- **WebSockets (opcional):** Para notificaciones en vivo
- **Service Workers:** Offline support (si aplica)

---

## IX. MONITOREO Y DEBUGGING

### **Herramientas Recomendadas**
1. **Browser DevTools:**
   - Network tab: Inspeccionar HTMX requests
   - Console: Ver errores Alpine/HTMX
   - Elements: Inspeccionar DOM changes en vivo

2. **HTMX Debug Mode:**
   ```javascript
   htmx.config.debugLevel = 'info'; // En browser console
   ```

3. **Alpine DevTools Extension** (Chrome/Firefox)
   - Inspecciona estado reactivo en vivo
   - Time-travel debugging

4. **Backend Logging:**
   ```python
   # En main.py o routes
   import logging
   logger = logging.getLogger(__name__)
   logger.info(f"GET /api/search - query='{q}'")
   ```

---

## X. CHECKLIST DE ARQUITECTURA

- [ ] **Base.html:** Contiene `function appShell()` y Alpine.js inicializado
- [ ] **Modales:** Estructura base `#modal-container` + `#modal-content` (HTMX target)
- [ ] **HTMX Events:** Todos los requests tienen `@htmx:before-request` y `@htmx:after-settle`
- [ ] **Alpine State:** Componentes usan state global, no x-init local
- [ ] **Templates:** Separados en componentes reutilizables (includes/)
- [ ] **API Endpoints:** Devuelven HTML parcial (no layout completo) para HTMX
- [ ] **CSS:** Tailwind aplicado; responsive en móvil
- [ ] **Error Handling:** Try-catch en JS, HTTP status codes en backend
- [ ] **Notificaciones:** Sistema toast para feedback al usuario
- [ ] **Docs:** Cada componente documentado (qué hace, qué estado usa)
