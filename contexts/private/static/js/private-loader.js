const PrivateLoader = {
    element: null,
    textElement: null,
    defaultMessage: 'Cargando...',

    init() {
        if (this.element) {
            return;
        }

        const existing = document.getElementById('private-loader');

        if (existing) {
            this.element = existing;
            this.textElement = document.getElementById('private-loader-text');
            return;
        }

        const overlay = document.createElement('div');
        overlay.id = 'private-loader';
        overlay.className = 'private-loader-overlay';
        overlay.hidden = true;
        overlay.setAttribute('role', 'status');
        overlay.setAttribute('aria-live', 'polite');
        overlay.setAttribute('aria-busy', 'false');
        overlay.innerHTML = `
            <div class="private-loader__content">
                <div class="private-loader__spinner" aria-hidden="true"></div>
                <p id="private-loader-text" class="private-loader__text">${this.defaultMessage}</p>
            </div>
        `;

        document.body.appendChild(overlay);
        this.element = overlay;
        this.textElement = overlay.querySelector('#private-loader-text');
    },

    show(message) {
        this.init();

        if (!this.element) {
            return;
        }

        if (this.textElement) {
            this.textElement.textContent = message || this.defaultMessage;
        }

        this.element.hidden = false;
        this.element.setAttribute('aria-busy', 'true');
        document.body.classList.add('private-loader-active');
    },

    hide() {
        this.init();

        if (!this.element) {
            return;
        }

        this.element.hidden = true;
        this.element.setAttribute('aria-busy', 'false');
        document.body.classList.remove('private-loader-active');
    },
};

window.PrivateLoader = PrivateLoader;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => PrivateLoader.init());
} else {
    PrivateLoader.init();
}
