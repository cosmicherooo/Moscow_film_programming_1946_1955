import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


hostname = 'localhost'
database = 'Film_Programming_Moscow_1946_1955'
username = 'postgres'
password = '***********'
port_id = 5432

if __name__ == '__main__':
# передаем ключевые значения для соединения с PostgreSQL
    conn = psycopg2.connect(dbname='postgres',
                            user=username,
                            host=hostname,
                            password=password)

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()

    # Создаем пустую базу данных в PostgreSQl
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(database))
        )

    cur.close()
    conn.close()
    # Создаем основу базы данных
    print(f'{database} has been successfully created!')

