# patch_rq_worker.py
from rq_win.worker import WindowsWorker as BaseWindowsWorker


class PatchedWindowsWorker(BaseWindowsWorker):
    def __init__(self, *args, worker_ttl=None, **kwargs):
        # Entferne den Parameter worker_ttl, falls vorhanden
        if 'worker_ttl' in kwargs:
            del kwargs['worker_ttl']
        super().__init__(*args, **kwargs)
