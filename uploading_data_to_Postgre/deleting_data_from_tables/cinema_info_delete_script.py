from delete_function import *

# очищаем всю таблицу
conn = psycopg2.connect(host=hostname,
                        dbname=database,
                        user=username,
                        password=password,
                        port=port_id)
cur = conn.cursor()
cur.execute('SELECT DISTINCT cinema_id FROM Cinema_info')
list_of_cinema_ids = [item[0] for item in cur.fetchall()]
cur.close()
conn.close()
print(list_of_cinema_ids)


if __name__ == '__main__':
    person_to_film_rows = deleting_by_id(table_name='Cinema_info',
                                         column_id_name='cinema_id',
                                         row_id_list=list_of_cinema_ids)
