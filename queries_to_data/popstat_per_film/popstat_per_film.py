from creating_db_template_in_postgres import *
import os
import sys
import pandas as pd
import numpy as np
import re
from functools import wraps
import time
import sys
import datetime


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


# аргумент is_cinema по умолчанию False. Означает, хотите ли, чтобы POPSTAT выдывался для каждого кинотеатра,
# по отдельности. Если вы хотите получить такой результат поставьте занчение True, если хотите
# произвести расчет POPSTAT только для фильма, передайте в аргумент функции значение True.
# Если вы хотите расчитать  POPSTAT для нескольких фильмов, то передайте названия кинокартин в виде кортежа&
# Если вы хотите посчитать POPSTAT для всех кинокартин, то передайте аргументу film_name значение True



@timer
def screenings_per_film(film_name='Александр Невский',
                        start_date=(1947, 1, 1),
                        end_date=(1948, 12, 31),
                        is_cinema = False,
                        by_year = True):


    try:
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password,
                                port=port_id)
        cur = conn.cursor()

    except:
        sys.exit('Unsuccessful connection!')

    year_start = datetime.date(start_date[0], start_date[1], start_date[2])
    year_end = datetime.date(end_date[0], end_date[1], end_date[2])

    if film_name is True:
        try:
            cur.execute('''SELECT title_original
                              FROM film;''')

            list_of_films = [item for item in cur.fetchall()]
            film_name_tuple = sum(list_of_films, ())


        except:
            sys.exit('Query to get all cinemas was unsuccessful')

    else:
        if type(film_name) != tuple:
            film_name_tuple = tuple([film_name])
        else:
            film_name_tuple = film_name

    list_to_filter_cinema_info_by_year = tuple(list(range(start_date[0], end_date[0]+1)))



    try:
        query_to_drop_is_exists = ''' DROP TABLE IF EXISTS screenings_filtered;
                                      DROP TABLE IF EXISTS film_filtered;
                                      DROP TABLE IF EXISTS film_screening;
                                      DROP TABLE IF EXISTS film_screenings_with_year;
                                      DROP TABLE IF EXISTS cinema_info_filtered;
                                      DROP TABLE IF EXISTS screenings_cinema_info_match;
                                      DROP TABLE IF EXISTS film_screenings_per_cinema;
                                      DROP TABLE IF EXISTS popstat_per_cinema;'''

        cur.execute(query_to_drop_is_exists)

    except:
        sys.exit('query_to_drop_is_exists cannot be executed!')

    try:
        query_to_filter_screenings = ''' CREATE TEMPORARY TABLE IF NOT EXISTS screenings_filtered
                                         AS 
                                         SELECT screening.screening_id,
                                                screening.day_of_screening,
                                                screening.film_id,
                                                screening.cinema_id
                                         FROM screening 
                                         WHERE %s <= day_of_screening AND day_of_screening <= %s;'''

        cur.execute(query_to_filter_screenings, (year_start, year_end,))

    except:
        sys.exit('query_to_filter_screenings cannot be executed!')

    try:
        query_to_filter_films = ''' CREATE TEMPORARY TABLE IF NOT EXISTS film_filtered
                                    AS 
                                    SELECT film.film_id,
                                           film.title_original
                                    FROM film
                                    WHERE film.title_original in %s;'''

        cur.execute(query_to_filter_films, (film_name_tuple, ))

    except:
        sys.exit('query_to_filter_films cannot be executed!')

    try:
        query_to_match_films_with_screenings = ''' CREATE TEMPORARY TABLE IF NOT EXISTS film_screening
                                                   AS
                                                   SELECT film_filtered.title_original, 
                                                          screenings_filtered.film_id,
                                                          screenings_filtered.cinema_id,
                                                          screenings_filtered.screening_id,
                                                          screenings_filtered.day_of_screening
                                                   FROM film_filtered, 
                                                        screenings_filtered
                                                   WHERE film_filtered.film_id = screenings_filtered.film_id;'''

        cur.execute(query_to_match_films_with_screenings)

    except:
        sys.exit('query_to_match_films_with_screenings cannot be executed!')

    try:
        query_to_film_screening_with_year = ''' CREATE TEMPORARY TABLE IF NOT EXISTS film_screenings_with_year
                                                AS
                                                SELECT film_screening.screening_id, 
                                                       film_screening.title_original,
                                                       film_screening.cinema_id,
                                                       EXTRACT(YEAR FROM film_screening.day_of_screening) as year_of_screening
                                                FROM film_screening;'''

        cur.execute(query_to_film_screening_with_year)

    except:
        sys.exit('query_to_film_screening_with_year cannot be executed!')


    try:
        query_to_filter_cinema_info = ''' CREATE TEMPORARY TABLE IF NOT EXISTS cinema_info_filtered
                                          AS 
                                          SELECT cinema.cinema_id, 
                                                 cinema.cinema_name_source,
                                                 cinema_info.cinema_info_id,
                                                 cinema_info.seats,
                                                 cinema_info.coef,
                                                 cinema_info.year
                                          FROM cinema_info,
                                               cinema
                                          WHERE cinema_info.year in %s
                                          AND cinema.cinema_id = cinema_info.cinema_id;'''

        cur.execute(query_to_filter_cinema_info, (list_to_filter_cinema_info_by_year,))

    except:
        sys.exit('query_to_filter_cinema_info cannot be executed!')

    try:
        query_to_match_screenings_with_cinema_info = ''' CREATE TEMPORARY TABLE IF NOT EXISTS screenings_cinema_info_match
                                                         AS
                                                         SELECT film_screenings_with_year.screening_id,
                                                                film_screenings_with_year.title_original,
                                                                film_screenings_with_year.cinema_id,
                                                                film_screenings_with_year.year_of_screening,
                                                                cinema_info_filtered.cinema_info_id,
                                                                cinema_info_filtered.cinema_name_source,
                                                                cinema_info_filtered.seats,
                                                                cinema_info_filtered.coef
                                                         FROM cinema_info_filtered, 
                                                              film_screenings_with_year
                                                        WHERE film_screenings_with_year.cinema_id = cinema_info_filtered.cinema_id
                                                        AND film_screenings_with_year.year_of_screening = cinema_info_filtered.year;'''

        cur.execute(query_to_match_screenings_with_cinema_info)

    except:
        sys.exit('query_to_match_screenings_with_cinema_info cannot be executed!')

    try:
        query_to_match_screenings_film_cinema_info = ''' CREATE TEMPORARY TABLE IF NOT EXISTS film_screenings_per_cinema
                                                         AS
                                                         SELECT count(screenings_cinema_info_match.screening_id) as num_of_screenings, 
                                                                screenings_cinema_info_match.title_original,
                                                                screenings_cinema_info_match.cinema_info_id,
                                                                screenings_cinema_info_match.cinema_name_source,
                                                                screenings_cinema_info_match.year_of_screening,
                                                                screenings_cinema_info_match.seats,
                                                                screenings_cinema_info_match.coef
                                                        FROM screenings_cinema_info_match
                                                        GROUP BY screenings_cinema_info_match.title_original,
                                                                 screenings_cinema_info_match.cinema_info_id,
                                                                 screenings_cinema_info_match.cinema_info_id,
                                                                 screenings_cinema_info_match.cinema_name_source,
                                                                 screenings_cinema_info_match.year_of_screening,
                                                                 screenings_cinema_info_match.seats,
                                                                 screenings_cinema_info_match.coef
                                                        ORDER BY year_of_screening;'''

        cur.execute(query_to_match_screenings_film_cinema_info)

    except:
        sys.exit('query_to_match_screenings_film_cinema_info cannot be executed!')

    try:
        query_to_popstat_per_cinema = ''' CREATE TEMPORARY TABLE IF NOT EXISTS popstat_per_cinema
                                          AS
                                          SELECT film_screenings_per_cinema.title_original,
                                                 film_screenings_per_cinema.cinema_name_source,
                                                 num_of_screenings * seats * coef AS POPSTAT,
                                                 film_screenings_per_cinema.num_of_screenings,
                                                 film_screenings_per_cinema.year_of_screening
                                          FROM film_screenings_per_cinema
                                          ORDER BY POPSTAT DESC;'''

        cur.execute(query_to_popstat_per_cinema)

    except:
        sys.exit('query_to_popstat_per_cinema cannot be executed!')


    if is_cinema is True and by_year is True:
        try:
            selection_query = '''SELECT *
                                 FROM popstat_per_cinema;'''

            cur.execute(selection_query)

            selected_table = [item for item in cur.fetchall()]

            cur.execute(query_to_drop_is_exists)

            cur.execute(query_to_drop_is_exists)

            cur.close()
            conn.close()

        except:
            sys.exit('selection_query cannot be executed!')

        output_dataframe = pd.DataFrame(selected_table,
                                        columns=['title_original',
                                                 'cinema_name_source',
                                                 'POPSTAT',
                                                 'num_of_screenings',
                                                 'year_of_screening'])

    elif is_cinema is True and by_year is False:

        try:
            query_to_popstat_per_cinema_overall = ''' CREATE TEMPORARY TABLE IF NOT EXISTS popstat_per_cinema_overall
                                                      AS
                                                      SELECT popstat_per_cinema.title_original,
                                                             popstat_per_cinema.cinema_name_source,
                                                             sum(popstat_per_cinema.popstat) as popstat,
                                                             sum(popstat_per_cinema.num_of_screenings) as num_of_screenings
                                                      FROM popstat_per_cinema
                                                      GROUP BY popstat_per_cinema.title_original,
                                                               popstat_per_cinema.cinema_name_source
                                                      ORDER BY POPSTAT DESC;'''

            cur.execute(query_to_popstat_per_cinema_overall)

        except:
            sys.exit('query_to_popstat_per_cinema_overall cannot be executed!')

        try:
            selection_query = '''SELECT *
                                 FROM popstat_per_cinema_overall;'''

            cur.execute(selection_query)

            selected_table = [item for item in cur.fetchall()]

            cur.execute(query_to_drop_is_exists)

            cur.execute(query_to_drop_is_exists)

            cur.close()
            conn.close()

        except:
            sys.exit('selection_query cannot be executed!')

        output_dataframe = pd.DataFrame(selected_table,
                                        columns=['title_original',
                                                 'cinema_name_source',
                                                 'POPSTAT',
                                                 'num_of_screenings'])

    elif is_cinema is False and by_year is True:

        try:
            query_to_popstat_per_film_by_year = ''' CREATE TEMPORARY TABLE IF NOT EXISTS popstat_per_film_by_year
                                                    AS
                                                    SELECT popstat_per_cinema.title_original,
                                                           sum(popstat_per_cinema.popstat) as popstat,
                                                           sum(popstat_per_cinema.num_of_screenings) as num_of_screenings,
                                                           popstat_per_cinema.year_of_screening
                                                    FROM popstat_per_cinema
                                                    GROUP BY popstat_per_cinema.title_original,
                                                             popstat_per_cinema.year_of_screening
                                                    ORDER BY POPSTAT DESC;'''

            cur.execute(query_to_popstat_per_film_by_year)

        except:
            sys.exit('query_to_popstat_per_film_by_year cannot be executed!')


        try:
            selection_query = '''SELECT *
                                 FROM popstat_per_film_by_year;'''

            cur.execute(selection_query)

            selected_table = [item for item in cur.fetchall()]

            cur.execute(query_to_drop_is_exists)

            cur.execute(query_to_drop_is_exists)

            cur.close()
            conn.close()

        except:
            sys.exit('selection_query cannot be executed!')

        output_dataframe = pd.DataFrame(selected_table,
                                        columns=['title_original',
                                                 'POPSTAT',
                                                 'num_of_screenings',
                                                 'year_of_screening'])

    elif is_cinema is False and by_year is False:

        try:
            query_to_popstat_per_film_overall = ''' CREATE TEMPORARY TABLE IF NOT EXISTS popstat_per_film_overall
                                                    AS
                                                    SELECT popstat_per_cinema.title_original,
                                                           sum(popstat_per_cinema.popstat) as popstat,
                                                           sum(popstat_per_cinema.num_of_screenings) as num_of_screenings
                                                    FROM popstat_per_cinema
                                                    GROUP BY popstat_per_cinema.title_original
                                                    ORDER BY POPSTAT DESC;'''

            cur.execute(query_to_popstat_per_film_overall)

        except:
            sys.exit('query_to_popstat_per_film_overall cannot be executed!')


        try:
            selection_query = '''SELECT *
                                 FROM popstat_per_film_overall;'''

            cur.execute(selection_query)

            selected_table = [item for item in cur.fetchall()]

            cur.execute(query_to_drop_is_exists)

            cur.execute(query_to_drop_is_exists)

            cur.close()
            conn.close()

        except:
            sys.exit('selection_query cannot be executed!')

        output_dataframe = pd.DataFrame(selected_table,
                                        columns=['title_original',
                                                 'POPSTAT',
                                                 'num_of_screenings'])

    return output_dataframe


if __name__ == '__main__':
    testing_df = screenings_per_film()
    print(testing_df)
    
