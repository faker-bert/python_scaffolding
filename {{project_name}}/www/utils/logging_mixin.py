import logging
from logging import Handler, Logger, StreamHandler
import loguru
import types

from app.configuration import conf


class InterceptHandler(logging.Handler):
    
    def emit(self, record: logging.LogRecord):
        # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
        logger_opt = loguru.logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())
        

def func(log_level):
    def wrapper(self, msg, *args, **kwargs):
        if self.isEnabledFor(log_level):
            self._log(log_level, msg, args, **kwargs)
    
    return wrapper


class LoggingMixin:
    """Convenience super-class to have a logger configured with the class name"""
    
    _log: Logger or None = None
    loguru_handler = InterceptHandler()
    loguru_handler.setFormatter(conf.get('logging', 'log_format'))
    custom_log_level = conf.getdict('logging', 'custom_logging_level')
    
    def __init__(self, context=None):
        self._set_context(context)
            
    @property
    def log(self) -> Logger:
        """Returns a logger."""
        if self._log is None:
            self._log = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)
            # self._log.addHandler(self.loguru_handler)
            logging.basicConfig(handlers=[self.loguru_handler], level=logging.INFO)
            for level_name, level in self.custom_log_level.items():
                logging.addLevelName(level, level_name)
    
                setattr(self._log, level_name.lower(), types.MethodType(func(level), self._log))
                
        return self._log
    
    def _set_context(self, context):  # todo ?
        """load handler"""
        if context is not None:
            set_context(self.log, context)
    
    def __getattr__(self, item):
        try:
            object.__getattribute__(self, item)
        except AttributeError:
            return getattr(self.log, item)
        return object.__getattribute__(self, item)


def set_context(logger: logging.Logger, context):
    _logger = logger


normal_logger = LoggingMixin()

if __name__ == '__main__':
    normal_logger.log.success('123')
    normal_logger.success('123')
    