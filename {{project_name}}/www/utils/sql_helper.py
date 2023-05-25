"""
description: 项目需求不确定, 直接使用sqlalchemy会带来较多不便, 所以采取sql语句生成的方式进行
"""
from typing import List, Optional, Union
from functools import wraps
import inspect
import sys

from app.utils.singleton import singleton
from app.utils.logging_mixin import LoggingMixin, normal_logger
from app.configuration import conf
from app.settings import global_settings


def sql_debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            sql = func(*args, **kwargs)
            
            if global_settings.sql_debug_mode or conf.getboolean('logging', 'sql_debug', fallback=False):
                normal_logger.log.debug(f'func: {func.__name__} -- params: {args} -- kw params: {kwargs}')
                normal_logger.log.debug(f'generate sql: {sql}')
        except Exception as error:
            normal_logger.log.error(f'func: {func.__name__} -- params: {args} -- kw params: {kwargs}')
            normal_logger.log.error(error)
            f_back = sys._getframe()
            for _ in range(global_settings.sql_trace_back_epoch):
                if f_back:
                    f_back = f_back.f_back
                    if f_back:
                        normal_logger.log.error(f'trace: {f_back}')
                else:
                    break
                
            return 'select 1;'
        return sql
    
    return wrapper


@singleton
class SQLHelper(LoggingMixin):
    
    def __init__(self, execute_immediately: bool = False):
        """
        :param execute_immediately: without transactions
        """
        super().__init__()
        self.execute_immediately = execute_immediately
            
    @sql_debug
    def insert(self, table: str, data: List[dict]):
        keys = data[0].keys()
        values = [
            '(' + ','.join([
                str(record.get(key, ''))
                if isinstance(record.get(key, ''), int) or isinstance(record.get(key, ''), float)
                else f"'{record.get(key, '')}'"
                for key in keys]) + ')'
            for record in data
        ]
        
        insert_sql = f'insert into {table}({",".join(keys)}) ' \
                     f'values {",".join(values)}'
        
        if self.execute_immediately:
            self.execute(insert_sql)
        
        return insert_sql
    
    @sql_debug
    def select(self,
               table: str, fields: Union[List[str], str],
               limit: Optional[int] = None, offset: Optional[int] = None,
               order_by: Optional[Union[list, str]] = None,
               additional_condition: Optional[dict] = None,
               **condition):
        fields = fields if isinstance(fields, list) else [fields]
        check_filed = [1 for field in fields if not isinstance(field, str)]
        if check_filed:
            raise ValueError(f"Fields' type must List[str], fields: {fields}")
        select_sql = f'select {",".join(fields)} from {table} '
        if condition:
            select_sql += self._generate_where_clause(condition)
        if additional_condition:
            if 'where' in select_sql:
                select_sql += self._generate_where_clause(additional_condition)[5:]
            else:
                select_sql += self._generate_where_clause(additional_condition)
        if limit:
            select_sql += f'limit {limit} '
        if offset:
            select_sql += f'offset {offset} '
        if order_by:
            select_sql += f'order by {",".join(order_by) if isinstance(order_by, list) else order_by}'
        return select_sql
    
    @sql_debug
    def update(self, table: str, change_data: dict, situation: dict):
        change_data_map = [
            key + ' = ' + (str(value) if not isinstance(value, str) else f"'{value}'")
            for key, value in change_data.items()
        ]
        # limit_situation = [f'{key} in {str(tuple(value if isinstance(value, list) else [value]))}'
        # # + (")" if isinstance(value, int) or isinstance(value[0], int) or len(value) == 1 else "')")
        #                    for key, value in situation.items()]
        update_sql = f'update {table} ' \
                     f'set {" ".join(change_data_map)} ' \
                     + self._generate_where_clause(situation)
        if self.execute_immediately:
            self.execute(update_sql)
        return update_sql
    
    @sql_debug
    def _generate_where_clause(self, condition: dict):
        condition = [f'{key} in {str(tuple(value if isinstance(value, list) else [value]))}'
                     # + (")" if isinstance(value, int) or isinstance(value[0], int) or len(value) == 1 else "')")
                     for key, value in condition.items()]
        return f'where {" and ".join(condition).replace(",)", ")")} '
    
    @sql_debug
    def execute(self, sql: str):
        ...


sql_helper: SQLHelper = SQLHelper()


if __name__ == '__main__':
    helper = SQLHelper()
    helper.update(
        table='table',
        change_data={'s': 'd'},
        situation={'d': [1, 2],
                   'asd': 2,
                   'dsd': ['1', '2'],
                   'as': 'k'
                   }
    )
    helper.insert(
        table='s',
        data=[
            {'d': [1, 2],
             'asd': 2,
             'dsd': ['1', '2'],
             'as': 'k'
             },
            {'d': [1, 2],
             'asd': 2,
             'dsd': ['1', '2'],
             'as': 'k'
             }
        ]
    )
    
    helper.select(
        'table',
        '2',
        offset=3,
        limit=4,
        d=[1, 2],
        asd=2,
        dsd=['1', '2'],
        ashj='k'
    )

    print(                sql_helper.select(
                    table='apollo_table_priority_config',
                    fields=['level', 'evolve_fields'],
                    order_by='level'
                ))