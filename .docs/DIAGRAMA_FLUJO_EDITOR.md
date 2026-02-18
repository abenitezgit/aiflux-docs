# 📊 DIAGRAMA DE FLUJO - Editor Tiptap

**Proyecto:** proyecto-docs  
**Tema:** Reactividad del Editor + Actualización de Barra  

---

## 1️⃣ FLUJO DE INICIALIZACIÓN

```
┌─────────────────────────────────────────────────────┐
│          CARGA DEL PÁGINA (DOMContentLoaded)        │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   Alpine.js carga    │
        │  appShell() función  │
        └──────────┬───────────┘
                   │
                   ├─ editorTick = 0
                   ├─ activeNoteId = ""
                   └─ mode = 'dashboard'
                   │
                   ▼
        ┌──────────────────────┐
        │  HTMX carga sidebar  │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  editor.js (módulo)  │
        │      importa         │
        │    Tiptap v3 CDN     │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  DOMContentLoaded    │
        │   en editor.js       │
        │                      │
        │  initEditor()        │
        │  → crea Editor()     │
        │  → 18 extensiones    │
        │  → event listeners   │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   Editor LISTO       │
        │  (vacío o cargar)    │
        └──────────────────────┘
```

---

## 2️⃣ FLUJO DE ESCRITURA Y REACTIVIDAD

```
┌──────────────────────────────────────────────────────────┐
│  USUARIO ESCRIBE O FORMATEA EN EL EDITOR                │
│  (ej: selecciona texto y presiona Ctrl+B)               │
└───────────────────┬──────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ Tiptap procesa cambio │
        │ (internal state)      │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ onUpdate({editor})    │
        │ dispara (callback)    │
        └───────────┬───────────┘
                    │
                    ├─ updateTOC(editor)
                    │  └─ Actualiza tabla contenidos
                    │
                    ├─ app.editorTick++
                    │  └─ ⭐ INCREMENTA REACTIVE PROPERTY
                    │
                    ├─ clearTimeout(saveTimeout)
                    │
                    └─ saveTimeout = setTimeout(...)
                       └─ Autosave después 1.5s
                    │
                    ▼
        ┌───────────────────────┐
        │ Alpine.js DETECTA     │
        │ editorTick ha cambiado│
        │                       │
        │ (reactivity trigger)  │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ activeStyles()        │
        │ se re-evalúa          │
        │                       │
        │ retorna:              │
        │ this.editorTick &&    │
        │ editor()              │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ Cada :class binding   │
        │ se actualiza:         │
        │                       │
        │ :class="activeStyles()│
        │  && editor()          │
        │  .isActive('bold')"   │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ editor().isActive()   │
        │ evalúa estado actual  │
        │                       │
        │ ✅ true  → bold ON   │
        │ ❌ false → bold OFF  │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ Clase CSS actualizada │
        │                       │
        │ SI activo:            │
        │ 'bg-indigo-500/20 ... '│
        │                       │
        │ SI inactivo:          │
        │ 'text-slate-400 ...   '│
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  BOTÓN SE ILUMINA ✅  │
        │                       │
        │  (background indigo)  │
        │  (o se oscurece)      │
        └───────────────────────┘

        LATENCIA: < 15ms (instantáneo)
```

---

## 3️⃣ FLUJO DE AUTOSAVE

```
┌──────────────────────────────────────┐
│  onUpdate() en editor.js             │
│  (de Tiptap event)                   │
└───────────┬──────────────────────────┘
            │
            ▼
    ┌────────────────────────┐
    │ clearTimeout()         │
    │ cancela timer anterior │
    │ (si existía)           │
    └───────┬────────────────┘
            │
            ▼
    ┌────────────────────────┐
    │ setTimeout(() => {     │
    │   saveNoteToServer()   │
    │ }, 1500)               │
    │                        │
    │ ESPERA 1.5 segundos    │
    │ sin más cambios        │
    └───────┬────────────────┘
            │
            ▼ (si no escribe más)
    ┌────────────────────────┐
    │ saveNoteToServer()     │
    │ ejecuta                │
    └───────┬────────────────┘
            │
            ├─ statusLabel = "Guardando..."
            │
            ├─ fetch PATCH /api/notes/{id}
            │  {
            │    "titulo": "...",
            │    "contenido": JSON.stringify(...)
            │  }
            │
            └─ statusLabel = "Guardado" (2s)

        RESULTADO: Contenido persistido en servidor ✅
```

---

## 4️⃣ FLUJO DE DETECCIÓN DE ESTILOS

```
┌─────────────────────────────────────────────────────┐
│  Cada botón en la barra tiene:                      │
│                                                     │
│  :class="activeStyles() &&                          │
│          editor().isActive('formato')"              │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │ activeStyles() evalúa:   │
    │                          │
    │ this.editorTick &&       │
    │ typeof editor === 'fn' &&│
    │ editor()                 │
    │                          │
    │ Retorna: editor instance │
    │ o undefined              │
    └──────────┬───────────────┘
               │
         Truthy? (editor existe)
               │
        ┌──────┴──────┐
        │             │
        ▼ SÍ         ▼ NO
    ┌────────────┐  ┌─────────┐
    │ Evalúa:   │  │ Clase   │
    │           │  │ por     │
    │ editor(). │  │ defecto │
    │ isActive( │  │ (gris)  │
    │ 'bold')   │  └─────────┘
    │           │
    │ true/false│
    └────┬──────┘
         │
      ┌──┴──────────┐
      │             │
      ▼ TRUE       ▼ FALSE
    ┌──────────┐  ┌──────────┐
    │ bg-ind-  │  │ text-    │
    │ igo-500  │  │ slate-4  │
    │ /20 +    │  │ 00 +     │
    │ text-ind │  │ hover... │
    │ igo-400  │  │          │
    └──────────┘  └──────────┘
         │             │
         └──────┬──────┘
                │
                ▼
        ┌──────────────────┐
        │ Botón renderizado│
        │ con clase final  │
        └──────────────────┘
```

---

## 5️⃣ CICLO DE VIDA COMPLETO (Timeline)

```
SEGUNDO 0:
┌─────────────────────────────────────────┐
│ User abre página                        │
│                                         │
│ 1. HTML se parsea                       │
│ 2. Alpine.js carga (defer)              │
│ 3. HTMX carga (defer)                   │
│ 4. editor.js carga (módulo)             │
│ 5. DOMContentLoaded → initEditor()      │
└─────────────────────────────────────────┘

SEGUNDO 0-5:
┌─────────────────────────────────────────┐
│ User navega a nota                      │
│                                         │
│ 1. Dispara 'note-selected'              │
│ 2. Fetch /api/notes/{id}                │
│ 3. Obtiene contenido JSON/HTML          │
│ 4. initEditor(contentToLoad)            │
│ 5. updateTOC() y updateInspector()      │
│ 6. Editor cargado con contenido         │
└─────────────────────────────────────────┘

SEGUNDO 5-15:
┌─────────────────────────────────────────┐
│ User escribe/formatea                   │
│                                         │
│ 5.1s - Escribe "Hola" (5 keypress)     │
│        → onUpdate x 5 dispara           │
│        → editorTick incrementa x5       │
│        → Alpine detecta cambio          │
│        → activeStyles() re-evalúa       │
│        → Botones no muestran cambio     │
│          (no hay formato aplicado)      │
│                                         │
│ 6.0s - Selecciona "Hola"               │
│        → onUpdate dispara               │
│        → editorTick++                   │
│        → editor().isActive('...')       │
│          retorna false (sin formato)    │
│        → Botones permanecen grises      │
│                                         │
│ 6.2s - Ctrl+B (aplica bold)            │
│        → onUpdate dispara               │
│        → editorTick++ (crucialmente)    │
│        → Alpine detecta cambio          │
│        → activeStyles() se re-evalúa    │
│        → editor().isActive('bold')      │
│          retorna TRUE                   │
│        → Botón Bold: clase cambia a     │
│          'bg-indigo-500/20 ...'         │
│        → BOTÓN SE ILUMINA ✨            │
│                                         │
│ 7.7s - User para de escribir           │
│        → Timer saveTimeout (1.5s)       │
│          expira                         │
│        → saveNoteToServer() ejecuta     │
│        → statusLabel = "Guardando..."   │
│        → Fetch PATCH /api/notes/{id}    │
│        → Respuesta 200 OK               │
│        → statusLabel = "Guardado"       │
│        → (fade out en 2s)               │
└─────────────────────────────────────────┘
```

---

## 6️⃣ ARQUITECTURA DE COMPONENTES

```
                    ┌─────────────────────┐
                    │   APP SHELL          │
                    │  (Alpine.js)         │
                    │                      │
                    │ • mode               │
                    │ • activeNoteId       │
                    │ • editorTick ← ⭐    │
                    │ • zenMode            │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
        ┌────────────┐  ┌──────────┐  ┌─────────────┐
        │ EDITOR.JS  │  │BASE.HTML │  │ BACKEND API │
        │  (335 ln)  │  │(758 ln)  │  │   /api/... │
        │            │  │          │  │             │
        │ • Editor   │  │ • Toolbar│  │ PATCH notes │
        │   instance │  │ • Alpine │  │             │
        │            │  │   binds  │  │ GET notes   │
        │ • onUpdate │  │          │  │             │
        │   handler  │  │ • CSS    │  │ POST upload │
        │            │  │   styles │  │             │
        │ • Autosave │  │          │  │             │
        │   logic    │  │ • Modals │  │             │
        │            │  │   dropd. │  │             │
        │ • Ext.     │  │          │  │             │
        │   configs  │  │ • Events │  │             │
        │            │  │   listeners  │             │
        └────────────┘  └──────────┘  └─────────────┘
             │               │              │
             └───────┬───────┴──────────────┘
                     │
              ┌──────▼──────┐
              │   Tiptap    │
              │   v3 (CDN)  │
              │             │
              │ • 18 ext    │
              │ • ProseMr   │
              │ • 6 langs   │
              └─────────────┘
```

---

## 7️⃣ PUNTOS CRÍTICOS

```
❌ PUEDE FALLAR SI:
├─ No hay "app.editorTick++" en onUpdate()
│  └─ Barra no se actualiza (no hay trigger)
│
├─ activeStyles() retorna undefined
│  └─ :class bindings no se evalúan
│
├─ Editor no se inicializa correctamente
│  └─ window.editor() es null
│
├─ Extensión no está cargada en array
│  └─ El comando no existe, error en console
│
└─ API endpoint /api/notes/{id} no responde
   └─ Autosave falla, contenido se pierde


✅ PARA FUNCIONAR CORRECTAMENTE:
├─ Alpine.js debe estar cargado ANTES de el código
│  └─ <script defer src="alpine..."></script>
│
├─ HTMX debe estar cargado DESPUÉS de Alpine
│  └─ <script defer src="htmx..."></script>
│
├─ editor.js debe estar en <script type="module">
│  └─ <script type="module" src="editor.js"></script>
│
├─ Todos los comandos deben estar con chain().focus()
│  └─ editor().chain().focus().toggleBold().run()
│
└─ El evento htmx:afterSettle debe procesar Alpine
   └─ document.addEventListener('htmx:afterSettle', ...)
```

---

## 8️⃣ MEJORAS FUTURAS

```
ACTUAL (✅ Implementado):
├─ Reactividad automática de barra
├─ 18 extensiones
├─ Autosave con debounce
├─ Markup JSON
└─ Tablas + Imágenes

MEJORAS POSIBLES (⏳ TODO):
├─ Undo/Redo con visualización
├─ Colaboración en tiempo real
├─ Comentarios inline
├─ Versioning de notas
├─ Búsqueda full-text
├─ Tags automáticos (IA)
├─ Comandos slash (/)
├─ Modo presentación
├─ Export a PDF/Markdown
├─ Integración con OpenAI
└─ Analytics de uso
```

---

**Diagrama de Flujo - 9 de febrero de 2026**  
**Proyecto: proyecto-docs (Smart Knowledge OS)**
