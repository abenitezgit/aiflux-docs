# 1. ARQUITECTURA TÉCNICA Y STACK

## 1. El "Modern Monolith" Stack
Elegimos este stack por su velocidad de desarrollo, mantenibilidad y rendimiento, evitando la complejidad innecesaria de SPAs pesadas (React/Next.js) para este caso de uso.

- **Backend:** Python + **FastAPI**.
- **Frontend Interactivo:** **HTMX** (para interacciones servidor-cliente) + **Alpine.js** (para estado UI efímero cliente-cliente como modales, dropdowns, drag & drop).
- **Estilos:** **Tailwind CSS**.
- **Base de Datos:** **Supabase** (PostgreSQL).
- **Editor de Texto:** **Tiptap** (Headless wrapper sobre Prosemirror), integrado vía Alpine.js.

## 2. Infraestructura de Inteligencia Artificial

### A. Gateway de Modelos: LiteLLM
Es la pieza central para la gestión de LLMs.
- **Función:** Actúa como Proxy unificado.
- **Lógica de Fallback:** Configuración obligatoria para saltar de proveedor si uno falla (ej: OpenAI -> Anthropic -> Azure -> Ollama).
- **Control de Gastos:** Uso de las capacidades de `litellm[proxy]` para trackear costos por usuario o proyecto y establecer límites (Budgeting).

### B. RAG (Retrieval Augmented Generation)
- **Almacenamiento:** Supabase con `pgvector`.
- **Flujo:** 
    1. Al guardar/actualizar nota -> Generar embedding (background task).
    2. Al escribir -> Búsqueda semántica asíncrona para mostrar "Notas Relacionadas" en el panel derecho.

### C. Agentes en Segundo Plano (Background Tasks)
Usar `FastAPI BackgroundTasks` o `Celery` (si escala) para:
- Análisis de sentimiento/tareas tras guardar una nota.
- Generación de resúmenes diarios ("Daily Briefing").
- Limpieza y sugerencia de etiquetas.

## 3. Estructura de Diseño (Frontend Architecture)

### Layout Base (Grid)
El `base.html` debe implementar una estructura flexible de **3 columnas**:
1.  **Sidebar Navegación (Izquierda Fija):** Iconos de modos (Inicio, Proyectos, Editor, Inbox).
2.  **Sidebar Contextual (Izquierda Variable):** Cambia según el modo (Agenda en Inicio, Árbol en Proyectos, TOC en Editor). Implementado con **HTMX Swaps**.
3.  **Main Stage (Centro):** Área de contenido scrolleable.
4.  **Sidebar Asistente (Derecha):** Panel colapsable para la IA.

### Componentes Clave
- **Omnibar:** Input central en el Dashboard que actúa como buscador y creador rápido (Inbox).
- **Editor Wrapper:** Componente Alpine.js que envuelve Tiptap para manejar el `contenteditable`, menús flotantes y enviar cambios al backend (autosave).

## 4. Modelo de Datos (Esquemático Simplificado)

- `users`: Gestión de autenticación.
- `projects`: Contenedor de alto nivel.
- `notes`: Unidad atómica. Campos clave: `content_json` (Tiptap), `content_text` (búsqueda), `embedding` (vector), `status` (inbox, active, archived).
- `tags`: Taxonomía flexible.
- `ai_logs`: Registro de interacciones y costos (vía LiteLLM).