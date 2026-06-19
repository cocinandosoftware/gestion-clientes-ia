const PrivateAiPrompt = {
    popup: null,
    form: null,
    openButton: null,
    closeButton: null,
    errorBox: null,
    successBox: null,
    submitButton: null,
    hintElement: null,
    messageField: null,

    getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find((row) => row.startsWith('csrftoken='));

        if (!cookieValue) {
            return '';
        }

        return cookieValue.split('=')[1];
    },

    showFeedback(element, message, type) {
        if (!element) {
            return;
        }

        element.hidden = false;
        element.textContent = message;
        element.className = `private-ai-prompt__feedback private-ai-prompt__feedback--${type}`;
    },

    hideFeedback(element) {
        if (!element) {
            return;
        }

        element.hidden = true;
        element.textContent = '';
    },

    configureFromButton(button) {
        if (!this.form || !button) {
            return;
        }

        const promptUrl = button.dataset.promptUrl || '';
        this.form.dataset.promptUrl = promptUrl;

        if (this.messageField && button.dataset.promptPlaceholder) {
            this.messageField.placeholder = button.dataset.promptPlaceholder;
        }

        if (this.hintElement && button.dataset.promptHint) {
            this.hintElement.textContent = button.dataset.promptHint;
        }
    },

    open(button) {
        if (!this.popup) {
            return;
        }

        this.openButton = button;
        this.configureFromButton(button);
        this.hideFeedback(this.errorBox);
        this.hideFeedback(this.successBox);

        this.popup.hidden = false;
        document.body.classList.add('private-ai-prompt-open');

        if (button) {
            button.setAttribute('aria-expanded', 'true');
        }

        if (this.messageField) {
            this.messageField.focus();
        }
    },

    close() {
        if (!this.popup) {
            return;
        }

        this.popup.hidden = true;
        document.body.classList.remove('private-ai-prompt-open');

        if (this.openButton) {
            this.openButton.setAttribute('aria-expanded', 'false');
            this.openButton = null;
        }
    },

    bindOpenButtons() {
        document.querySelectorAll('.private-ai-prompt__open').forEach((button) => {
            button.addEventListener('click', () => {
                this.open(button);
            });
        });
    },

    bindForm() {
        if (!this.form) {
            return;
        }

        this.form.addEventListener('submit', async (event) => {
            event.preventDefault();

            this.hideFeedback(this.errorBox);
            this.hideFeedback(this.successBox);

            const message = this.messageField?.value.trim() || '';
            const promptUrl = this.form.dataset.promptUrl || '';

            if (!message) {
                this.showFeedback(this.errorBox, 'Escribe un mensaje antes de enviar.', 'error');
                return;
            }

            if (!promptUrl) {
                this.showFeedback(this.errorBox, 'No se pudo enviar el mensaje.', 'error');
                return;
            }

            if (this.submitButton) {
                this.submitButton.disabled = true;
                this.submitButton.classList.add('is-loading');
            }

            PrivateLoader.show('Enviando mensaje...');

            try {
                const formData = new FormData();
                formData.append('message', message);

                const response = await fetch(promptUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCsrfToken(),
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: formData,
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    if (this.messageField) {
                        this.messageField.value = '';
                    }

                    this.showFeedback(
                        this.successBox,
                        data.message || 'Gracias por tu mensaje.',
                        'success',
                    );
                    return;
                }

                const errors = data.errors || ['No se pudo enviar el mensaje.'];
                this.showFeedback(this.errorBox, errors.join(' '), 'error');
            } catch (error) {
                this.showFeedback(this.errorBox, 'Error de conexión. Inténtalo de nuevo.', 'error');
            } finally {
                PrivateLoader.hide();

                if (this.submitButton) {
                    this.submitButton.disabled = false;
                    this.submitButton.classList.remove('is-loading');
                }
            }
        });
    },

    init() {
        this.popup = document.getElementById('private-ai-prompt');
        this.form = document.getElementById('private-ai-prompt-form');
        this.closeButton = document.getElementById('private-ai-prompt-close');
        this.errorBox = document.getElementById('private-ai-prompt-errors');
        this.successBox = document.getElementById('private-ai-prompt-success');
        this.submitButton = document.getElementById('private-ai-prompt-submit');
        this.hintElement = document.getElementById('private-ai-prompt-hint');
        this.messageField = document.getElementById('private-ai-prompt-message');

        if (!this.popup || !this.form) {
            return;
        }

        this.closeButton?.addEventListener('click', () => {
            this.close();
        });

        this.popup.addEventListener('click', (event) => {
            if (event.target === this.popup) {
                this.close();
            }
        });

        this.bindOpenButtons();
        this.bindForm();
    },
};

window.PrivateAiPrompt = PrivateAiPrompt;

document.addEventListener('DOMContentLoaded', () => {
    PrivateAiPrompt.init();
});
