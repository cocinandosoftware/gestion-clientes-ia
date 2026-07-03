class PrinceTrace:
    """Trazador didáctico del flujo. Solo escribe en terminal; ver regla 05-prince-terminal-tracing."""

    def __init__(self, enabled=False):
        self.enabled = enabled
        self.steps = []
        self._counter = 0

    @classmethod
    def from_settings(cls):
        from django.conf import settings

        return cls(enabled=settings.IA_PRINCE_ENABLED)

    def step(self, title, detail=''):
        if not self.enabled:
            return

        self._counter += 1
        entry = {
            'step': self._counter,
            'title': title,
            'detail': str(detail) if detail else '',
        }
        self.steps.append(entry)
        self._print_step(entry)

    def _print_step(self, entry):
        line = f'[Prince] Paso {entry["step"]}: {entry["title"]}'
        if entry['detail']:
            line += f' — {entry["detail"]}'
        print(line, flush=True)

    def as_list(self):
        return list(self.steps)
