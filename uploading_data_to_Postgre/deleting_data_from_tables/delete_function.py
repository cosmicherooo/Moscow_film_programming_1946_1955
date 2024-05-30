from creating_db_template_in_postgres import *
from creating_tables_db import *
from creating_execution_commands import *
import pandas as pd


def deleting_by_id(hostname='localhost',
                   database='Film_Programming_Moscow_1946_1955',
                   username='postgres',
                   password='85FibanironibI27',
                   port_id=5432,
                   table_name = 'Person',
                   column_id_name = 'person_id',
                   row_id_list = ['per0000001']):

    try:
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password,
                                port=port_id)
        cur = conn.cursor()

    except:
        print("Connection was unsuccessful!")

    sql = 'DELETE FROM ' + table_name + ' WHERE ' + column_id_name + ' = %s'

    list_of_deleted_rows = []

    for id in row_id_list:
        try:
            cur.execute(sql, (id,))
            list_of_deleted_rows.append(id)


        except (Exception, psycopg2.DatabaseError) as error:
            print(error)



    conn.commit()
    cur.close()
    conn.close()

    return list_of_deleted_rows

