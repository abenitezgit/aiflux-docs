# 📋 ESPECIFICACIÓN: Sistema de Quick View Flotante + Inbox Menu

## Resumen
Transformar el botón engranaje del Inbox en un menú contextual de 3 opciones, e implementar un sistema de "Quick View" flotante para previsualizar notas sin cambiar la nota activa.

---

## 1. MENÚ CONTEXTUAL DEL ENGRANAJE (Zona 2 - Inbox)

### Ubicación
`templates/modules/sidebar_inbox.html` - En cada tarjeta de nota

### Estructura
```html
<!-- Reemplazar el botón engranaje actual -->
<div class="gear-menu-container">
    <button class="gear-button" @click="toggleGearMenu($event, '{{ nota.id }}')">
        <i class="ph ph-gear"></i>
    </button>
    
    <div class="gear-dropdown" x-show="activeGearMenu === '{{ nota.id }}'">
        <button @click="openQuickView('{{ nota.id }}')">
            <i class="ph ph-eye"></i> Quick View
        </button>
        <button @click="$dispatch('open-modal-mover-nota', { id: '{{ nota.id }}' })">
            <i class="ph ph-arrow-right"></i> Mover Nota
        </button>
        <button @click="confirmDeleteNota('{{ nota.id }}')">
            <i class="ph ph-trash"></i> Eliminar Nota
        </button>
    </div>
</div>
```

### Comportamiento Alpine
```javascript
appShell() {
    return {
        // ... estado existente ...
        activeGearMenu: null, // Cuál engranaje está abierto
        
        toggleGearMenu(event, notaId) {
            event.stopPropagation();
            this.activeGearMenu = this.activeGearMenu === notaId ? null : notaId;
        },
        
        openQuickView(notaId) {
            // Ver sección 2 abajo
            this.createFloatingNote(notaId);
            this.activeGearMenu = null;
        },
        
        confirmDeleteNota(notaId) {
            if (confirm('¿Eliminar esta nota del Inbox?')) {
                this.deleteInboxNota(notaId);
            }
            this.activeGearMenu = null;
        },
        
        deleteInboxNota(notaId) {
            htmx.ajax('DELETE', `/inbox/eliminar/${notaId}`, {
                handler: (xhr) => {
                    // Actualizar lista del Inbox
                    document.body.dispatchEvent(
                        new CustomEvent('update-inbox-list')
                    );
                    // Actualizar contador
                    document.body.dispatchEvent(
                        new CustomEvent('update-inbox-count')
                    );
                }
            });
        }
    }
}
```

### CSS
```css
.gear-menu-container {
    position: relative;
}

.gear-button {
    opacity: 0;
    transition: opacity 0.2s;
    cursor: pointer;
}

/* Mostrar engranaje al pasar el mouse */
.note-card:hover .gear-button {
    opacity: 1;
}

.gear-dropdown {
    position: absolute;
    top: 100%;
    right: 0;
    background: #1a1d26;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
    padding: 0.5rem;
    min-width: 180px;
    z-index: 100;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
}

.gear-dropdown button {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    width: 100%;
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
    color: #cbd5e1;
    background: transparent;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
}

.gear-dropdown button:hover {
    background: rgba(99, 102, 241, 0.1);
    color: #818cf8;
}

.gear-dropdown button:active {
    transform: scale(0.95);
}
```

---

## 2. QUICK VIEW FLOTANTE (Zona 3/4 - Flotante)

### Concepto
- Ventana flotante, resizable, movible
- Muestra previsualización de nota (título + primeras líneas)
- Múltiples simultáneamente permitidas
- Solo se cierra manualmente (X)
- No interfiere con nota activa

### Estructura HTML
```html
<!-- base.html: Agregar contenedor para flotantes -->
<div id="floating-notes-container" class="fixed inset-0 pointer-events-none">
    <!-- Las notas flotantes se agregan aquí dinámicamente -->
</div>
```

### Template de Flotante
```html
<!-- templates/partials/floating_note.html -->
<div class="floating-note-window" 
     @mousedown.prevent="startDragFloatingNote($event, '{{ nota.id }}')"
     :style="{
         left: floatingNotes['{{ nota.id }}'].x + 'px',
         top: floatingNotes['{{ nota.id }}'].y + 'px',
         width: floatingNotes['{{ nota.id }}'].width + 'px',
         height: floatingNotes['{{ nota.id }}'].height + 'px',
         zIndex: floatingNotes['{{ nota.id }}'].zIndex
     }">
    
    <!-- HEADER (Arrastra) -->
    <div class="floating-note-header">
        <h4 class="floating-note-title">{{ nota.titulo }}</h4>
        <button @click="closeFloatingNote('{{ nota.id }}')">
            <i class="ph ph-x"></i>
        </button>
    </div>
    
    <!-- CONTENIDO (Previsualización) -->
    <div class="floating-note-content">
        {{ nota.contenido | truncate(500) }}
    </div>
    
    <!-- RESIZER (Esquina inferior derecha) -->
    <div class="floating-note-resizer"
         @mousedown.prevent="startResizeFloatingNote($event, '{{ nota.id }}')">
    </div>
</div>
```

### Comportamiento Alpine (en appShell)
```javascript
appShell() {
    return {
        // ... estado existente ...
        floatingNotes: {}, // { notaId: { x, y, width, height, zIndex, isDragging, ... } }
        draggingNoteId: null,
        dragOffset: { x: 0, y: 0 },
        
        createFloatingNote(notaId) {
            // Verificar si ya está abierta
            if (this.floatingNotes[notaId]) {
                // Si ya existe, traerla al frente
                this.floatingNotes[notaId].zIndex = this.getMaxZIndex() + 1;
                return;
            }
            
            // Cargar datos de la nota
            fetch(`/api/notes/${notaId}`)
                .then(r => r.json())
                .then(nota => {
                    // Posición aleatoria pero visible
                    const x = Math.random() * (window.innerWidth - 400);
                    const y = Math.random() * (window.innerHeight - 300) + 50;
                    
                    this.floatingNotes[notaId] = {
                        id: notaId,
                        titulo: nota.titulo,
                        contenido: nota.contenido,
                        x: x,
                        y: y,
                        width: 400,
                        height: 500,
                        zIndex: this.getMaxZIndex() + 1,
                        isDragging: false,
                        isResizing: false
                    };
                });
        },
        
        closeFloatingNote(notaId) {
            delete this.floatingNotes[notaId];
        },
        
        startDragFloatingNote(event, notaId) {
            const noteData = this.floatingNotes[notaId];
            this.draggingNoteId = notaId;
            this.dragOffset = {
                x: event.clientX - noteData.x,
                y: event.clientY - noteData.y
            };
            
            document.addEventListener('mousemove', this.dragFloatingNote.bind(this));
            document.addEventListener('mouseup', this.stopDragFloatingNote.bind(this));
        },
        
        dragFloatingNote(event) {
            if (!this.draggingNoteId) return;
            
            const noteData = this.floatingNotes[this.draggingNoteId];
            noteData.x = event.clientX - this.dragOffset.x;
            noteData.y = event.clientY - this.dragOffset.y;
        },
        
        stopDragFloatingNote() {
            this.draggingNoteId = null;
            document.removeEventListener('mousemove', this.dragFloatingNote);
            document.removeEventListener('mouseup', this.stopDragFloatingNote);
        },
        
        startResizeFloatingNote(event, notaId) {
            event.stopPropagation();
            const noteData = this.floatingNotes[notaId];
            const startX = event.clientX;
            const startY = event.clientY;
            const startWidth = noteData.width;
            const startHeight = noteData.height;
            
            const handleResize = (e) => {
                noteData.width = Math.max(300, startWidth + (e.clientX - startX));
                noteData.height = Math.max(200, startHeight + (e.clientY - startY));
            };
            
            const stopResize = () => {
                document.removeEventListener('mousemove', handleResize);
                document.removeEventListener('mouseup', stopResize);
            };
            
            document.addEventListener('mousemove', handleResize);
            document.addEventListener('mouseup', stopResize);
        },
        
        getMaxZIndex() {
            return Math.max(
                0,
                ...Object.values(this.floatingNotes).map(n => n.zIndex || 0)
            );
        }
    }
}
```

### CSS
```css
#floating-notes-container {
    z-index: 1000;
    pointer-events: auto;
}

.floating-note-window {
    position: fixed;
    background: #1a1d26;
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 0.75rem;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), 
                0 0 20px rgba(99, 102, 241, 0.2);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    transition: box-shadow 0.2s;
}

.floating-note-window:hover {
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), 
                0 0 30px rgba(99, 102, 241, 0.4);
}

.floating-note-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
    background: rgba(99, 102, 241, 0.1);
    border-bottom: 1px solid rgba(99, 102, 241, 0.2);
    cursor: move;
    user-select: none;
}

.floating-note-title {
    font-size: 0.875rem;
    font-weight: 600;
    color: #e2e8f0;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
}

.floating-note-header button {
    background: transparent;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    padding: 0.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.floating-note-header button:hover {
    color: #f87171;
}

.floating-note-content {
    flex: 1;
    padding: 1rem;
    overflow-y: auto;
    font-size: 0.875rem;
    line-height: 1.6;
    color: #cbd5e1;
}

.floating-note-resizer {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 20px;
    height: 20px;
    cursor: nwse-resize;
    background: linear-gradient(135deg, 
                transparent 0%, 
                transparent 50%, 
                rgba(99, 102, 241, 0.3) 50%);
}

.floating-note-resizer:hover {
    background: linear-gradient(135deg, 
                transparent 0%, 
                transparent 50%, 
                rgba(99, 102, 241, 0.6) 50%);
}
```

---

## 3. CAMBIO DE NOTA ACTIVA (Zona 2 - Click en tarjeta)

### Ubicación
`templates/modules/sidebar_inbox.html` - Click en área general de tarjeta (NO engranaje)

### Comportamiento
```javascript
// En appShell()
switchActiveNote(newNoteId) {
    if (this.activeNoteId === newNoteId) {
        return; // Misma nota, no hacer nada
    }
    
    // SIEMPRE preguntar (según especificación)
    if (confirm(`¿Cambiar a nota: "${notaTitulo}"?`)) {
        this.activeNoteId = newNoteId;
        
        // Cargar nota en editor
        fetch(`/api/notes/${newNoteId}`)
            .then(r => r.json())
            .then(nota => {
                // Actualizar editor (zona 3)
                document.getElementById('note-title-input').value = nota.titulo;
                document.getElementById('tiptap-content').innerHTML = nota.contenido;
                
                // Actualizar inspector (zona 4)
                this.loadNoteInspector(newNoteId);
            });
    }
}
```

### HTML (Tarjeta Inbox)
```html
<!-- Hacer que TODA la tarjeta sea clickeable, excepto el engranaje -->
<div class="note-card" @click.self="switchActiveNote('{{ nota.id }}')">
    <!-- Contenido de la tarjeta -->
    <h4>{{ nota.titulo }}</h4>
    <p>{{ nota.preview }}</p>
    
    <!-- El engranaje NO se ve afectado por este click -->
    <div class="gear-menu-container" @click.stop>
        <!-- Menú contextual -->
    </div>
</div>
```

---

## 4. ACTUALIZACIÓN DE LISTA (Después de eliminar/mover)

### En appShell()
```javascript
deleteInboxNota(notaId) {
    htmx.ajax('DELETE', `/inbox/eliminar/${notaId}`, {
        handler: (xhr) => {
            // 1. Recargar lista del Inbox
            document.body.dispatchEvent(
                new CustomEvent('update-inbox-list')
            );
            
            // 2. Actualizar contador en zona 1
            document.body.dispatchEvent(
                new CustomEvent('update-inbox-count')
            );
            
            // 3. Si la nota eliminada era la activa, volver a dashboard
            if (this.activeNoteId === notaId) {
                this.activeNoteId = null;
                this.mode = 'dashboard';
            }
        }
    });
}
```

---

## 5. ENDPOINTS NECESARIOS (Backend)

### DELETE /inbox/eliminar/{nota_id}
- Eliminar nota del inbox
- Retornar: `{ success: true }`

### POST /inbox/mover/{nota_id}
- Ya existe (modal actual)
- Solo cambiar target a modal

### GET /api/notes/{nota_id} (mejorar)
- Ya existe
- Asegurar que devuelve: `{ id, titulo, contenido, tema, cuaderno, ... }`

---

## 6. CHECKLIST DE IMPLEMENTACIÓN

- [ ] Crear menú contextual en engranaje (CSS + Alpine)
- [ ] Implementar Quick View flotante (HTML + CSS + Alpine)
- [ ] Sistema de drag/resize para flotantes
- [ ] Click en tarjeta → Pregunta de confirmación
- [ ] Actualizar lista después de eliminar/mover
- [ ] Actualizar contador de Inbox
- [ ] Manejar caso: nota activa eliminada → volver a dashboard
- [ ] Testing: 
  - [ ] Abrir múltiples Quick View
  - [ ] Mover/redimensionar flotantes
  - [ ] Cambiar nota activa
  - [ ] Eliminar nota (¿abierta en editor?)
  - [ ] Eliminar nota (¿abierta como Quick View?)

---

## 7. CASOS ESPECIALES

### Caso 1: ¿Qué pasa si cierras una nota flotante que era la activa?
**Respuesta:** Nada. La nota flotante es solo referencia, no cambia nada en el editor.

### Caso 2: ¿Qué pasa si cambias nota activa teniendo flotantes abiertas?
**Respuesta:** Las flotantes permanecen abiertas. Solo se actualiza zona 3 y 4.

### Caso 3: ¿Qué pasa al navegar (Inbox → Biblioteca)?
**Respuesta:** Las flotantes permanecen visibles. Se pueden dejar abiertas mientras navegas entre menús.

### Caso 4: ¿Qué pasa si eliminas una nota que está abierta como flotante?
**Respuesta:** La flotante desaparece (se remueve del DOM).

---

**Última actualización:** 10 de febrero de 2026
**Status:** 📝 Especificación Completa - Lista para Implementar
