# Fix Correcto: Quick View con Contenido Adecuado

**Fecha:** 10 de febrero de 2026  
**Status:** ✅ CORREGIDO

## Problema que Tenía

Estaba pasando **texto plano** a la ventana flotante del Quick View cuando debería:
1. **Mostrar texto plano en el preview** (para que se vea legible en la ventana flotante)
2. **Pasar JSON a editor Tiptap** cuando se edita (porque es lo que Tiptap entiende)

## Solución Correcta

Siguiendo el mismo patrón que ya existe en `switchActiveNote()`, ahora el Quick View:

### 1. Datos Almacenados (en `floatingNotes`)

```javascript
this.floatingNotes[notaId] = {
    id: notaId,
    titulo: nota.titulo,
    contenidoJson: nota.contenido,        // ← JSON original para editor Tiptap
    contenidoTexto: textoExtraido,        // ← Texto extraído para preview
    x, y, width, height, zIndex
};
```

### 2. Cómo se Usa en el Template

```html
<!-- Mostrar texto plano en ventana flotante -->
<div class="floating-note-content" x-text="nota.contenidoTexto || 'Sin contenido'"></div>

<!-- Botón para editar: usa switchActiveNote que carga el JSON correctamente -->
<button @click="switchActiveNote(notaId); closeFloatingNote(notaId)" class="floating-note-edit-btn">
    <i class="ph ph-pencil"></i> Editar
</button>
```

### 3. Flujo Completo

```
Usuario abre Quick View
  ↓
openQuickView() fetches /api/notes/{notaId}
  ↓
Guarda:
  - contenidoJson: nota.contenido (JSON de Tiptap)
  - contenidoTexto: extractTextFromTiptapJson(nota.contenido) (texto legible)
  ↓
Ventana flotante muestra: contenidoTexto (texto plano, legible)
  ↓
Usuario hace click en "Editar"
  ↓
switchActiveNote(notaId) es llamado
  ↓
switchActiveNote() hace fetch(/api/notes/{notaId})
  ↓
ed.commands.setContent(nota.contenido)  ← ¡AQUÍ! Se pasa el JSON al editor
  ↓
Tiptap carga correctamente el contenido JSON
```

## Por Qué Funciona Ahora

1. **Preview Legible:** Usa `contenidoTexto` que es texto plano extraído con regex
2. **Editor Correcto:** Usa `switchActiveNote()` que ya existe y sabe cómo pasar el JSON a Tiptap
3. **Sin Duplicación:** Reutiliza la lógica existente de `switchActiveNote()`
4. **Consistente:** Mismo flujo que cuando se carga una nota desde el Inbox/Cuaderno

## Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `templates/layouts/base.html` | Modificada `openQuickView()` para guardar `contenidoJson` y `contenidoTexto` |
| `templates/layouts/base.html` | Template del Quick View ahora muestra `contenidoTexto` |
| `templates/layouts/base.html` | Agregado botón "Editar" que llama a `switchActiveNote()` |
| `templates/layouts/base.html` | Agregados estilos CSS para `.floating-note-footer` y `.floating-note-edit-btn` |

## Testing

1. ✅ Abre Inbox
2. ✅ Click en nota → Click en gear → "Quick View"
3. ✅ Ventana flotante muestra TEXTO LEGIBLE (no JSON)
4. ✅ Click en botón "Editar" 
5. ✅ La nota se carga en el editor (no como texto, sino como contenido Tiptap)
6. ✅ El contenido se ve formateado correctamente en el editor

## Lecciones Aprendidas

✅ **Siempre revisar cómo se hace en otro lugar** - `switchActiveNote()` ya tenía la solución  
✅ **No inventar nuevas soluciones** - Reutilizar el código existente  
✅ **Separar presentación de datos** - Preview = texto, Editor = JSON  
✅ **El flujo es clave** - Entender cómo fluyen los datos a través del sistema
