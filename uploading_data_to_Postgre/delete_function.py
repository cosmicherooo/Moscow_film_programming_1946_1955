from creating_db_template_in_postgres import *
from creating_tables_db import *
from creating_execution_commands import *
import sys
from functools import wraps
import pandas as pd
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        wrapper.total_time += duration
        print(f"Execution time: {duration}")
        return result

    wrapper.total_time = 0
    return wrapper


@timer
def deleting_by_id(hostname=hostname,
                   database=database,
                   username=username,
                   password=password,
                   port_id=port_id,
                   table_name='Person',
                   column_id_name='person_id',
                   row_id_list=['per0000001'],
                   path_to_file='/Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/'):

    if len(row_id_list) == 0:
        print(f'You added an empty list as row_id_list arguement. Function was terminated')
        sys.exit("Exiting the program.")

    try:
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password,
                                port=port_id)
        cur = conn.cursor()

        sql = 'DELETE FROM ' + table_name + ' WHERE ' + column_id_name + ' = %s'

        list_of_deleted_rows = []
        list_of_undeleted_rows = []

        for id in row_id_list:
            try:
                cur.execute(sql, (id,))
                list_of_deleted_rows.append(id)

            except (Exception, psycopg2.DatabaseError) as error:
                list_of_undeleted_rows.append(id)
                print(error)

        conn.commit()
        cur.close()
        conn.close()

    except:
        print("Connection was unsuccessful!")


    creating_path = path_to_file + table_name + '_deleting' + '.txt'
    file = open(creating_path, 'w')
    if len(list_of_undeleted_rows) == 0:
        file.write('All rows were successfully deleted from your database!' + "\n")
        file.close()
        print('All rows were successfully deleted from your database!')
    else:
        for item in list_of_undeleted_rows:
            file.write('Rows with these values could not be deleted from your database!\n')
            file.write(item + "\n")
        file.close()
        print(f'Rows with certain values could not be deleted from your database! Look them up in output txt-file!\n'
              f'Path to your file is:{creating_path}')

    return len(list_of_undeleted_rows), (str(len(list_of_undeleted_rows) / len(row_id_list)) + ' %')

