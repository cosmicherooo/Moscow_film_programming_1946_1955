
import pandas as pd
import math
import numpy as np
from ast import literal_eval


# производим предобработку данных для создания таблиц
# - Cinema_info
# - Cinema
# - Institution

# загружаем изначальный датасет
cinemas_initial_df = pd.read_csv("Cinemas, 1946–1955.csv")

# создаем датасет Cinema

cinema = cinemas_initial_df[['cinema (source)',
                             'cinema (transliteration)']]

# удаляем возможные лишние пробелы в начале или конце строки

cinema['cinema (source)'] = cinema['cinema (source)'].str.strip()
cinema['cinema (transliteration)'] = cinema['cinema (transliteration)'].str.strip()

# удаляем дубликаты
cinema = cinema.drop_duplicates().reset_index(drop=True)


# присваиваем кинотеатрам ID

cinema_id = list(map(str, list(range(1, cinema.shape[0] + 1))))
cinema['cinema_id'] = cinema_id

def id_create_cinema(value):
    if len(value) == 1 and value != 'nan':
        return "cin000000" + value
    elif len(value) == 2 and value != 'nan':
        return "cin00000" + value
    elif len(value) == 3 and value != 'nan':
        return "cin0000" + value
    elif len(value) == 4 and value != 'nan':
        return "cin000" + value
    elif len(value) == 5 and value != 'nan':
        return "cin00" + value
    elif len(value) == 6 and value != 'nan':
        return "cin0" + value
    elif len(value) >= 7 and value != 'nan':
        return "cin" + value

cinema['cinema_id'] = cinema['cinema_id'].map(id_create_cinema)

# расставляем колонки в нужной последовательности и присваиваем другие названия
cinema = cinema[['cinema_id',
                 'cinema (source)',
                 'cinema (transliteration)']]


cinema = cinema.rename(columns={'cinema (source)': 'cinema_name_source',
                                'cinema (transliteration)': 'cinema_name_trans'})

# сохраняем необходимый для загрузки в базу датасет
cinema.to_csv('pre_processing/pre_processing_cinemas/Cinema.csv', sep=',', index=False, encoding='utf-8')
