from delete_function import *

# очищаем всю таблицу
conn = psycopg2.connect(host=hostname,
                        dbname=database,
                        user=username,
                        password=password,
                        port=port_id)
cur = conn.cursor()
cur.execute('SELECT DISTINCT periodic_id FROM Periodic')
list_of_periodic_ids = [item[0] for item in cur.fetchall()]
cur.close()
conn.close()


if __name__ == '__main__':
    statistics = deleting_by_id(table_name='Periodic',
                                column_id_name='periodic_id',
                                row_id_list=list_of_periodic_ids)

    statistics = list(statistics)
    statistics.append(deleting_by_id.total_time)
    print(statistics)