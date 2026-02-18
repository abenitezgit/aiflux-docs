# 🚦 ESTADO DEL SISTEMA: Docs.ai

> **Última Actualización:** 6 Febrero 2026
> **Estado Operativo:** Fase de Estabilización (Post-Reset)

---

## 🏆 VICTORIAS CONSOLIDADAS (No tocar)

1.  **Limpieza de Copy-Paste:** Actualmente, el editor acepta texto de fuentes externas perfectamente. Esto se debe al respeto estricto del esquema de TipTap y al aislamiento del editor. **Cualquier degradación en esta área es un error crítico.**
2.  **Deep Linking:** La ruta `/note/{id}` es funcional. Al recargar (F5), el servidor reconstruye la UI y el Bridge inyecta la nota correcta.
3.  **Navegación Fluida:** El paso de Dashboard a Notebook está saneado. Las barras laterales guardan su ancho y no interfieren con el lienzo central.
4.  **Omnibarra de Captura:** Envío asíncrono al Inbox con feedback visual de "typing dots" funcionando al 100%.

---

## ⚠️ LIMPIEZA Y SANEAMIENTO REALIZADO
*   **Archivos Legacy:** Se han eliminado `list_pane.html` y `sidebar_main.html` (obsoletos).
*   **Estructura de Carpetas:** Se han eliminado `app/models/` y `app/services/` para simplificar el contexto.
*   **Prototipos:** Movidos a `.research/`. La IA solo debe mirar `/templates` y `/static`.

---

## 🔜 PRÓXIMOS PASOS (Roadmap Inmediato)

### Fase 1: Persistencia (Autosave)
1.  **Título:** Sincronizar el título de la nota (textarea) con la base de datos.
2.  **Contenido:** Implementar `onUpdate` con `debounce` (1.5s) en el editor para enviar el JSON a la API.
3.  **Endpoint:** Crear `PATCH /api/notes/{id}` para actualizaciones parciales.

### Fase 2: Gestión de Notas (CRUD)
1.  **Creación:** Conectar el botón "Añadir Nota" de la Zona 2 para que genere una nota real en la DB y la cargue en el editor.
2.  **Eliminación:** Implementar borrado desde el Inspector o Sidebar.

### Fase 3: Triaje de Inbox
1.  Finalizar el flujo de "Mover nota" de Inbox a temas específicos, asegurando que al moverla, se elimine de la vista de Inbox y aparezca en su destino.