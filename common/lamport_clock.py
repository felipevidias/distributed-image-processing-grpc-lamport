from threading import Lock


class LamportClock:
    """Relógio lógico de Lamport.

    Regras usadas:
    1. Antes de um evento local ou envio de mensagem: C = C + 1.
    2. Ao receber mensagem com timestamp T: C = max(C, T) + 1.
    """

    def __init__(self, node_id: str):
        self.node_id = node_id
        self._time = 0
        self._lock = Lock()

    def tick(self) -> int:
        """Incrementa o relógio para evento local/envio."""
        with self._lock:
            self._time += 1
            return self._time

    def update(self, received_time: int) -> int:
        """Atualiza o relógio ao receber uma mensagem."""
        with self._lock:
            self._time = max(self._time, int(received_time)) + 1
            return self._time

    def value(self) -> int:
        with self._lock:
            return self._time

    def log(self, event: str) -> None:
        print(f"[Lamport={self.value():03d}] [{self.node_id}] {event}", flush=True)
