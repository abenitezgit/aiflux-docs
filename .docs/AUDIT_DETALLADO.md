# 🔬 AUDIT TÉCNICO DETALLADO - proyecto-docs

**Fecha:** 10 de febrero de 2026  
**Auditor:** Sistema automático  
**Scope:** Backend, Frontend, Assets, Documentación

---

## 1. ANÁLISIS DE FUNCIONES DUPLICADAS

### 1.1 clearInspector() - DUPLICADA CRÍTICA

**Ubicación 1: `editor.js` línea 106-124**
```javascript
const clearInspector = () => {
    // Limpiar TOC
    const tocContainer = document.querySelector('#note-toc');
    // ... (3 secciones limpias)
};
```
- **Scope:** Local a editor.js (módulo ES6)
- **Uso:** Llamada en listener `note-selected` (línea 350)
- **Accesibilidad:** ❌ NO es global

**Ubicación 2: `base.html` línea 331-349**
```javascript
clearInspector() {
    // Duplicated implementation
    // Limpiar TOC, etiquetas, adjuntos
}
```
- **Scope:** Alpine method en `appShell()`
- **Uso:** Llamada en `switchActiveNote()` (línea 371)
- **Accesibilidad:** ✅ Disponible globalmente en Alpine

**Problema:** Dos implementaciones identicas. Si una cambia, la otra queda obsoleta.

**Solución recomendada:**
1. Hacer `clearInspector` global en editor.js: `window.clearInspector = () => {...}`
2. Remover implementación de base.html
3. Llamarla como `window.clearInspector()` desde switchActiveNote()

---

### 1.2 updateInspector() - CONFLICTO DE SCOPE

**Definición correcta: `editor.js` línea 127**
```javascript
window.updateInspector = (data) => {
    // Manejo de tags, adjuntos
}
```
- ✅ Correctamente expuesta como global
- Usada en 3 lugares:
  - `editor.js` listener (línea 387)
  - `base.html` switchActiveNote (línea 407)
  - `base.html` loadNoteFromQuickView (línea 450)

**Veredicto:** ✅ CORRECTO

---

### 1.3 updateTOC() - CONFLICTO DE SCOPE

**Definición: `editor.js` línea 87**
```javascript
window.updateTOC = (editor) => {
    // Parsing de headings
}
```
- ✅ Correctamente expuesta como global
- Usada en 3 lugares:
  - `editor.js` listener (línea 382)
  - `base.html` switchActiveNote (línea 405)
  - `base.html` loadNoteFromQuickView (línea 448)

**Veredicto:** ✅ CORRECTO

---

## 2. ANÁLISIS DE FLUJOS DE CARGA DE NOTAS

### 2.1 Flujo A: sidebar_cuaderno (notebook mode)

**Trigger:** Click en nota en sidebar_cuaderno  
**Handler:** HTMX o Alpine listener  
**Evento:** Dispara `note-selected` con `{ detail: { id } }`

**Chain:**
```
Click nota → note-selected event → editor.js listener (línea 336)
  ↓
window.isPreventingSave = true
  ↓
fetch(/api/notes/{id})
  ↓
clearInspector() [LOCAL en editor.js]
  ↓
initEditor(contentToLoad) [window.initEditor]
  ↓
updateTOC(editor)
  ↓
updateInspector(data)
  ↓
setTimeout(() => window.isPreventingSave = false, 300)
```

**Protecciones:** ✅
- isPreventingSave activo ANTES de fetch
- initEditor respeta el flag
- Timeout de 300ms antes de desactivar

---

### 2.2 Flujo B: sidebar_inbox (inbox mode)

**Trigger:** Click en tarjeta de nota + confirmar diálogo  
**Handler:** Alpine method `switchActiveNote()`  
**Ubicación:** base.html línea 357-412

**Chain:**
```
Click tarjeta → confirm dialog → switchActiveNote(notaId)
  ↓
window.isPreventingSave = true [AGREGADO RECIENTEMENTE]
  ↓
fetch(/api/notes/{notaId})
  ↓
clearInspector() [Alpine method - base.html]
  ↓
setContent(content) [VÍA ed.commands]
  ↓
updateTOC(ed) [window.updateTOC]
  ↓
updateInspector(nota) [window.updateInspector]
  ↓
setTimeout(() => window.isPreventingSave = false, 300)
```

**Protecciones:** ✅ (Reciente)
- isPreventingSave activo ANTES del fetch
- timeout 300ms

**⚠️ Inconsistencia:** 
- Usa `ed.commands.setContent()` directo
- No usa `window.initEditor()` como sidebar_cuaderno
- Esto es viable porque el flag está activado, pero architecturally diferente

---

## 3. ANÁLISIS DE ESTADO GLOBAL

### 3.1 window.isPreventingSave

**Definición:** `editor.js` línea 47
```javascript
window.isPreventingSave = false;
```

**Usada en:**
1. Editor.js:
   - `saveNoteToServer()` línea 53: check antes de fetch
   - `onUpdate` callback línea 307: check antes de iniciar autosave
   - listener `note-selected`: SET true (342), SET false (393, 409)

2. Base.html:
   - `switchActiveNote()` línea 371: SET true, SET false en timeout

**⚠️ RIESGO:** Race condition si usuario:
1. Abre nota A (flag = true)
2. Inmediatamente abre nota B antes de 300ms
3. Flag se desactiva, pero nota A podría haber causado eventos pendientes

**Recomendación:** 
- Agregar `activeNoteId` check en `onUpdate`:
```javascript
onUpdate: ({ editor }) => {
    if (window.isPreventingSave || this.activeNoteId !== currentNotaId) return;
    // ...
}
```

---

## 4. ANÁLISIS DE ARCHIVOS HUÉRFANOS

### 4.1 inspector2.html

**Ubicación:** `/proyecto-docs/inspector2.html`  
**Tamaño:** ~3.5 KB  
**Propósito:** Mockup/prototipo del Inspector UI  
**Estado:** ❌ NO USADO

**Referencias externas:** Mencionado solo en CONTEXTO_COMPLETO.md (documentación)

**Acción recomendada:**
- Mover a `.archive/inspector2.html` O
- Documentar explícitamente como "experimental/reference"

---

### 4.2 Archivos de documentación obsoletos

#### ESPECIFICACION_QUICKVIEW_INBOX.md
- Fecha: Anterior a últimas correcciones (autosave fix)
- Contenido: Describe implementación que difiere de código actual
- Ejemplo: Menciona `loadNoteInspector()` que no existe

#### CONTEXTO_COMPLETO.md
- Contiene copias de inspector2.html (mockup)
- Contiene código de ESPECIFICACION_QUICKVIEW_INBOX
- Duplica documentación de base.html

**Acción recomendada:**
1. ESPECIFICACION_QUICKVIEW_INBOX.md → Eliminar o reescribir
2. CONTEXTO_COMPLETO.md → Remover secciones duplicadas

---

## 5. ANÁLISIS DE LÓGICA CONDICIONAL

### 5.1 Checks de isPreventingSave

**Ubicación 1:** editor.js línea 307
```javascript
onUpdate: ({ editor }) => { 
    if (window.isPreventingSave) return;
    // ...
}
```
- ✅ Previene autosave durante carga

**Ubicación 2:** editor.js línea 53
```javascript
if (window.isPreventingSave || !window.editor || !window.editor()) return;
```
- ✅ Triple check (flag + global + instancia)

**Ubicación 3:** editor.js línea 442
```javascript
if (window.isPreventingSave) return;
```
- ✅ En listeners de input del título

**Veredicto:** Protecciones bien colocadas

---

## 6. ANÁLISIS DE ASINCRONÍA

### 6.1 Fetch → setContent timing

**Pattern correcto:**
```
fetch() 
  .then(r => r.json())
  .then(data => {
      window.isPreventingSave = true;  // TOO LATE!
      // ...
  })
```

⚠️ **PROBLEMA:** En base.html `switchActiveNote()`, el flag se activa ANTES del fetch (línea 370), pero se desactiva EN el `.then()`. 

**Timing real:**
```
Línea 371: window.isPreventingSave = true
Línea 373: fetch() inicia
Línea 376: .then() callbacks se registran
[FETCH RESPONSE LLEGA]
Línea 385-408: .then() callbacks ejecutan
Línea 409-410: setTimeout desactiva flag en 300ms
```

✅ **CORRECTO:** El flag está activo cuando `setContent()` se ejecuta (dentro del .then)

---

## 7. CHECKLIST DE CONSISTENCIA

| Item | sidebar_notebook | sidebar_inbox | Estado |
|------|------------------|---------------|--------|
| Flag isPreventingSave | ✅ | ✅ | OK |
| clearInspector() | ✅ | ✅ | DUPLICADO |
| updateTOC() | ✅ | ✅ | OK |
| updateInspector() | ✅ | ✅ | OK |
| timeout 300ms | ✅ | ✅ | OK |
| Arquitectura uniforme | event-based | direct-call | INCONSISTENTE |

---

## 8. DEUDA TÉCNICA POR SEVERIDAD

### 🔴 CRÍTICA
- **clearInspector() duplicada:** Riesgo de divergencia
- **Documentación obsoleta:** Causa confusión

### 🟡 MEDIA
- **Flujos inconsistentes:** sidebar_notebook vs sidebar_inbox usan patrones diferentes
- **Archivos huérfanos:** inspector2.html sin propósito claro
- **Race condition potencial:** Multiple note loads simultáneos

### 🟢 BAJA
- **Comentarios desactualizados:** Algunos refieren a funciones antiguas
- **Falta documentación:** Flujo global de flags no documentado

---

## 9. RECOMENDACIONES CONCRETAS (ORDEN DE EJECUCIÓN)

### Fase 1: Crítica (Este sprint)
1. **Unificar clearInspector()**
   - Hacer global en editor.js como `window.clearInspector`
   - Remover de base.html
   - Actualizar calls en switchActiveNote()

2. **Eliminar especificaciones obsoletas**
   - Delete: ESPECIFICACION_QUICKVIEW_INBOX.md
   - Clean: CONTEXTO_COMPLETO.md (remover inspector2.html mockup)

3. **Documentar inspector2.html**
   - Mover a .archive/ con nota de descontinuación

### Fase 2: Mejora (Próximo sprint)
1. **Unificar flujos de carga**
   - Refactor sidebar_inbox switchActiveNote() para usar patrón event-based
   - O: Documentar explícitamente por qué son diferentes

2. **Race condition mitigation**
   - Agregar activeNoteId check en onUpdate callback
   - Considerar mutex o promise queue para carga secuencial

### Fase 3: Documentación (Cuando estable)
1. Crear ARCHITECTURE.md explicando:
   - Flujo de eventos note-selected
   - Patrón isPreventingSave
   - Cómo agregar nuevos contextos de notas

---

## 10. VALIDACIÓN POST-AUDIT

- [ ] clearInspector() duplicación eliminada
- [ ] Especificaciones obsoletas removidas
- [ ] inspector2.html archivado/documentado
- [ ] Tests de carga concurrente pasan
- [ ] Documentación arquitectónica actualizada

---

**Firme de auditor:** Sistema automático  
**Próxima revisión:** Después de implementar Fase 1
