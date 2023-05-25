import logging
import time
logger = logging.getLogger(__name__)


class Timer:
    _start_time: float or None = None
    duration: float or None = None
    
    def __init__(self):
        ...
    
    def __enter__(self):
        return self.start()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()
    
    def start(self):
        self._start_time = time.monotonic()
        return self
    
    def end(self):
        self.duration = time.monotonic() - self._start_time
        