# 🏛️ ARQUITECTURA MAESTRA: Docs.ai

> **DOCUMENTO DE REFERENCIA SUPREMO PARA LA IA**
> **REGLA DE ORO:** Este proyecto prioriza la estabilidad sobre la funcionalidad. Si una propuesta de código pone en riesgo la integridad del layout o del editor, será rechazada.

---

## 1. 🎯 Filosofía: "Estabilidad y Escenario Permanente"
El sistema evita el "parpadeo" y la destrucción de instancias de JavaScript. 
*   **DOM Inmortal:** Los contenedores del Editor (Zona 3) e Inspector (Zona 4) nunca se eliminan. Se gestionan con `x-show` para que los objetos JS (TipTap) no mueran.

---

## 2. 🛠️ Stack Tecnológico (Estricto)
*   **Backend:** FastAPI + SQLModel + Asyncpg.
*   **Frontend:** Alpine.js (Estado) + HTMX (Transporte) + TailwindCSS.
*   **Editor:** TipTap Headless (motor ProseMirror). **Es una Isla de Edición aislada.**
*   **Iconos:** Phosphor Icons (Estricto). Prohibido usar FontAwesome.

---

## 3. 📐 Patrones de Diseño Obligatorios

### A. El Layout de 4 Zonas (CSS Grid)
No se usa Flexbox para la macro-estructura. Se usan variables CSS persistentes:
1. **Zona 1 (Lentes):** Navegación global.
2. **Zona 2 (Contexto):** Sidebar redimensionable (Bibliotecas/Cuadernos/Notas).
3. **Zona 3 (El Lienzo):** Escenario del Editor.
4. **Zona 4 (El Inspector):** Panel de metadatos y TOC.

### B. El Puente del Editor (The Bridge)
La comunicación entre la Sidebar (HTMX) y el Editor (JS) se hace mediante un **Bus de Eventos**:
1. Se dispara `note-selected` con el ID de la nota.
2. El Bridge captura el evento, hace un `fetch` de la API y ejecuta `editor.commands.setContent()`.

---

## 4. 🛡️ Blindaje del Editor (REGLA INQUEBRANTABLE)
**El comportamiento de Copy-Paste y limpieza de texto es gestionado EXCLUSIVAMENTE por el Schema de TipTap.**

*   **PROHIBIDO:** Escribir funciones de "limpieza de HTML", interceptores de pegado manuales o filtros por Regex para el contenido.
*   **Por qué:** TipTap usa un árbol de nodos (JSON) que ya filtra toda la basura de fuentes externas (Word, Web, PDF). Intervenir manualmente rompe esta lógica nativa.
*   **Formato de Verdad:** El servidor y el cliente intercambian **JSON**. El HTML es secundario.
*   **No Re-inicializar:** El editor se crea una sola vez al cargar la página. **NUNCA** permitas que HTMX reemplace el `<div>` contenedor del editor.