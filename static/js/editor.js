/**
 * EDITOR.JS - REFACTORIZACIÓN ESTRUCTURAL (Preservación íntegra de lógica)
 * Responsabilidades segmentadas: Configuración, Persistencia, Assets, UI/Inspector y Eventos.
 */

import { Editor, Extension } from 'https://esm.sh/@tiptap/core';
import { StarterKit } from 'https://esm.sh/@tiptap/starter-kit';
import { Placeholder } from 'https://esm.sh/@tiptap/extension-placeholder';
import { Underline } from 'https://esm.sh/@tiptap/extension-underline';
import { Highlight } from 'https://esm.sh/@tiptap/extension-highlight';
import { Link } from 'https://esm.sh/@tiptap/extension-link';
import { TextStyle } from 'https://esm.sh/@tiptap/extension-text-style';
import { Color } from 'https://esm.sh/@tiptap/extension-color';
import { TextAlign } from 'https://esm.sh/@tiptap/extension-text-align';
import { Subscript } from 'https://esm.sh/@tiptap/extension-subscript';
import { Superscript } from 'https://esm.sh/@tiptap/extension-superscript';
import { TaskList } from 'https://esm.sh/@tiptap/extension-task-list';
import { TaskItem } from 'https://esm.sh/@tiptap/extension-task-item';
import { CodeBlockLowlight } from 'https://esm.sh/@tiptap/extension-code-block-lowlight';
import { Image } from 'https://esm.sh/@tiptap/extension-image';
import { Table } from 'https://esm.sh/@tiptap/extension-table';
import { TableCell } from 'https://esm.sh/@tiptap/extension-table-cell';
import { TableHeader } from 'https://esm.sh/@tiptap/extension-table-header';
import { TableRow } from 'https://esm.sh/@tiptap/extension-table-row';
import { common, createLowlight } from 'https://esm.sh/lowlight@3';
import { Heading } from 'https://esm.sh/@tiptap/extension-heading';
import { AICommand } from './extensions/ai-command.js';
import { AIDraft } from './extensions/ai-draft.js';
import { setupAIEventListeners } from './ai-events.js';



// -------------------------------------------------------------------------
// 1. CONFIGURACIÓN DE LENGUAJES (Lowlight)
// -------------------------------------------------------------------------
const lowlight = createLowlight(common);
import python from 'https://esm.sh/highlight.js/lib/languages/python';
import js from 'https://esm.sh/highlight.js/lib/languages/javascript';
import css from 'https://esm.sh/highlight.js/lib/languages/css';
import xml from 'https://esm.sh/highlight.js/lib/languages/xml'; 
import sql from 'https://esm.sh/highlight.js/lib/languages/sql';
import bash from 'https://esm.sh/highlight.js/lib/languages/bash';
import TurndownService from 'https://esm.sh/turndown';

// -------------------------------------------------------------------------
// 1.1. CONFIGURACIÓN TURNDOWN (Markdown Técnico)
// -------------------------------------------------------------------------
const turndownService = new TurndownService({
    headingStyle: 'atx',
    codeBlockStyle: 'fenced'
});

// REGLA: Bloques de Código (Fenced Code Blocks ```)
turndownService.addRule('codeBlock', {
    filter: 'pre',
    replacement: function (content, node) {
        // Buscamos el código real ignorando los botones de la UI
        const codeElement = node.querySelector('code');
        const language = codeElement 
            ? (codeElement.getAttribute('class') || '').replace('language-', '') 
            : '';
        
        // Extraemos el contenido eliminando el texto de los botones de copia
        const codeText = codeElement ? codeElement.textContent : node.textContent;
        
        return '\n```' + language + '\n' + codeText.trim() + '\n```\n';
    }
});

// REGLA: Limpieza de UI (Elimina botones y herramientas del export)
turndownService.addRule('cleanUI', {
    filter: (node) => {
        return node.classList.contains('code-tools') || node.tagName === 'BUTTON';
    },
    replacement: () => ''
});

lowlight.register('python', python);
lowlight.register('javascript', js);
lowlight.register('css', css);
lowlight.register('html', xml);
lowlight.register('sql', sql);
lowlight.register('bash', bash);

// -------------------------------------------------------------------------
// 2. ESTADO GLOBAL Y REFERENCIAS
// -------------------------------------------------------------------------
let editorInstance = null;
let saveTimeout = null;
window.isPreventingSave = false;
window.editor = () => editorInstance;

// -------------------------------------------------------------------------
// 3. MÓDULO DE PERSISTENCIA (Guardado en Servidor)
// -------------------------------------------------------------------------
const saveNoteToServer = async () => {
    const app = window.Alpine ? window.Alpine.$data(document.body) : null;
    const noteId = app ? app.activeNoteId : null;

    if (window.isPreventingSave || !window.editor || !window.editor() || !noteId) return;

    const statusLabel = document.querySelector('#save-status');
    if (statusLabel) statusLabel.innerText = "Guardando...";

    const titulo = document.querySelector('#note-title-input')?.value;
    const contenido = JSON.stringify(window.editor().getJSON());

    try {
        await fetch(`/api/notes/${noteId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ titulo, contenido })
        });
        document.body.dispatchEvent(new CustomEvent('refresh-notebook-sidebar'));
        if (statusLabel) {
            statusLabel.innerText = "Guardado";
            setTimeout(() => { statusLabel.innerText = ""; }, 2000);
        }
    } catch (error) {
        console.error("Error al guardar:", error);
    }
};

// -------------------------------------------------------------------------
// 4. MÓDULO DE ASSETS (Imágenes / Subidas)
// -------------------------------------------------------------------------
const uploadImageToServer = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    try {
        const response = await fetch('/api/upload/image', { method: 'POST', body: formData });
        if (!response.ok) throw new Error('Error en la subida');
        const data = await response.json();
        return data.url;
    } catch (error) {
        console.error("Upload failed:", error);
        return null;
    }
};

// -------------------------------------------------------------------------
// 5. MÓDULO UI & INSPECTOR (DOM Helpers)
// -------------------------------------------------------------------------
window.clearInspector = () => {
    const tocContainer = document.querySelector('#note-toc');
    if (tocContainer) tocContainer.innerHTML = '<p class="text-[10px] text-slate-600 italic">Cargando...</p>';
    const tagsContainer = document.querySelector('#note-tags');
    if (tagsContainer) tagsContainer.innerHTML = '<span class="text-[10px] text-slate-700 italic">Cargando...</span>';
    const adjContainer = document.querySelector('#note-attachments');
    if (adjContainer) adjContainer.innerHTML = '<span class="text-[10px] text-slate-700 italic">Cargando...</span>';
};

// Variable global para almacenar el listener del TOC
let tocClickListener = null;

window.updateTOC = (editor) => {
    const tocContainer = document.querySelector('#note-toc');
    if (!tocContainer) return;

    // 1. Extraer todos los títulos del documento actual
    const headings = [];
    editor.state.doc.descendants((node, pos) => {
        if (node.type.name === 'heading') {
            headings.push({
                level: node.attrs.level,
                text: node.textContent,
                pos: pos
            });
        }
    });

    // 2. Renderizar la TOC usando el ÍNDICE como referencia
    tocContainer.innerHTML = headings.length === 0 
        ? '<p class="text-[10px] text-slate-600 italic">Escribe un título (#) para el índice</p>'
        : headings.map((h, index) => `
            <a href="javascript:void(0)" 
               data-toc-index="${index}"
               class="toc-link flex items-center gap-3 px-3 py-2 rounded-lg text-xs transition-all duration-200 text-slate-400 hover:text-slate-200 hover:bg-white/5 group">
                <span class="bg-slate-700 w-1 h-1 rounded-full group-hover:bg-indigo-500"></span>
                <span class="truncate ${h.level === 1 ? 'font-bold text-slate-300' : h.level === 2 ? 'pl-2' : 'pl-4'}">${h.text}</span>
            </a>`).join('');

    // 3. Remover listener previo si existe
    if (tocClickListener) {
        tocContainer.removeEventListener('click', tocClickListener);
    }

    // 4. Crear nuevo listener y almacenarlo
    tocClickListener = (e) => {
        const link = e.target.closest('.toc-link');
        if (!link) return;

        const index = parseInt(link.getAttribute('data-toc-index'), 10);
        const proseHeadings = document.querySelectorAll('.ProseMirror h1, .ProseMirror h2, .ProseMirror h3');
        const target = proseHeadings[index];

        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    };

    // 5. Agregar el nuevo listener
    tocContainer.addEventListener('click', tocClickListener);
};

window.updateInspector = (data) => {
    const tagsContainer = document.querySelector('#note-tags');
    if (tagsContainer) {
        const tags = data.tags || [];
        tagsContainer.innerHTML = tags.length > 0 
            ? tags.map(tag => `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-white/5 border border-white/10 text-[11px] text-slate-300">
    <span>${tag}</span><button class="hover:text-red-400 text-slate-600"><i class="ph ph-x w-3 h-3"></i></button></span>`).join('')
            : '<span class="text-[10px] text-slate-700 italic">Sin etiquetas</span>';
    }
    const adjContainer = document.querySelector('#note-attachments');
    if (adjContainer) {
        const adjuntos = data.adjuntos || [];
        adjContainer.innerHTML = adjuntos.length > 0
            ? adjuntos.map(adj => `<div class="flex items-center justify-between p-2 rounded-lg hover:bg-white/5 transition-all">
    <div class="flex items-center gap-3"><i class="ph ph-file-text text-slate-500 w-4 h-4"></i><a href="${adj.url}" target="_blank" rel="noopener noreferrer" class="text-xs text-slate-400 hover:text-slate-200 transition-colors truncate">${adj.nombre}</a></div>
    <button hx-delete="/api/notes/attachment/${adj.id}" hx-target="#note-attachments" hx-confirm="¿Estás seguro de eliminar este archivo?" hx-indicator="#upload-indicator" class="text-slate-600 hover:text-red-400 transition-colors"><i class="ph ph-trash w-3.5 h-3.5"></i></button></div>`).join('')
            : '<span class="text-[10px] text-slate-700 italic">Sin archivos</span>';
        if (window.phosphor && window.phosphor.replace) window.phosphor.replace(adjContainer);
        if (window.htmx) window.htmx.process(adjContainer);
    }
};

// -------------------------------------------------------------------------
// 6. INICIALIZACIÓN DEL NÚCLEO (Tiptap Engine)
// -------------------------------------------------------------------------

const AICommands = Extension.create({
    name: 'aiCommands',
    addOptions() {
        return {
            suggestion: {
                char: '/',
                command: ({ editor, range, props }) => {
                    props.command({ editor, range });
                },
            },
        }
    },
    addProseMirrorPlugins() {
        return [
            Suggestion({
                editor: this.editor,
                ...this.options.suggestion,
            }),
        ]
    },
});

window.initEditor = (content = '') => {
    const container = document.querySelector('#tiptap-content');
    if (!container) return null;
    if (editorInstance) {
        editorInstance.commands.setContent(content);
        return editorInstance;
    }

    editorInstance = new Editor({
        element: container,
        extensions: [
            StarterKit.configure({ 
                heading: false,
                bulletList: { keepMarks: true }, 
                orderedList: { keepMarks: true },
                codeBlock: false, code: false
            }),

            Heading.configure({ levels: [1, 2, 3] }),

            AICommand,
            AIDraft,

            CodeBlockLowlight.extend({
                renderHTML({ HTMLAttributes }) {
                    return [
                        'pre', { ...HTMLAttributes, style: 'border-radius: 12px; overflow: hidden;' },
                        ['div', { class: 'code-tools', contenteditable: 'false' },
                            ['button', { class: 'tool-copy', type: 'button' }, ['i', { class: 'ph ph-copy' }]]
                        ],
                        ['code', { style: 'border-radius: 12px; display: block;' }, 0]
                    ]
                }
            }).configure({ 
                lowlight,
                HTMLAttributes: { class: 'bg-[#0d0e12] border border-white/10 group/code relative', style: 'border-radius: 12px; padding: 1rem; overflow: hidden;' } 
            }),
            Underline, Link.configure({ openOnClick: false, HTMLAttributes: { class: 'text-indigo-400 underline' } }),
            TextStyle, Color, Highlight.configure({ multicolor: true }), Subscript, Superscript, TaskList, TaskItem.configure({ nested: true }),
            Placeholder.configure({ placeholder: 'Escribe "/" para comandos...' }),
            TextAlign.configure({ types: ['heading', 'paragraph'] }),
            Image.configure({ inline: true, allowBase64: false, HTMLAttributes: { class: 'rounded-lg shadow-lg border border-white/5' } }),
            Table.configure({ resizable: true }), TableRow, TableHeader, TableCell,
        ],
        content: content,
        editorProps: {
            attributes: { class: 'outline-none prose prose-invert max-w-none focus:outline-none' },
            handlePaste(view, event) {
                const html = event.clipboardData.getData('text/html');
                if (html && (html.includes('<table') || html.includes('<tr'))) return false; 
                const items = (event.clipboardData || event.originalEvent.clipboardData).items;
                for (let item of items) {
                    if (item.type.indexOf('image') === 0) {
                        event.preventDefault();
                        const file = item.getAsFile();
                        uploadImageToServer(file).then(url => {
                            if (url) view.dispatch(view.state.tr.replaceSelectionWith(view.state.schema.nodes.image.create({ src: url })));
                        });
                        return true; 
                    }
                }
                return false;
            },
            handleDrop(view, event, slice, moved) {
                if (!moved && event.dataTransfer && event.dataTransfer.files && event.dataTransfer.files[0]) {
                    const file = event.dataTransfer.files[0];
                    if (file.type.startsWith('image/')) {
                        event.preventDefault();
                        uploadImageToServer(file).then(url => {
                            if (url) view.dispatch(view.state.tr.replaceSelectionWith(view.state.schema.nodes.image.create({ src: url })));
                        });
                        return true;
                    }
                }
                return false;
            }
        },
        onUpdate: ({ editor }) => { 
            if (window.isPreventingSave) return;
            const app = window.Alpine ? window.Alpine.$data(document.body) : null;
            if (!app || !app.activeNoteId) return;
            updateTOC(editor);
            app.editorTick++;
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(saveNoteToServer, 1500);
        },
        onSelectionUpdate: ({ editor }) => {
            if (window.Alpine) {
                const app = window.Alpine.$data(document.body);
                app.editorTick++;
            }
        },
    });
    return editorInstance;
};

// -------------------------------------------------------------------------
// 6.5 INICIALIZACIÓN DE EVENT LISTENERS PARA AI
// -------------------------------------------------------------------------
setupAIEventListeners();

// -------------------------------------------------------------------------
// 7. EVENT LISTENERS Y COORDINACIÓN GLOBAL
// -------------------------------------------------------------------------
window.addEventListener('note-selected', async (e) => {
    const noteId = e.detail.id;
    if (!window.Alpine) return;
    const app = window.Alpine.$data(document.body);
    app.activeNoteId = noteId; 
    app.aiLoading = true;
    window.isPreventingSave = true;

    try {
        const response = await fetch(`/api/notes/${noteId}`);
        if (!response.ok) throw new Error("Error cargando nota");
        const data = await response.json();
        window.clearInspector();
        let contentToLoad;
        try { contentToLoad = JSON.parse(data.contenido); } catch (err) { contentToLoad = data.contenido; }
        const editor = initEditor(contentToLoad);
        const titleInput = document.querySelector('#note-title-input');
        if (titleInput) {
            titleInput.value = data.titulo || '';
            titleInput.style.height = 'auto';
            titleInput.style.height = titleInput.scrollHeight + 'px';
        }
        updateTOC(editor);
        updateInspector(data);
        app.aiLoading = false; 
        setTimeout(() => { window.isPreventingSave = false; }, 300);
    } catch (error) {
        console.error("Error:", error);
        app.aiLoading = false;
        window.isPreventingSave = false; 
    }
});

document.addEventListener('click', (e) => {
    const copyBtn = e.target.closest('.tool-copy');
    if (copyBtn) {
        const pre = copyBtn.closest('pre');
        const code = pre.querySelector('code');
        let text = code.innerText.replace(/\u00a0/g, ' ');
        navigator.clipboard.writeText(text);
        const icon = copyBtn.querySelector('i');
        icon.className = 'ph ph-check text-emerald-400';
        setTimeout(() => icon.className = 'ph ph-copy', 2000);
    }
}, true);

document.addEventListener('input', (e) => {
    if (e.target.id === 'note-title-input') {
        const app = window.Alpine ? window.Alpine.$data(document.body) : null;
        if (window.isPreventingSave || !app || !app.activeNoteId) return;
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(saveNoteToServer, 1500);
    }
});

document.addEventListener('DOMContentLoaded', () => { if (!editorInstance) initEditor(); });

// -------------------------------------------------------------------------
// 8. MÓDULO DE EXPORTACIÓN (AXIOMA I.IV)
// -------------------------------------------------------------------------
window.editorActions = {
    /**
     * Exporta a Markdown limpiando nodos de UI
     */
    copyAsMarkdown: () => {
        if (!editorInstance) return;
        const html = editorInstance.getHTML();
        const markdown = turndownService.turndown(html);
        
        navigator.clipboard.writeText(markdown).then(() => {
            const statusLabel = document.querySelector('#save-status');
            if (statusLabel) {
                statusLabel.innerText = "Markdown copiado";
                setTimeout(() => { statusLabel.innerText = ""; }, 2000);
            }
        });
    },

    /**
     * Exporta a Texto Plano puro
     */
    copyAsText: () => {
        if (!editorInstance) return;
        const text = editorInstance.getText();
        navigator.clipboard.writeText(text).then(() => {
            const statusLabel = document.querySelector('#save-status');
            if (statusLabel) {
                statusLabel.innerText = "Texto copiado";
                setTimeout(() => { statusLabel.innerText = ""; }, 2000);
            }
        });
    },

    printNote: () => {
        const titleInput = document.querySelector('#note-title-input');
        const title = titleInput ? titleInput.value : 'Sin título';
        const content = editorInstance.getHTML();

        // 1. Crear Iframe invisible
        const iframe = document.createElement('iframe');
        iframe.style.position = 'fixed';
        iframe.style.right = '0';
        iframe.style.bottom = '0';
        iframe.style.width = '0';
        iframe.style.height = '0';
        iframe.style.border = '0';
        document.body.appendChild(iframe);

        // 2. Definir el documento de impresión con CSS Editorial
        const printDoc = `
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>${title}</title>
                <link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;700&display=swap" rel="stylesheet">
                <style>
                    /* Reset Base */
                    * { margin: 0; padding: 0; box-sizing: border-box; }
                    body { 
                        font-family: 'Merriweather', serif; 
                        line-height: 1.65; 
                        color: #1a1a1a; 
                        background: #fff; 
                        padding: 2.5cm 2cm; /* Margen editorial estándar */
                    }

                    /* Tipografía */
                    h1 { 
                        font-family: 'Inter', sans-serif; 
                        font-size: 28pt; 
                        margin-bottom: 0.8cm; 
                        line-height: 1.2;
                        color: #000;
                    }
                    h2 { font-family: 'Inter', sans-serif; font-size: 18pt; margin: 1cm 0 0.5cm; color: #333; }
                    h3 { font-family: 'Inter', sans-serif; font-size: 14pt; margin: 0.8cm 0 0.4cm; color: #444; }
                    
                    p { margin-bottom: 1.2em; font-size: 11pt; text-align: justify; }
                    
                    /* Listas */
                    ul, ol { margin-bottom: 1.2em; padding-left: 1.2cm; }
                    li { margin-bottom: 0.5em; font-size: 11pt; }

                    /* Bloques de Código */
                    pre { 
                        background: #f8f9fa; 
                        padding: 12pt; 
                        border-radius: 6px; 
                        border: 1px solid #e1e4e8; 
                        font-family: 'Courier New', monospace; 
                        font-size: 9.5pt;
                        white-space: pre-wrap;
                        word-break: break-all;
                        margin: 1.5em 0;
                        page-break-inside: avoid;
                    }
                    code { font-family: inherit; }

                    /* Citas */
                    blockquote {
                        border-left: 4px solid #6366f1;
                        padding: 10pt 20pt;
                        background: #fdfdfd;
                        font-style: italic;
                        color: #555;
                        margin: 1.5em 0;
                    }

                    /* Tablas */
                    table { border-collapse: collapse; width: 100%; margin: 1.5em 0; }
                    th, td { border: 1px solid #ddd; padding: 10px; text-align: left; font-size: 10pt; }
                    th { background: #f5f5f5; font-weight: bold; }

                    /* Imágenes */
                    img { max-width: 100%; height: auto; border-radius: 4px; margin: 1em 0; }

                    /* Configuración de Página */
                    @page { 
                        size: A4; 
                        margin: 0; /* Controlamos el margen desde el body */
                    }
                    
                    /* Prevenir cortes feos */
                    h1, h2, h3 { page-break-after: avoid; }
                    .ProseMirror { outline: none; }
                </style>
            </head>
            <body>
                <h1>${title}</h1>
                <div class="content">${content}</div>
                <script>
                    // Esperar a que las fuentes y recursos carguen
                    window.onload = function() {
                        setTimeout(() => {
                            window.print();
                            // El Iframe se auto-elimina después de que el usuario interactúa con el diálogo
                            setTimeout(() => { window.frameElement.remove(); }, 500);
                        }, 250);
                    };
                </script>
            </body>
            </html>
        `;

        // 3. Inyectar documento en el Iframe
        const doc = iframe.contentWindow.document;
        doc.open();
        doc.write(printDoc);
        doc.close();
    }

};