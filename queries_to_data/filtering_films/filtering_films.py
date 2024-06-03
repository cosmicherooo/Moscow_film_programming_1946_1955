from creating_db_template_in_postgres import *
import os
import sys
import pandas as pd
import numpy as np
import re
from functools import wraps
import time
import sys

# person_name=True - значит, вы не уточняете конкртных авторов, по которым вы хотите осуществлять поиск.
# Если вы хотите это сделать, то передайте в аргументе person_name кортеж имен
# country=True - значит, вы не уточняете конкртные страные, по которым вы хотите осуществлять поиск.
# Если вы хотите это сделать, то передайте в аргументе country кортеж стран в формате ISO_3166
# В значениях is_director, is_writer, is_actor вы можете указывать значения False или True, например,
# Если вы хотите узнать информацию о фильмах, где режиссером был Сергей Ейзенштейн, то помимо имя личности
# Можно указать значение True в параметре is_director (Если вы хотите найти картины, где Эйзенштейн был только режиссером),
# То в двух других параметрах стоит указать значения False.
# Если вы совсем не хотите осуществлять поиск по личностям, то укажите во всех трех значениях False.
# В значении duration_min можно указать минимальное время, которое должен идти фильма,
# в значении duration_max верхнюю границу.
# То же самое можно сделать и со значениями year_of_prod_min - самая ранняя дата, в течение которой вышел фильм;
# year_of_prod_max - верхняя временная граница, до которой мог выйти фильм.
# Аргумент функции and_pers_operator в значении True ищет те фильмы, участие в создании которых принимали все
# из указанных в значении person_name личности.

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        wrapper.total_time += duration
        print(f"Execution time: {duration}")
        return result

    wrapper.total_time = 0
    return wrapper


@timer
def filtering_films(person_name=True,
                    and_pers_operator=False,
                    is_director=True,
                    is_writer=True,
                    is_actor=True,
                    duration_min=0,
                    duration_max=240,
                    country=True,
                    year_of_prod_min=1900,
                    year_of_prod_max=1955):

    role_tuple = ()
    if is_director is True:
        role_tuple = role_tuple + ('Director',)
    if is_writer is True:
        role_tuple = role_tuple + ('Writer',)
    if is_actor is True:
        role_tuple = role_tuple + ('Actor',)
    if len(role_tuple) == 0:
        sys.exit("You has not chosen any person roles in the film!")

    year_tuple = tuple(list(range(year_of_prod_min, year_of_prod_max+1)))
    duration_tuple = tuple(list(range(duration_min, duration_max+1)))

    try:
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password,
                                port=port_id)
        cur = conn.cursor()


        if country is True:
             cur.execute('''SELECT iso_3166_1_alpha_2
                            FROM country;''')

             list_of_countries = [item for item in cur.fetchall()]
             list_of_countries = sum(list_of_countries, ())

        else:
            list_of_countries = country

        if person_name is True:
             cur.execute('''SELECT person_name
                            FROM person;''')

             list_of_persons = [item for item in cur.fetchall()]
             list_of_persons = sum(list_of_persons, ())

        else:
            list_of_persons = person_name


        query_to_drop_is_exists = ''' DROP TABLE IF EXISTS film_filtered;
                                      DROP TABLE IF EXISTS country_filtered;
                                      DROP TABLE IF EXISTS country_country_to_film;
                                      DROP TABLE IF EXISTS film_with_country;
                                      DROP TABLE IF EXISTS persons_occ;
                                      DROP TABLE IF EXISTS films_to_persons;'''
        try:
            cur.execute(query_to_drop_is_exists)

        except:
            print('query_to_drop_is_exists')

        query_to_filter_films = ''' CREATE TEMPORARY TABLE IF NOT EXISTS film_filtered
                                    AS 
                                    SELECT * 
                                    FROM film
                                    WHERE prod_year in %s
                                    AND duration in %s
                                    AND films_imdb_id IS NOT NULL;'''

        try:
            cur.execute(query_to_filter_films, (year_tuple, duration_tuple,))

        except:
            print('cur.execute(query_to_filter_films, (year_tuple, duration_tuple,))')



        query_to_filter_country = ''' CREATE TEMPORARY TABLE IF NOT EXISTS country_filtered
                                      AS 
                                      SELECT *
                                      FROM country
                                      WHERE iso_3166_1_alpha_2 in %s;'''

        try:
            cur.execute(query_to_filter_country, (list_of_countries,))

        except:
            print('cur.execute(query_to_filter_country, (list_of_countries,))')


        query_to_match_films_ids_to_countries = ''' CREATE TEMPORARY TABLE IF NOT EXISTS country_country_to_film
                                                    AS 
                                                    SELECT country_filtered.country_name,
                                                           country_to_film.film_id
                                                    FROM country_filtered, country_to_film
                                                    WHERE country_filtered.country_id = country_to_film.country_id;'''

        try:
            cur.execute(query_to_match_films_ids_to_countries)

        except:
            print('cur.execute(query_to_match_films_ids_to_countries)')



        query_to_match_films_to_countries = ''' CREATE TEMPORARY TABLE IF NOT EXISTS film_with_country
                                                AS 
                                                SELECT film_filtered.film_id,
                                                       film_filtered.title_original,
                                                       film_filtered.prod_year,
                                                       film_filtered.duration,
                                                       film_filtered.films_imdb_id,
                                                       country_country_to_film.country_name
                                                FROM film_filtered, country_country_to_film
                                                WHERE country_country_to_film.film_id = film_filtered.film_id;'''

        try:
            cur.execute(query_to_match_films_to_countries)

        except:
            print('cur.execute(query_to_match_films_to_countries)')



        query_to_filter_persons = ''' CREATE TEMPORARY TABLE IF NOT EXISTS persons_occ
                                      AS 
                                      SELECT p.person_id, 
                                             p.person_name, 
                                             pt.film_id, 
                                             pt.person_occ
                                      FROM person AS p, 
                                           person_to_film AS pt
                                      WHERE p.person_name in %s 
                                      AND p.person_id = pt.person_id
                                      AND pt.person_occ in %s; '''

        try:
            cur.execute(query_to_filter_persons, (list_of_persons, role_tuple,))

        except:
            print(' cur.execute(query_to_filter_persons, (person_name, role_tuple,))')


        query_to_match_films_with_persons = ''' CREATE TEMPORARY TABLE IF NOT EXISTS films_to_persons
                                                AS 
                                                SELECT persons_occ.person_id, 
                                                       persons_occ.person_name, 
                                                       persons_occ.person_occ,
                                                       film_with_country.film_id,
                                                       film_with_country.title_original,
                                                       film_with_country.prod_year,
                                                       film_with_country.duration,
                                                       film_with_country.films_imdb_id,
                                                       film_with_country.country_name
                                                FROM persons_occ, film_with_country
                                                WHERE persons_occ.film_id = film_with_country.film_id;'''

        try:
            cur.execute(query_to_match_films_with_persons)

        except:
            print('cur.execute(query_to_match_films_with_persons)')


        selection_query = '''SELECT * 
                             FROM films_to_persons;'''

        cur.execute(selection_query)

        selected_table = [item for item in cur.fetchall()]

        cur.execute(query_to_drop_is_exists)

        cur.close()
        conn.close()

        output_dataframe = pd.DataFrame(selected_table, columns=['person_id',
                                                                 'person_name',
                                                                 'person_occ',
                                                                 'film_id',
                                                                 'film_title',
                                                                 'year',
                                                                 'film_duration',
                                                                 'film_imdb_id',
                                                                 'film_country_of_origin'])

        output_dataframe['film_country_of_origin'] = output_dataframe['film_country_of_origin'].apply(lambda x: x.strip())

        df_person = output_dataframe[['person_name', 'person_occ', 'film_id']]

        df_person = (df_person.groupby(['film_id', 'person_occ'])
                     .agg({'person_name': lambda x: x.tolist()})
                     .reset_index())

        df_person['person_name'] = df_person['person_name'].apply(lambda x: list(set(x)))
        df_person['person_name'] = [','.join(map(str, l)) for l in df_person['person_name']]

        df_person = df_person.drop_duplicates()



        df_person = df_person.pivot(index='film_id', columns='person_occ', values='person_name')

        df_person = df_person.reset_index()

        if 'Actor' not in df_person.columns:
            df_person["Actor"] = np.nan

        if 'Director' not in df_person.columns:
            df_person["Director"] = np.nan

        if 'Writer' not in df_person.columns:
            df_person["Writer"] = np.nan

        df_person = df_person[['film_id', 'Actor', 'Director', 'Writer']]


        df_film = output_dataframe[['film_id', 'film_title', 'year', 'film_duration', 'film_country_of_origin']]
        df_film = df_film.drop_duplicates()

        final_df = df_film.merge(df_person, how='left', on='film_id')


        if and_pers_operator is True:

            row_indexes = []
            people_tuple = list_of_persons

            for row_index in range(0, final_df.shape[0]):
                actors = final_df.loc[row_index]['Actor']
                writers = final_df.loc[row_index]['Writer']
                directors = final_df.loc[row_index]['Director']
                all_people = list((actors, writers, directors))
                all_people = ' '.join([str(elem) for elem in all_people])
                tuple_iter = 0
                for i in range(0, len(people_tuple)):
                    if len(re.findall(str(people_tuple[i]), all_people)) != 0:
                        tuple_iter += 1

                if tuple_iter == len(people_tuple):
                    row_indexes.append(row_index)

            final_df = final_df.iloc[row_indexes]


        if is_director is False:
            final_df = final_df.drop(columns=['Director'])
        if is_writer is False:
            final_df = final_df.drop(columns=['Writer'])
        if is_actor is False:
            final_df = final_df.drop(columns=['Actor'])

        num_of_rows = final_df.shape[0]


    except:
        sys.exit("Your connection was unsuccessful!")

    return final_df, num_of_rows

if __name__ == '__main__':
    filtering_films()

# пустой запуск функции выводит сводную статистику по всем фильмам, для которых есть информация о режиссерах.
# Для поиска информации о фильмах, о которых нет информации про занятых в их производстве людей, используйте другие функции.


