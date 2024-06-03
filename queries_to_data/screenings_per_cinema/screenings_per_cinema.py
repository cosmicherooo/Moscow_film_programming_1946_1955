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
def screenings_per_cinema(cinema_name='Метрополь',
                          year=1946):

    year_start = datetime.date(year, 1, 1)
    year_end = datetime.date(year, 12, 31)

    if type(cinema_name) != tuple:
        cinema_name_tuple = tuple([cinema_name])
    else:
        cinema_name_tuple = cinema_name

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
                                      DROP TABLE IF EXISTS cinema_filtered;
                                      DROP TABLE IF EXISTS cinema_to_screening;'''

        cur.execute(query_to_drop_is_exists)

    except:
        sys.exit('query_to_drop_is_exists cannot be executed!')

    try:
        query_to_filter_screenings = ''' CREATE TEMPORARY TABLE IF NOT EXISTS screenings_filtered
                                         AS 
                                         SELECT screening.screening_id,	   
                                                screening.day_of_screening,
                                                screening.cinema_id
                                         FROM screening 
                                         WHERE %s <= day_of_screening AND day_of_screening <= %s;'''

        cur.execute(query_to_filter_screenings, (year_start, year_end,))

    except:
        sys.exit('query_to_filter_screenings cannot be executed!')

    try:
        query_to_filter_cinema = ''' CREATE TEMPORARY TABLE IF NOT EXISTS cinema_filtered
                                     AS 
                                     SELECT cinema.cinema_name_source, 
                                            cinema.cinema_id
                                     FROM cinema
                                     WHERE cinema.cinema_name_source in %s;'''

        cur.execute(query_to_filter_cinema, (cinema_name_tuple,))

    except:
        sys.exit('query_to_filter_cinema cannot be executed!')

    try:
        query_to_join_screening_cinema = ''' CREATE TEMPORARY TABLE IF NOT EXISTS cinema_to_screening
                                             AS 
                                             SELECT cinema_filtered.cinema_name_source, 
                                                    screenings_filtered.screening_id,
                                                    screenings_filtered.day_of_screening,
                                                    screenings_filtered.cinema_id
                                            FROM screenings_filtered, cinema_filtered
                                            WHERE screenings_filtered.cinema_id = cinema_filtered.cinema_id;'''

        cur.execute(query_to_join_screening_cinema)

    except:
        sys.exit('query_to_join_screening_cinema cannot be executed!')

    try:
        selection_query = '''SELECT count(cinema_to_screening.screening_id) as num_of_screenings, 
                                    cinema_to_screening.cinema_name_source
                             FROM cinema_to_screening
                             GROUP BY cinema_to_screening.cinema_name_source
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
                                             'cinema_name_source'])

    try:
        num_of_screenings = selected_table[0][0]
    except:
        num_of_screenings = 0

    return output_dataframe, num_of_screenings

if __name__ == '__main__':
    function_output = screenings_per_cinema()
    dataframe = function_output[0]
    num_of_screenings = function_output[1]
    print(dataframe)
    print(num_of_screenings)
