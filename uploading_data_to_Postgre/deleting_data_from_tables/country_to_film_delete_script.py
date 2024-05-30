from delete_function import *

# очищаем всю таблицу
conn = psycopg2.connect(host=hostname,
                        dbname=database,
                        user=username,
                        password=password,
                        port=port_id)
cur = conn.cursor()
cur.execute('SELECT DISTINCT country_id FROM country_to_film')
list_of_country_ids = [item[0] for item in cur.fetchall()]
cur.close()
conn.close()
print(list_of_country_ids)


if __name__ == '__main__':
    person_to_film_rows = deleting_by_id(table_name='country_to_film',
                                         column_id_name='country_id',
                                         row_id_list=list_of_country_ids)
