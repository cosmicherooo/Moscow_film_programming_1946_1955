from creating_db_template_in_postgres import *

table_names_list = ['Person',
                    'person_to_film',
                    'Film',
                    'Screening',
                    'Periodic',
                    'periodic_ref',
                    'Country',
                    'country_to_film',
                    'Cinema_info',
                    'Cinema',
                    'Institution']


variables_in_tables = [
    [
        ('person_id', 'char(10) NOT NULL PRIMARY KEY'),
        ('person_name', 'varchar(100) NOT NULL'),
        ('person_imdb_id', 'varchar(12)')
    ],
    [
        ('person_id', 'char(10) NOT NULL'),
        ('film_id', 'char(10) NOT NULL'),
        ('person_occ', 'varchar(10) NOT NULL')
    ],
    [
        ('film_id', 'char(10) NOT NULL PRIMARY KEY'),
        ('title_original', 'varchar(200) NOT NULL'),
        ('prod_year', 'integer'),
        ('duration', 'integer'),
        ('films_imdb_id', 'varchar(12)'),
    ],
    [
        ('screening_id', 'char(11) NOT NULL PRIMARY KEY'),
        ('day_of_screening', 'date NOT NULL'),
        ('weekday', 'char(3) NOT NULL'),
        ('film_title_source', 'varchar(200) NOT NULL'),
        ('film_title_trans', 'varchar(200) NOT NULL'),
        ('is_programme', 'boolean NOT NULL'),
        ('cinema_id', 'char(10) NOT NULL'),
        ('film_id', 'char(10) NOT NULL'),
        ('periodic_ref_id', 'char(10)')
    ],
    [
     ('periodic_id', 'char(10) NOT NULL PRIMARY KEY'),
     ('periodic_name_original', 'char(50) NOT NULL'),
     ('periodic_name_trans', 'char(50) NOT NULL')
    ],
    [
      ('periodic_ref_id', 'char(10) NOT NULL PRIMARY KEY'),
      ('periodic_issue', 'varchar(300) NOT NULL'),
      ('periodic_url', 'varchar(300)'),
      ('periodic_url_programme', 'varchar(300)'),
      ('periodic_date', 'date NOT NULL'),
      ('is_programme', 'boolean NOT NULL'),
      ('periodic_id', 'char(10) NOT NULL')
    ],
    [
      ('country_id', 'char(10) NOT NULL PRIMARY KEY'),
      ('country_name', 'char(30)'),
      ('ISO_3166_1_alpha_2', 'char(2) NOT NULL')
    ],
    [
      ('film_id', 'char(10) NOT NULL'),
      ('country_id', 'char(10) NOT NULL')
    ],
    [
      ('cinema_info_id', 'char(10) NOT NULL PRIMARY KEY'),
      ('year', 'integer NOT NULL'),
      ('run', 'integer'),
      ('seats', 'integer'),
      ('address_cinema', 'varchar(50)'),
      ('city', 'varchar(50) NOT NULL'),
      ('lat', 'float'),
      ('long', 'float'),
      ('sources', 'varchar(700) NOT NULL'),
      ('comments', 'varchar(700)'),
      ('reconstruction', 'boolean NOT NULL'),
      ('cinema_id', 'char(10) NOT NULL'),
      ('institution_id', 'char(10) NOT NULL'),
      ('country_id', 'char(10) NOT NULL')
    ],
    [
      ('cinema_id', 'char(10) NOT NULL PRIMARY KEY'),
      ('cinema_name_source', 'varchar(50) NOT NULL'),
      ('cinema_name_trans', 'varchar(50) NOT NULL')
    ],
    [
      ('institution_id', 'char(10) NOT NULL PRIMARY KEY'),
      ('institution_name', 'char(200) NOT NULL'),
      ('address_inst', 'varchar(50)'),
      ('city', 'varchar(50) NOT NULL'),
      ('country_id', 'varchar(10) NOT NULL')
    ]
    ]


if __name__ == '__main__':
    list_of_table_create_scripts = []

    for i in range(0, len(table_names_list)):
        create_table_command = 'CREATE TABLE IF NOT EXISTS ' + table_names_list[i]
        table_columns = create_table_command + "(" + ', '.join([' '.join(sub) for sub in variables_in_tables[i]]) + ')'
        list_of_table_create_scripts.append(table_columns)

    try:
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password,
                                port=port_id)

        cur = conn.cursor()

        iterator = 0

        for ex_query in list_of_table_create_scripts:
            query = sql.SQL(ex_query)

            cur.execute(query)
            conn.commit()
            print(f'{table_names_list[iterator]} is created!')

            iterator += 1

        cur.close()
        conn.close()

    except Exception as error:
        print(error)




