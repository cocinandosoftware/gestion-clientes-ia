const PrivateLoader = {
    element: null,
    textElement: null,
    defaultMessage: 'Cargando...',

    init() {
        this.element = document.getElementById('private-loader');
        this.textElement = document.getElementById('private-loader-text');
    },

    show(message) {
        if (!this.element) {
            this.init();
        }

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
        if (!this.element) {
            this.init();
        }

        if (!this.element) {
            return;
        }

        this.element.hidden = true;
        this.element.setAttribute('aria-busy', 'false');
        document.body.classList.remove('private-loader-active');
    },
};

window.PrivateLoader = PrivateLoader;
