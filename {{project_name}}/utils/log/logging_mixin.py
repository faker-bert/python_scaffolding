import logging
from logging import Handler, Logger, StreamHandler
import loguru


class InterceptHandler(logging.Handler):
    
    def emit(self, record: logging.LogRecord):
        # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
        logger_opt = loguru.logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


class LoggingMixin:
    """Convenience super-class to have a logger configured with the class name"""
    
    _log: Logger or None = None
    loguru_handler = InterceptHandler()
    loguru_handler.setFormatter(LOG_FORMAT)
    
    def __init__(self, context=None):
        self._set_context(context)
    
    @property
    def log(self) -> Logger:
        """Returns a logger."""
        if self._log is None:
            self._log = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)
            # self._log.addHandler(self.loguru_handler)
            logging.basicConfig(handlers=[self.loguru_handler], level=2)
        return self._log
    
    def _set_context(self, context):  # todo ?
        """load handler"""
        if context is not None:
            set_context(self.log, context)


def set_context(logger: logging.Logger, context):
    _logger = logger


