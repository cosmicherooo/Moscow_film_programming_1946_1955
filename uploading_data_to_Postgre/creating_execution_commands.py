from creating_db_template_in_postgres import *
from creating_tables_db import *

tables_insertion_commands = {}

for i in range(0, len(table_names_list)):
    table_name = table_names_list[i]
    values_names = ', '.join([s[0] for s in variables_in_tables[i]])

    qmarks = ','.join('%s' for s in variables_in_tables[i])

    beginning_of_insert_statement = "INSERT INTO " + table_name + '(%s) VALUES (%s);'
    insert_statement = beginning_of_insert_statement % (values_names, qmarks)

    tables_insertion_commands["{0}".format(table_name)] = insert_statement


