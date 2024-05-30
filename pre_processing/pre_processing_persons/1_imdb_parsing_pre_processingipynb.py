

import pandas as pd
import random
import time
#from imdb_class_parser import MovieInfoIMDb


# предобрабатываем изначальный датасет "Dataset_Moscow_1946-1955_UPD_Film Programming, 1946–1955.csv"

# загружаем датасет

film_programming_df = pd.read_csv("Dataset_Moscow_1946-1955_UPD_Film Programming, 1946–1955.csv")

# сначала нам нужны только колонки с оригинальным названием фильма "title (original)" и "IMDB id"
# предварительно нужно очистить неправильно конвертированные данные после выгрузки csv-файла из Google Sheets
unique_title = film_programming_df[['title (original)', 'IMDB id']].copy()
unique_title['IMDB id'] = unique_title['IMDB id'].astype(str)
unique_title['IMDB id'] = unique_title['IMDB id'].str.replace('.0', '')


# получаем только уникальные кинофильмы
unique_title = unique_title.drop_duplicates()

# присваиваем каждому фильму уникальный идентификатор

numb_for_flm_id = list(map(str, list(range(1, unique_title.shape[0] + 1))))
unique_title['film_id'] = numb_for_flm_id

def id_create_film(value):
    if len(value) == 1:
        return "flm000000" + value
    elif len(value) == 2:
        return "flm00000" + value
    elif len(value) == 3:
        return "flm0000" + value
    elif len(value) == 4:
        return "flm000" + value
    elif len(value) == 5:
        return "flm00" + value
    elif len(value) == 6:
        return "flm0" + value
    elif len(value) == 7:
        return "flm" + value

unique_title['film_id'] = unique_title['film_id'].map(id_create_film)

# затем приводим "IMDB id" в общепринятый вид: tt0050083

def id_create_imdb(value):
    if len(value) == 1 and value != 'nan':
        return "tt000000" + value
    elif len(value) == 2 and value != 'nan':
        return "tt00000" + value
    elif len(value) == 3 and value != 'nan':
        return "tt0000" + value
    elif len(value) == 4 and value != 'nan':
        return "tt000" + value
    elif len(value) == 5 and value != 'nan':
        return "tt00" + value
    elif len(value) == 6 and value != 'nan':
        return "tt0" + value
    elif len(value) >= 7 and value != 'nan':
        return "tt" + value

unique_title['IMDB id'] = unique_title['IMDB id'].map(id_create_imdb)


# затем создаем колонку со ссылками на страницу фильма на IMDB:

def creating_imdb_url(value):
  if value is not None:
    return str('https://www.imdb.com/title/' + value + "/")

unique_title['IMDB_url'] = unique_title['IMDB id'].map(creating_imdb_url)
unique_title = unique_title.reset_index(drop=True)



unique_title["Directors"] = None
unique_title["Writers"] = None
unique_title["Actors"] = None
unique_title["Country of origin"] = None
unique_title["Duration (min)"] = None
unique_title["Year of Production"] = None


unique_title.to_csv('pre_processing/pre_processing_persons/df_for_imdb_parsing.csv', sep=',', index=False, encoding='utf-8')
