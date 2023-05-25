from sqlalchemy.orm import Session as SASession
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import URL, Engine
from typing import Callable
from typing import Optional, List
from pydantic import BaseSettings, Field, validator, root_validator, DirectoryPath, IPvAnyAddress, HttpUrl, Extra
from typing import Dict, Any, Tuple
import os
import importlib
from pathlib import Path
from pydantic.env_settings import SettingsSourceCallable
import psycopg2
import inspect
from psycopg2.extras import RealDictCursor
import uuid


class AutoSettings(BaseSettings):
    module_home: Optional[DirectoryPath] = None
    
    @root_validator
    def set_home(cls, values):
        values['module_home'] = os.path.dirname(Path(importlib.util.find_spec(cls.__module__).origin).resolve())
        return values
    
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        env_file_encoding = 'utf-8'
        extra = 'allow'
        
        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return (
                init_settings,
                env_settings,
                file_secret_settings
            )
        
        
class GlobalSettings(AutoSettings):
    HOME: DirectoryPath = os.path.dirname(os.path.dirname(__file__))