## 🎯 ARQUITECTURA AI - NATIVA TIPTAP (Completada)

### Estado: ✅ FUNCIONAL

El slash command "/" ahora funciona completamente de forma nativa, respetando los Axiomas Fundamentales de tu Knowledge OS.

---

## 📊 Flujo de Usuario

```
1. Usuario escribe "/" en el editor
   ↓
2. Tiptap detecta "/" → AICommand.onStart() dispara evento
   ↓
3. Alpine escucha 'ai:command:open' → Abre modal prompt
   ↓
4. Usuario presiona ENTER
   ↓
5. AICommand.onKeyDown() dispara 'ai:command:select'
   ↓
6. Alpine escucha 'ai:command:select' → Ejecuta AI_ACTIONS.ask.handler()
   ↓
7. handler dispara 'ai:action:ask'
   ↓
8. Alpine escucha 'ai:action:ask' → Modal Ask AI aparece + enfoca input
   ↓
9. Usuario escribe su pregunta y presiona Enter/Apply
   ↓
10. Alpine dispara 'ai:prompt:submit' o 'ai:prompt:apply'
    ↓
11. ai-events.js procesa la acción (Fase 2: backend)
```

---

## 📁 Estructura de Archivos

```
/static/js/
├── editor.js (MODIFICADO)
│   ├─ Importa: AICommand, setupAIEventListeners
│   ├─ Agrega AICommand a extensiones
│   └─ Llama setupAIEventListeners()
│
├── extensions/
│   └── ai-command.js (NUEVO)
│       ├─ AICommand: Extensión Tiptap nativa
│       ├─ AI_ACTIONS: Acciones disponibles
│       └─ Emite: ai:command:* events
│
└── ai-events.js (NUEVO)
    ├─ setupAIEventListeners(): Registra listeners
    ├─ Escucha: ai:command:*, ai:action:*, ai:prompt:*
    └─ Sincroniza: Alpine state ↔ Eventos

/templates/layouts/base.html (MODIFICADO)
├─ REMOVIDO: aiMenu state (lo maneja Tiptap)
├─ SIMPLIFICADO: aiPrompt state
└─ MODIFICADO: Modal prompt (escucha eventos)
```

---

## 🔄 Flujo de Eventos

### Tiptap → Alpine (Upstream)

```javascript
// Cuando "/" es detectado
window.dispatchEvent(new CustomEvent('ai:command:open', {
    detail: { position: {x, y}, editor, timestamp }
}));

// Cuando usuario presiona Enter
window.dispatchEvent(new CustomEvent('ai:command:select', {
    detail: { action, range, timestamp }
}));

// Cuando se cancela (Escape, Backspace, etc)
window.dispatchEvent(new CustomEvent('ai:command:close', {
    detail: { reason: 'escape'|'backspace'|'exit' }
}));
```

### Alpine → Backend (Downstream)

```javascript
// Cuando usuario presiona Enter en el input
window.dispatchEvent(new CustomEvent('ai:prompt:submit', {
    detail: { input: string }
}));

// Cuando usuario presiona Apply
window.dispatchEvent(new CustomEvent('ai:prompt:apply', {
    detail: { input: string }
}));
```

---

## ✅ Axiomas Respetados

- ✅ **Event-Driven**: Tiptap emite eventos, Alpine escucha, sin acoplamiento directo
- ✅ **Segmentación**: Responsabilidades claras (Tiptap → Evento → Alpine → Backend)
- ✅ **Sin DOM manipulation vanilla**: Tiptap gestiona todo de forma nativa
- ✅ **Integridad del Inspector**: Sin efectos secundarios
- ✅ **Concurrency Lock**: Respeta `window.isPreventingSave`
- ✅ **Estética Immutable**: Solo Tailwind, sin hardcoding de estilos

---

## 🚀 Próximos Pasos (Fase 2)

En `ai-events.js`, el listener `ai:prompt:submit` debe:

1. **POST** a `/api/ai/generate` con:
   ```json
   {
       "noteId": app.activeNoteId,
       "content": editor.getHTML(),
       "prompt": input
   }
   ```

2. **Escuchar streaming response** (SSE o fetch streaming)

3. **Renderizar cambios** en el editor o mostrar diff

4. **User presiona Apply** → Aplicar cambios

---

## 🐛 Debugging

Si algo no funciona:

1. Recarga con **Cmd+Shift+R** (hard refresh)
2. Abre DevTools (Cmd+Option+I)
3. Escribe "/" en el editor
4. Revisa la consola para eventos (sin logs activos ahora, pero puedes agregar)

**Los logs fueron removidos para limpiar la consola. Si necesitas debug, agrega:**

```javascript
console.log('[AICommand] onStart - "/" detectado');
console.log('[AI] Modal abierto en posición:', position);
// etc.
```

---

## 📝 Notas de Implementación

- `commandProcessed` flag: Previene que `onExit` cierre el modal de Ask AI después de procesar Enter
- `allow()`: Actualmente permite "/" en cualquier contexto (puedes refinar si lo necesitas)
- Modal positioning: Se actualiza basado en `view.coordsAtPos(selection.from)`
- Modal ID: `#ai-prompt-modal` (único, Alpine lo renderiza)

---

**Status:** 🟢 LISTO PARA FASE 2 (Backend Integration)
