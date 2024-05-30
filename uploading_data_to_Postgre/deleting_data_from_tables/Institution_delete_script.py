from delete_function import *

# очищаем всю таблицу
conn = psycopg2.connect(host=hostname,
                        dbname=database,
                        user=username,
                        password=password,
                        port=port_id)
cur = conn.cursor()
cur.execute('SELECT DISTINCT institution_id FROM Institution')
list_of_institution_ids = [item[0] for item in cur.fetchall()]
cur.close()
conn.close()
print(list_of_institution_ids)


if __name__ == '__main__':
    person_to_film_rows = deleting_by_id(table_name='Institution',
                                         column_id_name='institution_id',
                                         row_id_list=list_of_institution_ids)
