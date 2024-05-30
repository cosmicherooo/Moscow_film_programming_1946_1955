from delete_function import *

# очищаем всю таблицу
conn = psycopg2.connect(host=hostname,
                        dbname=database,
                        user=username,
                        password=password,
                        port=port_id)
cur = conn.cursor()
cur.execute('SELECT DISTINCT screening_id FROM Screening')
list_of_screening_ids = [item[0] for item in cur.fetchall()]
cur.close()
conn.close()


if __name__ == '__main__':
    person_to_film_rows = deleting_by_id(table_name = 'Screening',
                                         column_id_name='screening_id',
                                         row_id_list=list_of_screening_ids)
