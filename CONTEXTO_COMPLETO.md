# CONTEXTO DEL PROYECTO: proyecto-docs
Generado automáticamente para revisión de código.

## 📁 Estructura del Proyecto
```
    📄 requirements.txt
    📄 Dockerfile
    📄 .gitignore
    📄 docker-compose.yml
    📄 . dockerignore
    📂 .docs/
        📄 1_ARQUITECTURA.md
        📄 SOLUCION_COMPLETADA.md
        📄 LISTA_CAMBIOS_IMPLEMENTADOS.md
        📄 DIAGRAMA_FLUJO_EDITOR.md
        📄 REPORTE_FINAL.md
        📄 AUDIT_RESUMEN.md
        📄 RESUMEN_EJECUTIVO.md
        📄 DIAGRAMA_CAMBIOS_ANTES_DESPUES.md
        📄 FIX_QUICKVIEW_RESUMEN_TEXTO.md
        📄 PORTAL_MENU_CONTEXTUAL.md
        📄 DIAGNOSTICO_MODAL.md
        📄 QUICK_REFERENCE_MODAL.md
        📄 FIX_MOVER_NOTA_MODAL.md
        📄 0.1_REGLAS_NEGOCIO.md
        📄 AUDIT_DETALLADO.md
        📄 FIX_QUICKVIEW_CORRECTO.md
        📄 0_REFERENCIA_LEGACY.md
        📄 IMPLEMENTACION_QUICKVIEW.md
        📄 CONTEXTO_ACTUAL.md
        📄 ANALISIS_FORENSE_CAUSA_RAIZ.md
        📄 VALIDACION_FLUJO_INBOX.md
        📄 SOLUCION_FINAL_MODAL.md
        📄 GUIA_PRUEBA_COMPLETA.md
        📄 IMPLEMENTACION_PORTAL_COMPLETA.md
        📄 2_ESTADO_ACTUAL.md
        📄 ESPECIFICACION_QUICKVIEW_INBOX.md
        📄 ANALISIS_ESTADOS_MODAL.md
        📄 SOLUCION_ARQUITECTONICA_MODAL.md
        📄 QUICK_REFERENCE_TIPTAP.md
        📄 ANALISIS_ESTRUCTURAL_PROFUNDO.md
        📄 VALIDACION_EDITOR_TIPTAP.md
        📄 1_ARQUITECTURA_PROPUESTA.md
        📄 INDICE_DOCUMENTACION.md
        📄 AUDIT_REMEDIACION.md
        📄 0_FILOSOFIA_PROYECTO.md
        📄 ANALISIS_ARQUITECTONICO_MODAL.md
        📄 CORRECCIONES_REACTIVIDAD_TIPTAP.md
        📄 2_SYSTEM_INSTRUCTIONS.md
        📄 TESTING_CHECKLIST.md
        📄 DIAGNOSTICO_FLUJO_CUADERNOS.md
        📄 ARQUITECTURA_HTMX_SWAPS.md
    📂 app/
        📄 models.py
        📄 __init__.py
        📄 main.py
        📂 routers/
            📄 auth.py
            📄 dashboard.py
        📂 core/
            📄 auth.py
            📄 config.py
            📄 database.py
            📄 security.py
    📂 utils/
        📄 migrar.py
    📂 static/
        📂 css/
            📄 styles.css
        📂 js/
            📄 editor.js
            📄 app.js
            📂 components/
    📂 .github/
        📄 copilot-instructions.md
    📂 .research/
        📄 idea4.html
        📄 inspector2.html
        📄 book1.html
        📄 idea2.html
        📄 idea3.html
        📄 contenido1.html
        📄 book3.html
        📄 contenido2.html
        📄 idea1.html
        📄 book2.html
        📄 book4.html
        📂 archive/
    📂 templates/
        📂 layouts/
            📄 base.html
        📂 modules/
            📄 sidebar_notebook.html
            📄 sidebar_dashboard.html
            📄 cockpit_pane.html
            📄 sidebar_projects.html
            📄 sidebar_inbox.html
        📂 pages/
            📄 register.html
            📄 login.html
        📂 partials/
            📄 modal_edit_categoria.html
            📄 modal_cuaderno.html
            📄 attachments_list.html
            📄 floating_note.html
            📄 modal_inbox_triaje.html
            📄 modal_eliminar_nota.html
            📄 modal_tema.html
            📄 modal_confirm_edit.html
            📄 editor_content.html
            📄 modal_categoria.html
            📄 modal_edit_cuaderno.html
            📄 modal_confirm_delete.html
            📄 modal_edit_tema.html
```

---

## 📄 Archivo: `.research/book1.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zen Writer Pro - Concepto</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400&display=swap" rel="stylesheet">
    <style>
        /* Tipografía de libro */
        .prose-book {
            font-family: 'Crimson Pro', serif;
            font-size: 21px;
            line-height: 1.6;
            color: #2d2d2d;
        }

        /* Simulación de página */
        .page-canvas {
            min-height: 29.7cm; /* Proporción A4 aproximada */
            width: 21cm;
            padding: 3cm 2.5cm;
            margin: 2rem auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            transition: all 0.5s ease;
        }

        /* Modos de Color */
        .theme-sepia { background-color: #f4ecd8; }
        .theme-sepia .page-canvas { background-color: #fdfaf3; color: #433422; }

        .theme-dark { background-color: #1a1a1a; }
        .theme-dark .page-canvas { background-color: #242424; color: #e0e0e0; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }

        /* Línea de "Página Siguiente" */
        .page-break-indicator {
            border-top: 1px dashed #ccc;
            height: 0;
            margin: 2rem -2.5cm;
            position: relative;
        }
        .page-break-indicator::after {
            content: "Página 2";
            position: absolute;
            right: 0;
            top: -10px;
            font-size: 10px;
            font-family: 'Inter', sans-serif;
            text-transform: uppercase;
            opacity: 0.5;
        }

        [contenteditable]:focus { outline: none; }
        
        /* Ocultar barra de scroll para máxima inmersión */
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: #8883; border-radius: 10px; }
    </style>
</head>
<body 
    x-data="{ 
        mode: 'sepia', 
        zen: true, 
        showToolbar: false,
        wordCount: 450,
        pageEstimate: 1
    }" 
    :class="'theme-' + mode"
    class="transition-colors duration-700 ease-in-out min-h-screen"
>

    <!-- Barra de Herramientas Flotante (Aparece al mover el mouse arriba) -->
    <nav 
        @mouseenter="showToolbar = true" 
        @mouseleave="showToolbar = false"
        :class="showToolbar ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4'"
        class="fixed top-0 left-0 right-0 z-50 transition-all duration-300 p-4 flex justify-center gap-4 bg-gradient-to-b from-black/10 to-transparent"
    >
        <div class="bg-white/80 backdrop-blur-md px-6 py-2 rounded-full shadow-2xl flex items-center gap-6 border border-white/20">
            <div class="flex gap-2">
                <button @click="mode = 'sepia'" class="w-6 h-6 rounded-full bg-[#f4ecd8] border border-black/10"></button>
                <button @click="mode = 'light'" class="w-6 h-6 rounded-full bg-white border border-black/10"></button>
                <button @click="mode = 'dark'" class="w-6 h-6 rounded-full bg-[#1a1a1a] border border-white/10"></button>
            </div>
            
            <div class="h-4 w-[1px] bg-gray-300"></div>
            
            <button class="text-sm font-medium text-gray-600 hover:text-black transition">Exportar PDF</button>
            <button @click="zen = !zen" class="text-sm font-medium text-indigo-600">
                <span x-text="zen ? 'Salir de Zen' : 'Modo Zen'"></span>
            </button>
        </div>
    </nav>

    <!-- Contenedor Principal -->
    <main :class="zen ? 'pt-10' : 'pt-20'" class="transition-all duration-500">
        
        <!-- El Manuscrito (Representa el editor de TipTap) -->
        <article class="page-canvas prose-book relative group">
            
            <!-- Título del Libro -->
            <header class="mb-12 text-center">
                <h1 contenteditable="true" class="text-4xl font-semibold opacity-80 mb-2 focus:opacity-100 italic">El Nombre del Viento</h1>
                <p class="text-xs tracking-widest uppercase opacity-40 font-sans">Capítulo Uno</p>
            </header>

            <!-- Área de Contenido de TipTap -->
            <div contenteditable="true" class="min-h-screen focus:outline-none">
                <p class="mb-6">
                    Hacía calor en la posada Roca de Guía. Era el calor sofocante y sordo de los finales de otoño. Era un calor hecho de silencios, y el silencio de la posada era un silencio triple.
                </p>
                <p class="mb-6">
                    El silencio más obvio era una calma hueca y desolada, hecha de las cosas que faltaban. Si hubiera soplado el viento, este habría suspirado entre las ramas, habría hecho chirriar el letrero de la posada en sus fijaciones y habría arrastrado el silencio calle abajo como si fueran hojas secas de otoño.
                </p>
                
                <!-- Simulador de Salto de Página Visual -->
                <div class="page-break-indicator my-12" contenteditable="false"></div>

                <p class="mb-6">
                    Si hubiera habido gente en la posada, aunque solo fuera un puñado de clientes, ellos habrían llenado el silencio con su conversación y sus risas, con el alboroto y el tintineo de los vasos...
                </p>
                <p class="text-gray-400 italic">Continúa escribiendo tu obra maestra aquí...</p>
            </div>

            <!-- Footer de la página -->
            <footer class="mt-20 text-center opacity-30 font-sans text-sm">
                — 1 —
            </footer>
        </article>
    </main>

    <!-- Barra de Estado Inferior (Minimalista) -->
    <div class="fixed bottom-6 left-1/2 -translate-x-1/2 flex items-center gap-8 px-6 py-2 rounded-full text-[10px] tracking-widest uppercase font-sans opacity-40 hover:opacity-100 transition-opacity">
        <div><span x-text="wordCount"></span> Palabras</div>
        <div><span x-text="pageEstimate"></span> Página A4</div>
        <div>Guardado en la Nube</div>
    </div>

</body>
</html>
```

---

## 📄 Archivo: `.research/book2.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Knowledge OS - Zen Concept</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --sepia-bg: #f4ecd8;
            --sepia-paper: #fdfaf3;
            --dark-bg: #0f1117;
            --dark-paper: #1a1d26;
        }

        body { font-family: 'Inter', sans-serif; transition: all 0.5s ease; }
        .serif { font-family: 'Crimson Pro', serif; }
        .mono { font-family: 'JetBrains Mono', monospace; }

        /* MODOS DE COLOR */
        .zen-writer { background-color: var(--sepia-bg); color: #433422; }
        .zen-study { background-color: var(--dark-bg); color: #cbd5e1; }

        /* EL PAPEL (APILADO) */
        .paper-stack {
            width: 21cm;
            min-height: 29.7cm;
            padding: 3cm 2.5cm;
            margin: 4rem auto;
            position: relative;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Efecto de hojas apiladas (Axioma de Finitud) */
        .zen-writer .paper-stack {
            background-color: var(--sepia-paper);
            box-shadow: 
                0 1px 1px rgba(0,0,0,0.1),
                0 10px 0 -5px var(--sepia-paper),
                0 10px 1px -4px rgba(0,0,0,0.1),
                0 20px 0 -10px var(--sepia-paper),
                0 20px 1px -9px rgba(0,0,0,0.1);
        }

        .zen-study .paper-stack {
            background-color: var(--dark-paper);
            width: 900px;
            padding: 2rem 4rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255,255,255,0.05);
        }

        /* LÍNEA DE ENFOQUE (TYPEWRITER MODE) */
        .focus-line {
            position: fixed;
            top: 50%;
            left: 0;
            right: 0;
            height: 1.8em;
            background: rgba(99, 102, 241, 0.05);
            border-top: 1px solid rgba(99, 102, 241, 0.1);
            border-bottom: 1px solid rgba(99, 102, 241, 0.1);
            pointer-events: none;
            z-index: 10;
        }

        /* NOTAS AL MARGEN (MODO ESTUDIO) */
        .margin-note {
            position: absolute;
            right: -260px;
            width: 220px;
            font-size: 0.75rem;
            padding: 1rem;
            background: rgba(99, 102, 241, 0.1);
            border-left: 2px solid #6366f1;
            border-radius: 0 0.5rem 0.5rem 0;
            color: #a5b4fc;
        }

        /* CURSOR MÁQUINA DE ESCRIBIR */
        .typewriter-cursor {
            display: inline-block;
            width: 2px;
            height: 1.2em;
            background: #6366f1;
            margin-left: 2px;
            animation: blink 1s infinite;
        }
        @keyframes blink { 50% { opacity: 0; } }

        [x-cloak] { display: none !important; }
    </style>
</head>
<body x-data="{ lens: 'writer' }" :class="'zen-' + lens">

    <!-- LÍNEA DE GUÍA (Solo visible en Escritura) -->
    <div class="focus-line" x-show="lens === 'writer'" x-transition></div>

    <!-- NAVEGACIÓN DE MODOS (EFÍMERA) -->
    <nav class="fixed top-6 left-1/2 -translate-x-1/2 z-[100] bg-white/10 backdrop-blur-lg border border-white/20 p-1 rounded-2xl flex gap-1 shadow-2xl">
        <button @click="lens = 'writer'" 
                :class="lens === 'writer' ? 'bg-white/20 text-white' : 'text-white/40 hover:text-white'"
                class="px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2">
            <i class="ph-fill ph-pen-nib"></i> Manuscrito
        </button>
        <button @click="lens = 'study'" 
                :class="lens === 'study' ? 'bg-indigo-600 text-white' : 'text-white/40 hover:text-white'"
                class="px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2">
            <i class="ph-fill ph-microscope"></i> Laboratorio
        </button>
    </nav>

    <!-- LIENZO PRINCIPAL -->
    <main class="relative z-20">
        
        <article class="paper-stack transition-all duration-700">
            
            <!-- HEADER DE PÁGINA -->
            <header class="mb-16 text-center" :class="lens === 'study' ? 'text-left mb-8' : ''">
                <h1 class="text-4xl font-semibold opacity-90 serif italic" 
                    :class="lens === 'study' ? 'not-italic font-sans text-white text-3xl mb-2' : ''">
                    El Nombre del Viento
                </h1>
                <p class="text-[10px] tracking-[0.3em] uppercase opacity-40 font-sans">
                    <span x-show="lens === 'writer'">Capítulo Uno: Un lugar de silencios</span>
                    <span x-show="lens === 'study'">Material de Análisis / Filosofía</span>
                </p>
            </header>

            <!-- CONTENIDO EDITORIAL -->
            <div class="serif text-xl leading-relaxed space-y-8 outline-none" 
                 :class="lens === 'study' ? 'font-sans text-base text-slate-300' : ''"
                 contenteditable="true">
                
                <p class="relative">
                    Hacía calor en la posada Roca de Guía. Era el calor sofocante y sordo de los finales de otoño. Era un calor hecho de silencios, y el silencio de la posada era un silencio triple.
                    
                    <!-- Nota al margen (Solo estudio) -->
                    <span x-show="lens === 'study'" class="margin-note top-0">
                        <b class="block mb-1 text-indigo-400">ANÁLISIS DE IA</b>
                        La estructura del "silencio triple" establece una atmósfera de misticismo. ¿Quieres ver cómo lo usa el autor en otros capítulos?
                    </span>
                </p>

                <p>
                    El silencio más obvio era una calma hueca y desolada, hecha de las cosas que faltaban. Si hubiera soplado el viento, este habría suspirado entre las ramas, habría hecho chirriar el letrero de la posada en sus fijaciones.
                    
                    <span x-show="lens === 'study'" class="inline-flex items-center gap-1 bg-indigo-500/20 text-indigo-300 px-1 rounded cursor-help">
                        chirriar <i class="ph ph-sparkle text-[10px]"></i>
                    </span>
                </p>

                <!-- SALTO DE PÁGINA VISUAL -->
                <div class="h-px bg-current opacity-5 my-12 relative flex justify-center items-center" x-show="lens === 'writer'">
                    <span class="bg-inherit px-4 text-[10px] uppercase tracking-widest opacity-20 serif italic">Página Siguiente</span>
                </div>

                <p>
                    Kote se encontraba tras la barra, frotando un trozo de madera de pino con un trapo blanco. El movimiento era rítmico, pausado, casi una meditación. 
                    <span x-show="lens === 'writer'" class="typewriter-cursor"></span>
                </p>

                <p x-show="lens === 'study'" class="p-4 bg-white/5 rounded-xl border border-white/10 italic text-slate-400">
                    "El hombre tenía el cabello de un rojo tan brillante como el fuego, y sus ojos eran distantes, como los de alguien que ha visto demasiado mundo."
                </p>
            </div>

            <!-- MARCA DE AGUA / PÁGINA -->
            <footer class="mt-24 text-center opacity-30 font-sans text-xs tracking-widest">
                — <span x-text="lens === 'writer' ? 'Folio 1' : 'Sección 1.1'"></span> —
            </footer>
        </article>

    </main>

    <!-- BARRA DE ESTADO INFERIOR -->
    <div class="fixed bottom-6 left-0 right-0 px-12 flex justify-between items-end pointer-events-none">
        
        <!-- Stats Izquierda -->
        <div class="bg-black/10 backdrop-blur-md px-4 py-2 rounded-lg border border-white/5 text-[10px] uppercase tracking-widest opacity-60 pointer-events-auto">
            <span class="font-bold" x-text="lens === 'writer' ? '428 palabras' : '8 min lectura'"></span>
        </div>

        <!-- Atajos IA Derecha -->
        <div class="flex flex-col gap-2 items-end">
            <template x-if="lens === 'study'">
                <button class="bg-indigo-600 text-white p-3 rounded-full shadow-2xl pointer-events-auto hover:scale-110 transition-transform">
                    <i class="ph-fill ph-sparkle text-xl"></i>
                </button>
            </template>
            <div class="bg-black/10 backdrop-blur-md px-4 py-2 rounded-lg border border-white/5 text-[10px] uppercase tracking-widest opacity-60 pointer-events-auto">
                Autoguardado: <span class="mono">Sync OK</span>
            </div>
        </div>
    </div>

</body>
</html>
```

---

## 📄 Archivo: `.research/book3.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Knowledge OS - Zen Writer Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
    
    <style>
        body { 
            background-color: #0f1117; 
            color: #cbd5e1; 
            font-family: 'Inter', sans-serif; 
            overflow: hidden; 
        }
        .serif { font-family: 'Crimson Pro', serif; }

        /* 1. NAVEGADOR DE PÁGINAS (IZQUIERDA) - Según tu dibujo */
        .page-strip {
            position: fixed;
            left: 2rem;
            top: 0;
            bottom: 0;
            width: 100px;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem 0;
            gap: 1.5rem;
            overflow-y: auto;
            z-index: 50;
        }
        .page-strip::-webkit-scrollbar { display: none; }

        .thumb-unit {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
        }
        .thumb-box {
            width: 50px;
            height: 70px;
            background: #22d3ee; /* El Cian de tu dibujo */
            opacity: 0.4;
            border-radius: 2px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .thumb-unit.active .thumb-box {
            opacity: 1;
            box-shadow: 0 0 15px rgba(34, 211, 238, 0.4);
            transform: scale(1.1);
        }
        .add-btn-small {
            width: 18px;
            height: 18px;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 2px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            color: rgba(255,255,255,0.5);
            cursor: pointer;
            transition: all 0.2s;
        }
        .add-btn-small:hover { background: rgba(255,255,255,0.1); color: white; }

        /* 2. ESCENARIO CENTRAL (EL PAPEL) */
        .stage {
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 4rem 0;
        }

        .active-page {
            width: 21cm;
            height: 29.7cm;
            background: #333333; /* El Gris oscuro de tu dibujo */
            padding: 3cm 2.5cm;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            position: relative;
            z-index: 20;
            color: white;
        }

        /* PÁGINAS GHOST (ARRIBA Y ABAJO) - Según tu dibujo */
        .ghost-page {
            width: 21cm;
            height: 120px; /* Solo una porción como en tu dibujo */
            background: #22d3ee; /* El Cian de tu dibujo */
            opacity: 0.2;
            display: flex;
            align-items: flex-end;
            justify-content: center;
            padding-bottom: 0.5rem;
            position: relative;
            filter: blur(1px);
        }
        .ghost-page.top { border-radius: 4px 4px 0 0; }
        .ghost-page.bottom { border-radius: 0 0 4px 4px; align-items: flex-start; padding-top: 0.5rem; }

        .add-btn-large {
            width: 24px;
            height: 24px;
            border: 1px solid rgba(255,255,255,0.3);
            background: rgba(15, 17, 23, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 14px;
            cursor: pointer;
            z-index: 30;
            margin: -12px 0; /* Para que flote en el corte */
        }

        /* 3. NAVEGACIÓN RÁPIDA (DERECHA) - Según tu dibujo */
        .fast-nav {
            position: fixed;
            right: 3rem;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            flex-direction: column;
            gap: 20vh; /* Espaciado amplio como en tu dibujo */
            z-index: 50;
        }
        .nav-arrow {
            font-size: 2rem;
            color: rgba(255,255,255,0.2);
            cursor: pointer;
            transition: all 0.3s;
        }
        .nav-arrow:hover { color: #22d3ee; transform: scale(1.2); }

        /* 4. LABORATORIO (NOTAS AL MARGEN - PRESERVADAS) */
        .margin-note {
            position: absolute;
            right: -260px;
            width: 220px;
            font-size: 0.75rem;
            padding: 1rem;
            background: rgba(99, 102, 241, 0.1);
            border-left: 2px solid #6366f1;
            border-radius: 0 0.5rem 0.5rem 0;
            color: #a5b4fc;
            text-align: left;
            font-family: 'Inter', sans-serif;
        }
    </style>
</head>
<body x-data="{ lens: 'writer', activePage: 2 }">

    <!-- 1. NAVEGADOR IZQUIERDO (Páginas Miniatura) -->
    <aside class="page-strip" x-show="lens === 'writer'">
        <template x-for="p in [1, 2, 3, 4, 5]">
            <div class="thumb-unit" :class="activePage === p ? 'active' : ''">
                <div class="thumb-box" @click="activePage = p"></div>
                <div class="add-btn-small"><i class="ph ph-plus"></i></div>
            </div>
        </template>
    </aside>

    <!-- 2. ESCENARIO CENTRAL -->
    <main class="stage">
        
        <!-- Ghost Page Arriba -->
        <div class="ghost-page top" x-show="lens === 'writer'">
            <div class="serif opacity-20 text-xs italic">Final de la página anterior...</div>
        </div>
        
        <!-- Botón añadir arriba -->
        <div class="add-btn-large" x-show="lens === 'writer'"><i class="ph ph-plus"></i></div>

        <!-- PÁGINA ACTIVA (Tu rectángulo gris) -->
        <article class="active-page serif">
            <h2 class="text-3xl font-bold mb-8">Capítulo II: Sombras</h2>
            
            <div class="text-xl leading-relaxed space-y-6 outline-none" contenteditable="true">
                <p class="relative">
                    El texto fluye aquí, en el corazón del folio gris. La concentración es absoluta. No hay bordes blancos que deslumbren, solo el pensamiento puro sobre el lienzo oscuro.
                    
                    <!-- NOTA DE LABORATORIO (Preservada idéntica) -->
                    <span x-show="lens === 'study'" class="margin-note top-0">
                        <b class="block mb-1 text-indigo-400">STICKY NOTE</b>
                        He mantenido este formato exactamente como pediste: margen derecho, borde azul y fondo translúcido.
                    </span>
                </p>

                <p>
                    Kote frotó la madera rítmicamente. En el dibujo que trazaste, este espacio era el protagonista. He respetado los márgenes internos para que el texto respire.
                </p>

                <p>
                    Cualquier palabra escrita aquí se siente definitiva, como tallada en piedra volcánica.
                </p>
            </div>

            <!-- Marca de página inferior -->
            <footer class="absolute bottom-12 left-0 right-0 text-center opacity-20 font-sans text-xs tracking-widest">
                — FOLIO <span x-text="activePage"></span> —
            </footer>
        </article>

        <!-- Botón añadir abajo -->
        <div class="add-btn-large" x-show="lens === 'writer'"><i class="ph ph-plus"></i></div>

        <!-- Ghost Page Abajo -->
        <div class="ghost-page bottom" x-show="lens === 'writer'">
            <div class="serif opacity-20 text-xs italic">Comienzo de la página siguiente...</div>
        </div>

    </main>

    <!-- 3. NAVEGACIÓN RÁPIDA (DERECHA) -->
    <nav class="fast-nav" x-show="lens === 'writer'">
        <i class="ph-fill ph-caret-double-up nav-arrow"></i>
        <i class="ph-fill ph-caret-double-down nav-arrow"></i>
    </nav>

    <!-- SELECTOR DE LENTE (Para probar el Laboratorio) -->
    <div class="fixed top-6 right-6 z-[100] flex gap-2">
        <button @click="lens = 'writer'" :class="lens === 'writer' ? 'bg-cyan-500 text-black' : 'bg-white/10 text-white'" class="px-4 py-2 rounded-full text-xs font-bold transition-all">Modo Escritor</button>
        <button @click="lens = 'study'" :class="lens === 'study' ? 'bg-indigo-600 text-white' : 'bg-white/10 text-white'" class="px-4 py-2 rounded-full text-xs font-bold transition-all">Modo Laboratorio</button>
    </div>

</body>
</html>
```

---

## 📄 Archivo: `.research/book4.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Knowledge OS - Zen Writer Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg-obsidian: #090a0f;
            --paper-slate: #1e2029;
            --accent-cyan: #22d3ee;
            --ghost-cyan: rgba(34, 211, 238, 0.03);
        }

        body { 
            background-color: var(--bg-obsidian); 
            color: #94a3b8; 
            font-family: 'Inter', sans-serif; 
            overflow: hidden; 
        }
        .serif { font-family: 'Crimson Pro', serif; }
        .mono { font-family: 'JetBrains Mono', monospace; }

        /* 1. NAVEGADOR DE PÁGINAS (IZQUIERDA) - Refinado */
        .page-strip {
            position: fixed;
            left: 0;
            top: 0;
            bottom: 0;
            width: 140px;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 3rem 0;
            gap: 2rem;
            background: linear-gradient(90deg, rgba(0,0,0,0.2) 0%, transparent 100%);
            z-index: 50;
        }

        .thumb-unit {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.75rem;
            position: relative;
        }

        .thumb-box {
            width: 54px;
            height: 76px;
            background: var(--paper-slate);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }

        /* Simulación de líneas de texto en la miniatura */
        .thumb-box::before {
            content: "";
            position: absolute;
            top: 10px; left: 10px; right: 10px; bottom: 10px;
            background-image: linear-gradient(transparent 50%, rgba(34, 211, 238, 0.1) 50%);
            background-size: 100% 6px;
        }

        .thumb-unit.active .thumb-box {
            border-color: var(--accent-cyan);
            box-shadow: 0 0 25px rgba(34, 211, 238, 0.15);
            transform: scale(1.15) translateX(5px);
        }

        .add-btn-mini {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            color: rgba(255,255,255,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .add-btn-mini:hover { 
            background: var(--accent-cyan); 
            color: black; 
            border-color: var(--accent-cyan);
            box-shadow: 0 0 10px var(--accent-cyan);
        }

        /* 2. ESCENARIO CENTRAL (EL PAPEL) - Profesional */
        .stage {
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem 0;
            overflow-y: auto;
        }
        .stage::-webkit-scrollbar { display: none; }

        .active-page {
            width: 21cm;
            min-height: 29.7cm;
            background: var(--paper-slate);
            padding: 3.5cm 3cm;
            box-shadow: 0 50px 100px -20px rgba(0, 0, 0, 0.8);
            position: relative;
            z-index: 20;
            color: #e2e8f0;
            border: 1px solid rgba(255,255,255,0.03);
        }

        /* PÁGINAS GHOST (ARRIBA Y ABAJO) - Elegantes */
        .ghost-page {
            width: 21cm;
            height: 140px;
            background: linear-gradient(to bottom, transparent, var(--ghost-cyan));
            border: 1px solid rgba(34, 211, 238, 0.05);
            position: relative;
            filter: blur(2px);
            opacity: 0.4;
            transition: opacity 0.3s;
        }
        .ghost-page.bottom { background: linear-gradient(to top, transparent, var(--ghost-cyan)); }
        .ghost-page:hover { opacity: 0.6; }

        .insertion-divider {
            width: 21cm;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(34, 211, 238, 0.2), transparent);
            margin: 1.5rem 0;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .add-btn-main {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: var(--bg-obsidian);
            border: 1px solid var(--accent-cyan);
            color: var(--accent-cyan);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            cursor: pointer;
            box-shadow: 0 0 15px rgba(34, 211, 238, 0.2);
            transition: all 0.3s;
        }
        .add-btn-main:hover { transform: scale(1.2); background: var(--accent-cyan); color: black; }

        /* 3. NAVEGACIÓN RÁPIDA (DERECHA) - Minimalista */
        .fast-nav {
            position: fixed;
            right: 4rem;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            flex-direction: column;
            gap: 15vh;
            z-index: 50;
        }
        .nav-arrow {
            font-size: 1.5rem;
            color: rgba(255,255,255,0.1);
            cursor: pointer;
            transition: all 0.3s;
        }
        .nav-arrow:hover { color: var(--accent-cyan); transform: translateY(-5px); }
        .nav-arrow.down:hover { transform: translateY(5px); }

        /* 4. LABORATORIO (STICKY NOTES - PRESERVADAS) */
        .margin-note {
            position: absolute;
            right: -280px;
            width: 240px;
            font-size: 0.8rem;
            padding: 1.25rem;
            background: rgba(34, 211, 238, 0.03);
            backdrop-filter: blur(8px);
            border-left: 3px solid var(--accent-cyan);
            border-radius: 0 0.75rem 0.75rem 0;
            color: #a5b4fc;
            text-align: left;
            font-family: 'Inter', sans-serif;
            box-shadow: 10px 10px 30px rgba(0,0,0,0.3);
        }

        /* Cursor Custom */
        .cursor-writer {
            display: inline-block;
            width: 2px;
            height: 1.2em;
            background: var(--accent-cyan);
            margin-left: 2px;
            animation: blink 1s infinite;
            vertical-align: middle;
        }
        @keyframes blink { 50% { opacity: 0; } }

        [x-cloak] { display: none !important; }
    </style>
</head>
<body x-data="{ lens: 'writer', activePage: 2 }">

    <!-- 1. Paginación Lateral (Basada en tu esquema) -->
    <aside class="page-strip" x-show="lens === 'writer'">
        <div class="thumb-unit">
             <div class="add-btn-mini"><i class="ph-bold ph-plus"></i></div>
        </div>
        <template x-for="p in [1, 2, 3, 4, 5]">
            <div class="thumb-unit" :class="activePage === p ? 'active' : ''">
                <div class="thumb-box" @click="activePage = p"></div>
                <span class="text-[9px] font-bold tracking-widest opacity-20 uppercase mt-1">Folio 0<span x-text="p"></span></span>
                <div class="add-btn-mini mt-2"><i class="ph-bold ph-plus"></i></div>
            </div>
        </template>
    </aside>

    <!-- 2. Escenario de Escritura -->
    <main class="stage">
        
        <!-- Ghost Page Superior -->
        <div class="ghost-page top" x-show="lens === 'writer'"></div>
        
        <!-- Corte de Página con Inserción -->
        <div class="insertion-divider" x-show="lens === 'writer'">
            <div class="add-btn-main"><i class="ph-bold ph-plus"></i></div>
        </div>

        <!-- PÁGINA ACTIVA (El corazón de tu idea) -->
        <article class="active-page serif">
            
            <header class="mb-12">
                <p class="mono text-[10px] uppercase tracking-[0.4em] text-cyan-500/50 mb-4">Proyecto: El Nombre del Viento</p>
                <h2 class="text-4xl font-semibold italic text-white/90">Capítulo II: Sombras en el Camino</h2>
            </header>
            
            <div class="text-xl leading-relaxed space-y-8 outline-none" contenteditable="true">
                <p class="relative">
                    Hacía calor en la posada Roca de Guía. Era el calor sofocante y sordo de los finales de otoño. Era un calor hecho de silencios, y el silencio de la posada era un silencio triple.
                    
                    <!-- LABORATORIO (Preservado a solicitud) -->
                    <span x-show="lens === 'study'" class="margin-note top-0">
                        <b class="block mb-2 text-cyan-400 tracking-wider uppercase text-[10px]">Asistente de Análisis</b>
                        Este formato ha sido preservado íntegramente: posición marginal derecha, borde de color y fondo translúcido. 
                    </span>
                </p>

                <p>
                    El silencio más obvio era una calma hueca y desolada, hecha de las cosas que faltaban. Si hubiera soplado el viento, este habría suspirado entre las ramas.
                </p>

                <p>
                    Kote se encontraba tras la barra, frotando un trozo de madera. En el dibujo que trazaste, este folio gris oscuro era el protagonista. He elevado el contraste para que el texto sea "obsidiana sobre humo". <span class="cursor-writer"></span>
                </p>
            </div>

            <!-- Numeración Editorial -->
            <footer class="absolute bottom-12 left-0 right-0 text-center opacity-20 mono text-[10px] tracking-[0.5em]">
                0<span x-text="activePage"></span> / 154
            </footer>
        </article>

        <!-- Corte de Página Inferior -->
        <div class="insertion-divider" x-show="lens === 'writer'">
            <div class="add-btn-main"><i class="ph-bold ph-plus"></i></div>
        </div>

        <!-- Ghost Page Inferior -->
        <div class="ghost-page bottom" x-show="lens === 'writer'"></div>

    </main>

    <!-- 3. Navegación Rápida (Derecha) -->
    <nav class="fast-nav" x-show="lens === 'writer'">
        <i class="ph-bold ph-caret-double-up nav-arrow"></i>
        <i class="ph-bold ph-caret-double-down nav-arrow down"></i>
    </nav>

    <!-- BARRA DE ESTADO (Elegante) -->
    <div class="fixed bottom-8 left-0 right-0 px-12 flex justify-between items-center pointer-events-none">
        <div class="flex gap-4 items-center bg-black/40 backdrop-blur-md px-6 py-2 rounded-full border border-white/5 pointer-events-auto">
            <div class="text-[10px] font-bold tracking-widest text-slate-500 uppercase">
                Métrica: <span class="text-white">2,410 palabras</span>
            </div>
            <div class="w-px h-3 bg-white/10"></div>
            <div class="text-[10px] font-bold tracking-widest text-slate-500 uppercase">
                Tiempo: <span class="text-white">45 min</span>
            </div>
        </div>

        <div class="flex gap-2 pointer-events-auto">
            <button @click="lens = 'writer'" :class="lens === 'writer' ? 'bg-cyan-500 text-black' : 'bg-white/5 text-slate-400'" class="px-5 py-2 rounded-full text-[10px] font-bold tracking-widest uppercase transition-all">Escritor</button>
            <button @click="lens = 'study'" :class="lens === 'study' ? 'bg-indigo-600 text-white' : 'bg-white/5 text-slate-400'" class="px-5 py-2 rounded-full text-[10px] font-bold tracking-widest uppercase transition-all">Laboratorio</button>
        </div>
    </div>

</body>
</html>
```

---

## 📄 Archivo: `.research/contenido1.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rediseño Contenido Premium</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');
        
        :root {
            --bg-main: #09090b;
            --sidebar-bg: #0f0f12;
            --accent-purple: #8b5cf6;
            --border-color: rgba(255, 255, 255, 0.06);
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-main);
            color: #d1d5db;
        }

        /* Efecto de cristal y profundidad */
        .library-card {
            background: linear-gradient(145deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0) 100%);
            border: 1px solid var(--border-color);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .library-card:hover {
            border-color: rgba(139, 92, 246, 0.3);
            background: rgba(139, 92, 246, 0.02);
        }

        /* Líneas conectoras elegantes */
        .tree-line {
            position: absolute;
            left: -18px;
            top: -10px;
            bottom: 10px;
            width: 1px;
            background: linear-gradient(to bottom, var(--border-color), var(--accent-purple), var(--border-color));
            opacity: 0.5;
        }

        .item-active {
            background: rgba(139, 92, 246, 0.1);
            color: white;
            box-shadow: inset 4px 0 0 var(--accent-purple);
        }

        .custom-scroll::-webkit-scrollbar { width: 3px; }
        .custom-scroll::-webkit-scrollbar-thumb { background: #27272a; border-radius: 10px; }
    </style>
</head>
<body class="flex h-screen overflow-hidden">

    <!-- PANEL CONTENIDO -->
    <aside class="w-80 bg-[#0f0f12] border-r border-white/5 flex flex-col h-full shadow-2xl">
        
        <!-- Header -->
        <div class="p-6 flex items-center justify-between">
            <div>
                <h2 class="text-[10px] font-bold uppercase tracking-[0.2em] text-gray-500">Biblioteca</h2>
                <p class="text-sm font-semibold text-white/90">Estructura de Trabajo</p>
            </div>
            <button class="w-8 h-8 rounded-full border border-white/5 flex items-center justify-center hover:bg-white/5 transition-colors">
                <i data-lucide="plus" class="w-4 h-4 text-gray-400"></i>
            </button>
        </div>

        <!-- Buscador Estilizado -->
        <div class="px-6 mb-6">
            <div class="relative">
                <input type="text" placeholder="Filtrar recursos..." 
                    class="w-full bg-white/[0.02] border border-white/5 rounded-xl py-2 pl-9 pr-4 text-xs focus:outline-none focus:border-purple-500/50 transition-all placeholder:text-gray-600">
                <i data-lucide="search" class="w-3.5 h-3.5 absolute left-3 top-2.5 text-gray-600"></i>
            </div>
        </div>

        <!-- Lista de Bibliotecas -->
        <div class="flex-1 overflow-y-auto custom-scroll px-4 space-y-3 pb-10" x-data="{ selected: 'personal' }">
            
            <!-- BIBLIOTECA GENERAL -->
            <div x-data="{ open: false }" class="library-card rounded-2xl overflow-hidden">
                <button @click="open = !open" class="w-full p-4 flex items-center justify-between group">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center border border-blue-500/20">
                            <i data-lucide="layout-grid" class="w-4 h-4 text-blue-400"></i>
                        </div>
                        <span class="text-xs font-medium text-gray-300 group-hover:text-white transition-colors">General</span>
                    </div>
                    <i data-lucide="chevron-down" class="w-3 h-3 text-gray-600 transition-transform" :class="open ? 'rotate-180' : ''"></i>
                </button>
            </div>

            <!-- BIBLIOTECA N8N -->
            <div x-data="{ open: false }" class="library-card rounded-2xl overflow-hidden">
                <button @click="open = !open" class="w-full p-4 flex items-center justify-between group">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-lg bg-orange-500/10 flex items-center justify-center border border-orange-500/20">
                            <i data-lucide="workflow" class="w-4 h-4 text-orange-400"></i>
                        </div>
                        <span class="text-xs font-medium text-gray-300 group-hover:text-white transition-colors">Tecnologías N8N</span>
                    </div>
                    <i data-lucide="chevron-down" class="w-3 h-3 text-gray-600 transition-transform" :class="open ? 'rotate-180' : ''"></i>
                </button>
            </div>

            <!-- BIBLIOTECA PERSONAL (Con Cuadernos) -->
            <div x-data="{ open: true }" class="library-card rounded-2xl overflow-hidden border-purple-500/20 bg-purple-500/[0.02]">
                <button @click="open = !open" class="w-full p-4 flex items-center justify-between group">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-lg bg-purple-500/10 flex items-center justify-center border border-purple-500/20">
                            <i data-lucide="castle" class="w-4 h-4 text-purple-400"></i>
                        </div>
                        <span class="text-xs font-semibold text-white">Personal</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-[9px] px-1.5 py-0.5 rounded-full bg-purple-500/20 text-purple-300 font-bold">2</span>
                        <i data-lucide="chevron-down" class="w-3 h-3 text-purple-400 transition-transform" :class="open ? 'rotate-180' : ''"></i>
                    </div>
                </button>

                <!-- Cuadernos -->
                <div x-show="open" x-collapse class="px-4 pb-4">
                    <div class="ml-8 border-l border-white/5 space-y-1 relative">
                        
                        <!-- Item Cuaderno 1 -->
                        <div class="relative group">
                            <div class="absolute -left-[1px] top-4 w-3 h-[1px] bg-white/10 group-hover:bg-purple-500/50 transition-colors"></div>
                            <button @click="selected = 'claves'" 
                                :class="selected === 'claves' ? 'item-active text-white' : 'text-gray-500 hover:text-gray-300'"
                                class="w-full text-left pl-6 py-2 rounded-lg text-xs transition-all flex items-center justify-between">
                                <span>Claves</span>
                                <i data-lucide="file-text" class="w-3 h-3 opacity-0 group-hover:opacity-40"></i>
                            </button>
                        </div>

                        <!-- Item Cuaderno 2 -->
                        <div class="relative group">
                            <div class="absolute -left-[1px] top-4 w-3 h-[1px] bg-white/10 group-hover:bg-purple-500/50 transition-colors"></div>
                            <button @click="selected = 'vehiculos'" 
                                :class="selected === 'vehiculos' ? 'item-active text-white' : 'text-gray-500 hover:text-gray-300'"
                                class="w-full text-left pl-6 py-2 rounded-lg text-xs transition-all flex items-center justify-between">
                                <span>Vehículos</span>
                                <i data-lucide="file-text" class="w-3 h-3 opacity-0 group-hover:opacity-40"></i>
                            </button>
                        </div>

                        <!-- Botón Añadir -->
                        <div class="relative group">
                            <div class="absolute -left-[1px] top-4 w-3 h-[1px] bg-white/5"></div>
                            <button class="w-full text-left pl-6 py-3 text-[10px] text-purple-400/60 hover:text-purple-400 uppercase tracking-tighter font-bold flex items-center gap-2 transition-all">
                                <i data-lucide="plus-square" class="w-3 h-3"></i>
                                Nuevo Cuaderno
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- BIBLIOTECA TÉCNICA -->
            <div x-data="{ open: false }" class="library-card rounded-2xl overflow-hidden">
                <button @click="open = !open" class="w-full p-4 flex items-center justify-between group">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-lg bg-zinc-500/10 flex items-center justify-center border border-zinc-500/20">
                            <i data-lucide="terminal" class="w-4 h-4 text-zinc-400"></i>
                        </div>
                        <span class="text-xs font-medium text-gray-300 group-hover:text-white transition-colors">Biblioteca Técnica</span>
                    </div>
                    <i data-lucide="chevron-down" class="w-3 h-3 text-gray-600 transition-transform" :class="open ? 'rotate-180' : ''"></i>
                </button>
            </div>

        </div>

        <!-- Footer / Stats -->
        <div class="p-6 bg-black/20 border-t border-white/5">
            <div class="flex items-center gap-4">
                <div class="relative">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-indigo-600 p-[1px]">
                        <div class="w-full h-full rounded-xl bg-[#0f0f12] flex items-center justify-center">
                            <i data-lucide="user" class="w-5 h-5 text-white/80"></i>
                        </div>
                    </div>
                    <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 border-2 border-[#0f0f12] rounded-full"></div>
                </div>
                <div class="flex flex-col">
                    <span class="text-xs font-bold text-white/90 leading-tight">Workspace Pro</span>
                    <span class="text-[10px] text-gray-500">v2.4.0 Active</span>
                </div>
            </div>
        </div>
    </aside>

    <!-- ÁREA DE TRABAJO (Preview) -->
    <main class="flex-1 p-10 bg-[#09090b] flex flex-col items-center justify-center relative overflow-hidden">
        <!-- Decoración de fondo -->
        <div class="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] bg-purple-600/5 blur-[120px] rounded-full"></div>
        <div class="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-blue-600/5 blur-[120px] rounded-full"></div>
        
        <div class="text-center z-10">
            <div class="w-20 h-20 rounded-3xl border border-white/5 bg-white/[0.02] flex items-center justify-center mx-auto mb-6 shadow-2xl">
                <i data-lucide="command" class="w-8 h-8 text-white/10"></i>
            </div>
            <h1 class="text-xl font-light text-white/20">Selecciona un cuaderno para empezar</h1>
        </div>
    </main>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>
```

---

## 📄 Archivo: `.research/contenido2.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rediseño Contenido Compacto</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');
        
        :root {
            --bg-main: #09090b;
            --sidebar-bg: #0f0f12;
            --accent-purple: #8b5cf6;
            --border-color: rgba(255, 255, 255, 0.06);
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-main);
            color: #d1d5db;
        }

        /* Tarjeta más compacta y ajustada */
        .library-card {
            background: linear-gradient(145deg, rgba(255,255,255,0.02) 0%, rgba(255,255,255,0) 100%);
            border: 1px solid var(--border-color);
            transition: all 0.2s ease;
        }

        .library-card:hover {
            border-color: rgba(139, 92, 246, 0.3);
            background: rgba(139, 92, 246, 0.02);
        }

        .item-active {
            background: rgba(139, 92, 246, 0.1);
            color: white;
            box-shadow: inset 3px 0 0 var(--accent-purple);
        }

        .custom-scroll::-webkit-scrollbar { width: 2px; }
        .custom-scroll::-webkit-scrollbar-thumb { background: #27272a; }
    </style>
</head>
<body class="flex h-screen overflow-hidden">

    <!-- PANEL CONTENIDO (Ancho reducido a w-64 para mayor ajuste) -->
    <aside class="w-64 bg-[#0f0f12] border-r border-white/5 flex flex-col h-full">
        
        <!-- Header -->
        <div class="p-5 flex items-center justify-between">
            <div>
                <h2 class="text-[9px] font-bold uppercase tracking-[0.2em] text-gray-500">Biblioteca</h2>
            </div>
            <button class="w-6 h-6 rounded-md border border-white/5 flex items-center justify-center hover:bg-white/5 transition-colors">
                <i data-lucide="plus" class="w-3.5 h-3.5 text-gray-500"></i>
            </button>
        </div>

        <!-- Buscador más discreto -->
        <div class="px-4 mb-4">
            <div class="relative">
                <input type="text" placeholder="Buscar..." 
                    class="w-full bg-white/[0.02] border border-white/5 rounded-lg py-1.5 pl-8 pr-3 text-[11px] focus:outline-none focus:border-purple-500/40 transition-all placeholder:text-gray-600">
                <i data-lucide="search" class="w-3 h-3 absolute left-2.5 top-2.5 text-gray-600"></i>
            </div>
        </div>

        <!-- Lista de Bibliotecas -->
        <div class="flex-1 overflow-y-auto custom-scroll px-3 space-y-2" x-data="{ selected: 'claves' }">
            
            <!-- BIBLIOTECA GENERAL -->
            <div x-data="{ open: false }" class="library-card rounded-xl overflow-hidden">
                <button @click="open = !open" class="w-full p-2.5 flex items-center justify-between group">
                    <div class="flex items-center gap-2.5">
                        <div class="w-6 h-6 rounded bg-blue-500/10 flex items-center justify-center border border-blue-500/10">
                            <i data-lucide="layout-grid" class="w-3.5 h-3.5 text-blue-400/80"></i>
                        </div>
                        <span class="text-[11px] font-medium text-gray-400 group-hover:text-gray-200 transition-colors">General</span>
                    </div>
                    <i data-lucide="chevron-right" class="w-3 h-3 text-gray-700 transition-transform" :class="open ? 'rotate-90' : ''"></i>
                </button>
            </div>

            <!-- BIBLIOTECA N8N -->
            <div x-data="{ open: false }" class="library-card rounded-xl overflow-hidden">
                <button @click="open = !open" class="w-full p-2.5 flex items-center justify-between group">
                    <div class="flex items-center gap-2.5">
                        <div class="w-6 h-6 rounded bg-orange-500/10 flex items-center justify-center border border-orange-500/10">
                            <i data-lucide="workflow" class="w-3.5 h-3.5 text-orange-400/80"></i>
                        </div>
                        <span class="text-[11px] font-medium text-gray-400 group-hover:text-gray-200 transition-colors">Tecnologías N8N</span>
                    </div>
                    <i data-lucide="chevron-right" class="w-3 h-3 text-gray-700 transition-transform" :class="open ? 'rotate-90' : ''"></i>
                </button>
            </div>

            <!-- BIBLIOTECA PERSONAL -->
            <div x-data="{ open: true }" class="library-card rounded-xl overflow-hidden border-purple-500/20 bg-purple-500/[0.01]">
                <button @click="open = !open" class="w-full p-2.5 flex items-center justify-between group">
                    <div class="flex items-center gap-2.5">
                        <div class="w-6 h-6 rounded bg-purple-500/10 flex items-center justify-center border border-purple-500/20">
                            <i data-lucide="castle" class="w-3.5 h-3.5 text-purple-400"></i>
                        </div>
                        <span class="text-[11px] font-semibold text-white/90">Personal</span>
                    </div>
                    <i data-lucide="chevron-right" class="w-3 h-3 text-purple-400/50 transition-transform" :class="open ? 'rotate-90' : ''"></i>
                </button>

                <!-- Cuadernos compactos -->
                <div x-show="open" x-collapse class="pb-2">
                    <div class="ml-7 border-l border-white/5 space-y-0.5 mt-1">
                        <button @click="selected = 'claves'" 
                            :class="selected === 'claves' ? 'item-active' : 'text-gray-500 hover:text-gray-300'"
                            class="w-full text-left pl-4 py-1.5 text-[10.5px] transition-all flex items-center justify-between group">
                            <span>Claves</span>
                            <i data-lucide="more-horizontal" class="w-3 h-3 mr-2 opacity-0 group-hover:opacity-40"></i>
                        </button>
                        <button @click="selected = 'vehiculos'" 
                            :class="selected === 'vehiculos' ? 'item-active' : 'text-gray-500 hover:text-gray-300'"
                            class="w-full text-left pl-4 py-1.5 text-[10.5px] transition-all flex items-center justify-between group">
                            <span>Vehículos</span>
                            <i data-lucide="more-horizontal" class="w-3 h-3 mr-2 opacity-0 group-hover:opacity-40"></i>
                        </button>
                        <button class="w-full text-left pl-4 py-2 text-[9px] text-purple-400/50 hover:text-purple-400 uppercase tracking-tighter font-bold flex items-center gap-1.5 transition-all">
                            <i data-lucide="plus-circle" class="w-3 h-3"></i>
                            Añadir
                        </button>
                    </div>
                </div>
            </div>

            <!-- BIBLIOTECA TÉCNICA -->
            <div x-data="{ open: false }" class="library-card rounded-xl overflow-hidden">
                <button @click="open = !open" class="w-full p-2.5 flex items-center justify-between group">
                    <div class="flex items-center gap-2.5">
                        <div class="w-6 h-6 rounded bg-zinc-500/10 flex items-center justify-center border border-zinc-500/10">
                            <i data-lucide="terminal" class="w-3.5 h-3.5 text-zinc-500"></i>
                        </div>
                        <span class="text-[11px] font-medium text-gray-400 group-hover:text-gray-200 transition-colors">Biblioteca Técnica</span>
                    </div>
                    <i data-lucide="chevron-right" class="w-3 h-3 text-gray-700 transition-transform" :class="open ? 'rotate-90' : ''"></i>
                </button>
            </div>
        </div>

        <!-- Sin footer, espacio limpio al final -->
        <div class="h-6"></div>

    </aside>

    <!-- ÁREA DE TRABAJO (Preview) -->
    <main class="flex-1 bg-[#09090b] flex flex-col items-center justify-center relative overflow-hidden">
        <div class="absolute top-0 right-0 w-full h-full pointer-events-none opacity-20" 
             style="background-image: radial-gradient(#1e1e1e 1px, transparent 1px); background-size: 32px 32px;"></div>
        
        <div class="text-center z-10">
            <h1 class="text-sm font-light text-white/10 tracking-[0.3em] uppercase">Editor de Entorno</h1>
        </div>
    </main>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>
```

---

## 📄 Archivo: `.research/idea1.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Knowledge OS</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Alpine.js -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <!-- Iconos Phosphor -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>

    <style>
        /* Efecto Glassmorphism */
        .glass {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Animación suave */
        .fade-in {
            animation: fadeIn 0.5s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Simulando el editor Tiptap */
        .tiptap-mock {
            outline: none;
            line-height: 1.8;
            font-size: 1.1rem;
        }
        .tiptap-mock p { margin-bottom: 1em; }
    </style>
</head>
<body class="bg-slate-900 text-slate-200 font-sans h-screen overflow-hidden selection:bg-indigo-500 selection:text-white" x-data="appData()">

    <div class="flex h-full">
        
        <!-- 1. BARRA LATERAL (MODOS / LENTES) -->
        <!-- En lugar de carpetas, mostramos "Intenciones" -->
        <aside class="w-20 flex flex-col items-center py-8 border-r border-slate-800 bg-slate-950 z-20">
            <div class="mb-8 text-indigo-500 text-3xl font-bold">
                <i class="ph ph-brain"></i>
            </div>

            <nav class="flex flex-col gap-6 w-full">
                <!-- Botón Dashboard -->
                <button @click="setMode('dashboard')" 
                        :class="mode === 'dashboard' ? 'text-white border-l-2 border-indigo-500 bg-indigo-500/10' : 'text-slate-500 hover:text-indigo-400'"
                        class="h-12 w-full flex items-center justify-center transition-all relative group">
                    <i class="ph ph-squares-four text-2xl"></i>
                    <span class="absolute left-16 bg-slate-800 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap border border-slate-700">Inicio</span>
                </button>

                <!-- Botón Proyectos (Estructurado) -->
                <button @click="setMode('projects')" 
                        :class="mode === 'projects' ? 'text-white border-l-2 border-indigo-500 bg-indigo-500/10' : 'text-slate-500 hover:text-indigo-400'"
                        class="h-12 w-full flex items-center justify-center transition-all relative group">
                    <i class="ph ph-folder-notch-open text-2xl"></i>
                    <span class="absolute left-16 bg-slate-800 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap border border-slate-700">Proyectos Activos</span>
                </button>

                <!-- Botón Escritor (Flow) -->
                <button @click="setMode('writer')" 
                        :class="mode === 'writer' ? 'text-white border-l-2 border-indigo-500 bg-indigo-500/10' : 'text-slate-500 hover:text-indigo-400'"
                        class="h-12 w-full flex items-center justify-center transition-all relative group">
                    <i class="ph ph-pen-nib text-2xl"></i>
                    <span class="absolute left-16 bg-slate-800 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap border border-slate-700">Modo Escritura</span>
                </button>
            </nav>

            <div class="mt-auto flex flex-col gap-4">
                <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-emerald-400 to-blue-500 flex items-center justify-center text-slate-900 font-bold text-xs cursor-pointer shadow-lg shadow-indigo-500/20">YO</div>
            </div>
        </aside>


        <!-- 2. ÁREA PRINCIPAL -->
        <main class="flex-1 flex flex-col relative overflow-hidden">
            
            <!-- Header Flotante / Barra Inteligente -->
            <header class="h-20 flex items-center px-8 border-b border-slate-800/50 justify-between bg-slate-900/50 backdrop-blur-sm z-10">
                <div class="flex flex-col">
                    <h2 class="text-lg font-medium text-white" x-text="pageTitle"></h2>
                    <span class="text-xs text-slate-500" x-text="subTitle"></span>
                </div>

                <!-- OMNIBAR: El corazón de la App -->
                <div class="flex-1 max-w-2xl mx-8 relative">
                    <div class="relative group">
                        <i class="ph ph-sparkle text-indigo-400 absolute left-4 top-3 animate-pulse"></i>
                        <input type="text" 
                               x-model="searchQuery"
                               @keydown.enter="handleSmartInput()"
                               placeholder="Pregunta a tu notas, o escribe 'Nuevo tema sobre Python'..." 
                               class="w-full bg-slate-800/50 border border-slate-700 rounded-full py-2.5 pl-10 pr-4 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all placeholder-slate-500 text-white shadow-lg shadow-black/20">
                        <div class="absolute right-3 top-2.5 text-xs text-slate-500 border border-slate-700 px-1.5 rounded">⌘K</div>
                    </div>
                </div>

                <div class="flex items-center gap-4 text-slate-400">
                    <div class="flex items-center gap-1 text-xs border border-slate-700 px-2 py-1 rounded-full bg-slate-800">
                        <span class="w-2 h-2 bg-emerald-500 rounded-full"></span>
                        <span>LiteLLM: Activo</span>
                    </div>
                </div>
            </main>
            </header>

            <!-- CONTENIDO DINÁMICO (HTMX Swap simulation) -->
            <div class="flex-1 overflow-y-auto p-8 relative">
                
                <!-- VISTA 1: DASHBOARD (El "Radar") -->
                <div x-show="mode === 'dashboard'" class="fade-in space-y-8 max-w-5xl mx-auto">
                    
                    <!-- Saludo IA -->
                    <div class="flex items-start gap-4 p-6 glass rounded-2xl border-l-4 border-indigo-500">
                        <div class="p-2 bg-indigo-500/20 rounded-lg text-indigo-400"><i class="ph ph-robot text-2xl"></i></div>
                        <div>
                            <h3 class="text-xl font-medium text-white mb-1">Buenos días.</h3>
                            <p class="text-slate-400 leading-relaxed">
                                Veo que ayer estuviste trabajando intensamente en <span class="text-indigo-300 cursor-pointer hover:underline">Análisis de Proyectos</span>. 
                                Tienes una nota sobre <b>"Documentación de IA"</b> que dejaste abierta. ¿Quieres continuar ahí o revisamos tus tareas pendientes?
                            </p>
                            <div class="mt-4 flex gap-3">
                                <button @click="setMode('projects')" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm rounded-lg transition-colors shadow-lg shadow-indigo-500/30">Continuar editando</button>
                                <button class="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 text-sm rounded-lg transition-colors">Crear resumen diario</button>
                            </div>
                        </div>
                    </div>

                    <!-- Grid de Sugerencias -->
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        
                        <!-- Card 1: Serendipia -->
                        <div class="glass p-5 rounded-xl hover:bg-slate-800/80 transition-colors cursor-pointer group">
                            <div class="flex justify-between items-start mb-3">
                                <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">Conexión</span>
                                <i class="ph ph-link text-slate-500 group-hover:text-amber-400"></i>
                            </div>
                            <h4 class="text-white font-medium mb-2">Docker & IA</h4>
                            <p class="text-sm text-slate-400">Encontré similitudes entre tu nota de "Despliegue" y "Modelos Locales". ¿Deberían fusionarse?</p>
                        </div>

                        <!-- Card 2: Recordatorio -->
                        <div class="glass p-5 rounded-xl hover:bg-slate-800/80 transition-colors cursor-pointer group">
                            <div class="flex justify-between items-start mb-3">
                                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Mantenimiento</span>
                                <i class="ph ph-recycle text-slate-500 group-hover:text-emerald-400"></i>
                            </div>
                            <h4 class="text-white font-medium mb-2">Limpieza de Tags</h4>
                            <p class="text-sm text-slate-400">Tienes 5 notas sin etiquetar creadas esta semana. La IA puede sugerir etiquetas.</p>
                        </div>

                        <!-- Card 3: Proyecto Activo -->
                        <div @click="setMode('projects')" class="glass p-5 rounded-xl hover:bg-slate-800/80 transition-colors cursor-pointer group border border-indigo-500/30">
                            <div class="flex justify-between items-start mb-3">
                                <span class="text-xs font-bold text-indigo-400 uppercase tracking-wider">En Foco</span>
                                <i class="ph ph-arrow-right text-slate-500 group-hover:text-indigo-400"></i>
                            </div>
                            <h4 class="text-white font-medium mb-2">Biblioteca Proyectos</h4>
                            <p class="text-sm text-slate-400">Actividad reciente: 12 notas nuevas en "Documentación de IA".</p>
                        </div>

                    </div>
                    
                    <!-- Sección Reciente (Masonry simulado) -->
                    <div>
                        <h3 class="text-slate-400 text-sm font-bold uppercase tracking-widest mb-4">Notas Recientes</h3>
                        <div class="columns-2 gap-6 space-y-6">
                            <div class="break-inside-avoid bg-slate-800 p-4 rounded-lg border border-slate-700 hover:border-slate-600 transition-colors">
                                <h4 class="text-white font-bold mb-2">Configuración LiteLLM</h4>
                                <p class="text-slate-400 text-sm">Snippet para configurar el fallback entre OpenAI y Anthropic...</p>
                                <div class="mt-3 flex gap-2">
                                    <span class="text-xs bg-slate-900 px-2 py-1 rounded text-slate-500">#python</span>
                                    <span class="text-xs bg-slate-900 px-2 py-1 rounded text-slate-500">#ai</span>
                                </div>
                            </div>
                            <div class="break-inside-avoid bg-slate-800 p-4 rounded-lg border border-slate-700 hover:border-slate-600 transition-colors">
                                <h4 class="text-white font-bold mb-2">Ideas App Personal</h4>
                                <p class="text-slate-400 text-sm">Lista de features para el dashboard. Importante integrar HTMX...</p>
                            </div>
                             <div class="break-inside-avoid bg-slate-800 p-4 rounded-lg border border-slate-700 hover:border-slate-600 transition-colors">
                                <h4 class="text-white font-bold mb-2">Arquitectura Hexagonal</h4>
                                <p class="text-slate-400 text-sm">Resumen del capítulo 4 del libro de Vernon...</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- VISTA 2: PROYECTOS (La estructura que mencionaste) -->
                <div x-show="mode === 'projects'" class="fade-in h-full flex flex-col">
                    
                    <div class="flex gap-6 h-full">
                        <!-- Sidebar interna del proyecto -->
                        <div class="w-64 hidden md:block">
                            <div class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-4 pl-2">Estructura</div>
                            <ul class="space-y-1">
                                <li class="px-3 py-2 rounded text-slate-400 hover:bg-slate-800 hover:text-white cursor-pointer"><i class="ph ph-folder mr-2"></i>Personal</li>
                                <li class="px-3 py-2 rounded bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 cursor-pointer">
                                    <div class="flex items-center"><i class="ph ph-folder-open mr-2"></i>Proyectos</div>
                                    <ul class="ml-6 mt-2 space-y-1 border-l border-slate-700 pl-2">
                                        <li class="text-white text-sm py-1">Análisis de Proyectos</li>
                                        <li class="text-slate-500 text-sm py-1 hover:text-white cursor-pointer">Gestión Financiera</li>
                                    </ul>
                                </li>
                                <li class="px-3 py-2 rounded text-slate-400 hover:bg-slate-800 hover:text-white cursor-pointer"><i class="ph ph-folder mr-2"></i>Archivo</li>
                            </ul>
                        </div>

                        <!-- Área de Contenido del Proyecto -->
                        <div class="flex-1 bg-slate-800/30 rounded-2xl border border-slate-800 overflow-hidden flex flex-col">
                            <div class="h-14 border-b border-slate-800 flex items-center px-6 justify-between bg-slate-900/50">
                                <div class="flex items-center gap-2 text-sm text-slate-400">
                                    <span>Proyectos</span> <i class="ph ph-caret-right"></i>
                                    <span>Análisis</span> <i class="ph ph-caret-right"></i>
                                    <span class="text-white font-medium">Documentación de IA</span>
                                </div>
                                <button class="text-indigo-400 hover:text-white text-sm flex items-center gap-1">
                                    <i class="ph ph-plus"></i> Nueva Nota
                                </button>
                            </div>

                            <!-- Lista de notas (Table view) -->
                            <div class="flex-1 p-4 overflow-y-auto">
                                <table class="w-full text-left text-sm text-slate-400">
                                    <thead class="text-xs uppercase bg-slate-800/50 text-slate-500">
                                        <tr>
                                            <th class="px-4 py-3 rounded-l-lg">Título</th>
                                            <th class="px-4 py-3">Etiquetas</th>
                                            <th class="px-4 py-3">Actualizado</th>
                                            <th class="px-4 py-3 rounded-r-lg">Estado IA</th>
                                        </tr>
                                    </thead>
                                    <tbody class="divide-y divide-slate-800">
                                        <tr class="hover:bg-slate-800/50 cursor-pointer transition-colors" @click="setMode('writer')">
                                            <td class="px-4 py-4 text-white font-medium flex items-center gap-3">
                                                <i class="ph ph-file-text text-xl text-slate-600"></i>
                                                Setup LiteLLM en Python
                                            </td>
                                            <td class="px-4 py-4"><span class="bg-indigo-500/10 text-indigo-400 px-2 py-1 rounded text-xs border border-indigo-500/20">Dev</span></td>
                                            <td class="px-4 py-4">Hoy, 10:30 AM</td>
                                            <td class="px-4 py-4"><i class="ph ph-check-circle text-emerald-500 text-lg" title="Analizado"></i></td>
                                        </tr>
                                        <tr class="hover:bg-slate-800/50 cursor-pointer transition-colors">
                                            <td class="px-4 py-4 text-white font-medium flex items-center gap-3">
                                                <i class="ph ph-file-text text-xl text-slate-600"></i>
                                                Modelos de Embedding (Supabase)
                                            </td>
                                            <td class="px-4 py-4"><span class="bg-slate-700 text-slate-300 px-2 py-1 rounded text-xs">Database</span></td>
                                            <td class="px-4 py-4">Ayer</td>
                                            <td class="px-4 py-4"><i class="ph ph-warning-circle text-amber-500 text-lg" title="Sugerencia pendiente"></i></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- VISTA 3: MODO ESCRITOR (Writer/Tiptap) -->
                <div x-show="mode === 'writer'" class="fade-in h-full max-w-4xl mx-auto flex gap-8">
                    
                    <!-- Editor Principal -->
                    <div class="flex-1 flex flex-col h-full">
                         <!-- Toolbar Tiptap Fake -->
                         <div class="flex items-center gap-2 mb-4 p-2 bg-slate-800 rounded-lg border border-slate-700 w-max sticky top-0 z-10">
                            <button class="p-1.5 hover:bg-slate-700 rounded text-slate-300"><i class="ph ph-text-b"></i></button>
                            <button class="p-1.5 hover:bg-slate-700 rounded text-slate-300"><i class="ph ph-text-italic"></i></button>
                            <div class="w-px h-4 bg-slate-600 mx-1"></div>
                            <button class="p-1.5 hover:bg-slate-700 rounded text-slate-300"><i class="ph ph-list-bullets"></i></button>
                            <div class="w-px h-4 bg-slate-600 mx-1"></div>
                            <button class="p-1.5 hover:bg-indigo-600 bg-indigo-500/20 text-indigo-400 rounded flex items-center gap-1 text-xs font-bold px-2">
                                <i class="ph ph-sparkle"></i> IA
                            </button>
                         </div>

                         <!-- Contenido Editable -->
                         <div class="flex-1 outline-none tiptap-mock text-slate-300 overflow-y-auto pr-4" contenteditable="true">
                            <h1 class="text-3xl font-bold text-white mb-6">Setup LiteLLM en Python</h1>
                            <p>LiteLLM funciona como un proxy gateway unificado para llamar a más de 100 modelos (OpenAI, Anthropic, Azure, etc.).</p>
                            <p>La característica principal es el <b>Fallback</b>. Si un modelo falla, usa otro automáticamente.</p>
                            <pre class="bg-slate-950 p-4 rounded-lg border border-slate-800 font-mono text-sm text-emerald-400 my-4">
from litellm import completion
# Código de ejemplo aquí...
                            </pre>
                            <p>Tengo que investigar cómo integrar esto con el sistema de control de gastos para limitar el presupuesto por usuario.</p>
                            <p class="text-slate-500 italic">Escribe "/" para comandos o "shift+/" para asistencia IA...</p>
                         </div>
                    </div>

                    <!-- Panel Lateral Derecho (La Guía IA) -->
                    <div class="w-72 hidden xl:block pt-16">
                        <div class="glass rounded-xl p-4 border-l-2 border-indigo-500">
                            <div class="flex items-center gap-2 text-indigo-400 mb-3 text-sm font-bold uppercase">
                                <i class="ph ph-magic-wand"></i> Asistente Activo
                            </div>
                            <div class="space-y-4">
                                <div class="bg-slate-800/50 p-3 rounded text-sm text-slate-300">
                                    <p class="mb-2">He detectado que hablas de <b>Control de Gastos</b>.</p>
                                    <p class="text-xs text-slate-500">En tu nota "SaaS Pricing" mencionaste límites de tokens. ¿Quieres relacionarlas?</p>
                                    <button class="mt-2 w-full py-1 bg-indigo-600/20 text-indigo-400 text-xs rounded border border-indigo-500/30 hover:bg-indigo-600/40">Relacionar Notas</button>
                                </div>
                                <div class="bg-slate-800/50 p-3 rounded text-sm text-slate-300">
                                    <p class="mb-2">¿Necesitas un ejemplo de código para los <b>Budgets</b> en LiteLLM?</p>
                                    <button class="mt-2 w-full py-1 bg-slate-700 text-slate-300 text-xs rounded hover:bg-slate-600">Generar Código</button>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>

            </div>
        
    </div>

    <!-- Lógica Alpine.js -->
    <script>
        function appData() {
            return {
                mode: 'dashboard', // dashboard, projects, writer
                searchQuery: '',
                
                get pageTitle() {
                    const titles = {
                        'dashboard': 'Centro de Mando',
                        'projects': 'Biblioteca de Proyectos',
                        'writer': 'Editor'
                    };
                    return titles[this.mode];
                },

                get subTitle() {
                    const subs = {
                        'dashboard': 'Resumen del día y sugerencias IA',
                        'projects': 'Explorando / Análisis / Documentación IA',
                        'writer': 'Guardado hace unos instantes...'
                    };
                    return subs[this.mode];
                },

                setMode(newMode) {
                    this.mode = newMode;
                },

                handleSmartInput() {
                    // Simulación simple de routing IA
                    const q = this.searchQuery.toLowerCase();
                    
                    if (q.includes('proyecto') || q.includes('ia') || q.includes('doc')) {
                        this.setMode('projects');
                    } else if (q.includes('escribir') || q.includes('nota') || q.includes('litellm')) {
                        this.setMode('writer');
                    } else {
                        // Default
                        alert("IA: He creado una nueva nota rápida en tu Inbox con: " + this.searchQuery);
                    }
                    this.searchQuery = '';
                }
            }
        }
    </script>
</body>
</html>
```

---

## 📄 Archivo: `.research/idea2.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Docs V2 - Centered Focus</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <style>
        /* Tipografía optimizada para lectura */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&display=swap');
        
        body { font-family: 'Inter', sans-serif; }
        .serif-text { font-family: 'Merriweather', serif; }

        .glass {
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(12px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* El "Papel" del editor */
        .editor-paper {
            max-width: 65ch; /* Ancho ideal de lectura (65 caracteres) */
            margin: 0 auto;
        }

        /* Scrollbar invisible pero funcional */
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    </style>
</head>
<body class="bg-[#0f1117] text-slate-300 h-screen overflow-hidden flex" x-data="appData()">

    <!-- 1. BARRA DE NAVEGACIÓN (Extrema Izquierda - Iconos) -->
    <nav class="w-16 bg-[#0B0C10] border-r border-white/5 flex flex-col items-center py-6 z-50 shrink-0">
        <div class="mb-8 text-indigo-500 text-3xl hover:rotate-12 transition-transform cursor-pointer"><i class="ph-fill ph-brain"></i></div>
        
        <div class="flex flex-col gap-4 w-full px-2">
            <template x-for="item in navItems">
                <button @click="setMode(item.id)" 
                        :class="mode === item.id ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25' : 'text-slate-500 hover:text-indigo-400 hover:bg-white/5'"
                        class="w-10 h-10 rounded-xl flex items-center justify-center transition-all group relative">
                    <i :class="item.icon" class="text-xl"></i>
                    <!-- Tooltip -->
                    <span class="absolute left-14 bg-slate-800 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity border border-white/10 whitespace-nowrap z-50 pointer-events-none" x-text="item.label"></span>
                </button>
            </template>
        </div>
        
        <div class="mt-auto mb-4">
            <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-purple-400 to-indigo-500 border-2 border-[#0B0C10] ring-2 ring-indigo-500/30"></div>
        </div>
    </nav>


    <!-- 2. PANEL IZQUIERDO (Contexto / Estructura / Navegación Secundaria) -->
    <!-- Este panel CAMBIA según el modo para dar uso a la izquierda -->
    <aside class="w-64 bg-[#13151b] border-r border-white/5 flex flex-col transition-all duration-300 shrink-0" 
           :class="zenMode ? '-ml-64 opacity-50' : ''">
        
        <!-- Header del Panel -->
        <div class="h-14 flex items-center px-5 border-b border-white/5">
            <span class="text-xs font-bold tracking-widest text-slate-500 uppercase" x-text="leftPanelTitle"></span>
        </div>

        <!-- Contenido Variable Izquierda -->
        <div class="flex-1 overflow-y-auto no-scrollbar p-2">
            
            <!-- A) Si estamos en DASHBOARD: Agenda / Timeline -->
            <div x-show="mode === 'dashboard'" class="space-y-6 p-2">
                <div>
                    <h4 class="text-white text-sm font-medium mb-3 flex items-center gap-2"><i class="ph-fill ph-calendar-check text-indigo-400"></i> Para hoy</h4>
                    <div class="space-y-2">
                        <div class="p-3 rounded-lg bg-white/5 border border-white/5 hover:border-indigo-500/30 transition-colors cursor-pointer group">
                            <div class="text-xs text-indigo-300 mb-1">10:00 AM</div>
                            <div class="text-sm text-slate-200 group-hover:text-white">Revisar Doc API</div>
                        </div>
                        <div class="p-3 rounded-lg bg-white/5 border border-white/5 hover:border-indigo-500/30 transition-colors cursor-pointer group">
                            <div class="text-xs text-orange-300 mb-1">Sin fecha</div>
                            <div class="text-sm text-slate-200 group-hover:text-white">Investigar Tiptap</div>
                        </div>
                    </div>
                </div>
                
                <div>
                    <h4 class="text-white text-sm font-medium mb-3 flex items-center gap-2"><i class="ph-fill ph-clock-counter-clockwise text-slate-400"></i> Historial</h4>
                    <ul class="space-y-1 text-sm text-slate-400">
                        <li class="px-2 py-1.5 hover:bg-white/5 rounded cursor-pointer truncate">Setup LiteLLM</li>
                        <li class="px-2 py-1.5 hover:bg-white/5 rounded cursor-pointer truncate">Notas de Supabase</li>
                        <li class="px-2 py-1.5 hover:bg-white/5 rounded cursor-pointer truncate">Ideas Dashboard</li>
                    </ul>
                </div>
            </div>

            <!-- B) Si estamos en PROJECTS: Árbol de Carpetas -->
            <div x-show="mode === 'projects'" class="text-sm font-medium text-slate-400 select-none">
                <div class="pl-2 py-2 hover:text-white cursor-pointer flex items-center gap-2"><i class="ph-fill ph-books text-slate-500"></i> Biblioteca</div>
                
                <!-- Carpeta Expandida -->
                <div class="mt-1">
                    <div class="pl-2 py-1.5 bg-indigo-500/10 text-indigo-300 rounded-md flex items-center gap-2 cursor-pointer border border-indigo-500/20">
                        <i class="ph-fill ph-folder-open"></i> Proyectos
                    </div>
                    <div class="pl-6 border-l border-white/10 ml-3.5 mt-1 space-y-1">
                        <div class="py-1.5 pl-2 text-white cursor-pointer hover:bg-white/5 rounded">Análisis Proyectos</div>
                        <div class="py-1.5 pl-2 hover:text-white cursor-pointer hover:bg-white/5 rounded">Finanzas</div>
                    </div>
                </div>

                <div class="pl-2 py-2 mt-1 hover:text-white cursor-pointer flex items-center gap-2"><i class="ph-fill ph-notebook text-slate-500"></i> Diario</div>
            </div>

            <!-- C) Si estamos en WRITER: Tabla de Contenido (Outline) -->
            <div x-show="mode === 'writer'" class="p-2">
                <div class="text-xs font-bold text-slate-500 mb-2 uppercase">En esta nota</div>
                <nav class="space-y-1 text-sm border-l border-slate-700 ml-1 pl-3">
                    <a href="#" class="block text-indigo-400 border-l-2 border-indigo-500 -ml-[14px] pl-3 py-1">Introducción</a>
                    <a href="#" class="block text-slate-400 hover:text-white py-1">¿Qué es LiteLLM?</a>
                    <a href="#" class="block text-slate-400 hover:text-white py-1">Configuración</a>
                    <a href="#" class="block text-slate-400 hover:text-white py-1 pl-2 text-xs">Instalación</a>
                    <a href="#" class="block text-slate-400 hover:text-white py-1 pl-2 text-xs">Variables de Entorno</a>
                    <a href="#" class="block text-slate-400 hover:text-white py-1">Conclusión</a>
                </nav>

                <div class="mt-8 pt-6 border-t border-white/5">
                    <div class="text-xs font-bold text-slate-500 mb-2 uppercase">Referencias</div>
                    <div class="flex flex-col gap-2">
                         <div class="flex items-center gap-2 p-2 rounded bg-slate-800/50 text-xs text-slate-300 cursor-pointer border border-transparent hover:border-indigo-500/50">
                            <i class="ph ph-link text-indigo-400"></i>
                            SaaS Pricing Models
                         </div>
                         <div class="flex items-center gap-2 p-2 rounded bg-slate-800/50 text-xs text-slate-300 cursor-pointer border border-transparent hover:border-indigo-500/50">
                            <i class="ph ph-link text-indigo-400"></i>
                            OpenAI API Docs
                         </div>
                    </div>
                </div>
            </div>

        </div>
    </aside>


    <!-- 3. ÁREA CENTRAL (El Canvas / Stage) -->
    <main class="flex-1 flex flex-col relative bg-[#0f1117] transition-all">
        
        <!-- Topbar Minimalista -->
        <header class="h-14 flex items-center justify-between px-8 border-b border-white/5 shrink-0">
            <!-- Breadcrumbs -->
            <div class="flex items-center gap-2 text-sm text-slate-500">
                <span x-text="mode === 'writer' ? 'Proyectos' : 'Inicio'"></span>
                <i class="ph-bold ph-caret-right text-xs"></i>
                <span class="text-white" x-text="pageTitle"></span>
            </div>

            <!-- Zen Mode Toggle -->
            <button @click="zenMode = !zenMode" class="text-slate-500 hover:text-white transition-colors" title="Modo Zen">
                <i :class="zenMode ? 'ph-fill ph-arrows-in-line-horizontal' : 'ph-fill ph-arrows-out-line-horizontal'"></i>
            </button>
        </header>

        <!-- CONTENIDO SCROLLEABLE -->
        <div class="flex-1 overflow-y-auto relative no-scrollbar">
            
            <!-- VISTA: DASHBOARD CENTRADO -->
            <div x-show="mode === 'dashboard'" class="max-w-4xl mx-auto py-12 px-8 fade-in">
                <h1 class="text-3xl font-light text-white mb-2">Buenos días, <span class="text-indigo-400 font-bold">Arquitecto.</span></h1>
                <p class="text-slate-400 text-lg mb-8">¿En qué conocimiento quieres profundizar hoy?</p>

                <!-- Omnibar Central -->
                <div class="relative group mb-12">
                    <div class="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
                    <div class="relative flex items-center bg-[#1a1d26] rounded-lg p-1 border border-white/10">
                        <i class="ph ph-sparkle text-indigo-400 text-xl ml-4"></i>
                        <input type="text" placeholder="Escribe 'Nueva nota sobre FastAPI' o pregunta a tus docs..." 
                               class="w-full bg-transparent border-none text-white text-lg px-4 py-3 focus:ring-0 placeholder-slate-600 font-light"
                               @keydown.enter="setMode('writer')">
                        <div class="pr-4 flex gap-2">
                             <span class="text-xs bg-[#252836] text-slate-400 px-2 py-1 rounded border border-white/5">⌘K</span>
                        </div>
                    </div>
                </div>

                <!-- Tarjetas de Inicio -->
                <div class="grid grid-cols-2 gap-6">
                    <div @click="setMode('projects')" class="p-6 rounded-2xl bg-[#15171e] border border-white/5 hover:border-indigo-500/50 cursor-pointer transition-all group hover:-translate-y-1">
                        <div class="flex items-center justify-between mb-4">
                            <div class="w-10 h-10 rounded-full bg-indigo-500/10 flex items-center justify-center text-indigo-400"><i class="ph-fill ph-folder-open text-xl"></i></div>
                            <span class="text-xs bg-indigo-500/20 text-indigo-300 px-2 py-1 rounded-full">Activo</span>
                        </div>
                        <h3 class="text-xl text-white font-medium mb-1 group-hover:text-indigo-400 transition-colors">Análisis de Proyectos</h3>
                        <p class="text-sm text-slate-400">12 notas modificadas esta semana. Última edición hace 2h.</p>
                    </div>

                    <div class="p-6 rounded-2xl bg-[#15171e] border border-white/5 hover:border-emerald-500/50 cursor-pointer transition-all group hover:-translate-y-1">
                         <div class="flex items-center justify-between mb-4">
                            <div class="w-10 h-10 rounded-full bg-emerald-500/10 flex items-center justify-center text-emerald-400"><i class="ph-fill ph-magic-wand text-xl"></i></div>
                            <span class="text-xs bg-emerald-500/20 text-emerald-300 px-2 py-1 rounded-full">Sugerencia</span>
                        </div>
                        <h3 class="text-xl text-white font-medium mb-1 group-hover:text-emerald-400 transition-colors">Repaso: Docker</h3>
                        <p class="text-sm text-slate-400">La IA sugiere fusionar tus notas de "Docker" con "Despliegue".</p>
                    </div>
                </div>
            </div>

            <!-- VISTA: WRITER (EL FOCO PRINCIPAL) -->
            <!-- Aquí aplicamos la teoría de "Centrado" -->
            <div x-show="mode === 'writer'" class="h-full flex flex-col fade-in">
                
                <div class="flex-1 py-12 px-8 editor-paper">
                    <!-- Área de Título -->
                    <input type="text" value="Setup LiteLLM en Python" 
                           class="w-full bg-transparent text-4xl font-bold text-white mb-8 border-none focus:ring-0 placeholder-slate-600 outline-none leading-tight"
                           placeholder="Título de la nota...">

                    <!-- Área de Texto (Simulación Tiptap) -->
                    <div class="serif-text text-lg leading-relaxed text-[#d1d5db] space-y-6 outline-none" contenteditable="true">
                        <p>LiteLLM funciona como un proxy gateway unificado para llamar a más de 100 modelos (OpenAI, Anthropic, Azure, etc.). Es la pieza fundamental para desacoplar nuestra lógica de negocio del proveedor de IA.</p>
                        
                        <h3 class="text-xl font-bold text-white mt-8 mb-4 font-sans">Configuración Básica</h3>
                        <p>Para iniciarlo, necesitamos instalar la librería con soporte para el servidor proxy.</p>
                        
                        <div class="bg-[#1a1d26] p-4 rounded-lg border border-white/10 font-mono text-sm text-emerald-400 my-6 relative group">
                            <button class="absolute top-2 right-2 text-slate-500 hover:text-white opacity-0 group-hover:opacity-100"><i class="ph ph-copy"></i></button>
                            pip install 'litellm[proxy]'<br>
                            litellm --model gpt-3.5-turbo
                        </div>

                        <p>La característica principal que buscamos es el <span class="bg-indigo-500/20 text-indigo-300 px-1 rounded cursor-pointer border-b border-indigo-500/40">Fallback</span>. Si un modelo falla por rate-limit, el sistema debe saltar al siguiente automáticamente sin lanzar excepción a la aplicación cliente.</p>

                        <p class="text-slate-500 italic mt-8">Presiona ' / ' para comandos IA...</p>
                    </div>
                    
                    <!-- Espacio al final para scroll cómodo -->
                    <div class="h-32"></div>
                </div>

                <!-- Barra de herramientas flotante (Estilo Medium/Notion) -->
                <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 bg-[#1e222e] border border-white/10 rounded-full px-4 py-2 flex items-center gap-4 shadow-2xl shadow-black/50 z-40 transition-all duration-300"
                     :class="zenMode ? 'opacity-0 hover:opacity-100 translate-y-10 hover:translate-y-0' : ''">
                    <span class="text-xs text-slate-500 mr-2 border-r border-white/10 pr-4">420 palabras</span>
                    <button class="text-slate-400 hover:text-white"><i class="ph-bold ph-text-b"></i></button>
                    <button class="text-slate-400 hover:text-white"><i class="ph-bold ph-text-italic"></i></button>
                    <button class="text-slate-400 hover:text-white"><i class="ph-bold ph-link"></i></button>
                    <div class="w-px h-4 bg-white/10"></div>
                    <button class="text-indigo-400 hover:text-indigo-300 flex items-center gap-1 text-sm font-medium"><i class="ph-fill ph-sparkle"></i> Pedir a IA</button>
                </div>

            </div>

        </div>
    </main>


    <!-- 4. PANEL DERECHO (Asistente IA / Herramientas) -->
    <!-- Colapsable para Modo Zen -->
    <aside class="w-80 bg-[#13151b] border-l border-white/5 flex flex-col transition-all duration-300 shrink-0 relative z-20"
           :class="zenMode ? '-mr-80 opacity-0' : ''">
        
        <div class="h-14 flex items-center px-6 border-b border-white/5 justify-between bg-[#13151b]">
            <span class="text-xs font-bold text-indigo-400 uppercase flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Copiloto Activo
            </span>
            <button class="text-slate-500 hover:text-white"><i class="ph ph-dots-three"></i></button>
        </div>

        <div class="flex-1 overflow-y-auto p-4 space-y-4">
            
            <!-- Chat Bubble IA -->
            <div class="bg-[#1e222e] rounded-xl p-4 border border-indigo-500/20 shadow-lg shadow-indigo-900/5 relative">
                <div class="absolute -left-2 top-4 w-2 h-2 bg-[#1e222e] border-l border-b border-indigo-500/20 transform rotate-45"></div>
                <p class="text-sm text-slate-200 leading-relaxed">
                    Estás escribiendo sobre <b>LiteLLM</b>. 
                </p>
                <p class="text-sm text-slate-400 mt-2">
                    En tu nota de "SaaS Pricing" (hace 3 días) mencionaste la necesidad de limitar costos.
                </p>
                <p class="text-sm text-slate-200 mt-2 font-medium">
                    ¿Quieres que inserte el snippet de configuración de `BudgetManager`?
                </p>
                
                <div class="mt-3 flex gap-2">
                    <button class="flex-1 bg-indigo-600 hover:bg-indigo-500 text-white text-xs py-1.5 rounded transition-colors">Insertar Código</button>
                    <button class="px-3 bg-white/5 hover:bg-white/10 text-slate-300 text-xs py-1.5 rounded transition-colors">No</button>
                </div>
            </div>

            <!-- Contexto Relacionado -->
            <div class="pt-4 border-t border-white/5">
                <h5 class="text-xs font-bold text-slate-500 uppercase mb-3">Conceptos Relacionados</h5>
                <div class="flex flex-wrap gap-2">
                    <span class="px-2 py-1 bg-slate-800 rounded border border-slate-700 text-xs text-slate-300 hover:border-indigo-500 cursor-pointer">API Gateway</span>
                    <span class="px-2 py-1 bg-slate-800 rounded border border-slate-700 text-xs text-slate-300 hover:border-indigo-500 cursor-pointer">Python Async</span>
                    <span class="px-2 py-1 bg-slate-800 rounded border border-slate-700 text-xs text-slate-300 hover:border-indigo-500 cursor-pointer">OpenAI Keys</span>
                </div>
            </div>

        </div>

        <!-- Input Chat Rápido -->
        <div class="p-4 border-t border-white/5 bg-[#13151b]">
            <div class="relative">
                <input type="text" placeholder="Pregunta algo..." class="w-full bg-[#0f1117] border border-white/10 rounded-lg py-2 pl-3 pr-8 text-sm text-slate-300 focus:outline-none focus:border-indigo-500 transition-colors">
                <button class="absolute right-2 top-2 text-indigo-500 hover:text-white"><i class="ph-fill ph-paper-plane-right"></i></button>
            </div>
        </div>
    </aside>

    <script>
        function appData() {
            return {
                mode: 'dashboard', 
                zenMode: false,
                navItems: [
                    { id: 'dashboard', icon: 'ph-fill ph-squares-four', label: 'Inicio' },
                    { id: 'projects', icon: 'ph-fill ph-folder-notch', label: 'Proyectos' },
                    { id: 'writer', icon: 'ph-fill ph-pen-nib', label: 'Editor' },
                    { id: 'search', icon: 'ph-bold ph-magnifying-glass', label: 'Buscar' },
                ],
                get pageTitle() {
                    const t = { 'dashboard': 'Centro de Mando', 'projects': 'Explorador', 'writer': 'Setup LiteLLM en Python' };
                    return t[this.mode];
                },
                get leftPanelTitle() {
                    const t = { 'dashboard': 'Agenda Personal', 'projects': 'Estructura', 'writer': 'Tabla de Contenido' };
                    return t[this.mode];
                },
                setMode(m) {
                    this.mode = m;
                    // Auto entrar/salir de Zen Mode según conveniencia (opcional)
                    if(m === 'writer') this.zenMode = false; 
                }
            }
        }
    </script>
</body>
</html>
```

---

## 📄 Archivo: `.research/idea3.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Docs V3 - Inbox Workflow</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&display=swap');
        
        body { font-family: 'Inter', sans-serif; }
        .serif-text { font-family: 'Merriweather', serif; }

        .glass { background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(12px); border-right: 1px solid rgba(255, 255, 255, 0.05); }
        .editor-paper { max-width: 65ch; margin: 0 auto; }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

        /* Animación para el badge de Inbox */
        .pulse-amber { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.7); animation: pulse-amber 2s infinite; }
        @keyframes pulse-amber {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(245, 158, 11, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
        }
    </style>
</head>
<body class="bg-[#0f1117] text-slate-300 h-screen overflow-hidden flex" x-data="appData()">

    <!-- 1. BARRA DE NAVEGACIÓN (Extrema Izquierda) -->
    <nav class="w-16 bg-[#0B0C10] border-r border-white/5 flex flex-col items-center py-6 z-50 shrink-0">
        <div class="mb-8 text-indigo-500 text-3xl hover:rotate-12 transition-transform cursor-pointer"><i class="ph-fill ph-brain"></i></div>
        
        <div class="flex flex-col gap-4 w-full px-2">
            <!-- Botón Dashboard -->
            <button @click="setMode('dashboard')" :class="mode === 'dashboard' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25' : 'text-slate-500 hover:text-indigo-400 hover:bg-white/5'" class="w-10 h-10 rounded-xl flex items-center justify-center transition-all group relative">
                <i class="ph-fill ph-squares-four text-xl"></i>
                <span class="absolute left-14 bg-slate-800 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity border border-white/10 whitespace-nowrap z-50 pointer-events-none">Inicio</span>
            </button>

            <!-- Botón INBOX (Nuevo) -->
            <button @click="setMode('inbox')" :class="mode === 'inbox' ? 'bg-amber-600 text-white shadow-lg shadow-amber-500/25' : 'text-slate-500 hover:text-amber-400 hover:bg-white/5'" class="w-10 h-10 rounded-xl flex items-center justify-center transition-all group relative">
                <i class="ph-fill ph-tray text-xl"></i>
                <!-- Contador de Inbox -->
                <span class="absolute -top-1 -right-1 bg-amber-500 text-white text-[9px] font-bold px-1 rounded-full border border-[#0B0C10]">3</span>
                <span class="absolute left-14 bg-slate-800 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity border border-white/10 whitespace-nowrap z-50 pointer-events-none">Bandeja de Entrada</span>
            </button>

            <!-- Botón Proyectos -->
            <button @click="setMode('projects')" :class="mode === 'projects' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25' : 'text-slate-500 hover:text-indigo-400 hover:bg-white/5'" class="w-10 h-10 rounded-xl flex items-center justify-center transition-all group relative">
                <i class="ph-fill ph-folder-notch text-xl"></i>
                <span class="absolute left-14 bg-slate-800 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity border border-white/10 whitespace-nowrap z-50 pointer-events-none">Proyectos</span>
            </button>
        </div>
        
        <div class="mt-auto mb-4">
            <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-purple-400 to-indigo-500 border-2 border-[#0B0C10] ring-2 ring-indigo-500/30"></div>
        </div>
    </nav>


    <!-- 2. PANEL IZQUIERDO (Dinámico) -->
    <aside class="w-64 bg-[#13151b] border-r border-white/5 flex flex-col transition-all duration-300 shrink-0" :class="zenMode ? '-ml-64 opacity-50' : ''">
        
        <div class="h-14 flex items-center px-5 border-b border-white/5 justify-between">
            <span class="text-xs font-bold tracking-widest text-slate-500 uppercase" x-text="leftPanelTitle"></span>
            <!-- Botón de limpiar inbox si estamos en modo inbox -->
            <button x-show="mode === 'inbox'" class="text-xs text-amber-500 hover:text-amber-300">Procesar Todo</button>
        </div>

        <div class="flex-1 overflow-y-auto no-scrollbar p-2">
            
            <!-- PANEL: DASHBOARD -->
            <div x-show="mode === 'dashboard'" class="space-y-6 p-2">
                <div class="p-4 bg-gradient-to-br from-amber-500/10 to-orange-500/5 rounded-lg border border-amber-500/20">
                    <h4 class="text-amber-400 text-xs font-bold uppercase mb-2 flex items-center gap-2">
                        <i class="ph-fill ph-tray"></i> Inbox (3)
                    </h4>
                    <p class="text-xs text-slate-400 mb-3">Tienes notas rápidas sin procesar.</p>
                    <button @click="setMode('inbox')" class="w-full py-1.5 bg-amber-500/20 text-amber-300 text-xs rounded hover:bg-amber-500/30 border border-amber-500/30">Revisar</button>
                </div>
                <!-- Agenda... -->
                <div>
                    <h4 class="text-white text-sm font-medium mb-3">Para hoy</h4>
                    <div class="space-y-2">
                        <div class="p-3 rounded-lg bg-white/5 border border-white/5 cursor-pointer"><div class="text-sm text-slate-200">Revisar Doc API</div></div>
                    </div>
                </div>
            </div>

            <!-- PANEL: INBOX LIST (NUEVO) -->
            <div x-show="mode === 'inbox'" class="space-y-2 p-1">
                <div class="text-xs text-slate-500 px-2 py-2">Hoy</div>
                <!-- Nota activa -->
                <div @click="openInboxItem(1)" class="p-3 rounded-lg bg-amber-500/10 border border-amber-500/40 cursor-pointer group">
                    <div class="flex justify-between items-start">
                        <h4 class="text-sm text-white font-medium truncate w-32" x-text="currentNote.title || 'Nota sin título'"></h4>
                        <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                    </div>
                    <p class="text-xs text-slate-400 mt-1 line-clamp-2" x-text="currentNote.body || 'Texto...'"></p>
                </div>
                
                <div class="text-xs text-slate-500 px-2 py-2 mt-4">Ayer</div>
                <div class="p-3 rounded-lg bg-white/5 border border-white/5 hover:bg-white/10 cursor-pointer opacity-70">
                    <h4 class="text-sm text-slate-300 font-medium">Link interesante Tiptap</h4>
                    <p class="text-xs text-slate-500 mt-1">Guardar para revisar luego...</p>
                </div>
                <div class="p-3 rounded-lg bg-white/5 border border-white/5 hover:bg-white/10 cursor-pointer opacity-70">
                    <h4 class="text-sm text-slate-300 font-medium">Idea App V2</h4>
                    <p class="text-xs text-slate-500 mt-1">Usar sidebar colapsable...</p>
                </div>
            </div>

            <!-- PANEL: WRITER (Contexto) -->
            <div x-show="mode === 'writer'" class="p-2">
                <div class="text-xs font-bold text-slate-500 mb-2 uppercase">Outline</div>
                <nav class="space-y-1 text-sm border-l border-slate-700 ml-1 pl-3">
                    <span class="text-slate-400">Sin encabezados</span>
                </nav>
            </div>
            
             <!-- PANEL: PROJECTS (Arbol) -->
             <div x-show="mode === 'projects'" class="p-2 text-sm text-slate-400">
                <div class="pl-2 py-2 hover:text-white cursor-pointer"><i class="ph-fill ph-folder-open mr-2"></i> Proyectos</div>
             </div>

        </div>
    </aside>


    <!-- 3. ÁREA CENTRAL -->
    <main class="flex-1 flex flex-col relative bg-[#0f1117] transition-all">
        
        <!-- Header -->
        <header class="h-14 flex items-center justify-between px-8 border-b border-white/5 shrink-0">
            <div class="flex items-center gap-2 text-sm text-slate-500">
                <span x-text="modeDisplay"></span>
                <i class="ph-bold ph-caret-right text-xs"></i>
                <!-- Título editable en el header si es Inbox -->
                <span class="text-white truncate max-w-xs" x-text="currentNote.title"></span>
                
                <!-- Badge de Inbox -->
                <span x-show="isInboxNote" class="ml-2 px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 text-xs border border-amber-500/30 flex items-center gap-1">
                    <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span> Inbox
                </span>
            </div>
            
            <div class="flex items-center gap-3">
                <button x-show="isInboxNote" class="text-xs bg-indigo-600 hover:bg-indigo-500 text-white px-3 py-1.5 rounded transition-colors flex items-center gap-1">
                    <i class="ph-bold ph-folder-notch-plus"></i> Clasificar
                </button>
                <button @click="zenMode = !zenMode" class="text-slate-500 hover:text-white transition-colors">
                    <i :class="zenMode ? 'ph-fill ph-arrows-in-line-horizontal' : 'ph-fill ph-arrows-out-line-horizontal'"></i>
                </button>
            </div>
        </header>

        <div class="flex-1 overflow-y-auto relative no-scrollbar">
            
            <!-- VISTA: DASHBOARD -->
            <div x-show="mode === 'dashboard'" class="max-w-4xl mx-auto py-16 px-8 fade-in">
                <h1 class="text-3xl font-light text-white mb-8 text-center">¿Qué quieres capturar?</h1>

                <!-- OMNIBAR DE CAPTURA RÁPIDA -->
                <div class="relative group max-w-2xl mx-auto">
                    <div class="absolute -inset-1 bg-gradient-to-r from-amber-500 via-orange-500 to-indigo-500 rounded-xl blur opacity-30 group-hover:opacity-60 transition duration-500"></div>
                    <div class="relative bg-[#1a1d26] rounded-xl border border-white/10 shadow-2xl">
                        <!-- Textarea que crece -->
                        <textarea 
                            x-model="quickInput"
                            @keydown.enter.prevent="handleQuickCapture($event)"
                            placeholder="Escribe una idea rápida, pega un texto o busca..." 
                            class="w-full bg-transparent border-none text-white text-lg px-6 py-4 focus:ring-0 placeholder-slate-500 font-light resize-none h-20"
                        ></textarea>
                        
                        <div class="px-4 py-2 flex justify-between items-center border-t border-white/5 bg-[#15171e] rounded-b-xl">
                            <div class="flex gap-2 text-xs text-slate-500">
                                <span class="bg-[#252836] px-2 py-1 rounded">Enter para capturar</span>
                                <span class="bg-[#252836] px-2 py-1 rounded">/ para comandos</span>
                            </div>
                            <button @click="handleQuickCapture()" class="text-indigo-400 hover:text-white transition-colors">
                                <i class="ph-fill ph-arrow-right text-xl"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Resumen rápido -->
                <div class="mt-16 grid grid-cols-3 gap-6 max-w-4xl mx-auto">
                    <div class="text-center p-4 rounded-lg hover:bg-white/5 cursor-pointer transition-colors">
                        <div class="text-2xl font-bold text-white mb-1">3</div>
                        <div class="text-xs text-slate-500 uppercase tracking-widest">En Inbox</div>
                    </div>
                    <div class="text-center p-4 rounded-lg hover:bg-white/5 cursor-pointer transition-colors">
                        <div class="text-2xl font-bold text-white mb-1">12</div>
                        <div class="text-xs text-slate-500 uppercase tracking-widest">En Proceso</div>
                    </div>
                    <div class="text-center p-4 rounded-lg hover:bg-white/5 cursor-pointer transition-colors">
                        <div class="text-2xl font-bold text-white mb-1">85%</div>
                        <div class="text-xs text-slate-500 uppercase tracking-widest">Salud Mental</div>
                    </div>
                </div>
            </div>

            <!-- VISTA: EDITOR / INBOX / WRITER -->
            <div x-show="mode === 'writer' || mode === 'inbox'" class="h-full flex flex-col fade-in">
                
                <!-- Aviso de Inbox (Banner superior opcional) -->
                <div x-show="isInboxNote" class="bg-amber-500/10 border-b border-amber-500/20 px-8 py-3 flex items-center justify-between">
                    <div class="flex items-center gap-2 text-amber-400 text-sm">
                        <i class="ph-fill ph-info"></i>
                        <span>Esta es una nota rápida sin clasificar. La IA ha sugerido un título.</span>
                    </div>
                    <button class="text-xs text-amber-300 hover:text-white underline decoration-amber-500/50">Mover a proyecto</button>
                </div>

                <div class="flex-1 py-12 px-8 editor-paper">
                    <!-- Título -->
                    <input type="text" x-model="currentNote.title" 
                           class="w-full bg-transparent text-4xl font-bold text-white mb-6 border-none focus:ring-0 placeholder-slate-600 outline-none leading-tight"
                           placeholder="Título de la nota...">

                    <!-- Cuerpo (Editable) -->
                    <div class="serif-text text-lg leading-relaxed text-[#d1d5db] space-y-6 outline-none min-h-[50vh]" contenteditable="true" x-ref="editorBody">
                        <!-- El contenido se inyecta aquí vía Alpine -->
                    </div>
                </div>
            </div>

        </div>
    </main>


    <!-- 4. PANEL DERECHO (AI) -->
    <aside class="w-80 bg-[#13151b] border-l border-white/5 flex flex-col shrink-0 relative z-20" :class="zenMode ? '-mr-80 opacity-0' : ''">
         <div class="h-14 flex items-center px-6 border-b border-white/5 justify-between bg-[#13151b]">
            <span class="text-xs font-bold text-indigo-400 uppercase flex items-center gap-2">Asistente</span>
        </div>
        <div class="p-6">
            <div x-show="isInboxNote" class="bg-[#1e222e] rounded-xl p-4 border border-amber-500/20 relative">
                <p class="text-sm text-slate-300 mb-3">
                    Analicé tu nota rápida. Parece tratar sobre <b>Frontend Architecture</b>.
                </p>
                <p class="text-xs text-slate-500 mb-3">¿Quieres que la mueva a:</p>
                <div class="flex flex-col gap-2">
                    <button class="text-left px-3 py-2 rounded bg-slate-800 hover:bg-indigo-600/20 border border-slate-700 hover:border-indigo-500 text-xs text-slate-300 transition-colors">
                        <i class="ph-bold ph-folder mr-1"></i> Proyectos / Dev
                    </button>
                     <button class="text-left px-3 py-2 rounded bg-slate-800 hover:bg-indigo-600/20 border border-slate-700 hover:border-indigo-500 text-xs text-slate-300 transition-colors">
                        <i class="ph-bold ph-folder mr-1"></i> Recursos / Librerías
                    </button>
                </div>
            </div>
        </div>
    </aside>

    <script>
        function appData() {
            return {
                mode: 'dashboard', 
                zenMode: false,
                quickInput: '',
                isInboxNote: false,
                
                // Modelo de nota actual
                currentNote: {
                    title: '',
                    body: ''
                },

                get modeDisplay() {
                    const t = { 'dashboard': 'Inicio', 'projects': 'Proyectos', 'writer': 'Editor', 'inbox': 'Bandeja de Entrada' };
                    return t[this.mode];
                },
                get leftPanelTitle() {
                    const t = { 'dashboard': 'Resumen', 'projects': 'Estructura', 'writer': 'Contenido', 'inbox': 'Pendientes' };
                    return t[this.mode];
                },

                setMode(m) {
                    this.mode = m;
                    // Resetear estado de inbox si salimos de writer/inbox a dashboard
                    if (m === 'dashboard') {
                        this.isInboxNote = false;
                        this.currentNote = { title: '', body: '' };
                    }
                    if (m === 'inbox') {
                        // Simular cargar la primera nota del inbox
                        this.openInboxItem(1);
                    }
                },

                handleQuickCapture(e) {
                    if (this.quickInput.trim() === '') return;

                    // 1. Detectar si es comando o contenido
                    // Aquí asumimos contenido para Quick Note
                    const content = this.quickInput;
                    
                    // 2. Generar título preliminar (Simulación IA)
                    const tempTitle = content.split(' ').slice(0, 5).join(' ') + '...';
                    const timestamp = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

                    // 3. Configurar estado
                    this.currentNote = {
                        title: `Nota rápida ${timestamp}`, // O tempTitle
                        body: content
                    };
                    
                    // 4. Cambiar UI
                    this.isInboxNote = true;
                    this.mode = 'inbox'; // O 'writer', visualmente similar pero 'inbox' activa el panel izquierdo correcto
                    
                    // 5. Inyectar en el editor (simulado)
                    setTimeout(() => {
                        this.$refs.editorBody.innerText = content;
                    }, 50);

                    // 6. Limpiar input
                    this.quickInput = '';
                },

                openInboxItem(id) {
                    this.isInboxNote = true;
                    this.mode = 'inbox';
                    this.currentNote = {
                        title: 'Análisis de Tiptap',
                        body: 'Investigar cómo integrar extensiones personalizadas en Tiptap para el soporte de IA...'
                    };
                    setTimeout(() => {
                        this.$refs.editorBody.innerText = this.currentNote.body;
                    }, 50);
                }
            }
        }
    </script>
</body>
</html>
```

---

## 📄 Archivo: `.research/idea4.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Knowledge OS - Master Version</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400&family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&display=swap');
        
        body { font-family: 'Inter', sans-serif; }
        .serif-text { font-family: 'Merriweather', serif; }
        .mono-text { font-family: 'JetBrains Mono', monospace; }

        /* Estilos base del sistema */
        .glass { background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.05); }
        .glass-panel { background: #13151b; border-right: 1px solid rgba(255, 255, 255, 0.05); }
        
        /* Editor centrado */
        .editor-paper { max-width: 68ch; margin: 0 auto; }
        
        /* Scrollbars ocultos */
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

        /* Animaciones */
        .fade-in-up { animation: fadeInUp 0.5s ease-out forwards; opacity: 0; transform: translateY(10px); }
        @keyframes fadeInUp { to { opacity: 1; transform: translateY(0); } }
        
        .delay-100 { animation-delay: 100ms; }
        .delay-200 { animation-delay: 200ms; }
        .delay-300 { animation-delay: 300ms; }

        /* Efecto de foco en cards */
        .smart-card { transition: all 0.3s ease; }
        .smart-card:hover { transform: translateY(-2px); border-color: rgba(99, 102, 241, 0.4); box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5); }
    </style>
</head>
<body class="bg-[#0f1117] text-slate-300 h-screen overflow-hidden flex selection:bg-indigo-500/30 selection:text-indigo-200" x-data="appData()">

    <!-- 1. NAVEGACIÓN PRINCIPAL (Extrema Izquierda) -->
    <nav class="w-16 bg-[#0B0C10] border-r border-white/5 flex flex-col items-center py-6 z-50 shrink-0">
        <div class="mb-8 text-indigo-500 text-3xl hover:text-white transition-colors cursor-pointer"><i class="ph-fill ph-brain"></i></div>
        
        <div class="flex flex-col gap-4 w-full px-2">
            <!-- Inicio -->
            <button @click="setMode('dashboard')" :class="mode === 'dashboard' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25' : 'text-slate-500 hover:text-indigo-400 hover:bg-white/5'" class="w-10 h-10 rounded-xl flex items-center justify-center transition-all group relative">
                <i class="ph-fill ph-squares-four text-xl"></i>
                <span class="absolute left-14 bg-[#1e222e] text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity border border-white/10 whitespace-nowrap z-50 pointer-events-none">Inicio</span>
            </button>

            <!-- Inbox (Con Badge) -->
            <button @click="setMode('inbox')" :class="mode === 'inbox' ? 'bg-amber-600 text-white shadow-lg shadow-amber-500/25' : 'text-slate-500 hover:text-amber-400 hover:bg-white/5'" class="w-10 h-10 rounded-xl flex items-center justify-center transition-all group relative">
                <i class="ph-fill ph-tray text-xl"></i>
                <span x-show="inboxCount > 0" class="absolute -top-1 -right-1 bg-amber-500 text-white text-[9px] font-bold px-1 rounded-full border border-[#0B0C10]" x-text="inboxCount"></span>
                <span class="absolute left-14 bg-[#1e222e] text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity border border-white/10 whitespace-nowrap z-50 pointer-events-none">Inbox</span>
            </button>

            <!-- Proyectos -->
            <button @click="setMode('projects')" :class="mode === 'projects' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25' : 'text-slate-500 hover:text-indigo-400 hover:bg-white/5'" class="w-10 h-10 rounded-xl flex items-center justify-center transition-all group relative">
                <i class="ph-fill ph-folder-notch text-xl"></i>
                <span class="absolute left-14 bg-[#1e222e] text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity border border-white/10 whitespace-nowrap z-50 pointer-events-none">Proyectos</span>
            </button>
        </div>
        
        <div class="mt-auto mb-4 group relative">
            <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-purple-400 to-indigo-500 border-2 border-[#0B0C10] ring-2 ring-indigo-500/30 cursor-pointer"></div>
        </div>
    </nav>


    <!-- 2. BARRA LATERAL CONTEXTUAL (Izquierda) -->
    <aside class="w-64 glass-panel flex flex-col transition-all duration-300 shrink-0" :class="zenMode ? '-ml-64 opacity-50' : ''">
        
        <div class="h-14 flex items-center px-5 border-b border-white/5 justify-between bg-[#13151b]">
            <span class="text-xs font-bold tracking-widest text-slate-500 uppercase" x-text="leftPanelTitle"></span>
        </div>

        <div class="flex-1 overflow-y-auto no-scrollbar p-3">
            
            <!-- CONTENIDO: DASHBOARD (Agenda + Stats) -->
            <div x-show="mode === 'dashboard'" class="space-y-6 fade-in-up">
                <!-- Mini Calendario / Agenda -->
                <div>
                    <h4 class="text-xs font-bold text-slate-500 uppercase mb-3 flex items-center gap-2">
                        <i class="ph-bold ph-calendar-blank"></i> Para Hoy
                    </h4>
                    <div class="space-y-2">
                        <div class="p-3 rounded-lg bg-white/5 border border-white/5 hover:border-indigo-500/30 transition-colors cursor-pointer group">
                            <div class="flex justify-between items-center mb-1">
                                <span class="text-xs text-indigo-300 bg-indigo-500/10 px-1.5 rounded">14:00</span>
                                <i class="ph-fill ph-check-circle text-slate-600 hover:text-emerald-500"></i>
                            </div>
                            <div class="text-sm text-slate-200 group-hover:text-white">Implementar LiteLLM</div>
                        </div>
                    </div>
                </div>

                <!-- Resumen de Inbox -->
                <div class="p-4 bg-gradient-to-br from-amber-500/5 to-orange-500/5 rounded-lg border border-amber-500/10">
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-amber-500 text-xs font-bold uppercase">Bandeja</span>
                        <span class="text-xs bg-amber-500/20 text-amber-400 px-1.5 rounded" x-text="inboxCount"></span>
                    </div>
                    <p class="text-xs text-slate-400 mb-3 leading-relaxed">Notas rápidas esperando ser procesadas por la IA.</p>
                    <button @click="setMode('inbox')" class="w-full py-1.5 bg-amber-500/10 text-amber-400 hover:text-white text-xs rounded hover:bg-amber-500 transition-colors border border-amber-500/20">Revisar</button>
                </div>
            </div>

            <!-- CONTENIDO: PROYECTOS (Árbol) -->
            <div x-show="mode === 'projects'" class="text-sm text-slate-400 fade-in-up">
                <div class="pl-2 py-2 hover:text-white cursor-pointer"><i class="ph-fill ph-books mr-2"></i> Biblioteca</div>
                <div class="mt-1">
                    <div class="pl-2 py-1.5 bg-indigo-500/10 text-indigo-300 rounded-md flex items-center gap-2 cursor-pointer border border-indigo-500/20">
                        <i class="ph-fill ph-folder-open"></i> Proyectos
                    </div>
                    <div class="pl-6 border-l border-white/10 ml-3.5 mt-1 space-y-1">
                        <div class="py-1.5 pl-2 text-white cursor-pointer hover:bg-white/5 rounded flex justify-between group">
                            <span>Análisis IA</span>
                            <span class="text-[10px] bg-slate-700 px-1 rounded opacity-0 group-hover:opacity-100">12</span>
                        </div>
                        <div class="py-1.5 pl-2 hover:text-white cursor-pointer hover:bg-white/5 rounded">Finanzas SaaS</div>
                    </div>
                </div>
            </div>

            <!-- CONTENIDO: EDITOR (TOC) -->
            <div x-show="mode === 'writer'" class="fade-in-up">
                <div class="text-xs font-bold text-slate-500 mb-3 uppercase pl-2">Tabla de Contenidos</div>
                <nav class="space-y-1 text-sm border-l border-slate-700 ml-2 pl-3">
                    <a href="#" class="block text-indigo-400 border-l-2 border-indigo-500 -ml-[14px] pl-3 py-1">Introducción</a>
                    <a href="#" class="block text-slate-400 hover:text-white py-1 transition-colors">Configuración</a>
                    <a href="#" class="block text-slate-400 hover:text-white py-1 pl-2 text-xs transition-colors">API Keys</a>
                    <a href="#" class="block text-slate-400 hover:text-white py-1 transition-colors">Conclusión</a>
                </nav>
            </div>
        </div>
    </aside>


    <!-- 3. ÁREA PRINCIPAL (Centro) -->
    <main class="flex-1 flex flex-col relative bg-[#0f1117] transition-all">
        
        <!-- Header Minimal -->
        <header class="h-14 flex items-center justify-between px-8 border-b border-white/5 shrink-0 bg-[#0f1117]/80 backdrop-blur-md z-10 sticky top-0">
            <div class="flex items-center gap-2 text-sm text-slate-500">
                <i class="ph-bold ph-house text-xs" x-show="mode === 'dashboard'"></i>
                <i class="ph-bold ph-pen-nib text-xs" x-show="mode === 'writer'"></i>
                <span x-text="modeDisplay"></span>
                <i class="ph-bold ph-caret-right text-xs" x-show="currentNote.title"></i>
                <span class="text-white truncate max-w-md font-medium" x-text="currentNote.title"></span>
            </div>
            
            <div class="flex items-center gap-3">
                <div class="flex items-center gap-1 text-[10px] bg-slate-800 px-2 py-1 rounded text-slate-400 border border-white/5">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span>LiteLLM Online</span>
                </div>
                <button @click="zenMode = !zenMode" class="text-slate-500 hover:text-white transition-colors p-1 rounded hover:bg-white/5">
                    <i :class="zenMode ? 'ph-fill ph-arrows-in-line-horizontal' : 'ph-fill ph-arrows-out-line-horizontal'"></i>
                </button>
            </div>
        </header>

        <!-- CANVAS SCROLLEABLE -->
        <div class="flex-1 overflow-y-auto relative no-scrollbar">
            
            <!-- VISTA: DASHBOARD (RICA EN INFORMACIÓN) -->
            <div x-show="mode === 'dashboard'" class="max-w-5xl mx-auto py-12 px-8">
                
                <!-- 1. Saludo y Briefing (V1/V2) -->
                <div class="mb-10 fade-in-up">
                    <h1 class="text-3xl font-light text-white mb-2">Hola, <span class="font-medium text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">Creador.</span></h1>
                    <p class="text-slate-400 text-lg flex items-center gap-2">
                        <i class="ph-fill ph-sparkle text-indigo-400"></i>
                        Tu foco ayer fue <span class="text-white border-b border-indigo-500/30">Python & IA</span>. Tienes 3 ideas pendientes de desarrollar.
                    </p>
                </div>

                <!-- 2. Omnibar de Captura (V3) -->
                <div class="relative group mb-12 fade-in-up delay-100">
                    <div class="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 via-purple-500 to-amber-500 rounded-xl blur opacity-20 group-hover:opacity-40 transition duration-500"></div>
                    <div class="relative bg-[#1a1d26] rounded-xl border border-white/10 shadow-2xl overflow-hidden">
                        <textarea 
                            x-model="quickInput"
                            @keydown.enter.prevent="handleQuickCapture()"
                            placeholder="¿Qué estás pensando? Escribe para capturar, '/' para comandos..." 
                            class="w-full bg-transparent border-none text-white text-lg px-6 py-5 focus:ring-0 placeholder-slate-500 font-light resize-none h-20"
                        ></textarea>
                        <div class="px-4 py-2 bg-[#15171e] flex justify-between items-center border-t border-white/5">
                            <div class="flex gap-3 text-xs text-slate-500 font-mono">
                                <span class="hover:text-white cursor-pointer"><span class="bg-[#252836] px-1.5 py-0.5 rounded mr-1">⌘K</span> Buscar</span>
                                <span class="hover:text-white cursor-pointer"><span class="bg-[#252836] px-1.5 py-0.5 rounded mr-1">/</span> Prompt</span>
                            </div>
                            <button @click="handleQuickCapture()" class="text-indigo-400 hover:text-white transition-colors">
                                <i class="ph-bold ph-arrow-return-left"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 3. Grid de Tarjetas "Vivas" (V1) -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 fade-in-up delay-200">
                    
                    <!-- Card: En Foco (Proyecto Activo) -->
                    <div @click="setMode('projects')" class="smart-card bg-[#15171e] p-5 rounded-2xl border border-white/5 cursor-pointer relative overflow-hidden group">
                        <div class="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                            <i class="ph-fill ph-folder-open text-6xl text-indigo-500"></i>
                        </div>
                        <div class="text-xs font-bold text-indigo-400 uppercase tracking-widest mb-3">Proyecto Activo</div>
                        <h3 class="text-white text-lg font-medium mb-1">Análisis de Proyectos</h3>
                        <p class="text-sm text-slate-400 mb-4 line-clamp-2">Estás documentando la integración de IA. Última edición hace 2 horas.</p>
                        <div class="flex items-center gap-2 text-xs text-slate-500">
                            <span class="bg-indigo-500/10 text-indigo-300 px-2 py-1 rounded">12 notas</span>
                            <span class="bg-indigo-500/10 text-indigo-300 px-2 py-1 rounded">Dev</span>
                        </div>
                    </div>

                    <!-- Card: Serendipia (Conexiones) -->
                    <div class="smart-card bg-[#15171e] p-5 rounded-2xl border border-white/5 cursor-pointer relative overflow-hidden group hover:border-amber-500/30">
                        <div class="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                            <i class="ph-fill ph-lightbulb text-6xl text-amber-500"></i>
                        </div>
                        <div class="text-xs font-bold text-amber-400 uppercase tracking-widest mb-3 flex items-center gap-2">
                            <i class="ph-bold ph-link"></i> Conexión
                        </div>
                        <h3 class="text-white text-lg font-medium mb-1">Docker + Embeddings</h3>
                        <p class="text-sm text-slate-400 mb-4">La IA detectó similitudes entre "Despliegue Local" y "Supabase Vector".</p>
                        <button class="text-xs bg-amber-500/10 text-amber-300 px-3 py-1.5 rounded border border-amber-500/20 hover:bg-amber-500 hover:text-white transition-colors">Fusionar Notas</button>
                    </div>

                    <!-- Card: Mantenimiento (Jardinero) -->
                    <div class="smart-card bg-[#15171e] p-5 rounded-2xl border border-white/5 cursor-pointer relative overflow-hidden group hover:border-emerald-500/30">
                         <div class="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                            <i class="ph-fill ph-plant text-6xl text-emerald-500"></i>
                        </div>
                        <div class="text-xs font-bold text-emerald-400 uppercase tracking-widest mb-3">Jardinero</div>
                        <h3 class="text-white text-lg font-medium mb-1">Etiquetado Auto</h3>
                        <p class="text-sm text-slate-400 mb-4">Hay 4 notas en Inbox sin etiquetas. ¿Aplicar taxonomía automática?</p>
                        <div class="w-full bg-slate-800 rounded-full h-1.5 mt-2 overflow-hidden">
                            <div class="bg-emerald-500 h-full w-2/3"></div>
                        </div>
                    </div>
                </div>

                <!-- 4. Notas Recientes (Masonry Grid V1) -->
                <div class="fade-in-up delay-300">
                    <h3 class="text-slate-500 text-sm font-bold uppercase tracking-widest mb-4">Trabajo Reciente</h3>
                    <div class="columns-1 md:columns-2 gap-6 space-y-6">
                        <!-- Nota 1 -->
                        <div @click="setMode('writer'); currentNote.title='Configuración LiteLLM'" class="break-inside-avoid bg-[#15171e] p-5 rounded-xl border border-white/5 hover:border-indigo-500/40 cursor-pointer transition-colors group">
                            <h4 class="text-white font-medium mb-2 group-hover:text-indigo-400 transition-colors">Configuración LiteLLM</h4>
                            <p class="text-slate-400 text-sm mb-3 leading-relaxed">Snippet para configurar el fallback entre OpenAI y Anthropic usando el proxy server...</p>
                            <div class="flex gap-2">
                                <span class="text-[10px] bg-slate-800 text-slate-400 px-2 py-1 rounded">#python</span>
                                <span class="text-[10px] bg-slate-800 text-slate-400 px-2 py-1 rounded">#ai</span>
                            </div>
                        </div>
                         <!-- Nota 2 -->
                        <div class="break-inside-avoid bg-[#15171e] p-5 rounded-xl border border-white/5 hover:border-indigo-500/40 cursor-pointer transition-colors group">
                            <h4 class="text-white font-medium mb-2 group-hover:text-indigo-400 transition-colors">Ideas App V4</h4>
                            <p class="text-slate-400 text-sm mb-3 leading-relaxed">Definir estructura de 3 columnas y usar Alpine para la reactividad...</p>
                            <span class="text-[10px] bg-slate-800 text-slate-400 px-2 py-1 rounded">#design</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- VISTA: EDITOR / WRITER / INBOX (EL FOCO) -->
            <div x-show="mode === 'writer' || mode === 'inbox'" class="h-full flex flex-col fade-in-up">
                
                <!-- Aviso si es Inbox -->
                <div x-show="mode === 'inbox'" class="bg-amber-500/10 border-b border-amber-500/10 px-6 py-2 flex items-center justify-center gap-2 text-xs text-amber-300">
                    <i class="ph-fill ph-tray"></i>
                    Modo Inbox: Esta nota aún no está clasificada.
                </div>

                <div class="flex-1 py-12 px-8 editor-paper">
                    <input type="text" x-model="currentNote.title" 
                           class="w-full bg-transparent text-4xl font-bold text-white mb-8 border-none focus:ring-0 placeholder-slate-600 outline-none leading-tight"
                           placeholder="Título...">

                    <!-- Contenido Simulado -->
                    <div class="serif-text text-lg leading-loose text-[#d1d5db] space-y-6 outline-none min-h-[60vh]" contenteditable="true" x-ref="editor">
                        <p>LiteLLM funciona como un proxy gateway unificado para llamar a más de 100 modelos (OpenAI, Anthropic, Azure, etc.).</p>
                        <p>Lo interesante para nuestra app en <b>FastAPI</b> es que permite gestionar presupuestos.</p>
                        <p class="text-slate-500 italic">Escribe "/" para invocar a la IA...</p>
                    </div>
                    <div class="h-32"></div> <!-- Espacio extra abajo -->
                </div>
            </div>

        </div>
    </main>


    <!-- 4. PANEL DERECHO (AI COPILOT) -->
    <aside class="w-80 glass-panel flex flex-col shrink-0 relative z-20" :class="zenMode ? '-mr-80 opacity-0' : ''">
         <div class="h-14 flex items-center px-6 border-b border-white/5 justify-between bg-[#13151b]">
            <span class="text-xs font-bold text-indigo-400 uppercase flex items-center gap-2">
                <i class="ph-fill ph-magic-wand"></i> Copiloto
            </span>
            <button class="text-slate-500 hover:text-white"><i class="ph ph-dots-three"></i></button>
        </div>
        
        <div class="flex-1 overflow-y-auto p-5 space-y-6">
            
            <!-- Contexto IA -->
            <div x-show="mode === 'writer' || mode === 'inbox'" class="fade-in-up">
                <div class="bg-[#1e222e] rounded-xl p-4 border border-indigo-500/20 shadow-lg relative">
                    <div class="absolute -left-2 top-4 w-2 h-2 bg-[#1e222e] border-l border-b border-indigo-500/20 transform rotate-45"></div>
                    <p class="text-sm text-slate-300 leading-relaxed mb-3">
                        Detecto que hablas de <b class="text-white">LiteLLM</b>.
                    </p>
                    <p class="text-xs text-slate-400 mb-3">
                        En tu proyecto "Finanzas SaaS" tienes una nota sobre <i>Budget Management</i>. ¿Quieres relacionarlas?
                    </p>
                    <div class="flex gap-2">
                        <button class="flex-1 bg-indigo-600/20 hover:bg-indigo-600 text-indigo-300 hover:text-white text-xs py-1.5 rounded transition-all border border-indigo-500/30">Sí, relacionar</button>
                    </div>
                </div>
            </div>

            <!-- Stats del Sistema (Visible en Dashboard) -->
            <div x-show="mode === 'dashboard'" class="fade-in-up delay-100">
                <h5 class="text-xs font-bold text-slate-500 uppercase mb-3">Estado del Sistema</h5>
                <div class="space-y-3">
                    <div class="flex justify-between items-center text-sm">
                        <span class="text-slate-400">Tokens hoy</span>
                        <span class="text-white font-mono">12,450</span>
                    </div>
                    <div class="flex justify-between items-center text-sm">
                        <span class="text-slate-400">Costo est.</span>
                        <span class="text-emerald-400 font-mono">$0.04</span>
                    </div>
                    <div class="w-full bg-slate-800 rounded-full h-1 mt-2">
                        <div class="bg-indigo-500 h-full w-1/4"></div>
                    </div>
                </div>

                <h5 class="text-xs font-bold text-slate-500 uppercase mt-8 mb-3">Sugerencias Rápidas</h5>
                <div class="space-y-2">
                    <div class="p-2 rounded hover:bg-white/5 cursor-pointer text-xs text-slate-300 border border-transparent hover:border-white/10 transition-colors">
                        <i class="ph-bold ph-plus-circle text-indigo-400 mr-1"></i> Crear entrada de diario
                    </div>
                    <div class="p-2 rounded hover:bg-white/5 cursor-pointer text-xs text-slate-300 border border-transparent hover:border-white/10 transition-colors">
                        <i class="ph-bold ph-arrows-merge text-amber-400 mr-1"></i> Revisar conexiones
                    </div>
                </div>
            </div>

        </div>

        <!-- Chat Input -->
        <div class="p-4 border-t border-white/5 bg-[#13151b]">
            <div class="relative">
                <input type="text" placeholder="Pregunta a la IA..." class="w-full bg-[#0f1117] border border-white/10 rounded-lg py-2 pl-3 pr-8 text-sm text-slate-300 focus:outline-none focus:border-indigo-500 transition-colors placeholder-slate-600">
                <button class="absolute right-2 top-2 text-indigo-500 hover:text-white"><i class="ph-fill ph-paper-plane-right"></i></button>
            </div>
        </div>
    </aside>

    <script>
        function appData() {
            return {
                mode: 'dashboard', // dashboard, projects, writer, inbox
                zenMode: false,
                quickInput: '',
                inboxCount: 3,
                
                currentNote: {
                    title: '',
                    body: ''
                },

                get modeDisplay() {
                    const t = { 'dashboard': 'Centro de Mando', 'projects': 'Biblioteca', 'writer': 'Editor', 'inbox': 'Bandeja de Entrada' };
                    return t[this.mode];
                },
                get leftPanelTitle() {
                    const t = { 'dashboard': 'Agenda & Resumen', 'projects': 'Explorador', 'writer': 'Estructura', 'inbox': 'Pendientes' };
                    return t[this.mode];
                },

                setMode(m) {
                    this.mode = m;
                    if (m === 'dashboard') {
                        this.currentNote.title = ''; 
                    }
                },

                handleQuickCapture() {
                    if (this.quickInput.trim() === '') return;
                    
                    const content = this.quickInput;
                    const timestamp = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                    
                    this.currentNote = {
                        title: `Nota rápida ${timestamp}`,
                        body: content
                    };
                    
                    // Efecto visual
                    this.inboxCount++;
                    this.quickInput = '';
                    this.setMode('inbox');
                    
                    setTimeout(() => {
                        if(this.$refs.editor) this.$refs.editor.innerText = content;
                    }, 100);
                }
            }
        }
    </script>
</body>
</html>
```

---

## 📄 Archivo: `.research/inspector2.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inspector UI - Fixed</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        body { font-family: 'Inter', sans-serif; background-color: #0d0f14; }
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #2d3139; border-radius: 10px; }
    </style>
</head>
<body class="text-slate-300 antialiased">

    <aside 
        x-data="{ 
            activeToc: 1,
            tags: ['Base de datos', 'PostgreSQL', 'Esquema'],
            attachments: [
                { id: 1, name: 'backup_process.py' },
                { id: 2, name: 'import_os.py' }
            ],
            removeTag(index) { this.tags.splice(index, 1) },
            removeFile(id) { this.attachments = this.attachments.filter(f => f.id !== id) }
        }"
        x-init="$nextTick(() => lucide.createIcons())"
        class="w-80 h-screen border-l border-white/5 flex flex-col bg-[#0d0f14] fixed right-0 top-0 shadow-2xl"
    >
        
        <!-- HEADER (Igual a la V1) -->
        <div class="p-6 pb-4 flex items-center justify-between border-b border-white/5">
            <div class="flex items-center gap-2">
                <i data-lucide="info" class="w-4 h-4 text-purple-400"></i>
                <h2 class="text-[11px] font-bold tracking-[0.2em] text-slate-500 uppercase">Inspector</h2>
            </div>
            <button class="hover:text-white transition-colors">
                <i data-lucide="more-horizontal" class="w-4 h-4 text-slate-500"></i>
            </button>
        </div>

        <!-- CONTENIDO SCROLLABLE -->
        <div class="flex-1 overflow-y-auto">
            
            <!-- SECCIÓN: TABLA DE CONTENIDOS (Igual a la V1) -->
            <section class="p-6">
                <h3 class="text-[10px] font-semibold text-slate-500 uppercase tracking-widest mb-4">Tabla de Contenidos</h3>
                <nav class="space-y-1">
                    <template x-for="(item, index) in ['Definición del Esquema', 'Tabla: cuadernos', 'Tabla: temas', 'Tabla: anotaciones']">
                        <a href="#" @click.prevent="activeToc = index"
                            :class="activeToc === index ? 'text-purple-400 bg-purple-500/5' : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'"
                            class="flex items-center gap-3 px-3 py-2 rounded-lg text-xs transition-all duration-200">
                            <span :class="activeToc === index ? 'bg-purple-400 w-1.5 h-1.5' : 'bg-slate-700 w-1 h-1'" class="rounded-full"></span>
                            <span x-text="item"></span>
                        </a>
                    </template>
                </nav>
            </section>

            <!-- SECCIÓN: ETIQUETAS (Restaurado icono plus-circle) -->
            <section class="px-6 py-4 border-t border-white/5">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-[10px] font-semibold text-slate-500 uppercase tracking-widest">Etiquetas</h3>
                    <button class="text-purple-400 hover:text-purple-300 transition-colors">
                        <i data-lucide="plus-circle" class="w-3.5 h-3.5"></i>
                    </button>
                </div>
                <div class="flex flex-wrap gap-2">
                    <template x-for="(tag, index) in tags" :key="index">
                        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-white/5 border border-white/10 text-[11px] text-slate-300">
                            <span x-text="tag"></span>
                            <button @click="removeTag(index)" class="hover:text-red-400">
                                <i data-lucide="x" class="w-3 h-3"></i>
                            </button>
                        </span>
                    </template>
                </div>
            </section>

            <!-- SECCIÓN: ARCHIVOS ADJUNTOS (Icono eliminar siempre visible) -->
            <section class="px-6 py-4 border-t border-white/5">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-[10px] font-semibold text-slate-500 uppercase tracking-widest">Archivos</h3>
                    <button class="text-purple-400 hover:text-purple-300 transition-colors">
                        <i data-lucide="paperclip" class="w-3.5 h-3.5"></i>
                    </button>
                </div>
                <div class="space-y-2">
                    <template x-for="file in attachments" :key="file.id">
                        <div class="flex items-center justify-between p-2 rounded-lg hover:bg-white/5 transition-all">
                            <div class="flex items-center gap-3">
                                <i data-lucide="file-text" class="w-4 h-4 text-slate-500"></i>
                                <span class="text-xs text-slate-400" x-text="file.name"></span>
                            </div>
                            <!-- Botón eliminar ahora visible sin hover -->
                            <button @click="removeFile(file.id)" class="text-slate-600 hover:text-red-400 transition-colors">
                                <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                            </button>
                        </div>
                    </template>
                </div>
            </section>
        </div>

        <!-- SECCIÓN INFERIOR: SHARE Y EXPORT EN UNA SOLA LÍNEA -->
        <div class="p-6 bg-[#0d0f14] border-t border-white/5">
            <div class="flex gap-2">
                <button class="flex-1 flex items-center justify-center gap-2 py-2.5 px-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-[11px] font-medium text-slate-200 transition-all active:scale-[0.98]">
                    <i data-lucide="share-2" class="w-3.5 h-3.5"></i>
                    Share
                </button>
                
                <button class="flex-1 flex items-center justify-center gap-2 py-2.5 px-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-xl text-[11px] font-semibold shadow-lg shadow-purple-900/20 transition-all active:scale-[0.98]">
                    <i data-lucide="file-up" class="w-3.5 h-3.5"></i>
                    Export PDF
                </button>
            </div>
        </div>

    </aside>

    <script>
        // Esto asegura que los iconos se carguen incluso dentro de los loops de Alpine
        document.addEventListener('alpine:initialized', () => {
            lucide.createIcons();
        });
    </script>
</body>
</html>
```

---

## 📄 Archivo: `Dockerfile`
```txt
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2 o librerías de C
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Exponer el puerto que usa FastAPI
EXPOSE 8000

# Comando para arrancar la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📄 Archivo: `app/__init__.py`
```py

```

---

## 📄 Archivo: `app/core/auth.py`
```py
from typing import Optional
from fastapi import Request, Depends, HTTPException, status
from jose import jwt, JWTError
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.config import settings
from app.core.database import get_db
from app.core.security import verify_password
from app.models import UsuarioDB

# Dependencia para obtener el usuario desde la Cookie
async def get_current_user(
    request: Request, 
    session: AsyncSession = Depends(get_db)
) -> Optional[UsuarioDB]:
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    # Limpieza del token (Bearer ...)
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None

    # Buscar usuario en DB
    try:
        u_uuid = uuid.UUID(user_id)
        result = await session.exec(select(UsuarioDB).where(UsuarioDB.id == u_uuid))
        user = result.first()
        return user
    except (ValueError, Exception):
        return None

# Dependencia estricta (lanza error si no hay usuario)
async def get_authenticated_user(user: Optional[UsuarioDB] = Depends(get_current_user)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Función de Login
async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[UsuarioDB]:
    statement = select(UsuarioDB).where(UsuarioDB.email == email)
    result = await session.exec(statement)
    user = result.first()
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
```

---

## 📄 Archivo: `app/core/config.py`
```py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Docs.ai"
    VERSION: str = "2.0.0"
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días

    # External
    SUPABASE_URL: str | None = None
    SUPABASE_KEY: str | None = None

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
```

---

## 📄 Archivo: `app/core/database.py`
```py
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.core.config import settings
from typing import AsyncGenerator
from supabase import create_client, Client
import os

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_KEY

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# 1. Ajuste de URL para Asyncpg
db_url = settings.DATABASE_URL
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url and db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# 2. Motor Asíncrono
# statement_cache_size=0 es crítico para Supabase/PgBouncer
engine = create_async_engine(
    db_url,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_recycle=300, # Recicla conexiones cada 5 min para evitar cierres de Supabase
    connect_args={
        "statement_cache_size": 0,
        "timeout": 60, # 60 segundos es generoso para el handshake SSL
    }
)

# 3. Factoría de Sesiones
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 4. Inyección de Seguridad (RLS)
async def init_rls(session: AsyncSession, user_id: str):
    """Inyecta el ID del usuario en la sesión para las políticas de seguridad de la DB"""
    if user_id:
        # Sanitización básica: asegurar que sea un UUID válido o string seguro
        await session.execute(text(f"SET LOCAL app.current_user_id = '{user_id}'"))

# 5. Dependencia para FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
```

---

## 📄 Archivo: `app/core/security.py`
```py
from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
import bcrypt  # <--- Usamos la librería nativa
from app.core.config import settings

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica el password usando bcrypt nativo"""
    # bcrypt requiere bytes, no strings
    if isinstance(plain_password, str):
        plain_password_bytes = plain_password.encode('utf-8')
    else:
        plain_password_bytes = plain_password
        
    if isinstance(hashed_password, str):
        hashed_password_bytes = hashed_password.encode('utf-8')
    else:
        hashed_password_bytes = hashed_password
        
    try:
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
    except ValueError:
        return False

def get_password_hash(password: str) -> str:
    """Genera el hash usando bcrypt nativo"""
    if isinstance(password, str):
        password_bytes = password.encode('utf-8')
    else:
        password_bytes = password
        
    # Generar salt y hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Devolvemos string para guardar en Postgres
    return hashed.decode('utf-8')
```

---

## 📄 Archivo: `app/main.py`
```py
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel
import os

from app.core.database import engine
from app.core.config import settings
from app.models import * 
from app.routers import dashboard, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, lifespan=lifespan)

# Asegurar que la carpeta static existe para evitar errores de montado
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates") 

# --- MANEJADOR DE ERRORES (Redirección al Login) ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    return exc

# --- RUTAS ---
@app.get("/")
async def root():
    """Redirige la raíz al dashboard directamente"""
    return RedirectResponse(url="/dashboard")

app.include_router(dashboard.router)
app.include_router(auth.router)
```

---

## 📄 Archivo: `app/models.py`
```py
import uuid
import json
import re
from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Column, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy import text

# --- USUARIO ---
class UsuarioDB(SQLModel, table=True):
    __tablename__ = "usuarios"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    email: str = Field(unique=True, index=True)
    hashed_password: str
    nombre: str
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )

# --- CATEGORÍA (Biblioteca) ---
class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    nombre: str
    icono: str = Field(default="folder")
    color: str = Field(default="#3b82f6")
    orden: int = Field(default=0)
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    # Relaciones
    cuadernos: List["Cuaderno"] = Relationship(
        back_populates="categoria",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

# --- CUADERNO / PROYECTO ---
class Cuaderno(SQLModel, table=True):
    __tablename__ = "cuadernos"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    nombre: str
    descripcion: Optional[str] = None
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    categoria_id: Optional[uuid.UUID] = Field(default=None, foreign_key="categorias.id")
    
    # Campos específicos de Proyecto
    tipo: str = Field(default="cuaderno")  # 'cuaderno' | 'proyecto'
    estado: str = Field(default="activo")
    fecha_limite: Optional[datetime] = None
    progreso: int = Field(default=0)

    # Relaciones
    categoria: Optional[Categoria] = Relationship(back_populates="cuadernos")
    temas: List["Tema"] = Relationship(
        back_populates="cuaderno",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    tareas: List["Tarea"] = Relationship(
        back_populates="cuaderno",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

# --- TAREA ---
class Tarea(SQLModel, table=True):
    __tablename__ = "tareas"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    titulo: str
    hecho: bool = Field(default=False)
    cuaderno_id: Optional[uuid.UUID] = Field(default=None, foreign_key="cuadernos.id")
    fecha_objetivo: Optional[datetime] = None
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    cuaderno: Optional[Cuaderno] = Relationship(back_populates="tareas")

# --- TEMA ---
class Tema(SQLModel, table=True):
    __tablename__ = "temas"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    nombre: str
    orden: int = Field(default=0)
    cuaderno_id: uuid.UUID = Field(foreign_key="cuadernos.id")
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    cuaderno: Optional[Cuaderno] = Relationship(back_populates="temas")
    anotaciones: List["Anotacion"] = Relationship(
        back_populates="tema",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

# --- ANOTACION ---
class Anotacion(SQLModel, table=True):
    __tablename__ = "anotaciones"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    titulo: str
    contenido: Optional[str] = None
    tags: List[str] = Field(default=[], sa_column=Column(ARRAY(String)))
    tema_id: uuid.UUID = Field(foreign_key="temas.id")
    created_at: Optional[datetime] = Field(default=None, sa_column_kwargs={"server_default": text("now()")})
    updated_at: Optional[datetime] = Field(default=None, sa_column_kwargs={"server_default": text("now()"), "onupdate": text("now()")})
    
    tema: Optional["Tema"] = Relationship(back_populates="anotaciones")
    adjuntos: List["Adjunto"] = Relationship(back_populates="anotacion", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    @property
    def resumen_texto(self) -> str:
        """Extrae texto plano de forma ultra-rápida usando Regex"""
        if not self.contenido or len(self.contenido) < 5:
            return ""
        
        content = self.contenido.strip()
        
        # Caso 1: Es JSON de TipTap (Empieza con {)
        if content.startswith('{'):
            # Usamos Regex para capturar solo lo que está dentro de "text":"..."
            # Es 100 veces más rápido que parsear el JSON completo
            textos = re.findall(r'"text"\s*:\s*"([^"]+)"', content)
            return " ".join(textos) if textos else ""
            
        # Caso 2: Es HTML Legacy
        # Limpiamos etiquetas <...> y devolvemos el texto
        return re.sub(r'<[^<]+?>', '', content)
    
# --- ADJUNTO ---
class Adjunto(SQLModel, table=True):
    __tablename__ = "adjuntos"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    url: str
    nombre_original: Optional[str] = None
    tipo_archivo: Optional[str] = None
    anotacion_id: uuid.UUID = Field(foreign_key="anotaciones.id")
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    anotacion: Optional[Anotacion] = Relationship(back_populates="adjuntos")
```

---

## 📄 Archivo: `app/routers/auth.py`
```py
from datetime import timedelta
from fastapi import APIRouter, Depends, Request, Response, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

# 1. ACTUALIZAR ESTA LÍNEA (Añadir los modelos faltantes)
from app.core.database import get_db, init_rls  # Añadimos init_rls
from app.core.config import settings
from app.core.auth import authenticate_user
from app.core.security import create_access_token, get_password_hash
from app.models import UsuarioDB, Categoria, Cuaderno, Tema # <--- Importar todos


router = APIRouter()
templates = Jinja2Templates(directory="templates")

# --- LOGIN ---
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request})

@router.post("/login")
async def login_action(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(session, email, password)
    if not user:
        return RedirectResponse(url="/login?error=1", status_code=status.HTTP_303_SEE_OTHER)
    
    # Crear Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    # Redirigir + Set Cookie
    resp = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    resp.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False # True si usas HTTPS en prod
    )
    return resp

# --- LOGOUT ---
@router.get("/logout")
async def logout():
    resp = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    resp.delete_cookie("access_token")
    return resp

# --- REGISTER ---
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("pages/register.html", {"request": request})

@router.post("/register")
async def register_action(
    email: str = Form(...),
    password: str = Form(...),
    nombre: str = Form(...),
    session: AsyncSession = Depends(get_db)
):
    # Verificar si existe
    statement = select(UsuarioDB).where(UsuarioDB.email == email)
    result = await session.exec(statement)
    if result.first():
        return RedirectResponse(url="/register?error=exists", status_code=status.HTTP_303_SEE_OTHER)
    
    # Crear Usuario
    hashed_pwd = get_password_hash(password)
    new_user = UsuarioDB(email=email, hashed_password=hashed_pwd, nombre=nombre)
    session.add(new_user)
    
    # IMPORTANTE: Necesitamos el ID generado para el RLS
    await session.flush() 

    # 2. AXIOMA II.I: Inyectar RLS para poder crear la estructura inicial
    # Sin esto, las políticas de Postgres que ejecutaste antes bloquearían la inserción
    await init_rls(session, str(new_user.id))

    # Crear Estructura Maestra
    try:
        # Categoría General
        cat_general = Categoria(nombre="General", user_id=new_user.id, icono="folder")
        session.add(cat_general)
        await session.flush()

        # Cuaderno Inbox
        inbox = Cuaderno(nombre="Inbox", user_id=new_user.id, categoria_id=cat_general.id, tipo="cuaderno")
        session.add(inbox)
        await session.flush()

        # Tema Capturas Rápidas
        tema_capturas = Tema(nombre="Capturas Rápidas", user_id=new_user.id, cuaderno_id=inbox.id)
        session.add(tema_capturas)

        await session.commit()
    except Exception as e:
        await session.rollback()
        print(f"Error creando estructura inicial: {e}")
        return RedirectResponse(url="/register?error=structure", status_code=status.HTTP_303_SEE_OTHER)

    return RedirectResponse(url="/login?registered=1", status_code=status.HTTP_303_SEE_OTHER)
```

---

## 📄 Archivo: `app/routers/dashboard.py`
```py
# app/routers/dashboard.py
from fastapi import APIRouter, Depends, Request, Form, Response, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select, desc, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from datetime import date, datetime
from pydantic import BaseModel
import mimetypes
import os

from app.core.database import get_db, init_rls
from app.core.auth import get_authenticated_user
from app.models import UsuarioDB, Categoria, Cuaderno, Anotacion, Tarea, Tema, Adjunto
from app.core.database import supabase
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    # RLS OBLIGATORIO
    await init_rls(session, str(user.id))

    # 1. Cargar Bibliotecas/Categorías
    stmt_cat = (
        select(Categoria)
        .where(Categoria.user_id == user.id)
        .order_by(Categoria.orden)
        .options(selectinload(Categoria.cuadernos))
    )
    categorias = (await session.exec(stmt_cat)).all()

    # 2. Tareas de hoy
    stmt_tareas = (
        select(Tarea)
        .where(Tarea.user_id == user.id, Tarea.hecho == False)
        .order_by(Tarea.fecha_objetivo.asc().nullslast())
        .limit(5)
    )
    agenda = (await session.exec(stmt_tareas)).all()

    # 3. Proyectos
    stmt_proy = (
        select(Cuaderno)
        .where(Cuaderno.user_id == user.id, Cuaderno.tipo == 'proyecto')
    )
    proyectos = (await session.exec(stmt_proy)).all()

    # 4. Notas Recientes
    stmt_recientes = (
        select(Anotacion)
        .where(Anotacion.user_id == user.id)
        .order_by(desc(Anotacion.updated_at))
        .limit(4)
        .options(selectinload(Anotacion.tema).selectinload(Tema.cuaderno))
    )
    recientes = (await session.exec(stmt_recientes)).all()

    return templates.TemplateResponse("layouts/base.html", {
        "request": request,
        "user": user,
        "view_mode": "dashboard",
        "categorias": categorias,
        "agenda": agenda,
        "proyectos": proyectos,
        "recientes": recientes,
        "today": date.today()
    })

@router.post("/inbox/captura")
async def captura_inbox(
    contenido: str = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    # Buscamos directamente el ID del tema inmutable
    stmt = (
        select(Tema.id)
        .join(Cuaderno)
        .where(
            Cuaderno.user_id == user.id,
            Cuaderno.nombre == "Inbox",
            Tema.nombre == "Capturas Rápidas"
        )
    )
    tema_id = (await session.exec(stmt)).first()

    if not tema_id:
        # Fallback de seguridad por si el usuario es antiguo y no tiene la estructura
        return Response(status_code=400) # O podrías llamar a una función de reparación

    nueva_nota = Anotacion(
        titulo=f"Nota {datetime.now().strftime('%H:%M')}",
        contenido=contenido,
        user_id=user.id,
        tema_id=tema_id
    )
    session.add(nueva_nota)
    await session.commit()

    resp = Response(status_code=204)
    resp.headers["HX-Trigger"] = "update-inbox-count, update-inbox-list"
    return resp

@router.get("/inbox/count")
async def get_inbox_count(
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    stmt = (
            select(func.count(Anotacion.id))
            .join(Tema, Anotacion.tema_id == Tema.id)
            .join(Cuaderno, Tema.cuaderno_id == Cuaderno.id)
            .where(
                Cuaderno.user_id == user.id,
                Cuaderno.nombre == "Inbox",
                Tema.nombre == "Capturas Rápidas"
            )
        )
        
    count = (await session.exec(stmt)).one()
        
    # Retornamos el número puro como texto plano
    return PlainTextResponse(str(count))

@router.get("/partial/sidebar/inbox", response_class=HTMLResponse)
async def get_sidebar_inbox(
    request: Request,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    # Buscamos las notas en la ruta GENERAL -> Inbox -> Capturas Rápidas
    stmt = (
        select(Anotacion)
        .join(Tema)
        .join(Cuaderno)
        .where(
            Cuaderno.user_id == user.id,
            Cuaderno.nombre == "Inbox",
            Tema.nombre == "Capturas Rápidas"
        )
        .order_by(desc(Anotacion.created_at))
    )
    notas = (await session.exec(stmt)).all()

    return templates.TemplateResponse("modules/sidebar_inbox.html", {
        "request": request,
        "notas": notas
    })

# También necesitamos el endpoint para restaurar la sidebar del dashboard
@router.get("/partial/sidebar/dashboard", response_class=HTMLResponse)
async def get_sidebar_dashboard(
    request: Request,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    stmt_cat = (
        select(Categoria)
        .where(Categoria.user_id == user.id)
        .order_by(Categoria.orden)
        .options(selectinload(Categoria.cuadernos))
    )
    categorias = (await session.exec(stmt_cat)).all()
    
    # Reutilizamos el partial que ya teníamos
    return templates.TemplateResponse("modules/sidebar_dashboard.html", {
        "request": request,
        "categorias": categorias
    })

@router.get("/partial/modal/inbox-actions/{nota_id}", response_class=HTMLResponse)
async def get_modal_inbox_actions(
    nota_id: uuid.UUID,
    request: Request,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    # Buscamos la nota (SQLModel/SQLAlchemy)
    # Al ser una sesión nueva por cada request, no hay caché de objeto.
    nota = await session.get(Anotacion, nota_id)
    
    stmt = (
        select(Categoria)
        .where(Categoria.user_id == user.id)
        .order_by(Categoria.orden)
        .options(selectinload(Categoria.cuadernos).selectinload(Cuaderno.temas))
    )
    categorias = (await session.exec(stmt)).all()

    response = templates.TemplateResponse("partials/modal_inbox_triaje.html", {
        "request": request,
        "nota": nota,
        "categorias": categorias
    })
    
    # Headers de hierro para evitar caché del navegador
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response

@router.get("/partial/modal/inbox-mover/{nota_id}", response_class=HTMLResponse)
async def get_modal_inbox_mover(
    nota_id: uuid.UUID,
    request: Request,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    """Retorna el nuevo modal de triaje con buscador y jerarquía completa"""
    await init_rls(session, str(user.id))
    
    # 1. Obtener la nota
    nota = await session.get(Anotacion, nota_id)
    if not nota:
        return PlainTextResponse("Nota no encontrada", status_code=404)
    
    # 2. Obtener toda la jerarquía (Biblioteca > Cuaderno > Tema)
    # Excluimos el cuaderno 'Inbox' de los destinos posibles
    stmt = (
        select(Categoria)
        .where(Categoria.user_id == user.id)
        .options(
            selectinload(Categoria.cuadernos)
            .selectinload(Cuaderno.temas)
        )
        .order_by(Categoria.orden)
    )
    result = await session.exec(stmt)
    categorias = result.all()
    
    return templates.TemplateResponse("partials/modal_inbox_triaje.html", {
        "request": request,
        "nota": nota,
        "categorias": categorias
    })

@router.post("/inbox/mover/{nota_id}")
async def mover_nota(
    nota_id: uuid.UUID,
    nuevo_tema_id: uuid.UUID = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    """Mueve la nota y dispara los triggers de actualización total"""
    await init_rls(session, str(user.id))
    
    nota = await session.get(Anotacion, nota_id)
    if not nota:
        raise HTTPException(status_code=404)

    # Actualizar destino
    nota.tema_id = nuevo_tema_id
    session.add(nota)
    await session.commit()
    
    # RESPUESTA AXIOMÁTICA: Triple Trigger para actualización en línea
    response = Response(status_code=204)
    # 1. Actualiza contador | 2. Limpia lista inbox | 3. Refresca sidebar de cuaderno (si está abierta)
    response.headers["HX-Trigger"] = "update-inbox-count, update-inbox-list, refresh-notebook-sidebar"
    return response

@router.delete("/inbox/eliminar/{nota_id}")
async def eliminar_nota(
    nota_id: uuid.UUID,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    nota = await session.get(Anotacion, nota_id)
    
    if nota:
        await session.delete(nota)
        await session.commit()
    
    # Respuesta 204 (Sin contenido) pero con Triggers para refrescar AMBAS sidebars
    # así funciona sea cual sea la vista donde estés.
    response = Response(status_code=204)
    response.headers["HX-Trigger"] = "update-inbox-count, update-inbox-list, refresh-notebook-sidebar"
    return response

# --- VISTA DE NAVEGACIÓN DENTRO DE UN CUADERNO (ZONA 2) ---
@router.get("/partial/sidebar/notebook/{notebook_id}", response_class=HTMLResponse)
async def get_sidebar_notebook(
    notebook_id: uuid.UUID,
    request: Request,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    # 1. Seguridad RLS
    await init_rls(session, str(user.id))
    
    # 2. Obtener el cuaderno con sus temas y la categoría a la que pertenece
    # Usamos selectinload para cargar los temas y las notas de forma eficiente
    stmt = (
        select(Cuaderno)
        .where(Cuaderno.id == notebook_id, Cuaderno.user_id == user.id)
        .options(
            selectinload(Cuaderno.categoria),
            selectinload(Cuaderno.temas).selectinload(Tema.anotaciones)
        )
    )
    result = await session.exec(stmt)
    cuaderno = result.first()

    if not cuaderno:
        return PlainTextResponse("Cuaderno no encontrado", status_code=404)

    # 3. Renderizar el nuevo partial que crearemos en el siguiente paso
    return templates.TemplateResponse("modules/sidebar_notebook.html", {
        "request": request,
        "cuaderno": cuaderno,
        "categoria": cuaderno.categoria
    })

@router.get("/api/notes/{note_id}")
async def get_note_data(
    note_id: uuid.UUID,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    # Seguridad RLS Obligatoria
    await init_rls(session, str(user.id))
    
    # Buscamos la nota con sus relaciones para el Inspector (Zona 4)
    stmt = (
        select(Anotacion)
        .where(Anotacion.id == note_id, Anotacion.user_id == user.id)
        .options(
            selectinload(Anotacion.tema).selectinload(Tema.cuaderno),
            selectinload(Anotacion.adjuntos)
        )
    )
    result = await session.exec(stmt)
    nota = result.first()

    if not nota:
        return Response(status_code=404)

    # Devolvemos un objeto JSON completo para que el JS lo procese
    return {
        "id": str(nota.id),
        "titulo": nota.titulo,
        "contenido": nota.contenido, # Aquí vendrá el HTML o JSON de TipTap
        "tags": nota.tags,
        "tema_nombre": nota.tema.nombre,
        "cuaderno_nombre": nota.tema.cuaderno.nombre,
        "adjuntos": [
            {"id": str(a.id), "nombre": a.nombre_original, "url": a.url, "tipo": a.tipo_archivo} 
            for a in nota.adjuntos
        ]
    }

@router.get("/note/{note_id}", response_class=HTMLResponse)
async def note_view(
    note_id: uuid.UUID,
    request: Request,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    # 1. RLS Obligatorio
    await init_rls(session, str(user.id))

    # 2. Cargar los datos básicos para la Sidebar (Igual que en /dashboard)
    stmt_cat = (
        select(Categoria)
        .where(Categoria.user_id == user.id)
        .order_by(Categoria.orden)
        .options(selectinload(Categoria.cuadernos))
    )
    categorias = (await session.exec(stmt_cat)).all()

    # 3. Cargar la nota específica para el "Escenario"
    stmt_nota = (
        select(Anotacion)
        .where(Anotacion.id == note_id, Anotacion.user_id == user.id)
        .options(
            selectinload(Anotacion.tema).selectinload(Tema.cuaderno)
        )
    )
    result_nota = await session.exec(stmt_nota)
    nota_activa = result_nota.first()

    if not nota_activa:
        # Si la nota no existe, redirigimos al dashboard
        return RedirectResponse(url="/dashboard")

    # 4. Renderizar base.html con el contexto de la nota
    return templates.TemplateResponse("layouts/base.html", {
        "request": request,
        "user": user,
        "view_mode": "notebook", # Forzamos modo notebook
        "categorias": categorias,
        "active_note": nota_activa, # Pasamos el objeto nota
        "active_note_id": str(nota_activa.id),
        "today": date.today()
    })

@router.post("/api/upload/image")
async def upload_editor_image(
    file: UploadFile = File(...),
    user: UsuarioDB = Depends(get_authenticated_user)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo no es una imagen")
    
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase no configurado")

    # Generar nombre único basado en el usuario (orden tipo Legacy)
    ext = mimetypes.guess_extension(file.content_type) or ".png"
    filename = f"inline_{user.id}/{uuid.uuid4().hex}{ext}"
    
    try:
        content = await file.read()
        # Subir al bucket configurado en el Legacy
        supabase.storage.from_("docs_assets").upload(
            path=filename,
            file=content,
            file_options={"content-type": file.content_type}
        )
        
        # Obtener la URL pública para el editor
        response = supabase.storage.from_("docs_assets").get_public_url(filename)
        return {"url": response}
        
    except Exception as e:
        print(f"Error subiendo a Supabase: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al subir la imagen")
    

# Clase para recibir actualizaciones parciales
class NoteUpdate(BaseModel):
    titulo: str | None = None
    contenido: str | None = None

@router.patch("/api/notes/{note_id}")
async def patch_note(
    note_id: uuid.UUID,
    note_data: NoteUpdate,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    # 1. Convertimos el modelo a un diccionario, ignorando los valores que no se enviaron
    update_values = note_data.dict(exclude_unset=True)
    
    if not update_values:
        return {"status": "no updates provided"}

    # 2. Ejecutamos una actualización quirúrgica en la DB
    # Esto solo toca las columnas titulo/contenido y no afecta a los adjuntos
    stmt = (
        update(Anotacion)
        .where(Anotacion.id == note_id, Anotacion.user_id == user.id)
        .values(**update_values)
    )
    
    await session.execute(stmt)
    await session.commit()
    
    return {"status": "success"}

@router.post("/api/notes/upload-attachment")
async def upload_attachment(
    request: Request,
    note_id: uuid.UUID = Form(...),
    file: UploadFile = File(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase no configurado")

    # 1. Subir a Supabase Storage
    ext = os.path.splitext(file.filename)[1]
    filename = f"att_{user.id}/{uuid.uuid4().hex}{ext}"
    content = await file.read()
    
    supabase.storage.from_("docs_assets").upload(
        path=filename,
        file=content,
        file_options={"content-type": file.content_type}
    )
    
    # 2. Obtener URL y guardar en DB
    public_url = supabase.storage.from_("docs_assets").get_public_url(filename)
    
    nuevo_adjunto = Adjunto(
        url=public_url,
        nombre_original=file.filename,
        tipo_archivo=file.content_type,
        anotacion_id=note_id,
        user_id=user.id
    )
    session.add(nuevo_adjunto)
    await session.commit()

    await init_rls(session, str(user.id))

    # 3. Recuperar todos los adjuntos de esta nota para devolver el partial actualizado
    stmt = select(Adjunto).where(Adjunto.anotacion_id == note_id)
    result = await session.exec(stmt)
    adjuntos = result.all()

    # Devolvemos el fragmento HTML (Partial)
    return templates.TemplateResponse("partials/attachments_list.html", {
        "request": request,
        "adjuntos": adjuntos
    })

# app/routers/dashboard.py

@router.delete("/api/notes/attachment/{attachment_id}")
async def delete_attachment(
    attachment_id: uuid.UUID,
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    # 1. Obtener el adjunto para saber a qué nota pertenece
    adjunto = await session.get(Adjunto, attachment_id)
    if not adjunto:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    note_id = adjunto.anotacion_id
    
    # 2. Borrar de la DB (Supabase Storage se podría borrar aquí también, 
    # pero por seguridad de momento solo quitamos la referencia)
    await session.delete(adjunto)
    await session.commit()
    
    await init_rls(session, str(user.id))

    # 3. Devolver la lista actualizada de la nota
    stmt = select(Adjunto).where(Adjunto.anotacion_id == note_id)
    result = await session.exec(stmt)
    adjuntos = result.all()
    
    return templates.TemplateResponse("partials/attachments_list.html", {
        "request": {}, # HTMX no necesita el request completo aquí
        "adjuntos": adjuntos
    })

# --- CREAR TEMA (MODAL) ---
@router.get("/partial/modal/nuevo-tema/{cuaderno_id}", response_class=HTMLResponse)
async def get_modal_nuevo_tema(cuaderno_id: uuid.UUID, request: Request):
    """Sirve el modal de creación de tema con el ID del cuaderno inyectado"""
    return templates.TemplateResponse("partials/modal_tema.html", {
        "request": request,
        "cuaderno_id": cuaderno_id
    })

@router.post("/api/temas/create")
async def create_tema(
    request: Request,
    cuaderno_id: uuid.UUID = Form(...),
    nombre: str = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    # 1. Obtener el orden máximo actual para poner el nuevo al final
    stmt_max = select(func.max(Tema.orden)).where(Tema.cuaderno_id == cuaderno_id)
    max_orden = (await session.exec(stmt_max)).first() or 0

    nuevo_tema = Tema(
        nombre=nombre,
        cuaderno_id=cuaderno_id,
        user_id=user.id,
        orden=max_orden + 1
    )
    session.add(nuevo_tema)
    await session.commit()

    # 2. Devolver la sidebar completa del cuaderno para refrescar la lista
    # Reutilizamos la lógica de la sidebar_notebook
    return await get_sidebar_notebook(cuaderno_id, request, user, session)

# --- CREAR NOTA (DENTRO DE UN TEMA) ---
@router.post("/api/notes/create")
async def create_note(
    request: Request,
    tema_id: uuid.UUID = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    
    # 1. Crear la nota lo más rápido posible
    nueva_nota = Anotacion(
        titulo="Sin título",
        contenido='{"type":"doc","content":[{"type":"paragraph"}]}',
        tema_id=tema_id,
        user_id=user.id
    )
    session.add(nueva_nota)
    await session.commit()
    
    # IMPORTANTE: Re-inyectar RLS inmediatamente para la siguiente consulta
    await init_rls(session, str(user.id))
    
    # 2. Solo necesitamos saber a qué cuaderno pertenece para refrescar la sidebar
    res = await session.execute(select(Tema.cuaderno_id).where(Tema.id == tema_id))
    cuaderno_id = res.scalar()

    # 3. Respuesta con refresco de Sidebar
    response = await get_sidebar_notebook(cuaderno_id, request, user, session)
    
    nota_id_str = str(nueva_nota.id)
    response.headers["HX-Trigger"] = f'{{"note-selected": {{"id": "{nota_id_str}"}} }}'
    return response

# --- GESTIÓN DE CATEGORÍAS (MODALES) ---

@router.get("/partial/modal/nueva-categoria", response_class=HTMLResponse)
async def get_modal_nueva_categoria(request: Request):
    """Retorna el modal para crear una nueva biblioteca/categoría"""
    return templates.TemplateResponse("partials/modal_categoria.html", {
        "request": request
    })

@router.post("/api/categorias/create")
async def create_categoria(
    request: Request,
    nombre: str = Form(...),
    icono: str = Form("folder"),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    """Crea una categoría y refresca la sidebar del dashboard"""
    await init_rls(session, str(user.id))
    
    # Obtener el orden máximo para ponerla al final
    stmt_max = select(func.max(Categoria.orden)).where(Categoria.user_id == user.id)
    max_orden = (await session.exec(stmt_max)).first() or 0

    nueva_cat = Categoria(
        nombre=nombre,
        icono=icono,
        user_id=user.id,
        orden=max_orden + 1
    )
    session.add(nueva_cat)
    await session.commit()

    # Refrescar la sidebar del dashboard para mostrar la nueva categoría
    return await get_sidebar_dashboard(request, user, session)

# --- EDICIÓN Y BORRADO DE CATEGORÍAS ---

@router.get("/partial/modal/edit-categoria/{cat_id}", response_class=HTMLResponse)
async def get_modal_edit_categoria(cat_id: uuid.UUID, request: Request, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db)):
    await init_rls(session, str(user.id))
    categoria = await session.get(Categoria, cat_id)
    return templates.TemplateResponse("partials/modal_edit_categoria.html", {
        "request": request,
        "categoria": categoria
    })

@router.patch("/api/categorias/{cat_id}")
async def patch_categoria(
    cat_id: uuid.UUID,
    nombre: str = Form(...),
    icono: str = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db),
    request: Request = None
):
    await init_rls(session, str(user.id))
    categoria = await session.get(Categoria, cat_id)
    if categoria:
        categoria.nombre = nombre
        categoria.icono = icono
        session.add(categoria)
        await session.commit()
    return await get_sidebar_dashboard(request, user, session)

@router.delete("/api/categorias/{cat_id}")
async def delete_categoria(cat_id: uuid.UUID, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db), request: Request = None):
    await init_rls(session, str(user.id))
    categoria = await session.get(Categoria, cat_id)
    if categoria:
        await session.delete(categoria)
        await session.commit()
    return await get_sidebar_dashboard(request, user, session)

# --- MODALES DE SEGURIDAD (DANGER ZONE) ---

@router.get("/partial/modal/confirm-delete-categoria/{cat_id}", response_class=HTMLResponse)
async def get_modal_confirm_delete_categoria(cat_id: uuid.UUID, request: Request, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db)):
    await init_rls(session, str(user.id))
    categoria = await session.get(Categoria, cat_id)
    return templates.TemplateResponse("partials/modal_confirm_delete.html", {
        "request": request,
        "obj_id": cat_id,
        "obj_name": categoria.nombre,
        "type": "biblioteca",
        "warning": "Se eliminarán permanentemente todos los cuadernos, temas y notas dentro de esta biblioteca.",
        "delete_url": f"/api/categorias/{cat_id}"
    })

@router.get("/partial/modal/confirm-delete-cuaderno/{notebook_id}", response_class=HTMLResponse)
async def get_modal_confirm_delete_cuaderno(notebook_id: uuid.UUID, request: Request, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db)):
    await init_rls(session, str(user.id))
    cuaderno = await session.get(Cuaderno, notebook_id)
    return templates.TemplateResponse("partials/modal_confirm_delete.html", {
        "request": request,
        "obj_id": notebook_id,
        "obj_name": cuaderno.nombre,
        "type": "cuaderno",
        "warning": "Se eliminarán permanentemente todos los temas y notas dentro de este cuaderno.",
        "delete_url": f"/api/cuadernos/{notebook_id}" # El endpoint de borrado de cuaderno lo crearemos en la siguiente etapa
    })

# --- GESTIÓN DE CUADERNOS (NOTEBOOKS) ---

@router.get("/partial/modal/nuevo-cuaderno/{cat_id}", response_class=HTMLResponse)
async def get_modal_nuevo_cuaderno(cat_id: uuid.UUID, request: Request):
    return templates.TemplateResponse("partials/modal_cuaderno.html", {
        "request": request,
        "cat_id": cat_id
    })

@router.post("/api/cuadernos/create")
async def create_cuaderno(
    request: Request,
    nombre: str = Form(...),
    cat_id: uuid.UUID = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db)
):
    await init_rls(session, str(user.id))
    nuevo_nb = Cuaderno(nombre=nombre, categoria_id=cat_id, user_id=user.id, tipo="cuaderno")
    session.add(nuevo_nb)
    await session.commit()
    return await get_sidebar_dashboard(request, user, session)

@router.get("/partial/modal/edit-cuaderno/{nb_id}", response_class=HTMLResponse)
async def get_modal_edit_cuaderno(nb_id: uuid.UUID, request: Request, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db)):
    await init_rls(session, str(user.id))
    cuaderno = await session.get(Cuaderno, nb_id)
    return templates.TemplateResponse("partials/modal_edit_cuaderno.html", {
        "request": request,
        "cuaderno": cuaderno
    })

@router.patch("/api/cuadernos/{nb_id}")
async def patch_cuaderno(
    nb_id: uuid.UUID,
    nombre: str = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db),
    request: Request = None
):
    await init_rls(session, str(user.id))
    cuaderno = await session.get(Cuaderno, nb_id)
    if cuaderno:
        cuaderno.nombre = nombre
        session.add(cuaderno)
        await session.commit()
    return await get_sidebar_dashboard(request, user, session)

@router.delete("/api/cuadernos/{nb_id}")
async def delete_cuaderno(nb_id: uuid.UUID, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db), request: Request = None):
    await init_rls(session, str(user.id))
    cuaderno = await session.get(Cuaderno, nb_id)
    if cuaderno:
        await session.delete(cuaderno)
        await session.commit()
    return await get_sidebar_dashboard(request, user, session)

# --- GESTIÓN DE TEMAS (NOTEBOOK) ---

@router.get("/partial/modal/edit-tema/{tema_id}", response_class=HTMLResponse)
async def get_modal_edit_tema(tema_id: uuid.UUID, request: Request, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db)):
    await init_rls(session, str(user.id))
    tema = await session.get(Tema, tema_id)
    return templates.TemplateResponse("partials/modal_edit_tema.html", {
        "request": request,
        "tema": tema
    })

@router.patch("/api/temas/{tema_id}")
async def patch_tema(
    tema_id: uuid.UUID,
    nombre: str = Form(...),
    user: UsuarioDB = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db),
    request: Request = None
):
    await init_rls(session, str(user.id))
    tema = await session.get(Tema, tema_id)
    if tema:
        tema.nombre = nombre
        session.add(tema)
        await session.commit()
    return await get_sidebar_notebook(tema.cuaderno_id, request, user, session)

@router.get("/partial/modal/confirm-delete-tema/{tema_id}", response_class=HTMLResponse)
async def get_modal_confirm_delete_tema(tema_id: uuid.UUID, request: Request, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db)):
    await init_rls(session, str(user.id))
    
    # CORRECCIÓN: Carga explícita de anotaciones para evitar el error MissingGreenlet
    stmt = select(Tema).where(Tema.id == tema_id).options(selectinload(Tema.anotaciones))
    result = await session.exec(stmt)
    tema = result.first()
    
    if not tema:
        return Response(status_code=404)

    return templates.TemplateResponse("partials/modal_confirm_delete.html", {
        "request": request,
        "obj_id": tema_id,
        "obj_name": tema.nombre,
        "type": "tema",
        "warning": f"Se eliminarán permanentemente todas las notas ({len(tema.anotaciones)}) dentro de este tema.",
        "delete_url": f"/api/temas/{tema_id}"
    })

@router.delete("/api/temas/{tema_id}")
async def delete_tema(tema_id: uuid.UUID, user: UsuarioDB = Depends(get_authenticated_user), session: AsyncSession = Depends(get_db), request: Request = None):
    await init_rls(session, str(user.id))
    tema = await session.get(Tema, tema_id)
    cuaderno_id = tema.cuaderno_id
    if tema:
        await session.delete(tema)
        await session.commit()
    return await get_sidebar_notebook(cuaderno_id, request, user, session)

@router.get("/partial/modal/confirm-edit/{nota_id}", response_class=HTMLResponse)
async def get_modal_confirm_edit(nota_id: uuid.UUID, request: Request):
    return templates.TemplateResponse("partials/modal_confirm_edit.html", {
        "request": request,
        "nota_id": nota_id
    })

@router.get("/partial/modal/eliminar-nota/{nota_id}", response_class=HTMLResponse)
async def get_modal_eliminar_nota(nota_id: uuid.UUID, request: Request, session: AsyncSession = Depends(get_db), user: UsuarioDB = Depends(get_authenticated_user)):
    await init_rls(session, str(user.id))
    nota = await session.get(Anotacion, nota_id)
    return templates.TemplateResponse("partials/modal_eliminar_nota.html", {
        "request": request,
        "nota": nota
    })
```

---

## 📄 Archivo: `docker-compose.yml`
```yml
version: '3.8'

services:
  web:
    build: .
    container_name: aiflux-docs-app
    restart: always
    ports:
      - "5005:8000"
    env_file:
      - .env
    volumes:
      - ./static:/app/static
      # No mapeamos el código completo en prod para mayor seguridad, 
      # pero sí static si necesitas persistencia de archivos subidos localmente.
```

---

## 📄 Archivo: `requirements.txt`
```txt
fastapi
uvicorn[standard]
pydantic
pydantic-settings
sqlmodel
asyncpg
python-dotenv
python-jose[cryptography]
bcrypt
python-multipart
jinja2
supabase


```

---

## 📄 Archivo: `static/css/styles.css`
```css
:root {
    /* Variables de Ancho Iniciales (Se sobreescriben con JS) */
    --w-sidebar: 260px;
    --w-list: 320px;
}

/* El Grid Maestro */
.app-grid {
    display: grid;
    /* Col 1: Sidebar | Col 2: Resizer A | Col 3: Lista | Col 4: Resizer B | Col 5: Main */
    grid-template-columns: var(--w-sidebar) 4px var(--w-list) 4px minmax(0, 1fr);
    height: 100vh;
    width: 100vw;
    overflow: hidden;
}

/* Resizers (Tiradores) */
.resizer {
    background-color: transparent;
    cursor: col-resize;
    transition: background-color 0.2s;
    z-index: 50;
    height: 100%;
}

.resizer:hover, .resizer.active {
    background-color: #3b82f6; /* Tailwind blue-500 */
}

/* Scrollbars sutiles para modo oscuro */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #555; }

/* Desplazamiento suave para toda la aplicación */
html {
    scroll-behavior: smooth;
}

/* Ajuste para que el título no quede pegado al borde superior al saltar */
.prose h1, .prose h2, .prose h3 {
    scroll-margin-top: 80px; /* Esto deja espacio para que no lo tape la toolbar */
}
```

---

## 📄 Archivo: `static/js/app.js`
```js
document.addEventListener('alpine:init', () => {
    Alpine.data('layout', () => ({
        sidebarWidth: localStorage.getItem('sidebarWidth') || 260,
        listWidth: localStorage.getItem('listWidth') || 320,
        isResizing: false,

        init() {
            // Aplicar anchos guardados al iniciar
            this.updateCSS();
        },

        startResize(event, panel) {
            event.preventDefault();
            this.isResizing = true;
            const startX = event.clientX;
            const startWidth = parseInt(panel === 'sidebar' ? this.sidebarWidth : this.listWidth);

            const doDrag = (e) => {
                const delta = e.clientX - startX;
                let newWidth = startWidth + delta;

                // Límites (Min/Max)
                if (newWidth < 150) newWidth = 150;
                if (newWidth > 600) newWidth = 600;

                if (panel === 'sidebar') this.sidebarWidth = newWidth;
                else this.listWidth = newWidth;

                this.updateCSS();
            };

            const stopDrag = () => {
                this.isResizing = false;
                // Guardar preferencia
                localStorage.setItem('sidebarWidth', this.sidebarWidth);
                localStorage.setItem('listWidth', this.listWidth);
                
                document.removeEventListener('mousemove', doDrag);
                document.removeEventListener('mouseup', stopDrag);
                document.body.style.cursor = '';
            };

            document.addEventListener('mousemove', doDrag);
            document.addEventListener('mouseup', stopDrag);
            document.body.style.cursor = 'col-resize';
        },

        updateCSS() {
            document.documentElement.style.setProperty('--w-sidebar', `${this.sidebarWidth}px`);
            document.documentElement.style.setProperty('--w-list', `${this.listWidth}px`);
        }
    }));
});
```

---

## 📄 Archivo: `static/js/editor.js`
```js
/**
 * EDITOR.JS - REFACTORIZACIÓN ESTRUCTURAL (Preservación íntegra de lógica)
 * Responsabilidades segmentadas: Configuración, Persistencia, Assets, UI/Inspector y Eventos.
 */

import { Editor } from 'https://esm.sh/@tiptap/core';
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
```

---

## 📄 Archivo: `templates/layouts/base.html`
```html
<!-- templates/layouts/base.html -->
<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Docs.ai | Knowledge OS</title>

    <!-- 1. Alpine.js Core (CARGA PRIMERO) -->
    <script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    
    <!-- 2. HTMX (CARGA DESPUÉS de Alpine, con defer) -->
    <script defer src="https://unpkg.com/htmx.org@1.9.10"></script>
    
    <!-- 3. Otros recursos -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono&display=swap" rel="stylesheet">

<script>
        function appShell() {
            return {
                // Estados de Vista
                mode: '{{ view_mode }}',
                aiLoading: false, 
                zenMode: false,
                modalOpen: false,
                editorTick: 0,
                
                // Estados de Navegación
                activeCuadernoId: null,   
                activeCategoriaId: null, 
                activeNoteId: '{{ active_note_id or "" }}',

                // Quick View Flotante
                floatingNotes: {}, 
                draggingNoteId: null,
                dragOffset: { x: 0, y: 0 },
                activeGearMenu: null,
                gearMenuCoords: { x: 0, y: 0 },

                // Zona 2 y 4 (Dimensiones)
                sidebarWidth: localStorage.getItem('sidebarWidth') || 256,
                isResizingSidebar: false,
                inspectorWidth: localStorage.getItem('inspectorWidth') || 300,
                isResizingInspector: false,

                openCategories: JSON.parse(localStorage.getItem('docs_open_categories')) || [],
                sidebarScrollTop: parseInt(localStorage.getItem('docs_sidebar_scroll')) || 0,
                openThemes: JSON.parse(localStorage.getItem('docs_open_themes')) || [],
                notebookScrollTop: parseInt(localStorage.getItem('docs_notebook_scroll')) || 0,

                init() {
                    document.addEventListener('update-inbox-list', () => { this.modalOpen = false; });
                    window.addEventListener('mousemove', (e) => { this.handleMouseMove(e); });
                    window.addEventListener('mouseup', () => { this.stopAllResizing(); });

                    if (this.activeNoteId && this.activeNoteId !== "") {
                        setTimeout(() => {
                            window.dispatchEvent(new CustomEvent('note-selected', { detail: { id: this.activeNoteId } }));
                        }, 300);
                    }
                },

                // AXIOMA I.II: PROTOCOLO DE LIMPIEZA ATÓMICA
                openModal(url) {
                    const target = document.getElementById('main-portal-target');
                    if (!target) return;
                    target.innerHTML = ''; // Elimina fantasmas visuales
                    this.modalOpen = true;
                    htmx.ajax('GET', url, { target: '#main-portal-target', swap: 'innerHTML' });
                },

                toggleTheme(id) {
                    if (this.openThemes.includes(id)) {
                        this.openThemes = this.openThemes.filter(i => i !== id);
                    } else {
                        this.openThemes.push(id);
                    }
                    localStorage.setItem('docs_open_themes', JSON.stringify(this.openThemes));
                },

                checkInitialTheme(id, isFirst) {
                    if (this.openThemes.length === 0 && isFirst) { this.openThemes.push(id); }
                },

                toggleCategory(id) {
                    if (this.openCategories.includes(id)) {
                        this.openCategories = this.openCategories.filter(i => i !== id);
                    } else {
                        this.openCategories.push(id);
                    }
                    localStorage.setItem('docs_open_categories', JSON.stringify(this.openCategories));
                },

                handleMouseMove(e) {
                    if (this.isResizingSidebar) {
                        let newWidth = e.clientX - 64;
                        if (newWidth > 200 && newWidth < 600) this.sidebarWidth = newWidth;
                    }
                    if (this.isResizingInspector) {
                        let newWidth = window.innerWidth - e.clientX;
                        if (newWidth > 200 && newWidth < 500) this.inspectorWidth = newWidth;
                    }
                },

                stopAllResizing() {
                    if (this.isResizingSidebar || this.isResizingInspector) {
                        this.isResizingSidebar = false;
                        this.isResizingInspector = false;
                        document.body.classList.remove('select-none', 'cursor-col-resize');
                        localStorage.setItem('sidebarWidth', this.sidebarWidth);
                        localStorage.setItem('inspectorWidth', this.inspectorWidth);
                    }
                },

                startResizeSidebar() { this.isResizingSidebar = true; document.body.classList.add('select-none', 'cursor-col-resize'); },
                startResizeInspector() { this.isResizingInspector = true; document.body.classList.add('select-none', 'cursor-col-resize'); },

                get modeDisplay() { return this.mode === 'dashboard' ? 'Inicio' : 'Editor'; },
                get leftPanelTitle() { return this.mode === 'dashboard' ? 'Biblioteca' : 'Contenido'; },

                openGearMenu(event, notaId) {
                    event.stopPropagation();
                    const btn = event.currentTarget;
                    const rect = btn.getBoundingClientRect();
                    if (this.activeGearMenu === notaId) { this.activeGearMenu = null; return; }
                    this.activeGearMenu = notaId;
                    const menuHeight = 220;
                    const spaceBelow = window.innerHeight - rect.bottom;
                    this.gearMenuCoords.x = rect.left - 160;
                    this.gearMenuCoords.y = (spaceBelow < menuHeight) ? rect.top - menuHeight + 40 : rect.bottom + 8;
                    setTimeout(() => { document.addEventListener('click', (e) => {
                        const portal = document.getElementById('global-gear-menu-portal');
                        if (portal && !portal.contains(e.target)) this.activeGearMenu = null;
                    }, { once: true }); }, 0);
                },

                // Dentro de appShell() en base.html

                renderTiptapToStaticHtml(jsonStr) {
                    if (!jsonStr) return "<p class='text-slate-500 italic'>Sin contenido</p>";
                    
                    try {
                        const data = (typeof jsonStr === 'string') ? JSON.parse(jsonStr) : jsonStr;
                        
                        const parseNode = (node) => {
                            // 1. Manejo de Texto y Formatos (Marks)
                            if (node.type === 'text') {
                                let text = node.text || "";
                                if (node.marks) {
                                    node.marks.forEach(mark => {
                                        if (mark.type === 'bold') text = `<strong class="text-white font-bold">${text}</strong>`;
                                        if (mark.type === 'italic') text = `<em class="italic text-slate-200">${text}</em>`;
                                        if (mark.type === 'underline') text = `<u class="underline decoration-indigo-500/50">${text}</u>`;
                                        if (mark.type === 'code') text = `<code class="bg-slate-800 px-1 rounded text-indigo-300 text-[10px] font-mono">${text}</code>`;
                                        if (mark.type === 'highlight') text = `<mark class="bg-indigo-500/40 text-indigo-200 px-0.5 rounded">${text}</mark>`;
                                        if (mark.type === 'textStyle' && mark.attrs?.color) text = `<span style="color: ${mark.attrs.color}">${text}</span>`;
                                    });
                                }
                                return text;
                            }

                            // 2. Procesar hijos recursivamente
                            const content = node.content ? node.content.map(parseNode).join("") : "";

                            // 3. Mapeo de Nodos con Clases de Tailwind (Preflight Bypass)
                            switch (node.type) {
                                case 'doc': 
                                    return content;
                                case 'paragraph': 
                                    return `<p class="mb-4 text-slate-300 leading-relaxed">${content}</p>`;
                                case 'heading':
                                    const level = node.attrs?.level || 1;
                                    const sizes = { 1: 'text-2xl', 2: 'text-xl', 3: 'text-lg' };
                                    const sizeClass = sizes[level] || 'text-md';
                                    return `<h${level} class="${sizeClass} font-bold text-white mt-6 mb-3 border-b border-white/5 pb-1">${content}</h${level}>`;
                                case 'bulletList': 
                                    return `<ul class="list-disc ml-6 mb-4 space-y-2 text-slate-300">${content}</ul>`;
                                case 'orderedList': 
                                    return `<ol class="list-decimal ml-6 mb-4 space-y-2 text-slate-300">${content}</ol>`;
                                case 'listItem': 
                                    return `<li class="pl-1">${content}</li>`;
                                case 'blockquote': 
                                    return `<blockquote class="border-l-4 border-indigo-500/50 pl-4 italic text-slate-400 my-6 bg-white/5 py-2 pr-2 rounded-r-lg">${content}</blockquote>`;
                                case 'codeBlock': 
                                    return `<pre class="bg-[#0d0e12] p-4 rounded-xl border border-white/10 font-mono text-[11px] my-5 overflow-x-auto text-emerald-400 shadow-inner"><code>${content}</code></pre>`;
                                case 'horizontalRule': 
                                    return `<hr class="border-white/10 my-8">`;
                                case 'hardBreak': 
                                    return `<br>`;
                                default: 
                                    return content;
                            }
                        };

                        return parseNode(data);
                    } catch (e) {
                        console.error("Error QuickView Render:", e);
                        return "<p class='text-red-400'>Error al procesar el formato de la nota</p>";
                    }
                },

                openQuickView(notaId) {
                    if (this.floatingNotes[notaId]) { 
                        this.floatingNotes[notaId].zIndex = this.getMaxZIndex() + 1; 
                        this.activeGearMenu = null; 
                        return; 
                    }
                    
                    fetch(`/api/notes/${notaId}`).then(r => r.json()).then(nota => {
                        const x = Math.random() * (window.innerWidth - 400) * 0.8;
                        const y = Math.random() * (window.innerHeight - 300) * 0.6 + 50;
                        
                        // Ejecutamos el renderizador de formato rico
                        const htmlRico = this.renderTiptapToStaticHtml(nota.contenido);
                        
                        this.floatingNotes[notaId] = {
                            id: notaId, 
                            titulo: nota.titulo || 'Sin título',
                            contenidoHtml: htmlRico, // <--- ESTE NOMBRE DEBE COINCIDIR CON EL x-html
                            x, y, width: 420, height: 500, zIndex: this.getMaxZIndex() + 1
                        };
                        this.activeGearMenu = null;
                    });
                },


                closeFloatingNote(notaId) { delete this.floatingNotes[notaId]; },
                startDragFloatingNote(event, notaId) {
                    const noteData = this.floatingNotes[notaId];
                    if (!noteData) return;
                    this.draggingNoteId = notaId;
                    this.dragOffset = { x: event.clientX - noteData.x, y: event.clientY - noteData.y };
                    noteData.zIndex = this.getMaxZIndex() + 1;
                    const onDrag = (e) => {
                        if (!this.draggingNoteId) return;
                        const n = this.floatingNotes[this.draggingNoteId];
                        n.x = e.clientX - this.dragOffset.x; n.y = e.clientY - this.dragOffset.y;
                    };
                    const stopDrag = () => {
                        this.draggingNoteId = null;
                        document.removeEventListener('mousemove', onDrag);
                        document.removeEventListener('mouseup', stopDrag);
                    };
                    document.addEventListener('mousemove', onDrag);
                    document.addEventListener('mouseup', stopDrag);
                },

                startResizeFloatingNote(event, notaId) {
                    event.stopPropagation();
                    const noteData = this.floatingNotes[notaId];
                    const startX = event.clientX, startY = event.clientY;
                    const startW = noteData.width, startH = noteData.height;
                    const onResize = (e) => {
                        noteData.width = Math.max(300, startW + (e.clientX - startX));
                        noteData.height = Math.max(200, startH + (e.clientY - startY));
                    };
                    const stopResize = () => { document.removeEventListener('mousemove', onResize); document.removeEventListener('mouseup', stopResize); };
                    document.addEventListener('mousemove', onResize);
                    document.addEventListener('mouseup', stopResize);
                },

                getMaxZIndex() { return Math.max(0, ...Object.values(this.floatingNotes).map(n => n.zIndex || 0)); },

                confirmDeleteInboxNota(notaId) {
                    if (confirm('¿Eliminar esta nota?')) {
                        htmx.ajax('DELETE', `/inbox/eliminar/${notaId}`, {
                            handler: () => {
                                document.body.dispatchEvent(new CustomEvent('update-inbox-list'));
                                document.body.dispatchEvent(new CustomEvent('update-inbox-count'));
                                document.body.dispatchEvent(new CustomEvent('refresh-notebook-sidebar'));
                                if (this.floatingNotes[notaId]) this.closeFloatingNote(notaId);
                                if (this.activeNoteId === notaId) { this.activeNoteId = null; this.mode = 'dashboard'; }
                            }
                        });
                    }
                    this.activeGearMenu = null;
                },

                switchActiveNote(newNoteId) {
                    if (this.activeNoteId === newNoteId) { this.mode = 'notebook'; return; }
                    this.openModal(`/partial/modal/confirm-edit/${newNoteId}`);
                },

                loadNoteFromQuickView(newNoteId) {
                    this.activeNoteId = newNoteId;
                    this.mode = 'notebook';
                    window.dispatchEvent(new CustomEvent('note-selected', { detail: { id: newNoteId } }));
                }
            }
        }
    </script>

    <style>
        /* 1. FUENTES: Fusionamos Inter, Mono y Merriweather */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono&family=Merriweather:ital,wght@0,300;0,400;0,700;1,300;1,400&display=swap');
        
        body { font-family: 'Inter', sans-serif; }
        .font-mono { font-family: 'JetBrains Mono', monospace; }

        #main-canvas {
            scroll-behavior: smooth;
        }

        /* 2. EL PAPEL: Tipografía Serif para el cuerpo de la nota */
        #tiptap-content { 
            font-family: 'Merriweather', serif; 
            font-weight: 400;
            color: #cbd5e1;
        }

        /* 3. ESTRUCTURA BASE (Preservada) */
        .glass-panel { background: #13151b; border-right: 1px solid rgba(255, 255, 255, 0.05); }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        [x-cloak] { display: none !important; }
        
        /* 4. HTMX TRANSITIONS & INDICATORS (Preservado y Sagrado) */
        .htmx-added { opacity: 0; transform: translateY(10px); }
        .htmx-settling { opacity: 1; transform: translateY(0); transition: all 0.3s ease-out; }

        .htmx-indicator { 
                    opacity: 0; 
                    display: none; 
                    pointer-events: none; 
                    transition: opacity 0.2s ease-in-out;
                }
                .htmx-request .htmx-indicator, .htmx-request.htmx-indicator { 
                    display: flex !important; 
                    opacity: 1; 
                    pointer-events: auto; 
                }

        /* 5. PUNTITOS IA (Preservado) */
        .typing-dot {
            width: 6px;
            height: 6px;
            background-color: #818cf8; /* Un índigo claro que resalta en el fondo oscuro */
            border-radius: 50%;
            display: inline-block;
            animation: typing 1.4s infinite ease-in-out both;
        }
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }

        @keyframes typing {
            0%, 80%, 100% { transform: scale(0); opacity: 0.3; }
            40% { transform: scale(1); opacity: 1; }
        }

        .ai-indicator-container {
            position: absolute; top: 1.5rem; left: 0; right: 0;
            display: flex; justify-content: center;
            pointer-events: none; z-index: 50;
        }

        /* 6. DISEÑO EDITORIAL (Prose) */
        .prose { color: #94a3b8; max-width: none; }
        .prose h1, .prose h2, .prose h3 { 
            font-family: 'Inter', sans-serif; 
            color: #e2e8f0; 
            font-weight: 700; 
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            scroll-margin-top: 100px;
        }
        .prose p { line-height: 1.8; margin-bottom: 1.25em; }
        .prose strong { color: #cbd5e1; font-weight: 600; }
        .prose ul { list-style-type: disc !important; padding-left: 1.5em !important; margin-bottom: 1em; }
        .prose ol { list-style-type: decimal !important; padding-left: 1.5em !important; margin-bottom: 1em; }
        .prose blockquote { 
            border-left: 3px solid #6366f1; 
            padding-left: 1.5em; 
            font-style: italic; 
            color: #94a3b8;
            margin: 1.5em 0;
        }
        .prose a { color: #818cf8; text-decoration: underline; cursor: pointer; }

        /* Forzar jerarquía visual de títulos en el editor */
        .prose h1 { font-size: 2.25rem !important; line-height: 2.5rem !important; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 0.5rem; }
        .prose h2 { font-size: 1.875rem !important; line-height: 2.25rem !important; }
        .prose h3 { font-size: 1.5rem !important; line-height: 2rem !important; }

        /* Estilo para el Bloque de Código (Zona 3) */
        .prose pre {
            background-color: #0d0e12 !important;
            padding: 0 !important; 
            margin: 2rem 0 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            overflow: visible !important; 
            position: relative;
        }

        .prose pre code {
            display: block;
            padding: 1.5rem !important;
            overflow-x: auto !important; 
            white-space: pre !important;  
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.85rem !important;
            line-height: 1.6 !important;
            color: #abb2bf; 
            display: block; 
        }

        /* Forzar visibilidad de herramientas al pasar el mouse sobre el bloque */
        pre:hover .code-tools {
            opacity: 1 !important;
            visibility: visible !important;
        }

        /* Estilo base para que no dependa solo de Tailwind */
        .code-tools {
            position: absolute !important;
            top: 12px !important;
            right: 12px !important;
            z-index: 50 !important;
            display: flex !important;
            gap: 8px !important;
            opacity: 0;
            visibility: hidden;
            transition: all 0.2s ease;
        }

        .code-tools button {
            background: rgba(30, 41, 59, 0.8) !important;
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #94a3b8 !important;
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 6px !important;
            cursor: pointer !important;
            transition: all 0.2s;
        }

        .code-tools button:hover {
            background: #6366f1 !important;
            color: white !important;
            border-color: #818cf8 !important;
        }

        /* --- COLORES DE SINTAXIS (One Dark Theme) --- */
        .hljs-keyword, .hljs-selector-tag { color: #c678dd; } 
        .hljs-string, .hljs-doctag { color: #98c379; }       
        .hljs-title, .hljs-section, .hljs-selector-id { color: #61afef; } 
        .hljs-variable, .hljs-template-variable { color: #d19a66; } 
        .hljs-comment, .hljs-quote { color: #5c6370; font-style: italic; } 
        .hljs-number, .hljs-literal { color: #d19a66; }
        .hljs-type, .hljs-built_in { color: #e5c07b; }
        .hljs-attr { color: #d19a66; }

        /* Diferenciar el código en línea */
        .prose :not(pre) > code {
            background-color: rgba(99, 102, 241, 0.1) !important;
            color: #818cf8 !important;
            padding: 0.2rem 0.4rem !important;
            border-radius: 0.4rem !important;
            font-size: 0.9em !important;
        }

        /* Ajustar el espacio entre párrafos */
        .prose p {
            margin-top: 0.5em !important;
            margin-bottom: 0.5em !important;
        }
        
        /* 7. UTILIDADES EXTRA */
        .resizer-hover:hover { background-color: rgba(99, 102, 241, 0.4); }

        /* Estilos de Scrollbar Personalizados */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #0f1117; }
        ::-webkit-scrollbar-thumb { background: #1e222e; border-radius: 10px; border: 1px solid #0f1117; }
        ::-webkit-scrollbar-thumb:hover { background: #312e81; }
        
        * { scrollbar-width: thin; scrollbar-color: #1e222e #0f1117; }

        /* 8. QUICK VIEW FLOTANTE */
        .floating-note-window {
            position: fixed;
            background: #1a1d26;
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 0.75rem;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), 
                        0 0 20px rgba(99, 102, 241, 0.2);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            transition: box-shadow 0.2s;
            pointer-events: auto;
        }

        .floating-note-window:hover {
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), 
                        0 0 30px rgba(99, 102, 241, 0.4);
        }

        .floating-note-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 1rem;
            background: rgba(99, 102, 241, 0.1);
            border-bottom: 1px solid rgba(99, 102, 241, 0.2);
            cursor: move;
            user-select: none;
            flex-shrink: 0;
        }

        .floating-note-title {
            font-size: 0.875rem;
            font-weight: 600;
            color: #e2e8f0;
            margin: 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            flex: 1;
        }

        .floating-note-header button {
            background: transparent;
            border: none;
            color: #94a3b8;
            cursor: pointer;
            padding: 0.25rem;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: color 0.2s;
            flex-shrink: 0;
        }

        .floating-note-header button:hover {
            color: #f87171;
        }

        .floating-note-content {
            flex: 1;
            padding: 1rem;
            overflow-y: auto;
            white-space: pre-wrap; /* Mantiene saltos de línea y ajusta el texto */
            font-size: 0.875rem;
            line-height: 1.6;
            color: #cbd5e1;
        }

        .floating-note-resizer {
            position: absolute;
            bottom: 0;
            right: 0;
            width: 20px;
            height: 20px;
            cursor: nwse-resize;
            background: linear-gradient(135deg, 
                        transparent 0%, 
                        transparent 50%, 
                        rgba(99, 102, 241, 0.3) 50%);
            flex-shrink: 0;
        }

        .floating-note-resizer:hover {
            background: linear-gradient(135deg, 
                        transparent 0%, 
                        transparent 50%, 
                        rgba(99, 102, 241, 0.6) 50%);
        }

        /* FOOTER DEL QUICK VIEW */
        .floating-note-footer {
            padding: 0.75rem 1rem;
            background: rgba(15, 23, 42, 0.5);
            border-top: 1px solid rgba(99, 102, 241, 0.2);
            display: flex;
            gap: 0.5rem;
            flex-shrink: 0;
        }

        .floating-note-edit-btn {
            flex: 1;
            padding: 0.5rem 0.75rem;
            background: rgba(99, 102, 241, 0.2);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: #a5b4fc;
            border-radius: 0.375rem;
            cursor: pointer;
            font-size: 0.75rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.25rem;
            transition: all 0.2s;
        }

        .floating-note-edit-btn:hover {
            background: rgba(99, 102, 241, 0.3);
            border-color: rgba(99, 102, 241, 0.5);
            color: #c7d2fe;
        }

        /* MENÚ CONTEXTUAL DEL ENGRANAJE */
        .gear-menu-container {
            position: relative;
            opacity: 1 !important; /* Forzamos que el contenedor del botón sea siempre opaco */
        }

        .gear-button {
            opacity: 0;
            transition: opacity 0.2s;
            cursor: pointer;
            background: transparent;
            border: none;
            color: #94a3b8;
            padding: 0.25rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Mostrar engranaje al pasar el mouse */
        .note-card:hover .gear-button {
            opacity: 1;
        }

        .gear-button:hover {
            color: #e2e8f0;
        }

        .gear-dropdown {
            position: absolute;
            top: 100%;
            right: 0;
            
            /* BLOQUEO DE TRANSPARENCIA: Usamos RGB para asegurar 0 canal alfa */
            background-color: rgb(26, 29, 38) !important; 
            background-image: none !important;
            opacity: 1 !important;
            
            /* FORZAR RENDERIZADO EN CAPA INDEPENDIENTE */
            transform: translateZ(0); 
            -webkit-transform: translateZ(0);
            
            /* ANULAR HERENCIA DE FILTROS */
            filter: none !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
            
            /* DISEÑO Y JERARQUÍA */
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 0.5rem;
            padding: 0.5rem;
            min-width: 190px;
            z-index: 99999 !important; /* Valor extremo */
            
            /* SOMBRA TOTALMENTE OPACA */
            box-shadow: 0 20px 50px rgba(0, 0, 0, 1) !important;
            pointer-events: auto;
        }

        /* --- PORTAL GLOBAL: Menú Contextual (position: fixed) --- */
        .gear-dropdown-portal {
            /* Estilos idénticos al gear-dropdown pero para position: fixed */
            background-color: rgb(26, 29, 38) !important;
            background-image: none !important;
            opacity: 1 !important;
            
            /* Renderizado GPU */
            transform: translateZ(0);
            -webkit-transform: translateZ(0);
            will-change: transform;
            
            /* NO HEREDA filtros del padre (eso es el punto) */
            filter: none !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
            
            /* Diseño */
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 0.5rem;
            padding: 0.5rem;
            min-width: 190px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 1);
            
            /* Asegurar que sea visible encima de todo */
            z-index: 9999;
            pointer-events: auto;
        }

        .gear-dropdown button, .gear-dropdown-btn {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            width: 100%;
            padding: 0.6rem 0.75rem;
            font-size: 0.875rem;
            color: #e2e8f0; /* Texto más claro para máxima legibilidad */
            background: transparent;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
            text-align: left;
        }

        .gear-dropdown button:hover, .gear-dropdown-btn:hover {
            background-color: rgba(99, 102, 241, 0.2) !important; /* Fondo índigo suave al pasar el mouse */
            color: #ffffff !important;
        }

        .gear-dropdown button:active, .gear-dropdown-btn:active {
            transform: scale(0.95);
        }

        /* --- ESTILOS PARA TABLAS EN EL EDITOR --- */

        /* 1. Contenedor general de la tabla */
        #tiptap-content table {
            border-collapse: collapse;
            table-layout: fixed;
            width: 100%;
            margin: 2rem 0;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* 2. Celdas (td) y Encabezados (th) */
        #tiptap-content table td,
        #tiptap-content table th {
            min-width: 1em;
            border: 1px solid #333; /* Borde visible en modo oscuro */
            padding: 10px 12px;
            vertical-align: top;
            box-sizing: border-box;
            position: relative;
            text-align: left;
        }

        /* 3. Estilo específico para encabezados */
        #tiptap-content table th {
            font-weight: bold;
            background-color: rgba(255, 255, 255, 0.05);
            color: #fff;
        }

        /* 4. Resaltado de celdas seleccionadas (Muy importante para gestión) */
        #tiptap-content table .selectedCell:after {
            z-index: 2;
            content: "";
            position: absolute;
            left: 0; right: 0; top: 0; bottom: 0;
            background: rgba(99, 102, 241, 0.15); /* Color índigo sutil */
            pointer-events: none;
        }

        /* 5. El tirador para cambiar el tamaño de columnas (resizable) */
        #tiptap-content table .column-resizer {
            position: absolute;
            right: -2px;
            top: 0;
            bottom: -2px;
            width: 4px;
            background-color: #6366f1;
            z-index: 20;
            cursor: col-resize;
        }

        /* 6. Mejorar la visualización de párrafos dentro de celdas */
        #tiptap-content table p {
            margin: 0 !important;
        }
        /* Efecto de desvanecimiento suave para cambios de HTMX */
        #contextual-sidebar {
            transition: all 0.3s ease;
        }

        /* Cuando HTMX está intercambiando contenido */
        .htmx-swapping #contextual-sidebar {
            opacity: 0;
            transform: scale(0.98);
        }

    </style>

    <script type="module" src="{{ url_for('static', path='/js/editor.js') }}"></script>
</head>

<!-- 2. CORRECCIÓN: x-data ahora llama a la función appShell() -->
<body class="bg-[#0f1117] text-slate-300 h-screen overflow-hidden flex selection:bg-indigo-500/30" 
      x-data="appShell()">

    <!-- Contenedor para Notas Flotantes (Quick View) -->
    <div id="floating-notes-container" class="fixed inset-0 pointer-events-none z-[1000]">
        <!-- Renderizar cada nota flotante dinámicamente -->
        <template x-for="(nota, notaId) in floatingNotes" :key="notaId">
            <div class="floating-note-window"
                 :style="{
                     left: nota.x + 'px',
                     top: nota.y + 'px',
                     width: nota.width + 'px',
                     height: nota.height + 'px',
                     zIndex: nota.zIndex
                 }">
                
                <!-- HEADER (Arrastra) -->
                <div class="floating-note-header" @mousedown="startDragFloatingNote($event, notaId)">
                    <h4 class="floating-note-title" x-text="nota.titulo || 'Sin título'"></h4>
                    <button @click.stop="closeFloatingNote(notaId)" type="button">
                        <i class="ph ph-x"></i>
                    </button>
                </div>
                
                <!-- CONTENIDO (Previsualización con texto extraído) -->
                <div class="floating-note-content select-text custom-scroll" 
                    @mousedown.stop 
                    x-html="nota.contenidoHtml || '<p class=\'text-slate-500 italic\'>Sin contenido</p>'"></div>
                
                <!-- BOTÓN EDITAR -->
                <div class="floating-note-footer">
                    <button @click="loadNoteFromQuickView(notaId); closeFloatingNote(notaId)" type="button" class="floating-note-edit-btn">
                        <i class="ph ph-pencil text-sm"></i> Editar
                    </button>
                </div>
                
                <!-- RESIZER (Esquina inferior derecha) -->
                <div class="floating-note-resizer"
                     @mousedown="startResizeFloatingNote($event, notaId)">
                </div>
            </div>
        </template>
    </div>

    <!-- Configuración de HTMX para compatible con Alpine + Editor Tiptap -->
    <script>
        document.addEventListener('htmx:beforeRequest', (event) => {
                // Si la petición va dirigida al contenido del modal, lo vaciamos inmediatamente
                if (event.detail.target.id === 'modal-content') {
                    event.detail.target.innerHTML = `
                        <div class="flex items-center justify-center p-12">
                            <div class="flex gap-1">
                                <span class="typing-dot"></span>
                                <span class="typing-dot"></span>
                                <span class="typing-dot"></span>
                            </div>
                        </div>
                    `;
                }
            });

        // Sincronizar HTMX con Alpine.js y forzar reactividad del editor
        document.addEventListener('htmx:afterSettle', (event) => {
            // 1. Procesar nuevos elementos con Alpine
            if (window.Alpine && typeof window.Alpine.process === 'function') {
                window.Alpine.process(event.detail.target);
                
                // 2. Forzar que Alpine reinitialice los bindings reactivos
                if (window.Alpine.flushAndStopDeferringMacros) {
                    window.Alpine.flushAndStopDeferringMacros();
                }
            }
            
            // 3. Reinicializar Phosphor Icons en los nuevos elementos
            if (window.phosphor && window.phosphor.replace) {
                window.phosphor.replace(event.detail.target);
            }
            
            // 4. Si el editor existe, forzar actualización de barra
            if (window.editor && typeof window.editor === 'function' && window.editor()) {
                const app = window.Alpine.$data(document.body);
                if (app) {
                    app.editorTick++;  // Fuerza re-evaluación de activeStyles()
                }
            }
        });
    </script>

    <!-- 1. NAVEGACIÓN DE LENTES -->
    <nav class="w-16 bg-[#0B0C10] border-r border-white/5 flex flex-col items-center py-6 z-50 shrink-0">
        <a href="/" class="mb-8 text-indigo-500 text-3xl hover:text-white transition-colors cursor-pointer">
            <i class="ph-fill ph-brain"></i>
        </a>
        
        <div class="flex flex-col gap-4 w-full px-2">
            <button @click="mode = 'dashboard'; resetSidebarToDefault('{{ categorias[0].id if categorias else '' }}')" 
                    :class="mode === 'dashboard' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25' : 'text-slate-500 hover:text-indigo-400 hover:bg-white/5'" 
                    class="w-10 h-10 rounded-xl flex items-center justify-center transition-all group relative"
                    hx-get="/partial/sidebar/dashboard" 
                    hx-target="#contextual-sidebar"
                    hx-indicator="#sidebar-indicator"
                    hx-swap="innerHTML">
                <i class="ph-fill ph-squares-four text-xl"></i>
            </button>

            <button @click="mode = 'inbox'" 
                    :class="mode === 'inbox' ? 'bg-amber-600 text-white shadow-lg shadow-amber-500/25' : 'text-slate-500 hover:text-amber-400 hover:bg-white/5'" 
                    class="w-10 h-10 rounded-xl flex items-center justify-center transition-all group relative"
                    hx-get="/partial/sidebar/inbox" 
                    hx-target="#contextual-sidebar"
                    hx-indicator="#sidebar-indicator">
                <i class="ph-fill ph-tray text-xl"></i>
                <span id="inbox-badge"
                    class="absolute -top-1 -right-1 bg-amber-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full border border-[#0B0C10] min-w-[18px] text-center"
                    x-data="{ count: '0' }"
                    x-show="count !== '0' && count !== ''"
                    hx-get="/inbox/count" 
                    hx-trigger="load, update-inbox-count from:body"
                    hx-target="this"
                    @htmx:after-on-load="count = $event.detail.xhr.responseText.trim()">
                </span>
            </button>

            <button @click="mode = 'directory'"
                    :class="mode === 'directory' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25' : 'text-slate-500 hover:text-indigo-400 hover:bg-white/5'"
                    class="w-10 h-10 rounded-xl flex items-center justify-center transition-all group relative">
                <i class="ph-fill ph-folder-notch text-xl"></i>
            </button>
        </div>
    </nav>

    <!-- 2. BARRA LATERAL CONTEXTUAL -->
    <aside class="glass-panel flex flex-col shrink-0 transition-[margin,opacity] duration-300 relative"
           :style="`width: ${sidebarWidth}px; ${zenMode ? 'margin-left: -' + sidebarWidth + 'px; opacity: 0;' : ''}`">
        
        <div class="h-14 flex items-center px-5 border-b border-white/5 bg-[#13151b] shrink-0">
            <span class="text-xs font-bold tracking-widest text-slate-500 uppercase" x-text="leftPanelTitle"></span>
        </div>

        <!-- Contenedor con Indicador Fijo -->
        <div class="flex-1 overflow-hidden relative">
            <!-- Indicador de carga para la Sidebar -->
            <div id="sidebar-indicator" class="htmx-indicator absolute inset-0 bg-[#0f1117]/60 backdrop-blur-[1px] z-50 flex items-center justify-center">
                <div class="flex gap-1">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </div>
            </div>

            <!-- El target de HTMX ahora es solo el contenido scrollable -->
            <div id="contextual-sidebar" class="h-full overflow-y-auto custom-scroll p-3">
                {% if view_mode == 'dashboard' %}
                    {% include 'modules/sidebar_dashboard.html' %}
                {% else %}
                    {% include 'modules/sidebar_projects.html' %}
                {% endif %}
            </div>
        </div>

        <!-- EL RESIZER (Tirador) -->
        <div class="absolute top-0 right-0 w-1 h-full cursor-col-resize hover:bg-indigo-500/50 transition-colors z-50"
             @mousedown="startResizeSidebar()">
        </div>
    </aside>

    <!-- 3. ÁREA PRINCIPAL -->
    <main class="flex-1 flex flex-col relative bg-[#0f1117]">        <header class="h-14 flex items-center justify-between px-8 border-b border-white/5 bg-[#0f1117]/80 backdrop-blur-md z-10">
            <div class="flex items-center gap-2 text-sm text-slate-500">
                <i class="ph-bold ph-house text-xs"></i>
                <span x-text="modeDisplay"></span>
            </div>
            <div class="flex items-center gap-3">
                <!-- NUEVO: Indicador de autoguardado -->
                <span id="save-status" class="text-[10px] text-slate-500 font-medium italic transition-opacity duration-300"></span>
                
                <div class="flex items-center gap-1 text-[10px] bg-slate-800 px-2 py-1 rounded text-slate-400 border border-white/5">
                <button @click="zenMode = !zenMode" class="text-slate-500 hover:text-white p-1 rounded hover:bg-white/5">
                    <i :class="zenMode ? 'ph-fill ph-arrows-in-line-horizontal' : 'ph-fill ph-arrows-out-line-horizontal'"></i>
                </button>
            </div>
        </header>

        <!-- Contenedor de Contenido (Dashboard o Editor) -->
        <div id="main-canvas" class="flex-1 overflow-y-auto no-scrollbar relative">
            <!-- OVERLAY DE CARGA PARA EL EDITOR -->
            <div x-show="aiLoading" 
                x-transition:enter="transition opacity ease-out duration-200"
                x-transition:enter-start="opacity-0"
                x-transition:enter-end="opacity-100"
                x-transition:leave="transition opacity ease-in duration-200"
                x-transition:leave-start="opacity-100"
                x-transition:leave-end="opacity-0"
                class="absolute inset-0 bg-[#0f1117]/80 backdrop-blur-[2px] z-[60] flex flex-col items-center justify-center pointer-events-none">
                <div class="flex gap-1 mb-2">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </div>
                <span class="text-[10px] font-bold text-indigo-400 uppercase tracking-widest">Sincronizando...</span>
            </div>
            
            <!-- VISTA DASHBOARD -->
            <div x-show="mode === 'dashboard'" x-transition.opacity.duration.300ms>
                {% if view_mode == 'dashboard' %}
                    {% include 'modules/cockpit_pane.html' %}
                {% endif %}
            </div>

            <!-- VISTA EDITOR (El Escenario Permanente) -->
            <div x-show="mode !== 'dashboard'" class="h-full relative" x-cloak>
                
                <!-- Capa: Estado Vacío (Se muestra cuando NO hay nota seleccionada) -->
                <div x-show="!activeNoteId || activeNoteId === ''" 
                     class="absolute inset-0 flex flex-col items-center justify-center text-slate-600 bg-[#0f1117] z-20">
                    <i class="ph ph-note-blank text-6xl mb-4 opacity-20"></i>
                    <p class="text-sm font-medium tracking-wide">Selecciona una nota para comenzar</p>
                </div>

                <!-- Escenario de Escritura (Se muestra cuando SÍ hay nota seleccionada) -->
                <!-- Escenario de Escritura -->
                <div id="editor-stage" 
                     x-show="activeNoteId && activeNoteId !== ''"
                     class="h-full flex flex-col transition-all duration-500 overflow-y-auto"
                     :class="zenMode ? 'max-w-[72ch] mx-auto' : 'max-w-[900px] mx-auto'">
                    
                    <div class="flex-1 py-12 px-8 relative">
                        <!-- 1. Título -->
                        <textarea id="note-title-input"
                                  placeholder="Título de la nota..."
                                  class="w-full bg-transparent text-2xl font-bold text-white mb-6 border-none focus:ring-0 placeholder-slate-800 outline-none leading-tight resize-none overflow-hidden"
                                  rows="1"
                                  oninput="this.style.height = ''; this.style.height = this.scrollHeight + 'px'"></textarea>

                        <!-- 2. Barra de Herramientas con Reactividad -->
                        <div class="sticky top-0 z-40 -mx-4 px-4 py-2 bg-[#0f1117]/80 backdrop-blur-md border-b border-white/5 mb-8">
                        <!-- Reemplaza el bloque <div id="fixed-toolbar"> dentro de tu base.html -->
                        <div id="fixed-toolbar" 
                            class="mx-auto flex items-center gap-1 bg-[#1a1d26]/80 backdrop-blur-md border border-white/10 p-1 rounded-xl w-max shadow-xl"
                            x-data="{ 
                                menuStyle: false, 
                                menuColor: false, 
                                menuAlign: false, 
                                menuMore: false,
                                activeStyles() { return this.editorTick && typeof editor === 'function' && editor() }
                            }">

                            <!-- GRUPO 1: ESTILO (H1, H2, H3) -->
                            <div class="relative">
                                <button @click="menuStyle = !menuStyle" @click.away="menuStyle = false"
                                        class="flex items-center gap-2 px-3 py-1.5 text-[11px] font-bold text-slate-300 hover:bg-white/5 rounded-lg transition-all">
                                    <span x-text="activeStyles() && editor().isActive('heading', { level: 1 }) ? 'H1' : 
                                                activeStyles() && editor().isActive('heading', { level: 2 }) ? 'H2' : 
                                                activeStyles() && editor().isActive('heading', { level: 3 }) ? 'H3' : 'Texto'"></span>
                                    <i class="ph ph-caret-down text-[10px]"></i>
                                </button>
                                <div x-show="menuStyle" x-transition class="absolute top-full mt-2 left-0 w-32 bg-[#1a1d26] border border-white/10 rounded-xl shadow-2xl p-1 z-50">
                                    <button @click="editor().chain().focus().setParagraph().run(); menuStyle = false" class="w-full text-left px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg">Párrafo</button>
                                    <button @click="editor().chain().focus().toggleHeading({ level: 1 }).run(); menuStyle = false" class="w-full text-left px-3 py-2 text-[11px] font-bold hover:bg-white/5 rounded-lg">Título 1</button>
                                    <button @click="editor().chain().focus().toggleHeading({ level: 2 }).run(); menuStyle = false" class="w-full text-left px-3 py-2 text-[11px] font-bold hover:bg-white/5 rounded-lg">Título 2</button>
                                    <button @click="editor().chain().focus().toggleHeading({ level: 3 }).run(); menuStyle = false" class="w-full text-left px-3 py-2 text-[11px] font-bold hover:bg-white/5 rounded-lg">Título 3</button>
                                </div>
                            </div>

                            <div class="w-px h-4 bg-white/10 mx-1"></div>

                            <!-- GRUPO 2: BÁSICOS -->
                            <button @click="editor().chain().focus().toggleBold().run()"
                                    :class="activeStyles() && editor().isActive('bold') ? 'bg-indigo-500/20 text-indigo-400' : 'text-slate-400 hover:text-white hover:bg-white/5'"
                                    class="w-8 h-8 flex items-center justify-center rounded-lg transition-all">
                                <i class="ph-bold ph-text-b"></i>
                            </button>
                            <button @click="editor().chain().focus().toggleItalic().run()"
                                    :class="activeStyles() && editor().isActive('italic') ? 'bg-indigo-500/20 text-indigo-400' : 'text-slate-400 hover:text-white hover:bg-white/5'"
                                    class="w-8 h-8 flex items-center justify-center rounded-lg transition-all">
                                <i class="ph-bold ph-text-italic"></i>
                            </button>
                            <button @click="editor().chain().focus().toggleUnderline().run()"
                                    :class="activeStyles() && editor().isActive('underline') ? 'bg-indigo-500/20 text-indigo-400' : 'text-slate-400 hover:text-white hover:bg-white/5'"
                                    class="w-8 h-8 flex items-center justify-center rounded-lg transition-all">
                                <i class="ph-bold ph-text-underline"></i>
                            </button>
                            <button @click="const url = window.prompt('URL:'); if(url) editor().chain().focus().setLink({ href: url }).run()"
                                    :class="activeStyles() && editor().isActive('link') ? 'bg-indigo-500/20 text-indigo-400' : 'text-slate-400 hover:text-white hover:bg-white/5'"
                                    class="w-8 h-8 flex items-center justify-center rounded-lg transition-all">
                                <i class="ph-bold ph-link"></i>
                            </button>

                            <div class="w-px h-4 bg-white/10 mx-1"></div>

                            <!-- NUEVO GRUPO: ALINEACIÓN (Añadir antes del Grupo 3 de Color) -->
                            <div class="relative" x-data="{ menuAlign: false }">
                                <button @click="menuAlign = !menuAlign" @click.away="menuAlign = false"
                                        class="w-8 h-8 flex items-center justify-center rounded-lg text-slate-400 hover:text-white transition-all hover:bg-white/5">
                                    <i class="ph-bold ph-text-align-left"></i>
                                </button>
                                <div x-show="menuAlign" x-transition class="absolute top-full mt-2 left-1/2 -translate-x-1/2 w-36 bg-[#1a1d26] border border-white/10 rounded-xl shadow-2xl p-1 z-50">
                                    <button @click="editor().chain().focus().setTextAlign('left').run(); menuAlign = false" class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg flex items-center gap-2"><i class="ph ph-text-align-left"></i> Izquierda</button>
                                    <button @click="editor().chain().focus().setTextAlign('center').run(); menuAlign = false" class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg flex items-center gap-2"><i class="ph ph-text-align-center"></i> Centro</button>
                                    <button @click="editor().chain().focus().setTextAlign('right').run(); menuAlign = false" class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg flex items-center gap-2"><i class="ph ph-text-align-right"></i> Derecha</button>
                                    <button @click="editor().chain().focus().setTextAlign('justify').run(); menuAlign = false" class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg flex items-center gap-2"><i class="ph ph-text-align-justify"></i> Justificar</button>
                                </div>
                            </div>

                            <!-- NUEVO GRUPO: TABLAS (Añadir después de Alineación) -->
                            <div class="relative" x-data="{ menuTable: false }">
                                <button @click="menuTable = !menuTable" @click.away="menuTable = false"
                                        class="w-8 h-8 flex items-center justify-center rounded-lg text-slate-400 hover:text-white transition-all hover:bg-white/5">
                                    <i class="ph-bold ph-table"></i>
                                </button>
                                <div x-show="menuTable" x-transition class="absolute top-full mt-2 left-1/2 -translate-x-1/2 w-44 bg-[#1a1d26] border border-white/10 rounded-xl shadow-2xl p-1 z-50">
                                    <button @click="editor().chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run(); menuTable = false" class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg flex items-center gap-2"><i class="ph ph-plus"></i> Insertar Tabla 3x3</button>
                                    <div class="w-full h-px bg-white/5 my-1"></div>
                                    <button @click="editor().chain().focus().addColumnAfter().run()" class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg">Añadir Columna</button>
                                    <button @click="editor().chain().focus().addRowAfter().run()" class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg">Añadir Fila</button>
                                    <button @click="editor().chain().focus().deleteTable().run(); menuTable = false" class="w-full px-3 py-2 text-[11px] hover:bg-red-500/20 text-red-400 rounded-lg">Eliminar Tabla</button>
                                </div>
                            </div>

                            <!-- GRUPO 3: COLOR (Paleta de la Foto 3) -->
                            <div class="relative">
                                <button @click="menuColor = !menuColor" @click.away="menuColor = false"
                                        :class="activeStyles() && (editor().isActive('textStyle') || editor().isActive('highlight')) ? 'text-indigo-400' : 'text-slate-400'"
                                        class="w-8 h-8 flex items-center justify-center rounded-lg transition-all hover:bg-white/5">
                                    <i class="ph-bold ph-palette"></i>
                                </button>
                                <div x-show="menuColor" x-transition class="absolute top-full mt-2 left-1/2 -translate-x-1/2 w-44 bg-[#1a1d26] border border-white/10 rounded-xl shadow-2xl p-3 z-50">
                                    <p class="text-[9px] font-bold text-slate-500 uppercase mb-2 tracking-widest">Texto</p>
                                    <div class="grid grid-cols-5 gap-2 mb-3">
                                        <!-- FILA 1 -->
                                        <!-- Blanco Puro -->
                                        <button @click="editor().chain().focus().setColor('#fff').run()" 
                                                class="w-5 h-5 rounded-full bg-white border border-white/10" title="Blanco Brillante"></button>
                                        <!-- Blanco Mate Opaco (Slate 400) -->
                                        <button @click="editor().chain().focus().setColor('#94a3b8').run()" 
                                                class="w-5 h-5 rounded-full bg-[#94a3b8]" title="Blanco Mate"></button>
                                        <!-- Rojo -->
                                        <button @click="editor().chain().focus().setColor('#f87171').run()" 
                                                class="w-5 h-5 rounded-full bg-red-400" title="Rojo"></button>
                                        <!-- Naranja -->
                                        <button @click="editor().chain().focus().setColor('#fb923c').run()" 
                                                class="w-5 h-5 rounded-full bg-orange-400" title="Naranja"></button>
                                        <!-- Ámbar / Amarillo -->
                                        <button @click="editor().chain().focus().setColor('#fbbf24').run()" 
                                                class="w-5 h-5 rounded-full bg-amber-400" title="Ámbar"></button>
                                        
                                        <!-- FILA 2 -->
                                        <!-- Verde Esmeralda -->
                                        <button @click="editor().chain().focus().setColor('#34d399').run()" 
                                                class="w-5 h-5 rounded-full bg-emerald-400" title="Verde"></button>
                                        <!-- Azul -->
                                        <button @click="editor().chain().focus().setColor('#60a5fa').run()" 
                                                class="w-5 h-5 rounded-full bg-blue-400" title="Azul"></button>
                                        <!-- Violeta -->
                                        <button @click="editor().chain().focus().setColor('#a78bfa').run()" 
                                                class="w-5 h-5 rounded-full bg-violet-400" title="Violeta"></button>
                                        <!-- Rosa -->
                                        <button @click="editor().chain().focus().setColor('#f472b6').run()" 
                                                class="w-5 h-5 rounded-full bg-pink-400" title="Rosa"></button>
                                        <!-- Reset -->
                                        <button @click="editor().chain().focus().unsetColor().run()" 
                                                class="w-5 h-5 rounded-full border border-white/20 text-[10px] flex items-center justify-center hover:bg-white/10 transition-colors" 
                                                title="Quitar Color">
                                            <i class="ph ph-x"></i>
                                        </button>
                                    </div>
                                    <p class="text-[9px] font-bold text-slate-500 uppercase mb-2 tracking-widest">Resaltado (Summernote)</p>
                                    <div class="grid grid-cols-5 gap-2">
                                        <button @click="editor().chain().focus().setHighlight({ color: '#323232' }).run()" class="w-5 h-5 rounded bg-[#323232] border border-white/10"></button>
                                        <button @click="editor().chain().focus().setHighlight({ color: '#1e3a8a' }).run()" class="w-5 h-5 rounded bg-blue-900"></button>
                                        <button @click="editor().chain().focus().setHighlight({ color: '#3f6212' }).run()" class="w-5 h-5 rounded bg-green-900"></button>
                                        <button @click="editor().chain().focus().unsetHighlight().run()" class="w-5 h-5 rounded border border-white/20 text-[10px]"><i class="ph ph-x"></i></button>
                                    </div>
                                </div>
                            </div>

                            <div class="w-px h-4 bg-white/10 mx-1"></div>

                            <!-- GRUPO 4: PÁRRAFO -->
                            <div class="relative">
                                <button @click="menuAlign = !menuAlign" @click.away="menuAlign = false"
                                        class="w-8 h-8 flex items-center justify-center rounded-lg text-slate-400 hover:text-white transition-all hover:bg-white/5">
                                    <i class="ph-bold ph-list-bullets"></i>
                                </button>
                                <div x-show="menuAlign" x-transition class="absolute top-full mt-2 left-1/2 -translate-x-1/2 w-36 bg-[#1a1d26] border border-white/10 rounded-xl shadow-2xl p-1 z-50">
                                    <button @click="editor().chain().focus().setTextAlign('left').run()" class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg flex items-center gap-2"><i class="ph ph-text-align-left"></i> Izquierda</button>
                                    <button @click="editor().chain().focus().setTextAlign('center').run()" class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg flex items-center gap-2"><i class="ph ph-text-align-center"></i> Centro</button>
                                    <button @click="editor().chain().focus().toggleBulletList().run()" class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg flex items-center gap-2"><i class="ph ph-list-bullets"></i> Lista</button>
                                    <button @click="editor().chain().focus().toggleTaskList().run()" class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg flex items-center gap-2"><i class="ph ph-check-square"></i> To-do List</button>
                                </div>
                            </div>

                            <div class="w-px h-4 bg-white/10 mx-1"></div>

                            <!-- GRUPO 5: MÁS (Dropdown ...) -->
                            <div class="relative">
                                <button @click="menuMore = !menuMore" @click.away="menuMore = false"
                                        class="w-8 h-8 flex items-center justify-center rounded-lg text-slate-400 hover:text-white transition-all hover:bg-white/5">
                                    <i class="ph-bold ph-dots-three-outline-vertical"></i>
                                </button>
                                <div x-show="menuMore" x-transition class="absolute top-full mt-2 right-0 w-36 bg-[#1a1d26] border border-white/10 rounded-xl shadow-2xl p-1 z-50">
                                    <button @click="editor().chain().focus().toggleSubscript().run()" class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg flex items-center gap-2"><i class="ph ph-text-subscript"></i> Subíndice</button>
                                    <button @click="editor().chain().focus().toggleSuperscript().run()" class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg flex items-center gap-2"><i class="ph ph-text-superscript"></i> Superíndice</button>
                                    <button @click="editor().chain().focus().toggleCodeBlock().run()" 
                                            class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg flex items-center gap-2">
                                        <i class="ph ph-code"></i> Bloque Código
                                    </button>
                                    <button @click="editor().chain().focus().toggleBlockquote().run()" class="w-full px-3 py-2 text-[11px] hover:bg-white/5 rounded-lg flex items-center gap-2"><i class="ph ph-quotes"></i> Cita</button>
                                </div>
                            </div>

                            <!-- BOTÓN IA -->
                            <button class="ml-2 px-4 py-1.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-[11px] font-bold rounded-xl flex items-center gap-2 shadow-lg shadow-indigo-500/20 hover:scale-105 transition-all">
                                <i class="ph-fill ph-sparkle"></i>
                                ASK AI
                            </button>
                        </div>
                        </div>

                        <!-- 3. Área de TipTap -->
                        <div id="editor-container" class="prose prose-invert prose-indigo max-w-none">
                            <div id="tiptap-content" class="min-h-[60vh] text-lg leading-relaxed text-slate-300 outline-none">
                                <!-- TipTap se inyectará aquí -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- 4. ZONA 4: EL INSPECTOR (DINÁMICO) -->
    <aside class="glass-panel border-l border-white/5 flex flex-col shrink-0 relative transition-all duration-300"
           x-show="!zenMode && mode !== 'dashboard'"
           x-transition:enter="transition ease-out duration-300"
           x-transition:enter-start="opacity-0 translate-x-10"
           x-transition:enter-end="opacity-100 translate-x-0"
           x-transition:leave="transition ease-in duration-300"
           x-transition:leave-start="opacity-100 translate-x-0"
           x-transition:leave-end="opacity-0 translate-x-10"
           :style="`width: ${inspectorWidth}px;`"
           x-cloak>
        
        <!-- El Resizer Izquierdo de la Zona 4 -->
        <div class="absolute top-0 left-0 w-1 h-full cursor-col-resize resizer-hover transition-colors z-50"
             @mousedown="startResizeInspector()">
        </div>

        <!-- HEADER NUEVO INSPECTOR -->
        <div class="p-6 pb-4 flex items-center justify-between border-b border-white/5 shrink-0">
            <div class="flex items-center gap-2">
                <i class="ph ph-info text-purple-400"></i>
                <h2 class="text-[11px] font-bold tracking-[0.2em] text-slate-500 uppercase">Inspector</h2>
            </div>
            <button class="hover:text-white transition-colors">
                <i class="ph ph-dots-three-horizontal text-slate-500"></i>
            </button>
        </div>

        <!-- CONTENIDO SCROLLABLE NUEVO -->
        <div class="flex-1 overflow-y-auto">
            
            <!-- SECCIÓN: TABLA DE CONTENIDOS -->
            <section class="p-6">
                <h3 class="text-[10px] font-semibold text-slate-500 uppercase tracking-widest mb-4">Tabla de Contenidos</h3>
                <nav id="note-toc" class="space-y-1">
                    <!-- JS inyectará aquí el TOC -->
                </nav>
            </section>

            <!-- SECCIÓN: ETIQUETAS -->
            <section class="px-6 py-4 border-t border-white/5">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-[10px] font-semibold text-slate-500 uppercase tracking-widest">Etiquetas</h3>
                    <button class="text-purple-400 hover:text-purple-300 transition-colors">
                        <i class="ph ph-plus-circle w-3.5 h-3.5"></i>
                    </button>
                </div>
                <div id="note-tags" class="flex flex-wrap gap-2">
                    <!-- JS inyectará aquí los Tags -->
                </div>
            </section>

            <!-- SECCIÓN: ARCHIVOS ADJUNTOS -->
            <section class="px-6 py-4 border-t border-white/5">
                <div class="flex items-center justify-between mb-4">
                    <div class="flex items-center gap-2">
                        <h3 class="text-[10px] font-semibold text-slate-500 uppercase tracking-widest">Archivos</h3>
                        <!-- SPINNER DE CARGA (HTMX lo muestra automáticamente) -->
                        <div id="upload-indicator" class="htmx-indicator">
                            <i class="ph ph-circle-notch animate-spin text-indigo-500 text-xs"></i>
                        </div>
                    </div>
                    
                    <form id="attachment-form" 
                        hx-post="/api/notes/upload-attachment" 
                        hx-encoding="multipart/form-data" 
                        hx-target="#note-attachments"
                        hx-indicator="#upload-indicator"
                        hx-trigger="change from:#file-input"
                        class="flex">
                        <input type="hidden" name="note_id" :value="activeNoteId">
                        <input type="file" name="file" id="file-input" class="hidden">
                        <button type="button" onclick="document.getElementById('file-input').click()" 
                                class="text-purple-400 hover:text-purple-300 transition-colors">
                            <i class="ph ph-paperclip w-3.5 h-3.5"></i>
                        </button>
                    </form>
                </div>
                
                <div id="note-attachments" class="space-y-2">
                    <!-- El contenido se carga aquí -->
                    <span class="text-[10px] text-slate-700 italic">Selecciona una nota</span>
                </div>
            </section>
        </div>

        <!-- SECCIÓN INFERIOR: SHARE Y EXPORT -->
        <div class="p-6 bg-[#0d0f14] border-t border-white/5 shrink-0">
            <div class="flex gap-2">
                <button class="flex-1 flex items-center justify-center gap-2 py-2.5 px-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-[11px] font-medium text-slate-200 transition-all active:scale-[0.98]">
                    <i class="ph ph-share-network w-3.5 h-3.5"></i>
                    Share
                </button>
                
                <button class="flex-1 flex items-center justify-center gap-2 py-2.5 px-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-xl text-[11px] font-semibold shadow-lg shadow-purple-900/20 transition-all active:scale-[0.98]">
                    <i class="ph ph-file-pdf w-3.5 h-3.5"></i>
                    Export PDF
                </button>
            </div>
        </div>
    </aside>

    <!-- Contenedor Global de Modales (Portal Sagrado) -->
    <div id="modal-container" 
        class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/60 backdrop-blur-sm"
        x-show="modalOpen" 
        x-cloak 
        x-transition:enter="transition opacity ease-out duration-200"
        x-transition:enter-start="opacity-0"
        x-transition:enter-end="opacity-100"
        x-transition:leave="transition opacity ease-in duration-200"
        x-transition:leave-start="opacity-100"
        x-transition:leave-end="opacity-0">
        
        <!-- EL PORTAL SAGRADO: Único target permitido para inyección de modales -->
        <div id="main-portal-target" 
             @click.outside="modalOpen = false"
             class="w-full max-w-md mx-4 relative z-[10000]">
             <!-- El contenido se inyecta y limpia aquí mediante openModal() -->
        </div>
    </div>

    <!-- PORTAL GLOBAL: Menú Contextual Multi-Contexto (Corregido) -->
    <div id="global-gear-menu-portal" class="fixed inset-0 pointer-events-none z-[900]" x-cloak>
        <div class="gear-dropdown-portal pointer-events-auto"
             x-show="activeGearMenu !== null"
             x-transition.opacity.duration.150ms
             :style="`position: fixed; top: ${gearMenuCoords.y}px; left: ${gearMenuCoords.x}px; z-index: 901;`"
             @click.outside="activeGearMenu = null"
             style="display: none;">
            
            <!-- CASO A: BIBLIOTECAS (Prefix CAT_) -->
            <template x-if="activeGearMenu && activeGearMenu.toString().startsWith('CAT_')">
                <div class="flex flex-col">
                    <button type="button" @click="openModal(`/partial/modal/edit-categoria/${activeGearMenu.replace('CAT_', '')}`); activeGearMenu = null;" class="gear-dropdown-btn">
                        <i class="ph ph-pencil-simple text-sm"></i> <span>Editar Biblioteca</span>
                    </button>
                    <button type="button" @click="openModal(`/partial/modal/confirm-delete-categoria/${activeGearMenu.replace('CAT_', '')}`); activeGearMenu = null;" class="gear-dropdown-btn text-red-400">
                        <i class="ph ph-trash text-sm"></i> <span>Eliminar Biblioteca</span>
                    </button>
                </div>
            </template>

            <!-- CASO B: CUADERNOS (Prefix NB_) -->
            <template x-if="activeGearMenu && activeGearMenu.toString().startsWith('NB_')">
                <div class="flex flex-col">
                    <button type="button" @click="openModal(`/partial/modal/edit-cuaderno/${activeGearMenu.replace('NB_', '')}`); activeGearMenu = null;" class="gear-dropdown-btn">
                        <i class="ph ph-pencil-simple text-sm"></i> <span>Editar Cuaderno</span>
                    </button>
                    <button type="button" @click="openModal(`/partial/modal/confirm-delete-cuaderno/${activeGearMenu.replace('NB_', '')}`); activeGearMenu = null;" class="gear-dropdown-btn text-red-400">
                        <i class="ph ph-trash text-sm"></i> <span>Eliminar Cuaderno</span>
                    </button>
                </div>
            </template>

            <!-- CASO C: NOTAS (Dentro de global-gear-menu-portal en base.html) -->
            <template x-if="activeGearMenu && !activeGearMenu.toString().startsWith('CAT_') && !activeGearMenu.toString().startsWith('NB_') && !activeGearMenu.toString().startsWith('TM_')">
                <div class="flex flex-col">
                    <button @click="openQuickView(activeGearMenu); activeGearMenu = null" class="gear-dropdown-btn">
                        <i class="ph ph-eye text-sm"></i> <span>Quick View</span>
                    </button>
                    <button @click="openModal(`/partial/modal/inbox-mover/${activeGearMenu}`); activeGearMenu = null;" class="gear-dropdown-btn">
                        <i class="ph ph-arrow-right text-sm"></i> <span>Mover Nota</span>
                    </button>
                    <!-- NUEVO: Botón de eliminación con modal corregido -->
                    <button @click="openModal(`/partial/modal/eliminar-nota/${activeGearMenu}`); activeGearMenu = null;" 
                            class="gear-dropdown-btn text-red-400">
                        <i class="ph ph-trash text-sm"></i> <span>Eliminar Nota</span>
                    </button>
                </div>
            </template>

            <!-- CASO D: TEMAS (Prefix TM_) -->
            <template x-if="activeGearMenu && activeGearMenu.toString().startsWith('TM_')">
                <div class="flex flex-col">
                    <button type="button" @click="openModal(`/partial/modal/edit-tema/${activeGearMenu.replace('TM_', '')}`); activeGearMenu = null;" class="gear-dropdown-btn">
                        <i class="ph ph-pencil-simple text-sm"></i> <span>Editar Tema</span>
                    </button>
                    <button type="button" @click="openModal(`/partial/modal/confirm-delete-tema/${activeGearMenu.replace('TM_', '')}`); activeGearMenu = null;" class="gear-dropdown-btn text-red-400">
                        <i class="ph ph-trash text-sm"></i> <span>Eliminar Tema</span>
                    </button>
                </div>
            </template>
        </div>
    </div>

</body>
</html>
```

---

## 📄 Archivo: `templates/modules/cockpit_pane.html`
```html
<!-- templates/modules/cockpit_pane.html -->
<div class="max-w-5xl mx-auto py-12 px-8 fade-in-up">
    
    <!-- Briefing -->
    <div class="mb-10">
        <h1 class="text-3xl font-light text-white mb-2">Hola, <span class="font-medium text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">{{ user.nombre }}.</span></h1>
        <p class="text-slate-400 text-lg flex items-center gap-2">
            <i class="ph-fill ph-sparkle text-indigo-400"></i>
            Tienes <span class="text-white font-bold">{{ agenda|length }}</span> tareas pendientes para hoy.
        </p>
    </div>

    <!-- OMNIBARRA -->
    <div class="relative group mb-12">
        <!-- Efecto de resplandor (Glow) -->
        <div class="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 via-purple-500 to-amber-500 rounded-xl blur opacity-20 group-hover:opacity-40 transition duration-500"></div>
        
        <!-- templates/modules/cockpit_pane.html -->
        <div class="relative bg-[#1a1d26] rounded-xl border border-white/10 shadow-2xl overflow-hidden"
            x-data="{ content: '' }">
            
            <textarea 
                x-model="content"
                placeholder="¿Qué estás pensando? (Shift + Enter para enviar)" 
                class="w-full bg-transparent border-none text-white text-lg px-6 py-5 focus:ring-0 placeholder-slate-500 font-light resize-none h-32"
                
                @keydown.enter.shift.prevent="
                    if(content.trim().length > 0) {
                        aiLoading = true; // <-- ACTIVAR PUNTITOS
                        // 1. Enviamos la petición de forma asíncrona e inmediata
                        htmx.ajax('POST', '/inbox/captura', { 
                            values: { contenido: content },
                            handler: (xhr) => {
                                aiLoading = false; // <-- DESACTIVAR PUNTITOS al completar
                                // 2. Dispara evento para actualizar el contador del badge
                                document.body.dispatchEvent(new CustomEvent('update-inbox-count'));
                            }
                        });
                        // 3. Limpiamos el campo al instante (Sensación de velocidad)
                        content = '';
                    }
                "
            ></textarea>

            <!-- PIE DE PÁGINA -->
            <div class="px-4 py-2 bg-[#15171e] flex justify-between items-center border-t border-white/5">
                <div class="flex gap-4 text-[10px] text-slate-500 font-mono">
                    <span class="flex items-center gap-1.5 hover:text-white cursor-pointer transition-colors group/btn">
                        <kbd class="bg-[#252836] px-1.5 py-0.5 rounded text-slate-400 border border-white/5">⌘K</kbd> 
                        <span>Buscar</span>
                    </span>
                    <span class="flex items-center gap-1.5 text-slate-400">
                        <kbd class="bg-[#252836] px-1.5 py-0.5 rounded border border-white/5">Shift + ↵</kbd> 
                        <span>Enviar</span>
                    </span>
                </div>

                <!-- Botón de envío manual corregido -->
                <button class="text-slate-500 hover:text-indigo-400 transition-colors"
                        @click="if(content.trim().length > 0) { htmx.ajax('POST', '/inbox/captura', { values: { contenido: content } }); content = ''; }">
                    <i class="ph-bold ph-arrow-return-left"></i>
                </button>
            </div>
        </div>

    </div>

    <!-- GRID DE TARJETAS -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <!-- Card Proyectos -->
        <div class="bg-[#15171e] p-5 rounded-2xl border border-white/5 hover:border-indigo-500/30 transition-all cursor-pointer group">
            <div class="text-xs font-bold text-indigo-400 uppercase tracking-widest mb-3">En Foco</div>
            <h3 class="text-white text-lg font-medium mb-1">Proyectos Activos</h3>
            <p class="text-xs text-slate-500">{{ proyectos|length }} proyectos en curso.</p>
        </div>

        <!-- Card Agenda -->
        <div class="bg-[#15171e] p-5 rounded-2xl border border-white/5 hover:border-amber-500/30 transition-all cursor-pointer">
            <div class="text-xs font-bold text-amber-400 uppercase tracking-widest mb-3">Agenda</div>
            <div class="space-y-2">
                {% for tarea in agenda[:2] %}
                <div class="flex items-center gap-2 text-xs text-slate-300">
                    <i class="ph ph-circle text-slate-600"></i>
                    <span class="truncate">{{ tarea.titulo }}</span>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- Card IA Jardinero -->
        <div class="bg-[#15171e] p-5 rounded-2xl border border-white/5 hover:border-emerald-500/30 transition-all cursor-pointer">
            <div class="text-xs font-bold text-emerald-400 uppercase tracking-widest mb-3">Jardinero IA</div>
            <p class="text-xs text-slate-500">Analizando 3 notas sin clasificar en tu Inbox...</p>
        </div>
    </div>

    <!-- NOTAS RECIENTES -->
    <div class="mt-12">
        <h3 class="text-slate-500 text-xs font-bold uppercase tracking-widest mb-6">Trabajo Reciente</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            {% for nota in recientes %}
            <div class="bg-[#15171e] p-5 rounded-xl border border-white/5 hover:border-indigo-500/40 transition-all cursor-pointer group">
                <h4 class="text-white font-medium mb-2 group-hover:text-indigo-400">{{ nota.titulo or 'Sin título' }}</h4>
                <p class="text-slate-500 text-xs line-clamp-2">
                    {{ nota.tema.cuaderno.nombre }} / {{ nota.tema.nombre }}
                </p>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
```

---

## 📄 Archivo: `templates/modules/sidebar_dashboard.html`
```html
<!-- templates/modules/sidebar_dashboard.html -->
<div id="sidebar-dashboard-container" 
     class="flex flex-col h-full space-y-2 fade-in-up select-none overflow-y-auto custom-scroll"
     x-init="
        setTimeout(() => {
            $el.scrollTo({ top: sidebarScrollTop, behavior: 'instant' });
        }, 50);
     "
     @scroll.debounce.150ms="sidebarScrollTop = $el.scrollTop; localStorage.setItem('docs_sidebar_scroll', $el.scrollTop)">
    
    <!-- HEADER -->
    <div class="p-5 flex items-center justify-between">
        <div>
            <h2 class="text-[9px] font-bold uppercase tracking-[0.2em] text-gray-500">Biblioteca</h2>
        </div>
        <!-- Botón Crear Categoría -->
        <button @click="openModal('/partial/modal/nueva-categoria')"
                class="w-6 h-6 rounded-md border border-white/5 flex items-center justify-center hover:bg-white/5 transition-colors">
            <i class="ph ph-plus text-[14px] text-gray-500"></i>
        </button>
    </div>

    <!-- BUSCADOR -->
    <div class="px-4 mb-4">
        <div class="relative">
            <input type="text" placeholder="Buscar..." 
                class="w-full bg-white/[0.02] border border-white/5 rounded-lg py-1.5 pl-8 pr-3 text-[11px] focus:outline-none focus:border-purple-500/40 transition-all placeholder:text-gray-600">
            <i class="ph ph-magnifying-glass text-[12px] absolute left-2.5 top-2.5 text-gray-600"></i>
        </div>
    </div>

    <!-- LISTA DE BIBLIOTECAS/CATEGORÍAS -->
    <div class="flex-1 px-3 space-y-2">
        {% for cat in categorias %}
        
        {% set icon_map = {
            'folder': 'folder', 'code': 'code', 'graduation-cap': 'graduation-cap',
            'briefcase': 'briefcase', 'chess': 'castle-turret', 'inbox': 'tray',
            'chalkboard-teacher': 'chalkboard-teacher', 'school': 'school',
            'microchip': 'cpu', 'film': 'film-strip', 'music': 'music-notes',
            'tools': 'wrench', 'robot': 'robot', 'industry': 'factory',
            'microscope': 'microscope'
        } %}
        {% set db_icon = cat.icono if cat.icono else 'folder' %}
        {% set final_icon = icon_map.get(db_icon, db_icon) %}

        <div class="library-card rounded-xl overflow-hidden group/cat"
             :class="openCategories.includes('{{ cat.id }}') ? 'border-purple-500/20 bg-purple-500/[0.01]' : ''">
            
            <!-- CABECERA COLAPSABLE -->
            <div class="w-full p-2.5 flex items-center justify-between group transition-colors">
                <div class="flex items-center gap-2.5 cursor-pointer flex-1" @click="toggleCategory('{{ cat.id }}')">
                    <div class="w-6 h-6 rounded bg-blue-500/10 flex items-center justify-center border border-blue-500/10"
                         :class="openCategories.includes('{{ cat.id }}') ? 'bg-purple-500/10 border-purple-500/20' : ''">
                        <i class="ph-fill ph-{{ final_icon }} text-[14px]"
                           :class="openCategories.includes('{{ cat.id }}') ? 'text-purple-400' : 'text-blue-400/80'"></i>
                    </div>
                    <span class="text-[13.2px] font-medium transition-colors"
                          :class="openCategories.includes('{{ cat.id }}') ? 'text-white/90 font-semibold' : 'text-gray-400 group-hover:text-gray-200'">
                        {{ cat.nombre }}
                    </span>
                </div>

                <div class="flex items-center gap-2">
                    <!-- Engranaje de Gestión de Categoría (Solo visible en hover de la card) -->
                    <button class="opacity-0 group-hover/cat:opacity-100 text-slate-500 hover:text-white transition-opacity p-1"
                            @click.stop="openGearMenu($event, 'CAT_{{ cat.id }}')">
                        <i class="ph ph-gear text-[14px]"></i>
                    </button>
                    <i class="ph ph-caret-right w-3 h-3 text-gray-700 transition-transform cursor-pointer"
                       @click="toggleCategory('{{ cat.id }}')"
                       :class="openCategories.includes('{{ cat.id }}') ? 'rotate-90 text-purple-400/50' : ''"></i>
                </div>
            </div>

            <!-- CUADERNOS (COLAPSABLE - JERARQUÍA CON TIMELINE) -->
            <div x-show="openCategories.includes('{{ cat.id }}')" x-collapse class="pb-2">
                
                <!-- CONTENEDOR RELATIVO PARA EL TIMELINE -->
                <div class="relative ml-6 mt-1 space-y-2">
                    
                    <!-- LÍNEA VERTICAL MAESTRA -->
                    <div class="absolute left-[-14px] top-0 bottom-4 w-px bg-slate-800"></div>

                    {% for cuaderno in cat.cuadernos %}
                    <div class="relative group/item flex items-center">
                        
                        <!-- CONECTOR HORIZONTAL (L-Shape) -->
                        <div class="absolute left-[-14px] top-1/2 -translate-y-1/2 w-3.5 h-px bg-slate-800 group-hover/item:bg-emerald-500/50"></div>

                        <!-- TARJETA DELGADA DE CUADERNO -->
                        <div class="flex-1 flex items-center justify-between p-1.5 ml-0 rounded-lg border transition-all duration-200 cursor-pointer overflow-hidden"
                             :class="activeCuadernoId === '{{ cuaderno.id }}' 
                                     ? 'bg-emerald-500/10 border-emerald-500/30 shadow-lg shadow-emerald-900/10' 
                                     : 'bg-white/[0.01] border-white/5 hover:border-white/10 hover:bg-white/[0.03]'"
                             @click="activeCuadernoId = '{{ cuaderno.id }}'; activeCategoriaId = '{{ cat.id }}'; mode = 'notebook';">
                            
                            <!-- Contenido de la Tarjeta -->
                            <div class="flex items-center gap-2.5 flex-1 min-w-0"
                                 hx-get="/partial/sidebar/notebook/{{ cuaderno.id }}"
                                 hx-target="#contextual-sidebar"
                                 hx-indicator="#sidebar-indicator"
                                 hx-swap="innerHTML">
                                
                                <div class="w-5 h-5 flex items-center justify-center rounded-md shrink-0"
                                     :class="activeCuadernoId === '{{ cuaderno.id }}' ? 'text-emerald-400' : 'text-slate-600 group-hover/item:text-slate-400'">
                                    <i class="ph-fill ph-book-bookmark text-[13px]"></i>
                                </div>

                                <span class="text-[11px] truncate transition-colors"
                                      :class="activeCuadernoId === '{{ cuaderno.id }}' ? 'text-white font-semibold' : 'text-slate-400 group-hover/item:text-slate-200'">
                                    {{ cuaderno.nombre }}
                                </span>
                            </div>

                            <!-- Engranaje -->
                            <button @click.stop="openGearMenu($event, 'NB_{{ cuaderno.id }}')"
                                    type="button"
                                    class="opacity-0 group-hover/item:opacity-100 text-slate-500 hover:text-white transition-opacity px-2 shrink-0">
                                <i class="ph ph-gear text-[13px]"></i>
                            </button>
                        </div>
                    </div>
                    {% endfor %}

                    <!-- BOTÓN AÑADIR CUADERNO (Conector de Timeline) -->
                    <div class="relative flex items-center">
                        <div class="absolute left-[-14px] top-1/2 -translate-y-1/2 w-3.5 h-px bg-slate-800"></div>
                        <button @click="openModal('/partial/modal/nuevo-cuaderno/{{ cat.id }}')"
                                class="w-full py-1.5 rounded-lg border border-dashed border-white/5 hover:border-cyan-500/30 hover:bg-cyan-500/5 transition-all group">
                            <div class="flex items-center justify-center gap-2 text-[9px] font-bold text-slate-600 group-hover:text-cyan-400 uppercase tracking-widest">
                                <i class="ph ph-plus-circle"></i>
                                <span>Añadir Cuaderno</span>
                            </div>
                        </button>
                    </div>

                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    <div class="h-6"></div>
</div>
```

---

## 📄 Archivo: `templates/modules/sidebar_inbox.html`
```html
<!-- templates/modules/sidebar_inbox.html -->

<!-- Añadimos hx-trigger para que se recargue cuando se capture una nota -->
<div id="inbox-sidebar-container" 
     class="flex flex-col h-full space-y-4 fade-in-up select-none"
     hx-get="/partial/sidebar/inbox"
     hx-trigger="update-inbox-list from:body"
     hx-target="this"
     hx-swap="outerHTML">
    
    <!-- Título de Ruta -->
    <div class="px-2 mb-2">
        <div class="flex items-center gap-2 text-[10px] font-bold text-amber-500 uppercase tracking-widest">
            <i class="ph-bold ph-tray"></i>
            <span>General <i class="ph ph-caret-right text-[8px] mx-1"></i> Inbox</span>
        </div>
    </div>

    <!-- Lista de Tarjetas de Notas -->
    <div class="space-y-3">
        {% for nota in notas %}
            <div class="group note-card bg-[#1a1d26] p-4 rounded-xl border border-white/5 hover:border-amber-500/30 transition-all cursor-pointer relative"
                @click="switchActiveNote('{{ nota.id }}')">
                
                <div class="flex justify-between items-start mb-2">
                    <h4 class="text-xs font-bold text-slate-200 truncate pr-6">{{ nota.titulo }}</h4>
                    
                    <!-- Engranaje: El .stop es VITAL para que al configurar la nota no se intente editarla -->
                    <button class="gear-button"
                            @click.stop="openGearMenu($event, '{{ nota.id }}')"
                            type="button">
                        <i class="ph-bold ph-gear text-sm"></i>
                    </button>
                </div>

                <p class="text-[11px] text-slate-500 line-clamp-3 leading-relaxed">
                    {{ nota.resumen_texto }}
                </p>

                <div class="mt-3 text-[9px] text-slate-600 font-mono">
                    {{ nota.created_at.strftime('%d %b, %H:%M') }}
                </div>
            </div>
        {% else %}
        <div class="py-12 text-center">
            <i class="ph ph-sparkle text-slate-700 text-3xl mb-2"></i>
            <p class="text-xs text-slate-600">Bandeja vacía</p>
        </div>
        {% endfor %}
    </div>
</div>
```

---

## 📄 Archivo: `templates/modules/sidebar_notebook.html`
```html
<!-- templates/modules/sidebar_notebook.html -->
<div id="notebook-sidebar-container" 
     class="flex flex-col h-full fade-in-up select-none overflow-y-auto custom-scroll"
     hx-get="/partial/sidebar/notebook/{{ cuaderno.id }}"
     hx-trigger="refresh-notebook-sidebar from:body"
     hx-target="this"
     hx-swap="outerHTML"
     x-init="
        setTimeout(() => { $el.scrollTop = notebookScrollTop; }, 50);
     "
     @scroll.debounce.150ms="notebookScrollTop = $el.scrollTop; localStorage.setItem('docs_notebook_scroll', $el.scrollTop)">
    
    <!-- CABECERA: CONTEXTO DEL CUADERNO -->
    <div class="px-3 py-4 border-b border-white/5 bg-[#13151b]/50 backdrop-blur-md sticky top-0 z-30">
        <div class="flex items-center gap-3">
            <button hx-get="/partial/sidebar/dashboard" 
                    hx-target="#contextual-sidebar"
                    hx-indicator="#sidebar-indicator"
                    hx-swap="innerHTML"
                    @click="activeCuadernoId = null; activeCategoriaId = null; mode = 'dashboard'; notebookScrollTop = 0;"
                    class="w-8 h-8 flex items-center justify-center rounded-full bg-white/[0.03] border border-white/5 text-slate-500 hover:text-white hover:bg-white/10 transition-all">
                <i class="ph-bold ph-arrow-left"></i>
            </button>
            
            <div class="flex flex-col truncate flex-1">
                <span class="text-[9px] font-bold text-slate-600 uppercase tracking-widest leading-none mb-1">
                    {{ categoria.nombre }}
                </span>
                <h3 class="text-sm font-bold text-slate-100 truncate">
                    {{ cuaderno.nombre }}
                </h3>
            </div>

            <!-- Botón Añadir Tema (Corregido y Axiomático) -->
            <button type="button"
                    @click="openModal('/partial/modal/nuevo-tema/{{ cuaderno.id }}')"
                    class="w-8 h-8 flex items-center justify-center rounded-lg text-slate-500 hover:text-indigo-400 hover:bg-indigo-500/10 transition-all">
                <i class="ph-bold ph-plus-circle text-xl"></i>
            </button>
        </div>
    </div>

    <!-- LISTADO DE TEMAS Y NOTAS -->
    <div class="flex-1 py-4 px-3 space-y-6">
        {% if cuaderno.temas %}
            {% for tema in cuaderno.temas | sort(attribute='orden') %}
            <div class="group/tema block" 
                 x-init="checkInitialTheme('{{ tema.id }}', {{ 'true' if loop.first else 'false' }})">
                
                <!-- ENCABEZADO DE TEMA (Con Engranaje) -->
                <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-3 cursor-pointer flex-1" @click="toggleTheme('{{ tema.id }}')">
                        <div class="w-5 h-5 flex items-center justify-center rounded-md transition-colors"
                             :class="openThemes.includes('{{ tema.id }}') ? 'bg-indigo-500/20 text-indigo-400' : 'bg-slate-800 text-slate-600'">
                            <i class="ph-bold text-[10px]" :class="openThemes.includes('{{ tema.id }}') ? 'ph-caret-down' : 'ph-caret-right'"></i>
                        </div>
                        
                        <span class="text-[10px] font-bold uppercase tracking-[0.15em] transition-colors"
                              :class="openThemes.includes('{{ tema.id }}') ? 'text-slate-200' : 'text-slate-500 group-hover/tema:text-slate-300'">
                            {{ tema.nombre }}
                        </span>
                    </div>

                    <div class="flex items-center gap-2">
                        <!-- Engranaje de Tema -->
                        <button class="opacity-0 group-hover/tema:opacity-100 text-slate-500 hover:text-white transition-opacity p-1"
                                @click.stop="openGearMenu($event, 'TM_{{ tema.id }}')">
                            <i class="ph ph-gear text-[13px]"></i>
                        </button>
                        
                        <span class="text-[9px] font-mono text-slate-600 bg-slate-800/50 px-1.5 py-0.5 rounded border border-white/5">
                            {{ tema.anotaciones|length }}
                        </span>
                    </div>
                </div>

                <!-- LISTA DE NOTAS -->
                <div x-show="openThemes.includes('{{ tema.id }}')" x-collapse class="relative ml-[6px] pl-6 space-y-3 mt-2 pb-2">
                    <div class="absolute left-0 top-0 bottom-0 w-px bg-slate-800/50 z-0"></div>

                    {% for nota in tema.anotaciones %}
                    <div class="relative group/note cursor-pointer"
                         @click="
                            activeNoteId = '{{ nota.id }}'; 
                            window.dispatchEvent(new CustomEvent('note-selected', { detail: { id: '{{ nota.id }}' } }));
                            window.history.pushState({}, '', '/note/{{ nota.id }}');
                         ">
                        <div class="absolute -left-[27px] top-4 w-2 h-2 rounded-full border-2 transition-all duration-300 z-10"
                             :class="activeNoteId === '{{ nota.id }}' 
                                     ? 'bg-indigo-500 border-indigo-400 shadow-[0_0_8px_rgba(99,102,241,0.5)]' 
                                     : 'bg-[#0f1117] border-slate-700 group-hover/note:border-slate-500'">
                        </div>

                        <div class="note-card bg-[#1a1d26] p-3 rounded-xl border transition-all duration-300 hover:translate-x-1"
                            :class="activeNoteId === '{{ nota.id }}' 
                                    ? 'border-indigo-500/40 bg-indigo-500/[0.05] shadow-lg shadow-indigo-500/5' 
                                    : 'border-white/[0.03] hover:border-white/10 hover:bg-[#1a1d26]/80'">
                            
                            <div class="flex justify-between items-start mb-1">
                                <div class="flex items-center gap-2 truncate pr-6">
                                    <i class="ph text-sm"
                                       :class="activeNoteId === '{{ nota.id }}' ? 'ph-note-blank-fill text-indigo-400' : 'ph-note-blank text-slate-500'"></i>
                                    <h4 class="text-[12px] font-bold truncate transition-colors"
                                        :class="activeNoteId === '{{ nota.id }}' ? 'text-white' : 'text-slate-300 group-hover/note:text-white'">
                                        {{ nota.titulo or 'Sin título' }}
                                    </h4>
                                </div>
                                <button class="gear-button" @click.stop="openGearMenu($event, '{{ nota.id }}')" type="button">
                                    <i class="ph-bold ph-gear text-[12px]"></i>
                                </button>
                            </div>
                            <p class="text-[10px] text-slate-500 line-clamp-2 leading-relaxed font-medium">
                                {{ nota.resumen_texto }}
                            </p>
                            <div class="mt-2 text-[9px] text-slate-600 font-mono">
                                {{ nota.created_at.strftime('%d %b, %H:%M') }}
                            </div>
                        </div>
                    </div>
                    {% endfor %}

                    <div class="relative group/add">
                        <div class="absolute -left-[26px] top-4 w-1.5 h-1.5 rounded-full border border-dashed border-slate-700"></div>
                        <button hx-post="/api/notes/create" hx-vals='{"tema_id": "{{ tema.id }}"}' hx-target="#notebook-sidebar-container" hx-indicator="#sidebar-indicator" hx-swap="outerHTML" @click="aiLoading = true" hx-on::after-request="aiLoading = false" class="w-full text-left p-2 rounded-lg border border-dashed border-white/5 hover:border-indigo-500/30 hover:bg-indigo-500/5 transition-all group">
                            <span class="text-[10px] font-bold text-slate-500 group-hover:text-indigo-400 uppercase tracking-tighter flex items-center gap-2">
                                <i class="ph ph-plus-circle text-xs"></i> Añadir Nota
                            </span>
                        </button>
                    </div>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <!-- ESTADO VACÍO -->
            <div class="flex flex-col items-center justify-center py-20 px-6 text-center">
                <div class="w-16 h-16 bg-white/[0.02] border border-white/5 rounded-2xl flex items-center justify-center mb-4">
                    <i class="ph ph-folder-dotted text-slate-700 text-3xl"></i>
                </div>
                <h4 class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-2">Cuaderno Vacío</h4>
                <p class="text-[11px] text-slate-600 leading-relaxed mb-6">
                    Comienza organizando este cuaderno creando tu primer tema.
                </p>
                <button hx-get="/partial/modal/nuevo-tema/{{ cuaderno.id }}"
                        hx-target="#modal-content"
                        @click="modalOpen = true"
                        class="px-4 py-2 bg-indigo-600/10 hover:bg-indigo-600 border border-indigo-500/20 text-indigo-400 hover:text-white text-[10px] font-bold rounded-lg transition-all uppercase tracking-widest">
                    Crear primer tema
                </button>
            </div>
        {% endif %}
    </div>
</div>
```

---

## 📄 Archivo: `templates/modules/sidebar_projects.html`
```html
<!-- templates/modules/sidebar_projects.html -->
<div class="text-sm text-slate-400 fade-in-up">
    <div class="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-4 px-2">Explorador</div>
    <div class="space-y-1">
        {% for cat in categorias %}
        <div x-data="{ open: true }">
            <div @click="open = !open" class="flex items-center justify-between px-2 py-2 hover:bg-white/5 rounded cursor-pointer group">
                <div class="flex items-center gap-2">
                    <i class="ph-fill ph-folder text-indigo-500"></i>
                    <span class="text-xs font-medium text-slate-300">{{ cat.nombre }}</span>
                </div>
                <i class="ph ph-caret-down text-[10px] transition-transform" :class="open ? '' : '-rotate-90'"></i>
            </div>
            <div x-show="open" x-collapse class="ml-4 border-l border-white/5 pl-2 space-y-1 mt-1">
                {% for cuaderno in cat.cuadernos %}
                <div class="py-1.5 px-2 text-[11px] hover:text-indigo-400 cursor-pointer truncate">
                    {{ cuaderno.nombre }}
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
</div>
```

---

## 📄 Archivo: `templates/pages/login.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar Sesión - Docs.ai</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'); body { font-family: 'Inter', sans-serif; }</style>
</head>
<body class="bg-slate-50 min-h-screen flex items-center justify-center p-4">

    <div class="w-full max-w-md bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
        <div class="bg-blue-600 p-8 text-center">
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-white/20 mb-4 text-white">
                <i class="fa-solid fa-feather-pointed text-2xl"></i>
            </div>
            <h1 class="text-2xl font-bold text-white tracking-wide">Docs.ai</h1>
            <p class="text-blue-100 text-sm mt-1">Tu segundo cerebro digital</p>
        </div>

        <div class="p-8">
            <h2 class="text-xl font-semibold text-slate-800 text-center mb-6">Bienvenido de nuevo</h2>

            {% if request.query_params.get('error') == '1' %}
            <div class="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-r shadow-sm">
                <p class="text-sm text-red-700 font-medium"><i class="fa-solid fa-circle-xmark mr-2"></i>Credenciales incorrectas</p>
            </div>
            {% endif %}

            {% if request.query_params.get('registered') == '1' %}
            <div class="mb-6 bg-green-50 border-l-4 border-green-500 p-4 rounded-r shadow-sm">
                <p class="text-sm text-green-700 font-medium"><i class="fa-solid fa-circle-check mr-2"></i>¡Cuenta creada! Inicia sesión.</p>
            </div>
            {% endif %}

            <form action="/login" method="POST" class="space-y-5">
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
                    <input type="email" name="email" required placeholder="tu@email.com" class="block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:ring-blue-500 focus:border-blue-500 shadow-sm" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Contraseña</label>
                    <input type="password" name="password" required placeholder="••••••••" class="block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:ring-blue-500 focus:border-blue-500 shadow-sm" />
                </div>
                <button type="submit" class="w-full flex justify-center py-2.5 px-4 rounded-lg shadow-sm text-sm font-medium text-white bg-slate-800 hover:bg-slate-900 transition-colors">
                    Iniciar Sesión
                </button>
            </form>
        </div>
        <div class="bg-slate-50 px-8 py-4 border-t border-slate-100 text-center">
            <p class="text-sm text-slate-600">¿No tienes cuenta? <a href="/register" class="font-medium text-blue-600 hover:text-blue-500">Regístrate gratis</a></p>
        </div>
    </div>
</body>
</html>
```

---

## 📄 Archivo: `templates/pages/register.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crear Cuenta - Docs.ai</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'); body { font-family: 'Inter', sans-serif; }</style>
</head>
<body class="bg-slate-50 min-h-screen flex items-center justify-center p-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
        <div class="bg-blue-600 p-8 text-center">
            <h1 class="text-2xl font-bold text-white tracking-wide">Registro Docs.ai</h1>
        </div>
        <div class="p-8">
            <h2 class="text-xl font-semibold text-slate-800 text-center mb-6">Crea tu cuenta</h2>

            {% if request.query_params.get('error') == 'exists' %}
            <div class="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-r shadow-sm">
                <p class="text-sm text-red-700">El correo ya está registrado.</p>
            </div>
            {% endif %}

            <form action="/register" method="POST" class="space-y-5">
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Nombre Completo</label>
                    <input type="text" name="nombre" required placeholder="Ej: Ana Pérez" class="block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:ring-blue-500 focus:border-blue-500 shadow-sm" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
                    <input type="email" name="email" required placeholder="tu@email.com" class="block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:ring-blue-500 focus:border-blue-500 shadow-sm" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Contraseña</label>
                    <input type="password" name="password" required placeholder="••••••••" class="block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:ring-blue-500 focus:border-blue-500 shadow-sm" />
                </div>
                <button type="submit" class="w-full flex justify-center py-2.5 px-4 rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 transition-colors">
                    Registrarse
                </button>
            </form>
        </div>
        <div class="bg-slate-50 px-8 py-4 border-t border-slate-100 text-center">
            <p class="text-sm text-slate-600">¿Ya tienes cuenta? <a href="/login" class="font-medium text-blue-600 hover:text-blue-500">Inicia sesión</a></p>
        </div>
    </div>
</body>
</html>
```

---

## 📄 Archivo: `templates/partials/attachments_list.html`
```html
<!-- templates/partials/attachments_list.html -->
{% for adj in adjuntos %}
<div class="flex items-center justify-between p-2 rounded-lg hover:bg-white/5 transition-all">
    <div class="flex items-center gap-3">
        <i class="ph ph-file-text text-slate-500 w-4 h-4"></i>
        <a href="{{ adj.url }}" 
           target="_blank" 
           rel="noopener noreferrer"
           class="text-xs text-slate-400 hover:text-slate-200 transition-colors truncate">
            {{ adj.nombre_original }}
        </a>
    </div>
    
    <!-- Botón de Borrado -->
    <button hx-delete="/api/notes/attachment/{{ adj.id }}"
            hx-target="#note-attachments"
            hx-confirm="¿Estás seguro de eliminar este archivo?"
            hx-indicator="#upload-indicator"
            class="text-slate-600 hover:text-red-400 transition-colors">
        <i class="ph ph-trash w-3.5 h-3.5"></i>
    </button>
</div>
{% else %}
<span class="text-[10px] text-slate-700 italic">Sin archivos adjuntos</span>
{% endfor %}
```

---

## 📄 Archivo: `templates/partials/editor_content.html`
```html

```

---

## 📄 Archivo: `templates/partials/floating_note.html`
```html
<!-- templates/partials/floating_note.html -->
<!-- Esta plantilla se renderiza dinámicamente con Alpine.js en JavaScript -->
<!-- NO se usa con HTMX, se construye en el cliente con Alpine -->

<!-- Nota: Este archivo es una referencia. El HTML real se crea dinámicamente en el navegador -->
<!-- Vea la sección "createFloatingNote" en appShell() para la lógica de creación -->

```

---

## 📄 Archivo: `templates/partials/modal_categoria.html`
```html
<!-- templates/partials/modal_categoria.html -->
<div class="bg-[#1a1d26] border border-white/10 rounded-2xl shadow-2xl overflow-hidden fade-in-up"
     x-data="{ selectedIcon: 'folder' }">
    
    <!-- Header -->
    <div class="px-6 py-4 border-b border-white/5 flex justify-between items-center">
        <h3 class="text-sm font-bold text-white uppercase tracking-widest">Nueva Biblioteca</h3>
        <button @click="modalOpen = false" class="text-slate-500 hover:text-white">
            <i class="ph ph-x"></i>
        </button>
    </div>

    <form hx-post="/api/categorias/create" 
          hx-target="#contextual-sidebar" 
          hx-swap="innerHTML"
          @htmx:after-request="modalOpen = false"
          class="p-6">
        
        <!-- Input de Nombre -->
        <div class="mb-6">
            <label class="block text-[10px] text-slate-500 uppercase font-bold mb-2">Nombre de la Biblioteca</label>
            <input type="text" 
                   name="nombre" 
                   required 
                   autofocus
                   placeholder="Ej: INVESTIGACIÓN"
                   class="w-full bg-[#0f1117] border border-white/10 rounded-lg px-4 py-3 text-sm text-white focus:border-indigo-500 outline-none transition-all">
        </div>

        <!-- Selector de Iconos -->
        <div class="mb-8">
            <label class="block text-[10px] text-slate-500 uppercase font-bold mb-3">Identidad Visual (Icono)</label>
            <input type="hidden" name="icono" :value="selectedIcon">
            
            <div class="grid grid-cols-5 gap-3">
                {% set icons = [
                    'folder', 'code', 'graduation-cap', 'briefcase', 'castle-turret',
                    'tray', 'chalkboard-teacher', 'school', 'cpu', 'film-strip',
                    'music-notes', 'wrench', 'robot', 'factory', 'microscope'
                ] %}
                
                {% for icon in icons %}
                <button type="button" 
                        @click="selectedIcon = '{{ icon }}'"
                        :class="selectedIcon === '{{ icon }}' ? 'bg-indigo-500/20 border-indigo-500 text-indigo-400' : 'bg-[#0f1117] border-white/5 text-slate-600 hover:text-slate-300'"
                        class="w-10 h-10 flex items-center justify-center rounded-xl border transition-all">
                    <i class="ph-fill ph-{{ icon }} text-lg"></i>
                </button>
                {% endfor %}
            </div>
        </div>

        <!-- Botón Acción -->
        <button type="submit" 
                class="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl transition-all shadow-lg shadow-indigo-500/20 flex items-center justify-center gap-2 group">
            <span>Crear Biblioteca</span>
            <i class="ph ph-arrow-right transition-transform group-hover:translate-x-1"></i>
        </button>
    </form>
</div>
```

---

## 📄 Archivo: `templates/partials/modal_confirm_delete.html`
```html
<!-- templates/partials/modal_confirm_delete.html -->
<div class="w-full bg-[#1a1d26] border border-red-500/30 rounded-2xl shadow-2xl overflow-hidden fade-in-up"
     x-data="{ confirmationName: '', expectedName: '{{ obj_name }}' }">
    
    <!-- Header -->
    <div class="px-6 py-4 border-b border-red-500/10 bg-red-500/5 flex justify-between items-center">
        <div class="flex items-center gap-2 text-red-400">
            <i class="ph-fill ph-warning-octagon text-lg"></i>
            <h3 class="text-xs font-bold uppercase tracking-widest">Borrado de Seguridad</h3>
        </div>
        <button @click="modalOpen = false" class="text-slate-500 hover:text-white">
            <i class="ph ph-x"></i>
        </button>
    </div>

    <div class="p-8">
        <p class="text-sm text-slate-300 mb-2">Estás a punto de eliminar la {{ type }}:</p>
        <p class="text-lg font-bold text-white mb-4">"{{ obj_name }}"</p>
        
        <div class="p-4 bg-red-500/10 border border-red-500/20 rounded-xl mb-6">
            <p class="text-xs text-red-300 leading-relaxed">
                <i class="ph-bold ph-info mr-1"></i> {{ warning }}
            </p>
        </div>

        <div class="mb-8">
            <label class="block text-[10px] text-slate-500 uppercase font-bold mb-2">Escribe el nombre para confirmar:</label>
            <input type="text" 
                   x-model="confirmationName"
                   placeholder="Escribe el nombre aquí..."
                   class="w-full bg-[#0f1117] border border-white/10 rounded-lg px-4 py-3 text-sm text-white focus:border-red-500 outline-none transition-all">
        </div>

        <!-- Botón de Borrado Unificado -->
        <button hx-delete="{{ delete_url }}"
                {% if type == 'tema' %}
                    hx-target="#notebook-sidebar-container"
                    hx-swap="outerHTML"
                {% else %}
                    hx-target="#contextual-sidebar"
                    hx-swap="innerHTML"
                {% endif %}
                hx-indicator="#sidebar-indicator"
                :disabled="confirmationName !== expectedName"
                @click="modalOpen = false; aiLoading = true"
                @htmx:after-request="aiLoading = false"
                class="w-full py-4 bg-red-600 hover:bg-red-500 ...">
            <i class="ph ph-trash"></i>
            <span>Eliminar definitivamente</span>
        </button>
    </div>
</div>
```

---

## 📄 Archivo: `templates/partials/modal_confirm_edit.html`
```html
<!-- templates/partials/modal_confirm_edit.html -->
<div class="bg-[#1a1d26] border border-white/10 rounded-2xl shadow-2xl overflow-hidden fade-in-up">
    <div class="p-8 text-center">
        <!-- Icono animado sutil -->
        <div class="w-20 h-20 bg-indigo-500/10 rounded-full flex items-center justify-center mx-auto mb-6 border border-indigo-500/20">
            <i class="ph ph-pencil-line text-4xl text-indigo-400"></i>
        </div>
        
        <h3 class="text-xl font-bold text-white mb-2">¿Editar Nota?</h3>
        <p class="text-sm text-slate-400 mb-8 max-w-[280px] mx-auto">
            
        </p>

        <div class="flex gap-3">
            <button @click="modalOpen = false" 
                    class="flex-1 py-3 bg-white/5 hover:bg-white/10 text-slate-400 font-bold rounded-xl transition-all border border-white/5">
                Cancelar
            </button>
            
            <button @click="
                        mode = 'notebook';
                        activeNoteId = '{{ nota_id }}';
                        window.dispatchEvent(new CustomEvent('note-selected', { detail: { id: '{{ nota_id }}' } }));
                        modalOpen = false;
                    "
                    class="flex-1 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl transition-all shadow-lg shadow-indigo-500/20">
                Confirmar
            </button>
        </div>
    </div>
</div>
```

---

## 📄 Archivo: `templates/partials/modal_cuaderno.html`
```html
<!-- templates/partials/modal_cuaderno.html -->
<div class="bg-[#1a1d26] border border-white/10 rounded-2xl shadow-2xl overflow-hidden fade-in-up">
    <div class="px-6 py-4 border-b border-white/5 flex justify-between items-center">
        <h3 class="text-sm font-bold text-white uppercase tracking-widest">Nuevo Cuaderno</h3>
        <button @click="modalOpen = false" class="text-slate-500 hover:text-white">
            <i class="ph ph-x"></i>
        </button>
    </div>

    <form hx-post="/api/cuadernos/create" 
          hx-target="#contextual-sidebar" 
          hx-swap="innerHTML"
          hx-indicator="#sidebar-indicator"
          @submit="aiLoading = true"
          @htmx:after-request="modalOpen = false; aiLoading = false"
          class="p-6">
        
        <input type="hidden" name="cat_id" value="{{ cat_id }}">
        
        <div class="mb-6">
            <label class="block text-[10px] text-slate-500 uppercase font-bold mb-2">Nombre del Cuaderno</label>
            <input type="text" 
                   name="nombre" 
                   required 
                   autofocus
                   placeholder="Ej: Notas de Ingeniería"
                   class="w-full bg-[#0f1117] border border-white/10 rounded-lg px-4 py-3 text-sm text-white focus:border-indigo-500 outline-none transition-all">
        </div>

        <button type="submit" 
                class="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl transition-all shadow-lg shadow-indigo-500/20 flex items-center justify-center gap-2">
            <i class="ph ph-book-bookmark"></i>
            <span>Crear Cuaderno</span>
        </button>
    </form>
</div>
```

---

## 📄 Archivo: `templates/partials/modal_edit_categoria.html`
```html
<!-- templates/partials/modal_edit_categoria.html -->
<div class="bg-[#1a1d26] border border-white/10 rounded-2xl shadow-2xl overflow-hidden fade-in-up"
     x-data="{ selectedIcon: '{{ categoria.icono }}' }">
    
    <!-- Header -->
    <div class="px-6 py-4 border-b border-white/5 flex justify-between items-center">
        <h3 class="text-sm font-bold text-white uppercase tracking-widest">Editar Biblioteca</h3>
        <button @click="modalOpen = false" class="text-slate-500 hover:text-white">
            <i class="ph ph-x"></i>
        </button>
    </div>

    <form hx-patch="/api/categorias/{{ categoria.id }}" 
          hx-target="#contextual-sidebar" 
          hx-swap="innerHTML"
          hx-indicator="#sidebar-indicator"
          @submit="aiLoading = true"
          @htmx:after-request="modalOpen = false; aiLoading = false"
          class="p-6">
        
        <!-- Input de Nombre -->
        <div class="mb-6">
            <label class="block text-[10px] text-slate-500 uppercase font-bold mb-2">Nombre de la Biblioteca</label>
            <input type="text" 
                   name="nombre" 
                   value="{{ categoria.nombre }}"
                   required 
                   class="w-full bg-[#0f1117] border border-white/10 rounded-lg px-4 py-3 text-sm text-white focus:border-indigo-500 outline-none transition-all">
        </div>

        <!-- Selector de Iconos -->
        <div class="mb-8">
            <label class="block text-[10px] text-slate-500 uppercase font-bold mb-3">Identidad Visual (Icono)</label>
            <input type="hidden" name="icono" :value="selectedIcon">
            
            <div class="grid grid-cols-5 gap-3">
                {% set icons = [
                    'folder', 'code', 'graduation-cap', 'briefcase', 'castle-turret',
                    'tray', 'chalkboard-teacher', 'school', 'cpu', 'film-strip',
                    'music-notes', 'wrench', 'robot', 'factory', 'microscope'
                ] %}
                
                {% for icon in icons %}
                <button type="button" 
                        @click="selectedIcon = '{{ icon }}'"
                        :class="selectedIcon === '{{ icon }}' ? 'bg-indigo-500/20 border-indigo-500 text-indigo-400' : 'bg-[#0f1117] border-white/5 text-slate-600 hover:text-slate-300'"
                        class="w-10 h-10 flex items-center justify-center rounded-xl border transition-all">
                    <i class="ph-fill ph-{{ icon }} text-lg"></i>
                </button>
                {% endfor %}
            </div>
        </div>

        <!-- Botón de Acción Único -->
        <div class="flex flex-col gap-3">
            <button type="submit" 
                    class="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl transition-all shadow-lg shadow-indigo-500/20 flex items-center justify-center gap-2 group">
                <i class="ph ph-floppy-disk"></i>
                <span>Guardar Cambios</span>
            </button>
        </div>
    </form>
</div>
```

---

## 📄 Archivo: `templates/partials/modal_edit_cuaderno.html`
```html
<!-- templates/partials/modal_edit_cuaderno.html -->
<div class="bg-[#1a1d26] border border-white/10 rounded-2xl shadow-2xl overflow-hidden fade-in-up">
    <div class="px-6 py-4 border-b border-white/5 flex justify-between items-center">
        <h3 class="text-sm font-bold text-white uppercase tracking-widest">Editar Cuaderno</h3>
        <button @click="modalOpen = false" class="text-slate-500 hover:text-white">
            <i class="ph ph-x"></i>
        </button>
    </div>

    <form hx-patch="/api/cuadernos/{{ cuaderno.id }}" 
          hx-target="#contextual-sidebar" 
          hx-swap="innerHTML"
          hx-indicator="#sidebar-indicator"
          @submit="aiLoading = true"
          @htmx:after-request="modalOpen = false; aiLoading = false"
          class="p-6">
        
        <div class="mb-6">
            <label class="block text-[10px] text-slate-500 uppercase font-bold mb-2">Nombre del Cuaderno</label>
            <input type="text" 
                   name="nombre" 
                   value="{{ cuaderno.nombre }}"
                   required 
                   class="w-full bg-[#0f1117] border border-white/10 rounded-lg px-4 py-3 text-sm text-white focus:border-indigo-500 outline-none transition-all">
        </div>

        <button type="submit" 
                class="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl transition-all shadow-lg shadow-indigo-500/20 flex items-center justify-center gap-2">
            <i class="ph ph-floppy-disk"></i>
            <span>Guardar Cambios</span>
        </button>
    </form>
</div>
```

---

## 📄 Archivo: `templates/partials/modal_edit_tema.html`
```html
<!-- templates/partials/modal_edit_tema.html -->
<div class="bg-[#1a1d26] border border-white/10 rounded-2xl shadow-2xl overflow-hidden fade-in-up">
    <div class="px-6 py-4 border-b border-white/5 flex justify-between items-center">
        <h3 class="text-sm font-bold text-white uppercase tracking-widest">Editar Tema</h3>
        <button @click="modalOpen = false" class="text-slate-500 hover:text-white">
            <i class="ph ph-x"></i>
        </button>
    </div>

    <form hx-patch="/api/temas/{{ tema.id }}" 
          hx-target="#notebook-sidebar-container" 
          hx-swap="outerHTML"
          hx-indicator="#sidebar-indicator"
          @submit="aiLoading = true"
          @htmx:after-request="modalOpen = false; aiLoading = false"
          hx-on::after-request="aiLoading = false"
          class="p-6">
        
        <div class="mb-6">
            <label class="block text-[10px] text-slate-500 uppercase font-bold mb-2">Nombre del Tema</label>
            <input type="text" 
                   name="nombre" 
                   value="{{ tema.nombre }}"
                   required 
                   class="w-full bg-[#0f1117] border border-white/10 rounded-lg px-4 py-3 text-sm text-white focus:border-indigo-500 outline-none transition-all">
        </div>

        <button type="submit" 
                @click="modalOpen = false; aiLoading = true"
                class="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl transition-all shadow-lg shadow-indigo-500/20 flex items-center justify-center gap-2">
            <i class="ph ph-floppy-disk"></i>
            <span>Guardar Cambios</span>
        </button>
    </form>
</div>
```

---

## 📄 Archivo: `templates/partials/modal_eliminar_nota.html`
```html
<!-- templates/partials/modal_eliminar_nota.html -->
<div class="w-full max-w-sm mx-auto bg-[#1a1d26] border border-red-500/30 rounded-2xl shadow-2xl overflow-hidden fade-in-up">
    <div class="p-8 text-center">
        <!-- Icono de Alerta -->
        <div class="w-16 h-16 bg-red-500/10 rounded-full flex items-center justify-center mx-auto mb-4 border border-red-500/20">
            <i class="ph-bold ph-trash text-3xl text-red-500"></i>
        </div>
        
        <h3 class="text-lg font-bold text-white mb-2">¿Eliminar nota?</h3>
        <p class="text-xs text-slate-400 mb-8 leading-relaxed">
            Esta acción es irreversible. La nota <span class="text-slate-200 font-bold">"{{ nota.titulo }}"</span> desaparecerá de tu cerebro digital.
        </p>

        <!-- FORMULARIO HOMOLOGADO -->
        <form hx-delete="/inbox/eliminar/{{ nota.id }}"
              hx-swap="none"
              hx-on::after-request="aiLoading = false"
              @submit="modalOpen = false; aiLoading = true"
              @htmx:after-request="modalOpen = false; aiLoading = false">

            <div class="flex gap-3">
                <!-- Cancelar -->
                <button type="button" 
                        @click="modalOpen = false" 
                        class="flex-1 py-3 bg-white/5 hover:bg-white/10 text-slate-400 font-bold rounded-xl transition-all text-xs">
                    No, mantener
                </button>
                
                <!-- Confirmar -->
                <button type="submit"
                        @click="modalOpen = false; aiLoading = true" 
                        class="flex-1 py-3 bg-red-600 hover:bg-red-500 text-white font-bold rounded-xl transition-all shadow-lg shadow-red-900/20 text-xs">
                    Sí, eliminar
                </button>
            </div>
        </form>
    </div>
</div>
```

---

## 📄 Archivo: `templates/partials/modal_inbox_triaje.html`
```html
<!-- templates/partials/modal_inbox_triaje.html -->

{# 1. Preparamos la lista de destinos en una variable de Jinja para evitar errores de sintaxis en el HTML #}
{% set destinos_list = [] %}
{% for cat in categorias %}
    {% for cuad in cat.cuadernos %}
        {% if cuad.nombre != 'Inbox' %}
            {% for tema in cuad.temas %}
                {% set search_string = (cat.nombre ~ ' ' ~ cuad.nombre ~ ' ' ~ tema.nombre) | lower %}
                {% set _ = destinos_list.append({
                    'id': tema.id | string,
                    'tema': tema.nombre,
                    'cuaderno': cuad.nombre,
                    'categoria': cat.nombre,
                    'searchStr': search_string
                }) %}
            {% endfor %}
        {% endif %}
    {% endfor %}
{% endfor %}

<div class="w-full max-w-md bg-[#1a1d26] border border-white/10 rounded-2xl shadow-2xl overflow-hidden fade-in-up relative"
     x-data='{ 
        search: "",
        confirming: false,
        destinos: {{ destinos_list | tojson }},
        get filteredDestinos() {
            if (!this.search) return this.destinos;
            return this.destinos.filter(d => d.searchStr.includes(this.search.toLowerCase()));
        }
     }'>
    
    <!-- HEADER -->
    <div class="px-6 py-4 border-b border-white/5 flex justify-between items-center bg-[#13151b]">
        <div class="flex flex-col">
            <h3 class="text-[10px] font-bold text-indigo-400 uppercase tracking-[0.2em]">Mover Nota</h3>
            <p class="text-xs text-slate-300 font-medium truncate w-64">"{{ nota.titulo }}"</p>
        </div>
        <button @click="modalOpen = false" class="text-slate-500 hover:text-white transition-colors">
            <i class="ph ph-x text-lg"></i>
        </button>
    </div>

    <!-- BUSCADOR -->
    <div class="p-4 bg-[#0f1117] border-b border-white/5">
        <div class="relative">
            <i class="ph ph-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"></i>
            <input type="text" 
                   x-model="search"
                   placeholder="Buscar destino..." 
                   class="w-full bg-white/[0.03] border border-white/10 rounded-xl py-2.5 pl-10 pr-4 text-sm text-white focus:outline-none focus:border-indigo-500/50 transition-all"
                   autofocus>
        </div>
    </div>

    <!-- LISTA DE DESTINOS -->
    <div class="max-h-[400px] overflow-y-auto custom-scroll min-h-[120px]">
        
        <!-- Casos de error / Vacío -->
        <template x-if="destinos.length === 0">
            <div class="p-10 text-center">
                <p class="text-xs text-slate-500">No hay temas disponibles. Crea uno primero.</p>
            </div>
        </template>

        <template x-if="destinos.length > 0 && filteredDestinos.length === 0">
            <div class="p-10 text-center">
                <p class="text-xs text-slate-500">No hay coincidencias.</p>
            </div>
        </template>

        <!-- Lista Interactiva -->
        <div class="p-2 space-y-1">
            <template x-for="item in filteredDestinos" :key="item.id">
                <button type="button"
                        class="w-full text-left p-3 rounded-xl border border-transparent hover:border-indigo-500/30 hover:bg-indigo-500/5 transition-all group flex items-center justify-between"
                        @click="confirming = true; htmx.ajax('POST', '/inbox/mover/{{ nota.id }}', { values: { nuevo_tema_id: item.id } })"
                        @htmx:after-request="modalOpen = false; confirming = false">
                    
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center text-slate-500 group-hover:text-indigo-400">
                            <i class="ph-fill ph-hash"></i>
                        </div>
                        <div class="flex flex-col">
                            <span class="text-[11px] font-bold text-slate-200" x-text="item.tema"></span>
                            <span class="text-[9px] text-slate-500 uppercase tracking-wider">
                                <span x-text="item.categoria"></span> <i class="ph ph-caret-right text-[7px] mx-1"></i> <span x-text="item.cuaderno"></span>
                            </span>
                        </div>
                    </div>
                    <i class="ph ph-arrow-right text-slate-700 group-hover:text-indigo-500 transition-transform group-hover:translate-x-1"></i>
                </button>
            </template>
        </div>
    </div>

    <!-- FEEDBACK OVERLAY -->
    <div x-show="confirming" 
         class="absolute inset-0 bg-[#1a1d26]/90 backdrop-blur-sm z-50 flex flex-col items-center justify-center"
         x-cloak x-transition>
        <i class="ph-fill ph-check-circle text-indigo-500 text-5xl mb-2 animate-bounce"></i>
        <p class="text-sm font-bold text-white uppercase tracking-widest">Movido</p>
    </div>

</div>
```

---

## 📄 Archivo: `templates/partials/modal_tema.html`
```html
<!-- templates/partials/modal_tema.html -->
<div class="w-full max-w-md mx-auto bg-[#1a1d26] border border-white/10 rounded-2xl shadow-2xl overflow-hidden fade-in-up">
    
    <!-- Header -->
    <div class="px-6 py-4 border-b border-white/5 flex justify-between items-center">
        <h3 class="text-sm font-bold text-white uppercase tracking-widest">Nuevo Tema</h3>
        <button @click="modalOpen = false" class="text-slate-500 hover:text-white">
            <i class="ph ph-x"></i>
        </button>
    </div>

    <!-- Formulario de Creación -->
    <form hx-post="/api/temas/create" 
          hx-target="#notebook-sidebar-container" 
          hx-swap="outerHTML"
          hx-indicator="#sidebar-indicator"
          @submit="aiLoading = true"
          @htmx:after-request="modalOpen = false; aiLoading = false"
          hx-on::after-request="aiLoading = false"
          class="p-6">
        
        <!-- Campo oculto para vincular al cuaderno actual -->
        <input type="hidden" name="cuaderno_id" value="{{ cuaderno_id }}">
        
        <div class="mb-6">
            <label class="block text-[10px] text-slate-500 uppercase font-bold mb-2">Nombre del Tema</label>
            <input type="text" 
                   name="nombre" 
                   required 
                   autofocus
                   placeholder="Ej: Análisis de Requerimientos"
                   class="w-full bg-[#0f1117] border border-white/10 rounded-lg px-4 py-3 text-sm text-white focus:border-indigo-500 outline-none transition-all">
        </div>

        <!-- Botón de Acción -->
        <button type="submit" 
                @click="modalOpen = false; aiLoading = true"
                class="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl transition-all shadow-lg shadow-indigo-500/20 flex items-center justify-center gap-2 group">
            <i class="ph ph-plus-circle transition-transform group-hover:scale-110"></i>
            <span>Crear Tema</span>
        </button>
    </form>
</div>
```

---

## 📄 Archivo: `utils/migrar.py`
```py
import os
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select
from app.models import UsuarioDB, Categoria, Cuaderno, Tema, Anotacion

load_dotenv()

SOURCE_URL = os.getenv("DATABASE_URL_SUPABASE").replace("postgres://", "postgresql://", 1)
DEST_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)

dest_engine = create_engine(DEST_URL)

def clean_uuid(val):
    if val is None: return None
    s_val = str(val).strip()
    if not s_val or s_val == "" or s_val == "None": return None
    try:
        return uuid.UUID(s_val)
    except Exception:
        return None

def run_smart_migration():
    # user_mapping almacenará { id_supabase: id_vps }
    user_mapping = {} 

    print("🔌 Conectando al origen (Supabase)...")
    try:
        src_conn = psycopg2.connect(SOURCE_URL)
        src_cur = src_conn.cursor(cursor_factory=RealDictCursor)
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    try:
        with Session(dest_engine) as dest_session:
            print("\n🔍 Paso 1: Mapeando identidades de usuario...")
            # Los usuarios usualmente se pueden leer porque son la base de la autenticación
            src_cur.execute("SELECT * FROM usuarios")
            src_users = src_cur.fetchall()
            
            for s_user in src_users:
                old_id = clean_uuid(s_user['id'])
                stmt = select(UsuarioDB).where(UsuarioDB.email == s_user['email'])
                d_user = dest_session.exec(stmt).first()

                if d_user:
                    user_mapping[old_id] = d_user.id
                    print(f"   - Usuario: {s_user['email']} ({old_id} -> {d_user.id})")
                else:
                    print(f"   - Nuevo usuario: {s_user['email']}. Migrando cuenta...")
                    new_user = UsuarioDB(
                        id=old_id, email=s_user['email'], 
                        hashed_password=s_user['hashed_password'], 
                        nombre=s_user['nombre'], created_at=s_user['created_at']
                    )
                    dest_session.add(new_user)
                    user_mapping[old_id] = old_id
            
            dest_session.commit()

            # PLAN DE MIGRACIÓN POR USUARIO (Para bypass de RLS)
            migration_plan = [
                (Categoria, "categorias", "Categorías"),
                (Cuaderno, "cuadernos", "Cuadernos"),
                (Tema, "temas", "Temas"),
                (Anotacion, "anotaciones", "Anotaciones")
            ]

            for model_class, table_name, label in migration_plan:
                print(f"\n📦 Migrando {label}...")
                migrated_count = 0
                already_exists_count = 0
                
                # AXIOMA: Iteramos por cada usuario mapeado para "engañar" al RLS
                for old_uid, new_uid in user_mapping.items():
                    try:
                        # 1. Configuramos la sesión de Postgres con el ID del usuario de Supabase
                        src_cur.execute(f"SET app.current_user_id = '{old_uid}';")
                        
                        # 2. Pedimos los datos de ese usuario específicamente
                        src_cur.execute(f"SELECT * FROM {table_name} WHERE user_id = %s", (str(old_uid),))
                        rows = src_cur.fetchall()
                        
                        if not rows:
                            continue

                        for row in rows:
                            data = dict(row)
                            curr_id = clean_uuid(data.get('id'))
                            
                            if not curr_id: continue

                            # 3. Verificar si el registro ya existe en el VPS
                            if dest_session.get(model_class, curr_id):
                                already_exists_count += 1
                                continue

                            # 4. Re-mapear identidades
                            data['id'] = curr_id
                            data['user_id'] = new_uid # El ID del VPS
                            
                            if 'categoria_id' in data: data['categoria_id'] = clean_uuid(data['categoria_id'])
                            if 'cuaderno_id' in data: data['cuaderno_id'] = clean_uuid(data['cuaderno_id'])
                            if 'tema_id' in data: data['tema_id'] = clean_uuid(data['tema_id'])

                            # Limpiar Tags
                            if 'tags' in data:
                                t = data['tags']
                                if t is None: data['tags'] = []
                                elif isinstance(t, str): data['tags'] = t.strip('{}').split(',') if t.strip('{}') else []

                            # Insertar
                            try:
                                new_item = model_class(**data)
                                dest_session.add(new_item)
                                migrated_count += 1
                            except Exception as e:
                                dest_session.rollback()
                                print(f"      ⚠️ Error en registro {curr_id}: {e}")

                        dest_session.commit()
                        
                    except Exception as e:
                        print(f"   ⚠️ Error leyendo {label} para usuario {old_uid}: {e}")
                        src_conn.rollback()

                print(f"   ✅ {migrated_count} migrados.")
                if already_exists_count > 0:
                    print(f"   ℹ️  {already_exists_count} ya existían en destino.")

    except Exception as e:
        print(f"❌ Error crítico: {e}")
    finally:
        src_cur.close()
        src_conn.close()
        print("\n🚀 Proceso finalizado.")

if __name__ == "__main__":
    run_smart_migration()
```

---

