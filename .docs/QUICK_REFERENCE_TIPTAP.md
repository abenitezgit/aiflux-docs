# 🚀 QUICK REFERENCE - Editor Tiptap

**Proyecto:** proyecto-docs  
**Módulo:** Editor WYSIWYG  
**Referencia rápida para desarrolladores**

---

## 📍 Archivos Clave

```
static/js/editor.js                    ← Motor Tiptap (335 líneas)
templates/layouts/base.html           ← UI + Toolbar (758 líneas)
```

---

## 🎯 Flujo de Reactividad (CRÍTICO)

```javascript
// 1. Usuario escribe/modifica en editor
editor.onUpdate({ editor }) => {
    
    // 2. Incrementar editorTick
    app.editorTick++  // ← VITAL
    
    // 3. Alpine.js detecta cambio
    // 4. activeStyles() se re-evalúa
    // 5. Cada :class binding se actualiza
    // 6. Botones se iluminan/oscurecen
}
```

**Sin `editorTick++` la barra NO se actualiza** ⚠️

---

## 🎨 Agregar Nuevo Botón

### Paso 1: Verificar que la extensión esté cargada

```javascript
// static/js/editor.js línea 42-80
// ✅ Busca que la extensión esté en el array

StarterKit.configure({ ... }),      // Ya tiene Bold, Italic, etc
Color,                              // ✅ Está
TextAlign,                          // ✅ Está
```

### Paso 2: Agregar botón en la toolbar

```html
<!-- templates/layouts/base.html línea ~560 -->

<button @click="editor().chain().focus().toggleBold().run()"
        :class="activeStyles() && editor().isActive('bold') ? 'bg-indigo-500/20 text-indigo-400' : 'text-slate-400'"
        class="w-8 h-8 flex items-center justify-center rounded-lg transition-all hover:bg-white/5">
    <i class="ph-bold ph-text-b"></i>
</button>
```

**Patrón:** `@click="editor().chain().focus().[comando]().run()"` + `:class` binding

### Paso 3: Test

1. Escribe algo
2. Selecciona texto
3. Haz click en botón
4. Verifica que el estilo se aplique Y el botón se illumine

---

## 🔍 Formato Detectado

```javascript
// Verificar si un formato está activo:
editor().isActive('bold')              // true/false
editor().isActive('italic')            // true/false
editor().isActive('heading', {level:1}) // true/false
editor().isActive('textAlign', {alignment:'left'}) // true/false
editor().isActive('link')              // true/false
editor().isActive('color')             // true/false
editor().isActive('highlight')         // true/false
editor().isActive('codeBlock')         // true/false
editor().isActive('bulletList')        // true/false
editor().isActive('taskList')          // true/false
```

---

## 🛠️ Comandos Útiles

```javascript
// Formateo básico
editor().chain().focus().toggleBold().run()
editor().chain().focus().toggleItalic().run()
editor().chain().focus().toggleUnderline().run()

// Headings
editor().chain().focus().setParagraph().run()
editor().chain().focus().toggleHeading({level:1}).run()
editor().chain().focus().toggleHeading({level:2}).run()

// Listas
editor().chain().focus().toggleBulletList().run()
editor().chain().focus().toggleTaskList().run()

// Color
editor().chain().focus().setColor('#f87171').run()  // Rojo
editor().chain().focus().setColor('#60a5fa').run()  // Azul
editor().chain().focus().unsetColor().run()         // Remover

// Resaltado
editor().chain().focus().setHighlight({color:'#323232'}).run()
editor().chain().focus().unsetHighlight().run()

// Link
const url = window.prompt('URL:');
if(url) editor().chain().focus().setLink({href:url}).run()

// Alineación
editor().chain().focus().setTextAlign('left').run()
editor().chain().focus().setTextAlign('center').run()

// Tablas
editor().chain().focus().insertTable({rows:3, cols:3}).run()
editor().chain().focus().addColumnAfter().run()
editor().chain().focus().addRowAfter().run()
editor().chain().focus().deleteTable().run()

// Código
editor().chain().focus().toggleCodeBlock().run()

// Blockquote
editor().chain().focus().toggleBlockquote().run()

// Sub/Sup
editor().chain().focus().toggleSubscript().run()
editor().chain().focus().toggleSuperscript().run()
```

---

## 🎨 Estructura del Toolbar

```html
<div id="fixed-toolbar" 
     x-data="{ 
         menuStyle: false, 
         activeStyles() { return this.editorTick && typeof editor === 'function' && editor() }
     }">
    
    <!-- Grupo 1: Estilos -->
    <!-- Grupo 2: Básicos -->
    <!-- etc... -->
    
</div>
```

**Puntos de entrada:**
- `x-data`: Declara variables de estado
- `activeStyles()`: Función getter para editor instance
- `@click.away`: Cierra menús al hacer click fuera

---

## 💾 Guardar Contenido

```javascript
// static/js/editor.js línea 215-237

const contenido = JSON.stringify(window.editor().getJSON());
// ← SIEMPRE JSON, no HTML

fetch(`/api/notes/${noteId}`, {
    method: 'PATCH',
    body: JSON.stringify({ titulo, contenido })
});
```

**Importante:** Guardar siempre como JSON para máxima compatibilidad.

---

## 📖 Cargar Contenido

```javascript
// static/js/editor.js línea 248-292

// Lógica híbrida:
try {
    contentToLoad = JSON.parse(data.contenido);  // Nuevo (JSON)
} catch (err) {
    contentToLoad = data.contenido;  // Legacy (HTML)
}

initEditor(contentToLoad);
```

**Soporta ambos formatos automáticamente** ✅

---

## 🐛 Debugging

```javascript
// En el navegador (DevTools > Console):

// Ver instancia del editor
window.editor()

// Ver contenido actual (JSON)
window.editor().getJSON()

// Ver contenido como HTML
window.editor().getHTML()

// Ver si está en foco
window.editor().isFocused

// Ver todas las extensiones
window.editor().extensionManager.extensions

// Resetear contenido
window.editor().commands.setContent('')

// Setear contenido específico
window.editor().commands.setContent('<p>Hola</p>')
```

---

## ⚡ Performance Tips

### 1. NO usar setInterval para verificar estado
```javascript
// ❌ MAL
setInterval(() => {
    updateButtons();
}, 100);

// ✅ BIEN - Usa evento onUpdate de Tiptap
editor.onUpdate(({ editor }) => {
    app.editorTick++;  // Alpine se actualiza
});
```

### 2. NO re-crear editor en cada cambio
```javascript
// ❌ MAL
if (editorInstance) {
    new Editor({ ... });  // Crea nueva instancia
}

// ✅ BIEN - Reutilizar
if (editorInstance) {
    editorInstance.commands.setContent(content);
    return editorInstance;
}
```

### 3. Debounce autosave
```javascript
// ✅ BIEN - Esperar a que user pare de escribir
clearTimeout(saveTimeout);
saveTimeout = setTimeout(() => {
    saveNoteToServer();
}, 1500);  // 1.5 segundos
```

---

## 🧪 Prueba Rápida

Abre DevTools y ejecuta:

```javascript
// 1. Verificar que editor está cargado
window.editor() 

// 2. Setear contenido
window.editor().commands.setContent('<p><strong>Hola</strong> mundo</p>')

// 3. Forzar update (como si user escribiera)
window.editorInstance.view.dispatch(
    window.editorInstance.state.tr
)

// 4. Ver que editorTick se incrementó
window.Alpine.$data(document.body).editorTick
```

---

## 📚 Referencias

- **Tiptap Docs:** https://tiptap.dev
- **Extensiones:** https://tiptap.dev/extensions
- **Colores:** tailwindcss.com/docs/colors
- **Icons:** phosphoricons.com

---

## ✅ Checklist antes de Producción

- [ ] Todas las 18 extensiones cargadas
- [ ] Toolbar visible y sticky
- [ ] Botones responden al click
- [ ] Barra se actualiza al cambiar formato
- [ ] Autosave guarda en JSON
- [ ] Imágenes se suben a Supabase
- [ ] Tablas son editables
- [ ] Pegado de HTML preserva estructura
- [ ] Dark mode se ve bien
- [ ] Mobile responsive ✓

---

**Referencia Rápida - 9 de febrero de 2026**
