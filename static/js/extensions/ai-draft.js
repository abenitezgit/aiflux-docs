/**
 * AI Draft Mark - Marca texto generado por IA como "draft"
 * Renderiza en azul (indicador visual de que es provisional)
 */

import { Mark } from 'https://esm.sh/@tiptap/core'

export const AIDraft = Mark.create({
    name: 'aiDraft',
    
    addOptions() {
        return {
            HTMLAttributes: { class: 'ai-draft-text' },
        }
    },
    
    parseHTML() {
        return [{ tag: 'span.ai-draft-text' }]
    },
    
    renderHTML({ HTMLAttributes }) {
        return ['span', { ...HTMLAttributes, class: 'ai-draft-text' }, 0]
    },
})
