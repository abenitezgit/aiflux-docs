# 🏗️ ARQUITECTURA HTMX: Patrones de Swap

## Regla de Oro

**La estrategia de swap depende de la INTENCIÓN, no de la tecnología.**

---

## Patrón 1: NAVEGACIÓN Entre Vistas (innerHTML)

**Cuándo:** Cambio entre componentes PRINCIPALES (Dashboard ↔ Notebook ↔ Inbox)

**Dónde:** `#contextual-sidebar` (contenedor WRAPPER)

**Por qué:** El wrapper `#contextual-sidebar` es **permanente y estable**. Solo reemplazamos su CONTENIDO.

```html
<!-- base.html -->
<div id="contextual-sidebar" class="flex-1 overflow-hidden p-3">
    <!-- Aquí va: sidebar_dashboard.html O sidebar_notebook.html O sidebar_inbox.html -->
</div>
```

**Implementación:**

```html
<!-- sidebar_dashboard.html: Botón para cargar cuaderno -->
<button hx-get="/partial/sidebar/notebook/{{ cuaderno.id }}"
        hx-target="#contextual-sidebar"
        hx-swap="innerHTML">
    Abrir Cuaderno
</button>

<!-- sidebar_notebook.html: Botón para volver a dashboard -->
<button hx-get="/partial/sidebar/dashboard"
        hx-target="#contextual-sidebar"
        hx-swap="innerHTML">
    Atrás
</button>
```

**⚠️ REGLA CRÍTICA:**
- Cuando usas `innerHTML`, el ELEMENTO TARGET NO DESAPARECE
- Solo su contenido se reemplaza
- El contenedor `#contextual-sidebar` permanece en el DOM

---

## Patrón 2: ACTUALIZACIONES Internas (outerHTML)

**Cuándo:** Refrescar o editar contenido DENTRO de un vista (tema, notas)

**Dónde:** `#notebook-sidebar-container` (el componente completo)

**Por qué:** El componente puede necesitar renovarse por completo (scroll, estado interno, etc.)

```html
<!-- sidebar_notebook.html -->
<div id="notebook-sidebar-container" ...>
    <!-- Contenido de temas y notas -->
</div>
```

**Implementación:**

```html
<!-- modal_tema.html: Crear o editar tema -->
<form hx-post="/partial/sidebar/notebook/actualizar-tema"
      hx-target="#notebook-sidebar-container"
      hx-swap="outerHTML">
    Guardar Tema
</form>
```

**✅ REGLA CRÍTICA:**
- Cuando usas `outerHTML`, el ELEMENTO MISMO SE REEMPLAZA
- El div con `id="notebook-sidebar-container"` desaparece y reaparece
- Alpine y HTMX reinicializan el componente completamente
- Los listeners de scroll, etc., se restablecen

---

## Comparativa Visual

```
┌─ #contextual-sidebar (PERMANENTE - innerHTML)
│
├── sidebar_dashboard.html  ← 1ª vez
├─→ sidebar_notebook.html   ← 2ª vez (reemplaza contenido)
├─→ sidebar_inbox.html      ← 3ª vez (reemplaza contenido)
│
└─ Permanece visible. Solo cambia QUÉ hay dentro.

---

┌─ sidebar_notebook.html
│  ├─ #notebook-sidebar-container (REEMPLAZABLE - outerHTML)
│  │
│  ├─ [Temas...]
│  ├─ [Notas...]
│  │
│  └─ Cuando editas un tema → reemplaza TODO el container
│     (incluyendo listeners, estado de scroll, etc.)
```

---

## Errores Comunes (Para IA o Desarrolladores)

### ❌ INCORRECTO: Usar outerHTML para navegación principal

```html
<!-- MALO: sidebar_dashboard.html -->
<div id="sidebar-dashboard-container"
     hx-target="#sidebar-dashboard-container"  <!-- ⚠️ RECURSIVO -->
     hx-swap="outerHTML">
```

**Resultado:** El componente intenta reemplazarse a sí mismo. Confusión en el DOM.

---

### ❌ INCORRECTO: Usar innerHTML para actualizaciones internas

```html
<!-- MALO: modal_tema.html -->
<form hx-post="/partial/sidebar/notebook/actualizar-tema"
      hx-target="#notebook-sidebar-container"
      hx-swap="innerHTML">  <!-- ⚠️ Solo reemplaza CONTENIDO -->
```

**Resultado:** Los listeners de scroll y estado DENTRO del container no se reinicializan. Bugs raros.

---

## Jerarquía Correcta

```
NIVEL 1: Navegación Principal (innerHTML)
  - Target: #contextual-sidebar
  - Componentes: sidebar_dashboard, sidebar_notebook, sidebar_inbox
  - Estrategia: Reemplaza CONTENIDO

NIVEL 2: Actualizaciones Internas (outerHTML)
  - Target: #notebook-sidebar-container (o similar)
  - Operaciones: Editar tema, crear tema, refrescar notas
  - Estrategia: Reemplaza COMPONENTE COMPLETO

NIVEL 3: Cambios Puntuales (none/outros)
  - Target: N/A o específico (#modal-content, etc.)
  - Operaciones: Validaciones, modales, etc.
  - Estrategia: Custom
```

---

## Checklist para Nuevas Características

Si NECESITAS agregar HTMX a un nuevo componente:

1. **¿Es navegación principal?** → `innerHTML` a `#contextual-sidebar`
2. **¿Es actualización dentro de un vista?** → `outerHTML` al ID del componente
3. **¿Es algo especial?** → `none` o target custom

**Nunca:**
- ❌ Mezcles patrones en el mismo componente sin documentar
- ❌ Hagas un target recursivo (elemento apunta a sí mismo con outerHTML)
- ❌ Asumas que una IA inferirá tu intención

---

## Para Futuras IAs (Prompts)

Si pides a una IA que modifique componentes HTMX, sé explícito:

```
Modifica sidebar_notebook.html para mostrar notas en tarjetas.

IMPORTANTE: 
- Usa SOLO HTML/CSS
- NO cambies hx-swap de "#contextual-sidebar"
- Los atributos HTMX existentes son intencionales:
  - hx-target="#notebook-sidebar-container" hx-swap="outerHTML" 
    es para EDITAR temas dentro del notebook
  - hx-target="#contextual-sidebar" hx-swap="innerHTML"
    es para NAVEGAR entre dashboard/notebook
- Mantén ambos patrones intactos
```

---

**Última Actualización:** 10 de febrero de 2026
**Status:** 🔒 Arquitectura Estable - NO CAMBIAR SIN REVISAR ESTE DOCUMENTO
