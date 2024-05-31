from creating_db_template_in_postgres import *
from creating_tables_db import *

if __name__ == '__main__':

    conn = psycopg2.connect(dbname='postgres',
                            user=username,
                            host=hostname,
                            password=password)

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()

    try:
        cur.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(
            sql.Identifier(database))
            )
        print(f'{database} has been successfully dropped!')

    except:
        print(f'Your database: {database} - is non-existent')

    cur.close()
    conn.close()
