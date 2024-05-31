from creating_db_template_in_postgres import *
from creating_tables_db import *
from function_drop_table import *

# скрипт удаляет все таблицы из базы данных

for table_name in table_names_list:
    drop_table(table_name=table_name)