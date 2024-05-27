import pandas as pd
import math
import numpy as np
from ast import literal_eval

# создаем датасет Cinema_info

# Загружаем необходимые датасеты
cinemas_initial_df = pd.read_csv("/content/Cinemas, 1946–1955.csv")
cinema = pd.read_csv("/content/Cinema.csv")
institution = pd.read_csv("/content/Institution.csv")
country = pd.read_csv("/content/Country.csv")

# преобразуем NaN в None
cinemas_initial_df = cinemas_initial_df.replace(np.nan, None)
cinemas_initial_df = cinemas_initial_df.replace('Unknown', None)

# сбрасываем колонку 'cinema (ID)'
cinemas_initial_df = cinemas_initial_df.drop(columns=['cinema (ID)'])


# разбиваем на отдельные колонки колонки "lat,long" и "city, country"

cinemas_initial_df[['lat', 'long']] = cinemas_initial_df['lat,long'].str.split(',', expand=True)
cinemas_initial_df = cinemas_initial_df.drop(columns=['lat,long'])

# меняем тип переменной в колонках 'lat' и 'long' на float
cinemas_initial_df[['lat', 'long']] = cinemas_initial_df[['lat', 'long']] .fillna(0).astype('float')
cinemas_initial_df[['lat', 'long']] = cinemas_initial_df[['lat', 'long']] .replace(0, None)

cinemas_initial_df[['city', 'country']] = cinemas_initial_df['city, country'].str.split(', ', expand=True)
cinemas_initial_df = cinemas_initial_df.drop(columns=['city, country'])

# меняем тип данные в колонке run с float на int
cinemas_initial_df['run'] = cinemas_initial_df['run'].fillna(0).astype('int')
cinemas_initial_df['run'] = cinemas_initial_df['run'].replace(0, None)

# меняем тип переменных в колонке 'reconstruction' на boolean
cinemas_initial_df['reconstruction'].replace({0: False, 1: True}, inplace=True)


# присваиваем колонку с ID 'cinema_info_id'

cinemas_inf_id = list(map(str, list(range(1, cinemas_initial_df.shape[0] + 1))))
cinemas_initial_df['cinema_info_id'] = cinemas_inf_id

def id_create_cin_inf(value):
    if len(value) == 1:
        return "cid000000" + value
    elif len(value) == 2:
        return "cid00000" + value
    elif len(value) == 3:
        return "cid0000" + value
    elif len(value) == 4:
        return "cid000" + value
    elif len(value) == 5:
        return "cid00" + value
    elif len(value) == 6:
        return "cid0" + value
    elif len(value) == 7:
        return "cid" + value

cinemas_initial_df['cinema_info_id'] = cinemas_initial_df['cinema_info_id'].map(id_create_cin_inf)


# переименовываем колонки для дальнейшего объединения

cinemas_initial_df = cinemas_initial_df.rename({'cinema (source)': 'cinema_name_source',
                                                'cinema (transliteration)': 'cinema_name_trans',
                                                'affiliation': 'institution_name',
                                                'country': 'ISO_3166_1_alpha_2',
                                                'address': 'address_cinema'}, axis=1)

# объединяем с другими таблицами, чтобы присвоить внешние ключи

cinemas_initial_df = pd.merge(cinemas_initial_df, country[['ISO_3166_1_alpha_2', "country_id"]], on="ISO_3166_1_alpha_2", how="left")
cinemas_initial_df = pd.merge(cinemas_initial_df, institution[['institution_name', "institution_id"]], on="institution_name", how="left")
cinemas_initial_df = pd.merge(cinemas_initial_df, cinema[['cinema_id', "cinema_name_source"]], on="cinema_name_source", how="left")

# сбрасываем ненужные колонки
cinemas_initial_df = cinemas_initial_df.drop(columns=['ISO_3166_1_alpha_2', 'institution_name', 'cinema_name_source', 'cinema_name_trans'])

# расставляем колонки в верном порядке
cinema_info = cinemas_initial_df[['cinema_info_id',
                                  'year',
                                  'run',
                                  'seats',
                                  'address_cinema',
                                  'city',
                                  'lat',
                                  'long',
                                  'sources',
                                  'comments',
                                  'reconstruction',
                                  'cinema_id',
                                  'institution_id',
                                  'country_id']]

# сохраняем в виде файла формата csv с названием "Cinema_info"
cinema_info.to_csv('Cinema_info.csv', sep=',', index=False, encoding='utf-8')
