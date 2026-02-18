/**
 * AICommand Extension for Tiptap
 * 
 * Extensión nativa de Tiptap que maneja el comando "/" para acciones de IA.
 * 
 * ARQUITECTURA:
 * - Extiende Command de Tiptap (nativo)
 * - Emite eventos personalizados para que Alpine/UI reaccionen
 * - NO usa Alpine state directamente (separación de responsabilidades)
 * - NO manipula DOM directamente (Tiptap gestiona la suggestion UI)
 * 
 * FLUJO:
 * 1. Usuario escribe "/" → onStart()
 * 2. Sistema emite "ai:command:open" → Alpine muestra modal
 * 3. Usuario presiona Enter/Escape → onExit()
 * 4. Sistema emite "ai:command:close" → Alpine cierra modal
 * 5. Si selecciona opción → Sistema emite "ai:command:select" → Ejecuta acción
 */

import { Extension } from 'https://esm.sh/@tiptap/core';
import { Suggestion } from 'https://esm.sh/@tiptap/suggestion';

/**
 * Definición de acciones de IA disponibles
 * Estas son las acciones que pueden dispararse desde el slash command
 */
const AI_ACTIONS = {
    ask: {
        id: 'ask',
        label: 'Ask AI',
        icon: 'ph-sparkle',
        description: 'Ask AI for help with editing',
        handler: (editor, action) => {
            // Disparar evento para que Alpine abra el modal de prompt
            window.dispatchEvent(new CustomEvent('ai:action:ask', {
                detail: { 
                    editor,
                    action,
                    timestamp: Date.now()
                }
            }));
        }
    }
};

// Flag para saber si ya procesamos el comando (evita cerrar después de Enter)
let commandProcessed = false;

/**
 * Configuración de la Suggestion de Tiptap
 * 
 * ESTRUCTURA CORRECTA:
 * - char: qué carácter dispara la suggestion
 * - name: nombre del comando
 * - allow: filtro de contexto
 * - render: retorna un objeto con onStart, onUpdate, onKeyDown, onExit
 */
const aiSuggestionConfig = {
    // Patrón que detecta el comando (en este caso "/")
    char: '/',
    
    // Comando de Tiptap que maneja el contenido
    name: 'aiCommand',
    
    // Filtro: Permitir "/" en cualquier contexto
    allow: ({ state, range }) => {
        return true;
    },
    
    /**
     * render() es OBLIGATORIO en Tiptap Suggestion
     * Debe retornar un objeto con los handlers de ciclo de vida
     */
    render: () => ({
        /**
         * onStart: Se dispara cuando se detecta el patrón "/" en una posición válida
         */
        onStart: (props) => {
            // Resetear el flag cuando se abre el comando
            commandProcessed = false;
            
            // En Tiptap Suggestion, el editor se pasa directamente
            const editor = props.editor;
            const range = props.range; // ⚠️ Necesario para guardar la posición
            if (!editor) return;
            
            // Calcular posición visual del cursor
            const { view } = editor;
            const { state } = view;
            const { selection } = state;
            const coords = view.coordsAtPos(selection.from);
            
            // Emitir evento para que Alpine abra el modal
            // Incluir el range para poder insertar en la posición correcta después
            window.dispatchEvent(new CustomEvent('ai:command:open', {
                detail: {
                    position: { x: coords.left, y: coords.bottom + 5 },
                    range: range, // ✅ Pasar posición exacta del "/" en el editor
                    editor,
                    timestamp: Date.now()
                }
            }));
        },
        
        /**
         * onUpdate: Se dispara mientras el usuario escribe después del "/"
         */
        onUpdate: (props) => {
            const { query, editor } = props;
            
            window.dispatchEvent(new CustomEvent('ai:command:update', {
                detail: {
                    query,
                    editor,
                    availableActions: Object.values(AI_ACTIONS),
                    timestamp: Date.now()
                }
            }));
        },
        
        /**
         * onKeyDown: Maneja teclas especiales dentro del suggestion
         */
        onKeyDown: (props) => {
            const { event, view, range } = props;
            
            if (!view) return false;
            
            // Escape: Cerrar el modal sin hacer nada
            if (event.key === 'Escape') {
                window.dispatchEvent(new CustomEvent('ai:command:close', {
                    detail: { reason: 'escape', timestamp: Date.now() }
                }));
                
                view.dispatch(
                    view.state.tr.delete(range.from, range.to)
                );
                
                return true;
            }
            
            // Enter: Ejecutar la acción "Ask"
            if (event.key === 'Enter') {
                // Marcar que procesamos el comando (evita que onExit cierre el modal)
                commandProcessed = true;
                
                window.dispatchEvent(new CustomEvent('ai:command:select', {
                    detail: {
                        action: AI_ACTIONS.ask,
                        range,
                        timestamp: Date.now()
                    }
                }));
                
                // Eliminar el "/" del editor
                view.dispatch(
                    view.state.tr.delete(range.from, range.to)
                );
                
                return true;
            }
            
            // Backspace: Borrar el "/" y cerrar
            if (event.key === 'Backspace') {
                window.dispatchEvent(new CustomEvent('ai:command:close', {
                    detail: { reason: 'backspace', timestamp: Date.now() }
                }));
                
                return false;
            }
            
            return false;
        },
        
        /**
         * onExit: Se dispara cuando la suggestion range se invalida
         * 
         * IMPORTANTE: No disparar ai:command:close si ya procesamos el comando con Enter
         * (porque eso cerraría el modal de Ask AI que acabamos de abrir)
         */
        onExit: (props) => {
            // Si ya procesamos el comando, NO emitir close
            // (el modal de Ask AI debe permanecer abierto)
            if (commandProcessed) {
                commandProcessed = false; // Resetear para próximo comando
                return;
            }
            
            window.dispatchEvent(new CustomEvent('ai:command:close', {
                detail: { reason: 'exit', timestamp: Date.now() }
            }));
        }
    })
};

/**
 * Extensión de Tiptap que define el comando "/" para IA
 * 
 * PATRÓN: Extension que crea un Suggestion plugin
 * El editor se disponibiliza vía this.editor en addProseMirrorPlugins
 */
export const AICommand = Extension.create({
    name: 'aiCommand',
    
    addProseMirrorPlugins() {
        console.log('[AICommand] Inicializando plugin');
        
        return [
            Suggestion({
                editor: this.editor,
                ...aiSuggestionConfig
            })
        ];
    }
});

/**
 * Acciones disponibles (exportadas para que otros módulos las usen)
 */
export { AI_ACTIONS };
