const PrivateTooltip = {
    bind(root = document) {
        const tooltips = root.querySelectorAll('[data-private-tooltip]');

        tooltips.forEach((tooltip) => {
            this.bindOne(tooltip);
        });
    },

    bindOne(tooltip) {
        const trigger = tooltip.querySelector('.private-tooltip__trigger');
        const panel = tooltip.querySelector('.private-tooltip__panel');

        if (!trigger || !panel) {
            return;
        }

        const margin = 8;

        const positionPanel = () => {
            panel.classList.remove('is-above');

            const triggerRect = trigger.getBoundingClientRect();
            const panelRect = panel.getBoundingClientRect();

            let top = triggerRect.bottom + margin;
            let left = triggerRect.left;

            if (left + panelRect.width > window.innerWidth - margin) {
                left = window.innerWidth - panelRect.width - margin;
            }

            if (left < margin) {
                left = margin;
            }

            if (top + panelRect.height > window.innerHeight - margin) {
                top = triggerRect.top - panelRect.height - margin;
                panel.classList.add('is-above');
            }

            panel.style.top = `${top}px`;
            panel.style.left = `${left}px`;
        };

        const show = () => {
            panel.hidden = false;

            requestAnimationFrame(() => {
                positionPanel();
                panel.classList.add('is-visible');
            });
        };

        const hide = () => {
            panel.classList.remove('is-visible', 'is-above');
            panel.hidden = true;
            panel.style.top = '';
            panel.style.left = '';
        };

        trigger.addEventListener('mouseenter', show);
        trigger.addEventListener('focus', show);
        trigger.addEventListener('mouseleave', hide);
        trigger.addEventListener('blur', hide);
    },
};

window.PrivateTooltip = PrivateTooltip;
