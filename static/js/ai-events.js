/**
 * AI EVENT HANDLER - Escucha eventos de la extensión AICommand
 * 
 * RESPONSABILIDADES:
 * - Escuchar eventos emitidos por AICommand
 * - Sincronizar estado Alpine con eventos
 * - Coordinar entre Tiptap y UI (Alpine)
 * 
 * PATRÓN: Event-Driven (Axioma fundamental)
 * No acoplamos Tiptap con Alpine - solo emitimos/escuchamos eventos
 */

export function setupAIEventListeners() {
    // Obtener referencia a Alpine
    const getAlpineData = () => {
        return window.Alpine && window.Alpine.$data(document.body);
    };
    
    /**
     * EVENTO: "ai:command:open"
     * Se dispara cuando el usuario escribe "/" en una posición válida
     * 
     * ACCIÓN: Abrir el modal de prompt (mostrarlo)
     *         Guardar la posición del "/" para la inserción posterior
     */
    window.addEventListener('ai:command:open', (e) => {
        const app = getAlpineData();
        if (!app) return;
        
        const { position, range } = e.detail;
        
        // ⚠️ CRÍTICO: Guardar la posición exacta del "/" en el editor
        // Esta información se usa cuando el usuario presiona "Apply"
        app.aiPrompt.cursorPos = range ? range.from : null;
        app.aiPrompt.slashRange = range; // Guardar el rango completo para referencia
        
        // Actualizar posición del modal basada en cursor (visual/CSS)
        app.aiPrompt.x = position.x;
        app.aiPrompt.y = position.y;
        
        // Limpiar input previo
        app.aiPrompt.input = '';
        app.aiPrompt.streaming = false;
        app.aiPrompt.response = '';
        
        // Mostrar modal
        app.aiPrompt.show = true;
        
        console.log('📍 "/" detectado en posición:', app.aiPrompt.cursorPos);
    });
    
    /**
     * EVENTO: "ai:command:close"
     * Se dispara cuando se cancela el comando (Escape, Backspace, onExit)
     * 
     * ACCIÓN: Cerrar el modal
     */
    window.addEventListener('ai:command:close', (e) => {
        const app = getAlpineData();
        if (!app) return;
        
        // Cerrar modal
        app.aiPrompt.show = false;
    });
    
    /**
     * EVENTO: "ai:command:select"
     * Se dispara cuando el usuario selecciona una acción del menú "/"
     * 
     * ACCIÓN: Ejecutar la acción (en este caso, siempre es "Ask AI")
     */
    window.addEventListener('ai:command:select', (e) => {
        const app = getAlpineData();
        if (!app) return;
        
        const { action, range } = e.detail;
        const editor = window.editor();
        if (!editor) return;
        
        // Ejecutar el handler de la acción
        if (action.handler) {
            action.handler(editor, action);
        }
    });
    
    /**
     * EVENTO: "ai:action:ask"
     * Se dispara cuando el usuario presiona Enter en "Ask AI"
     * (Emitido por AI_ACTIONS.ask.handler)
     * 
     * ACCIÓN: Mantener el modal abierto (user escribirá su pregunta aquí)
     */
    window.addEventListener('ai:action:ask', (e) => {
        const app = getAlpineData();
        if (!app) return;
        
        // Enfocar el input para que el usuario comience a escribir
        setTimeout(() => {
            const input = document.querySelector('#ai-prompt-modal input');
            if (input) {
                input.focus();
                input.select();
            }
        }, 50);
    });
    
    /**
     * EVENTO: "ai:prompt:submit"
     * Se dispara cuando el usuario presiona Enter en el input del prompt
     * O cuando presiona el botón de flecha arriba
     * 
     * ACCIÓN: Enviar el prompt a la IA
     */
    window.addEventListener('ai:prompt:submit', async (e) => {
        const app = getAlpineData();
        if (!app || app.aiPrompt.streaming) return;
        
        const { input } = e.detail;
        
        if (!input.trim()) {
            return;
        }
        
        // Marcar que estamos en streaming (desabilita botones)
        app.aiPrompt.streaming = true;
        
        try {
            // 1. Obtener contenido del editor
            // window.editor es una FUNCIÓN que retorna la instancia del editor
            const editor = window.editor?.();
            if (!editor) {
                console.error('❌ Editor no disponible');
                app.aiPrompt.streaming = false;
                return;
            }
            
            // Extraer solo texto limpio (sin HTML tags)
            const noteHTML = editor.getHTML();
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = noteHTML;
            const noteText = tempDiv.innerText || '';
            
            // 2. Obtener note ID desde Alpine state
            const app = getAlpineData();
            const noteId = app?.activeNoteId || null;
            
            if (!noteId) {
                console.error('❌ Note ID no disponible');
                app.aiPrompt.streaming = false;
                return;
            }
            
            // 3. Llamar backend
            console.log('🚀 Enviando prompt al backend...', { noteId, prompt: input });
            
            const response = await fetch('/api/ai/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]')?.content || ''
                },
                body: JSON.stringify({
                    noteId: noteId,
                    content: noteText,  // Texto limpio, sin HTML
                    prompt: input
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || `API error: ${response.status}`);
            }
            
            const result = await response.json();
            
            // 4. Guardar respuesta en aiPrompt para mostrar en modal
            app.aiPrompt.response = result.response;
            
            console.log('✅ Respuesta recibida:', result.response);
            
        } catch (error) {
            console.error('❌ Error en ai:prompt:submit:', error);
            app.aiPrompt.response = `Error: ${error.message}`;
        } finally {
            app.aiPrompt.streaming = false;
        }
    });
    
    /**
     * EVENTO: "ai:prompt:apply"
     * Se dispara cuando el usuario presiona el botón "Apply"
     * 
     * ACCIÓN: Insertar respuesta en el editor como texto azul (draft)
     *         Reemplazar el "/" original en su posición exacta
     */
    window.addEventListener('ai:prompt:apply', (e) => {
        const app = getAlpineData();
        if (!app) return;
        
        const response = app.aiPrompt.response;
        if (!response || !response.trim()) {
            console.warn('⚠️  No hay respuesta para aplicar');
            return;
        }
        
        const editor = window.editor?.();
        if (!editor) {
            console.error('❌ Editor no disponible');
            return;
        }
        
        try {
            // ⚠️ CRÍTICO: Usar la posición guardada en ai:command:open
            const slashRange = app.aiPrompt.slashRange;
            
            if (!slashRange) {
                console.error('❌ No hay posición guardada del "/"');
                return;
            }
            
            const { from, to } = slashRange;
            
            // Insertar respuesta en la posición exacta, reemplazando el "/"
            editor.chain()
                .deleteRange(from, to)                      // Borrar el "/" y comandos posteriores
                .insertContent(response)                    // Insertar respuesta
                .run();
            
            console.log('✅ Respuesta insertada en posición:', from);
            
            // Intentar marcar como draft (azul) si el usuario lo confirma
            // Por ahora, solo insertamos el texto normal
            // TODO: Implementar marca de draft después de validar
            
        } catch (error) {
            console.error('❌ Error insertando respuesta:', error);
        } finally {
            // Limpiar modal
            app.aiPrompt.show = false;
            app.aiPrompt.input = '';
            app.aiPrompt.response = '';
            app.aiPrompt.slashRange = null;
            app.aiPrompt.cursorPos = null;
        }
    });
    
    /**
     * EVENTO: "ai:command:update"
     * Se dispara mientras el usuario escribe después del "/"
     * 
     * Útil para futuros filtrados de opciones
     */
    window.addEventListener('ai:command:update', (e) => {
        // Por ahora no hacemos nada
        // En futuro, podría filtrar acciones basadas en query
    });
    
    /**
     * EVENTO: "ai:chat:send"
     * Se dispara cuando el usuario envía un mensaje en el chat modal
     * 
     * ACCIÓN: Enviar mensaje al backend, agregar a historial, mostrar respuesta
     */
    window.addEventListener('ai:chat:send', async (e) => {
        const app = getAlpineData();
        if (!app || !app.floatingChat) return;
        
        const userMessage = e.detail.message;
        if (!userMessage || !userMessage.trim()) return;
        
        console.log('💬 CHAT SEND EVENT FIRED', { userMessage });
        
        // 1. Agregar mensaje del usuario al historial
        app.floatingChat.messages.push({
            role: 'user',
            content: userMessage
        });
        
        // 2. Limpiar input y marcar como enviando
        app.floatingChat.input = '';
        app.floatingChat.streaming = true;
        
        try {
            // 3. Obtener contenido del editor
            const editor = window.editor?.();
            if (!editor) {
                throw new Error('Editor no disponible');
            }
            
            // Extraer solo texto limpio (sin HTML tags)
            const noteHTML = editor.getHTML();
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = noteHTML;
            const noteText = tempDiv.innerText || '';
            
            // 4. Obtener note ID
            const noteId = app?.activeNoteId || null;
            
            // 5. Enviar al backend
            console.log('💬 Enviando mensaje al chat...', { userMessage, noteId, contentLength: noteText.length });
            
            const response = await fetch('/api/ai/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]')?.content || ''
                },
                body: JSON.stringify({
                    noteId: noteId,
                    content: noteText,
                    prompt: userMessage
                })
            });
            
            console.log('📡 Response status:', response.status);
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || `API error: ${response.status}`);
            }
            
            const result = await response.json();
            
            // 6. Agregar respuesta al historial
            app.floatingChat.messages.push({
                role: 'assistant',
                content: result.response
            });
            
            console.log('✅ Mensaje de chat recibido');
            
            // 7. Scroll al último mensaje
            setTimeout(() => {
                const chatContainer = document.getElementById('chat-messages');
                if (chatContainer) {
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            }, 100);
            
        } catch (error) {
            console.error('❌ Error en ai:chat:send:', error);
            app.floatingChat.messages.push({
                role: 'assistant',
                content: `Error: ${error.message}`
            });
        } finally {
            app.floatingChat.streaming = false;
        }
    });
}

