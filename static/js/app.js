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