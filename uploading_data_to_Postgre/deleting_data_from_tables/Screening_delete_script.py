from delete_function import *

# очищаем всю таблицу
conn = psycopg2.connect(host=hostname,
                        dbname=database,
                        user=username,
                        password=password,
                        port=port_id)
cur = conn.cursor()
cur.execute('SELECT DISTINCT is_programme FROM Screening')
list_of_screening_ids = [item[0] for item in cur.fetchall()]
cur.close()
conn.close()


if __name__ == '__main__':
    statistics = deleting_by_id(table_name = 'Screening',
                                column_id_name='is_programme',
                                row_id_list=list_of_screening_ids)

    statistics = list(statistics)
    statistics.append(deleting_by_id.total_time)
    print(statistics)
