# Portal Global del Menú Contextual

## Visión General

El **Portal Global del Menú Contextual** es la solución arquitectónica a la "Jaula de Cristal" (cristal de `backdrop-filter` en sidebars). En lugar de anidar el menú dentro de tarjetas de notas (donde heredaba filtros y semitransparencia), el menú vive en un **contenedor global position: fixed** que está fuera de cualquier contexto de apilamiento heredado.

---

## El Problema Original

### Antes del Portal

```html
<!-- sidebar_notebook.html -->
<div class="note-card">
    <div class="gear-menu-container">  <!-- ❌ Dentro del contenedor con backdrop-filter -->
        <button>Engranaje</button>
        <div class="gear-dropdown">     <!-- ❌ Heredaba opacidad del padre -->
            <button>Quick View</button>
            <!-- ... -->
        </div>
    </div>
</div>
```

**Síntoma:** El dropdown era semitransparente/invisible porque el `backdrop-filter` del contenedor padre (sidebar con glassmorphism) creaba un stacking context que afectaba a todos los hijos.

---

## La Solución: Portal Centralizado

### Arquitectura

```
┌─ base.html (root)
│
├─ <div id="modal-container">        ← z-index: 100
│
└─ <div id="global-gear-menu-portal"> ← z-index: 999 (sin herencia de filtros)
    └─ <div class="gear-dropdown-portal">
        ├─ <button>Quick View</button>
        ├─ <button>Mover Nota</button>
        └─ <button>Eliminar</button>
```

### Ventajas

1. **Sin Herencia de Filtros:** El portal está fuera de la jaula de cristal → 100% opaco
2. **Position: Fixed:** Coordenadas globales, no afectadas por scroll de sidebar
3. **Reactividad Pura:** Alpine.js maneja todo (`x-show`, `:style`, `@click`)
4. **Centralización:** Un único menú para Inbox, Notebooks, futuras vistas
5. **Escalabilidad:** Agregar nuevas opciones al menú = 1 cambio en `base.html`

---

## Flujo de Funcionamiento

### 1. Usuario hace click en engranaje (cualquier vista)

```html
<!-- sidebar_notebook.html o sidebar_inbox.html -->
<button @click.stop="openGearMenu($event, '{{ nota.id }}')">
    <i class="ph-bold ph-gear"></i>
</button>
```

### 2. Alpine ejecuta `openGearMenu(event, notaId)`

```javascript
// base.html - appShell()
openGearMenu(event, notaId) {
    event.stopPropagation();
    
    // Capturar coordenadas del botón
    const btn = event.currentTarget;
    const rect = btn.getBoundingClientRect();
    
    // Toggle: si está abierto, cerrar
    if (this.activeGearMenu === notaId) {
        this.activeGearMenu = null;
        return;
    }
    
    // Abrir menú
    this.activeGearMenu = notaId;
    this.gearMenuCoords = {
        x: rect.left,
        y: rect.bottom + 8
    };
    
    // Listener para cerrar al click fuera
    setTimeout(() => {
        document.addEventListener('click', this.closeGearMenuOnClickOutside.bind(this), { once: true });
    }, 0);
}
```

### 3. Portal renderiza el menú reactivamente

```html
<!-- base.html - global-gear-menu-portal -->
<div class="gear-dropdown-portal"
     x-show="activeGearMenu !== null"  <!-- ← Se muestra si hay nota activa -->
     :style="`position: fixed; top: ${gearMenuCoords.y}px; left: ${gearMenuCoords.x}px;`">
    
    <button @click="openQuickView(activeGearMenu); activeGearMenu = null">
        Quick View
    </button>
    
    <button :hx-get="`/partial/modal/inbox-mover/${activeGearMenu}`"
            @click="activeGearMenu = null; modalOpen = true">
        Mover Nota
    </button>
    
    <button @click="confirmDeleteInboxNota(activeGearMenu); activeGearMenu = null">
        Eliminar
    </button>
</div>
```

### 4. Usuario hace click en opción

Cada opción ejecuta:

- **Quick View:** `openQuickView(notaId)` → Crea flotante, dispara evento `note-selected`
- **Mover Nota:** HTMX request → `hx-get` + `hx-target="#modal-content"` (abre modal)
- **Eliminar:** `confirmDeleteInboxNota(notaId)` → DELETE request + recarga sidebar

---

## Estados de Alpine Críticos

### `activeGearMenu`
- **null:** Menú cerrado, portal oculto (`x-show="activeGearMenu !== null"`)
- **notaId (uuid):** Menú abierto, mostrando opciones para esa nota

### `gearMenuCoords`
```javascript
{
    x: 150,  // Píxeles desde left (posición del botón)
    y: 225   // Píxeles desde top (posición del botón + 8px)
}
```

### Cierre Automático
- Click en opción → se ejecuta ` activeGearMenu = null`
- Click fuera → evento `@click.outside` → `activeGearMenu = null`

---

## Respeto a Axiomas

### ✅ Axioma de Fuente Única de Carga (Event-Driven)
- El menú **no carga** la nota. Solo dispara acciones.
- `openQuickView()` es quien carga y dispara `window.dispatchEvent('note-selected')`

### ✅ Axioma de Integridad del Inspector
- El menú **nunca toca** el Inspector.
- Las funciones resultantes (`openQuickView`, `confirmDeleteInboxNota`) sí respetan `clearInspector()` → `updateTOC()` → `updateInspector()`

### ✅ Axioma del Bloqueo de Concurrencia
- El menú **no mutá datos**. Solo presenta opciones.
- Validación de `isPreventingSave` ocurre en `confirmDeleteInboxNota()`, no en el portal

### ✅ Axioma de Segmentación de Responsabilidades
- Portal es un componente visual en `appShell()` de `base.html`
- Acciones son responsabilidad de `editor.js` (para Quick View, etc.) o `dashboard.py` (para DELETE/HTMX)

### ✅ Axioma de Estética Inmutable
- Paleta: `bg-[#1a1d26]`, `indigo-500`, `slate-300` (coherente con diseño)
- Espaciado: Tailwind estándar, mismo que el resto de la UI

---

## Cambios Realizados

### 1. **base.html**
- Agregado portal global: `<div id="global-gear-menu-portal">`
- Nueva función: `openGearMenu(event, notaId)`
- Nueva función: `closeGearMenuOnClickOutside(event)`
- Estados nuevos: `gearMenuCoords`
- Estilos: `.gear-dropdown-portal` y `.gear-dropdown-btn`

### 2. **sidebar_notebook.html**
- ❌ Eliminado: `<div class="gear-menu-container">` con dropdown anidado
- ✅ Agregado: `<button @click.stop="openGearMenu($event, '{{ nota.id }}')">`

### 3. **sidebar_inbox.html**
- ❌ Eliminado: dropdown anidado en tarjeta
- ✅ Agregado: botón que dispara `openGearMenu()`

### 4. **Corrección Post-Testing: HTMX Dinámico** ⚡
- ❌ NO funciona: `:hx-get="\`/partial/modal/inbox-mover/${activeGearMenu}\`"`
- ✅ SÍ funciona: `@click="htmx.ajax('GET', '/partial/modal/inbox-mover/${activeGearMenu}', {target, swap})"`
- **Razón:** HTMX necesita URLs concretas, no templates de Alpine

---

## Testing & Validación

### Checklist de Prueba

- [ ] Abrir Inbox → hacer click en engranaje de una nota → menú aparece
- [ ] Menú está correctamente posicionado (abajo del botón, sin recorte)
- [ ] Hacer click en "Quick View" → nota se abre como flotante
- [ ] Hacer click en "Mover Nota" → modal se abre
- [ ] Hacer click en "Eliminar" → nota se elimina, sidebar se recarga
- [ ] Click fuera del menú → menú se cierra
- [ ] Abrir dos notas diferentes → menú se posiciona correctamente para cada una
- [ ] Notebook → engranaje en tarjeta → funciona igual que Inbox
- [ ] Navegación Dashboard → Notebook → Click en engranaje → funciona

### Síntomas de Éxito

- ✅ Menú es **100% opaco** (no semitransparente)
- ✅ Menú no se recorta al bottom de la pantalla
- ✅ Menú posición se actualiza al cambiar de nota
- ✅ Transición suave al abrir/cerrar (`x-transition.opacity`)

---

## Futuros Mejoras

### Potencial de Expansión

1. **Submenu para "Mover Nota":** En lugar de modal, mostrar submenu con categorías/cuadernos
2. **Más opciones:** Duplicar nota, Cambiar etiqueta, Pinear nota
3. **Atajos de teclado:** `Ctrl+Shift+M` para abrir menú de nota activa
4. **Menús contextuales en otras vistas:** Temas, Categorías, etc. (reutilizar portal)

---

## Referencias

- **Archivo de Axiomas:** `/AXIOMAS_KNOWLEDGE_OS.md`
- **Copilot Instructions:** `/.github/copilot-instructions.md` (Patrón 1: innerHTML vs Patrón 2: outerHTML)
- **Arquitectura HTMX:** Sección "Patrón de Partials"

---

**Última actualización:** 10 de febrero de 2026  
**Status:** ✅ Implementado y Documentado  
**Compliance:** 100% Axiomas respetados
