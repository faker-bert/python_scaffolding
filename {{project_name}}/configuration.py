import os
from configparser import ConfigParser
from typing import Optional, Any
import logging
from {{project_name}}.utils.module_importer import import_string

log = logging.getLogger(__name__)


class {{project_name}}ConfigParser(ConfigParser):

    """Custom Woflow Configparser supporting defaults and deprecated options"""


    # This method transforms option names on every read, get, or set operation.
    # The default converts the name to lowercase.
    # This also means that when a configuration file gets written,
    # all keys will be lowercase. Override this method if that’s unsuitable.
    optionxform = lambda self, option: option

    def __init__(self, default_config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if default_config is None:
            ...
        self.{{project_name}}_defaults = ConfigParser(*args, **kwargs)

        if default_config is not None:
            self.{{project_name}}_defaults.read_string(default_config)

    def get(self, section: str, key: str, **kwargs)->Optional[str]:
        # get value base on section and key
        section = str(section).lower()
        key = str(key).lower()

        option = os.environ.get(f'{{project_name}}_{section}_{key}', None) # self._get_enviroment_variables(section, key)
        if option:
            return option
        return self._get_option_from_cfg_file(section, key, **kwargs)

    def _get_option_from_cfg_file(self, section, key, **kwargs):
        if self.{{project_name}}_defaults.has_option(section, key) or 'fallback' in kwargs:
            # 待定
            return self.{{project_name}}_defaults.get(section, key, **kwargs)
            # return expand_env_var(self.airflow_defaults.get(section, key, **kwargs))

        else:
            log.warning("<section/key> [%s/%s] not found in config", section, key)
            return None

    def _get_enviroment_variables(self, section, key)->Optional[str]:
        option = self._get_env_var_option(section, key)
        return option if option else None

    def _get_env_var_option(self, section, key)->Optional[str]:
        # todo 预留
        env_key = f'{{project_name}}_{section}_{key}'
        if env_key in os.environ:
            return os.environ[env_key]
        return None

    def getint(self, section, key, **kwargs)->int:
        val = self.get(section, key, **kwargs)
        try:
            return int(val)
        except ValueError:
            log.warning(
                f'Failed to convert value to int. Please check "{key}" key in "{section}" section. '
                f'Current value: "{val}".'
            )
        return 0

    def getfloat(self, section, key, **kwargs)->float:
        val = self.get(section, key, **kwargs)
        try:
            return float(val)
        except ValueError:
            log.warning(
                f'Failed to convert value to int. Please check "{key}" key in "{section}" section. '
                f'Current value: "{val}".'
            )
        return 0.0

    def getboolean(self, section, key, **kwargs)->bool:
        val = str(self.get(section, key, **kwargs)).lower().strip()
        if val in ('t', 'true', '1'):
            return True
        elif val in ('f', 'false', '0'):
            return False

    def getimport(self, section, key, **kwargs)->Any:
        full_path = conf.get(section=section, key=key, **kwargs)
        try:
            return import_string(full_path)
        except ImportError as e:
            log.error(e)
            return None

    def has_option(self, section: str, option: str) -> bool:
        try:
            # Using self.get() to avoid reimplementing the priority order
            # of config variables (env, config, cmd, defaults)
            # UNSET to avoid logging a warning about missing values
            val = self.get(section, option, fallback=None)
            if val:
                return True
            return False
        except:
            return False

def initialize_config()->{{project_name}}ConfigParser:
    # default_config = '{{project_name}}.cfg'

    with open(os.path.join(os.path.dirname(__file__), '{{project_name}}.cfg'), 'r') as file:
        default_config = file.read()
    local_config ={{project_name}}ConfigParser(default_config)

    return local_config


conf = initialize_config()


if __name__ == '__main__':
    # print(conf.get('webserver', 'port'))
    # print(conf.get('webserver', 'po123rt'))
    # import os.path
    # print(os.path.expandvars('23wer'))
    print(conf.has_option('webserver', 'web_server_port'))
    print(conf.getint('webserver', 'sd', fallback='2we8383'))
