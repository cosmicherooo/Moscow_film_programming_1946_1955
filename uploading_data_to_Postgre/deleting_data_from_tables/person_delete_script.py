from delete_function import *

# очищаем всю таблицу
conn = psycopg2.connect(host=hostname,
                        dbname=database,
                        user=username,
                        password=password,
                        port=port_id)
cur = conn.cursor()
cur.execute('SELECT person_id FROM Person')
list_of_persons_ids = [item[0] for item in cur.fetchall()]
cur.close()
conn.close()

if __name__ == '__main__':
    statistics = deleting_by_id(table_name='Person',
                                column_id_name='person_id',
                                row_id_list=list_of_persons_ids)

    statistics = list(statistics)
    statistics.append(deleting_by_id.total_time)
    print(statistics)
    