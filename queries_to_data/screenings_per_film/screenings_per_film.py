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


@timer
def screenings_per_film(film_name='Александр Невский',
                        year=1947):

    year_start = datetime.date(year, 1, 1)
    year_end = datetime.date(year, 12, 31)

    if type(film_name) != tuple:
        film_name_tuple = tuple([film_name])
    else:
        film_name_tuple = film_name

    try:
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password,
                                port=port_id)
        cur = conn.cursor()

    except:
        sys.exit('Unsuccessful connection!')

    try:
        query_to_drop_is_exists = ''' DROP TABLE IF EXISTS screenings_filtered;
                                      DROP TABLE IF EXISTS film_filtered;
                                      DROP TABLE IF EXISTS screenings_to_film;'''

        cur.execute(query_to_drop_is_exists)

    except:
        sys.exit('query_to_drop_is_exists cannot be executed!')


    try:
        query_to_filter_screenings = ''' CREATE TEMPORARY TABLE IF NOT EXISTS screenings_filtered
                                         AS 
                                         SELECT screening.screening_id,	   
                                                screening.day_of_screening,
                                                screening.film_id
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
        query_screenings_to_film = ''' CREATE TEMPORARY TABLE IF NOT EXISTS screenings_to_film
                                       AS 
                                       SELECT screenings_filtered.screening_id,
                                              screenings_filtered.day_of_screening,
                                              screenings_filtered.film_id, 
                                              film_filtered.title_original
                                      FROM screenings_filtered, 
                                           film_filtered
                                      WHERE screenings_filtered.film_id = film_filtered.film_id;'''

        cur.execute(query_screenings_to_film)

    except:
        sys.exit('query_screenings_to_film cannot be executed!')

    try:
        selection_query = '''SELECT count(screenings_to_film.screening_id) as num_of_screenings, 
                                    screenings_to_film.title_original
                             FROM screenings_to_film
                             GROUP BY screenings_to_film.title_original,
                                      screenings_to_film.film_id
                             ORDER BY num_of_screenings DESC;'''

        cur.execute(selection_query)

        selected_table = [item for item in cur.fetchall()]

        cur.execute(query_to_drop_is_exists)

        cur.execute(query_to_drop_is_exists)

        cur.close()
        conn.close()

    except:
        sys.exit('selection_query cannot be executed!')

    output_dataframe = pd.DataFrame(selected_table,
                                    columns=['num_of_screenings',
                                             'film_name_original'])

    try:
        num_of_screenings = selected_table[0][0]
    except:
        num_of_screenings = 0

    return output_dataframe, num_of_screenings

if __name__ == '__main__':
    function_output = screenings_per_film()
    dataframe = function_output[0]
    num_of_screenings = function_output[1]
    print(dataframe)
    print(num_of_screenings)
