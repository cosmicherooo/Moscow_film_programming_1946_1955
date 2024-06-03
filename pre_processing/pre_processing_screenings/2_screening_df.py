import pandas as pd
import math
import numpy as np
from ast import literal_eval

screenings_pre_1 = pd.read_csv("pre_processing/pre_processing_screenings/screenings_split_1.csv")
screenings_pre_2 = pd.read_csv("pre_processing/pre_processing_screenings/screenings_split_2.csv")
screenings_pre = pd.concat([screenings_pre_1, screenings_pre_2], axis = 0).reset_index()


cinema = pd.read_csv("pre_processing/pre_processing_cinemas/Cinema.csv")
film = pd.read_csv("pre_processing/pre_processing_films/Film.csv")
periodic_ref_id = pd.read_csv("/pre_processing/pre_rpocessing_periodics/periodic_ref.csv")
raw_cinema = pd.read_csv("Cinemas, 1946–1955.csv")

# переименовываем колонки

screenings_pre = screenings_pre.rename({'cinema..ID.': 'cinema (ID)',
                                        'first.day.of.screening': 'day_of_screening',
                                        'screening.days': 'screening_days',
                                        'title..source.': 'film_title_source',
                                        'title..transliteration.': 'film_title_trans',
                                        'title..original.': 'title_original',
                                        'IMDB.id': 'films_imdb_id',
                                        'source': 'source',
                                        'country.of.origin': 'country_of_origin',
                                        'rn': 'rn',
                                        'Day_of_the_week': 'weekday'}, axis=1)

# возвращаем изначальные названия кинотеатрам

screenings_pre = pd.merge(screenings_pre, raw_cinema[['cinema (ID)', "cinema (source)"]], on="cinema (ID)", how="left")

# сбрасываем ненужные колонки
screenings_pre = screenings_pre.drop(columns=['cinema (ID)', 'screening_days', 'films_imdb_id',
                                              'country_of_origin', 'rn'])

# еще раз переименовываем

screenings_pre = screenings_pre.rename({'cinema (source)': 'cinema_name_source'}, axis=1)

# объединяем с другими датасетами
screenings_pre = pd.merge(screenings_pre, cinema[['cinema_id', "cinema_name_source"]], on="cinema_name_source", how="left")

film = film.rename({'title (original)': 'title_original'}, axis=1)

screenings_pre = pd.merge(screenings_pre, film[['film_id', "title_original"]], on="title_original", how="left")



# объединяем с другими датасетами
screenings_pre['day_of_screening'] = screenings_pre['day_of_screening'].str.replace('-', '/')
periodic_ref_id = periodic_ref_id.rename({'periodic_date': 'day_of_screening'}, axis=1)
periodic_ref_id['day_of_screening']= pd.to_datetime(periodic_ref_id['day_of_screening'])
screenings_pre['day_of_screening']= pd.to_datetime(screenings_pre['day_of_screening'])
screenings_pre = pd.merge(screenings_pre, periodic_ref_id[['periodic_ref_id', 'is_programme', 'day_of_screening']], on="day_of_screening", how="left")

screenings_pre["is_programme"] = screenings_pre["is_programme"].replace(np.nan, None)

screenings_pre["is_programme"] = screenings_pre["is_programme"].map(lambda x: literal_eval(x) if type(x) == str else x)
screenings_pre["is_programme"].fillna(False, inplace=True)

screenings_pre = screenings_pre.drop(columns=['cinema_name_source', 'title_original', 'source', 'cinema_name_source', 'source'])

# присваиваем колонку с ID 'screening_id'

screening_id = list(map(str, list(range(1, screenings_pre.shape[0] + 1))))
screenings_pre['screening_id'] = screening_id

def id_create_screen(value):
    if len(value) == 1:
        return "scr0000000" + value
    elif len(value) == 2:
        return "scr000000" + value
    elif len(value) == 3:
        return "scr00000" + value
    elif len(value) == 4:
        return "scr0000" + value
    elif len(value) == 5:
        return "scr000" + value
    elif len(value) == 6:
        return "scr00" + value
    elif len(value) == 7:
        return "scr0" + value
    elif len(value) == 8:
        return "scr" + value

screenings_pre['screening_id'] = screenings_pre['screening_id'].map(id_create_screen)



# располагаем колонки в верной последовательности
screenings = screenings_pre[['screening_id',
                                  'day_of_screening',
                                  'weekday',
                                  'film_title_source',
                                  'film_title_trans',
                                  'is_programme',
                                  'cinema_id',
                                  'film_id',
                                  'periodic_ref_id']]
                              
screenings.to_csv('pre_processing/pre_processing_screenings/Screening.csv', sep=',', index=False, encoding='utf-8')
