from creating_db_template_in_postgres import *
from creating_tables_db import *


def drop_table(hostname=hostname,
               database=database,
               username=username,
               password=password,
               port_id=port_id,
               table_name='Person'):

    conn = psycopg2.connect(host=hostname,
                            dbname=database,
                            user=username,
                            password=password,
                            port=port_id)

    cur = conn.cursor()

    try:
        sql_drop = '''DROP TABLE ''' + table_name
        cur.execute(sql_drop)
        conn.commit()
        print(f'{table_name} is dropped!')
    except:
        print(f'{table_name} is not present in your database!')

    cur.close()
    conn.close()



if __name__ == '__main__':
    drop_table(table_name=str(input()))
