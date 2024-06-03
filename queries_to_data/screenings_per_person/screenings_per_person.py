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

def screenings_per_person(role = 'Actor',
                          year = 1946,
                          person_name = 'Sergei Eisenstein'):

    role_tuple = tuple([role])
    year_start = datetime.date(year, 1, 1)
    year_end = datetime.date(year, 12, 31)
    person_tuple = tuple([person_name])

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
                                      DROP TABLE IF EXISTS persons_occ;
                                      DROP TABLE IF EXISTS person_with_film;
                                      DROP TABLE IF EXISTS screenings_with_person;'''

        cur.execute(query_to_drop_is_exists)

    except:
        sys.exit('query_to_drop_is_exists cannot be executed!')

    try:
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
                                      AND pt.person_occ in %s;'''

        cur.execute(query_to_filter_persons, (person_tuple, role_tuple,))

    except:
        sys.exit('query_to_filter_persons cannot be executed!')

    try:
        query_to_match_films_to_persons = ''' CREATE TEMPORARY TABLE IF NOT EXISTS person_with_film
                                                 AS 
                                                 SELECT persons_occ.person_id, 
                                                        persons_occ.person_name, 
                                                        persons_occ.person_occ,
                                                        film.film_id,
                                                        film.title_original
                                                        FROM persons_occ, film
                                                 WHERE persons_occ.film_id = film.film_id;'''

        cur.execute(query_to_match_films_to_persons)

    except:
        sys.exit('query_to_match_films_to_persons cannot be executed!')

    try:
        query_to_filter_screenings = ''' CREATE TEMPORARY TABLE IF NOT EXISTS screenings_filtered
                                         AS 
                                         SELECT screening.screening_id,	   
                                                screening.day_of_screening,
                                                screening.film_id
                                         FROM screening 
                                         WHERE %s <= day_of_screening AND day_of_screening <= %s;'''

        cur.execute(query_to_filter_screenings, (year_start, year_end, ))

    except:
        sys.exit('query_to_filter_screenings cannot be executed!')

    try:
        query_tom_match_person_with_screenings = '''CREATE TEMPORARY TABLE IF NOT EXISTS screenings_with_person
                                                    AS 
                                                    SELECT screenings_filtered.screening_id,
                                                           screenings_filtered.day_of_screening, 
                                                           person_with_film.person_id, 
                                                           person_with_film.person_name, 
                                                           person_with_film.person_occ,
                                                           person_with_film.film_id,
                                                           person_with_film.title_original
                                                    FROM screenings_filtered, person_with_film
                                                    WHERE screenings_filtered.film_id = person_with_film.film_id;'''

        cur.execute(query_tom_match_person_with_screenings)

    except:
        sys.exit('query_tom_match_person_with_screenings cannot be executed!')

    try:
        selection_query = '''SELECT count(screenings_with_person.screening_id) as num_of_screenings, 
                                    screenings_with_person.person_name,
                                    screenings_with_person.person_occ
                                    FROM screenings_with_person
                                    GROUP BY screenings_with_person.person_name, 
                                    screenings_with_person.person_occ;'''

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
                                             'person_name',
                                             'person_occ'])

    try:
        num_of_screenings = selected_table[0][0]

    except:
        num_of_screenings = 0

    return output_dataframe, num_of_screenings




