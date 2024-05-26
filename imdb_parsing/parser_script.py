import pandas as pd
import random
import time
from imdb_class_parser import MovieInfoIMDb

# предобрабатываем изначальный датасет "Dataset_Moscow_1946-1955_UPD_Film Programming, 1946–1955.csv"

# загружаем датасет

film_programming_df = pd.read_csv("imdb_parsing/Dataset_Moscow_1946-1955_UPD_Film Programming, 1946–1955.csv")

# сначала нам нужны только колонки с оригинальным названием фильма "title (original)" и "IMDB id"
# предварительно нужно очистить неправильно конвертированные данные после выгрузки csv-файла из Google Sheets
unique_title = film_programming_df[['title (original)', 'IMDB id']].copy()
unique_title.drop(unique_title.tail(1).index,inplace=True)
unique_title[['IMDB id']] = unique_title[['IMDB id']].astype(str)
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


folder_to_save = '/content/sample_data/'


# запускаем цикл с применением импортированного класса, который добавляет в датасет необходимые для нас данные.
for i in range(0, unique_title.shape[0]):

  if (unique_title['IMDB_url'][i]) is not None:

    imdb_url = unique_title['IMDB_url'][i]
    film_id = unique_title['film_id'][i]

    film_in_cycle = MovieInfoIMDb(film_id, imdb_url)
    film_in_cycle.reading_html()
    #film_in_cycle.writing_html_into_txt(folder_to_save)

    film_in_cycle.add_actors_names()
    film_in_cycle.add_country_of_origin()
    film_in_cycle.add_directors_names()
    film_in_cycle.add_film_duration()
    film_in_cycle.add_writers_names()
    film_in_cycle.add_year_of_production()

    unique_title['Directors'][i] = film_in_cycle.directors_names
    unique_title['Writers'][i] = film_in_cycle.writers_names
    unique_title['Actors'][i] = film_in_cycle.actors_names
    unique_title['Country of origin'][i] = film_in_cycle.country_of_origin
    unique_title['Duration (min)'][i] = film_in_cycle.duration
    unique_title['Year of Production'][i] = film_in_cycle.year_of_production


    value = random.randint(0, 5)
    time.sleep(value)
  else:
    pass


# проводим дальнейшую предобработку, в ходе которой будет сформировано два датасета для загрузки в базу данных
# Person и person_to_film

df_after_parsing = unique_title

directors_df = df_after_parsing[['film_id', 'title (original)', 'Directors']].copy()
writers_df = df_after_parsing[['film_id', 'title (original)', 'Writers']].copy()
actors_df = df_after_parsing[['film_id', 'title (original)', 'Actors']].copy()
duration_df = df_after_parsing[['film_id', 'title (original)', 'Duration (min)']].copy()
country_df = df_after_parsing[['film_id', 'title (original)', 'Country of origin']].copy()
year_of_production_df = df_after_parsing[['film_id', 'title (original)', 'Year of Production']].copy()


writers_df_collapsed = writers_df.explode('Writers').fillna('').reset_index(drop=True)
writers_df_collapsed[['IMDb_ID', 'Writers']] = pd.DataFrame(writers_df_collapsed['Writers'].tolist(), index=writers_df_collapsed.index)
writers_df_collapsed = writers_df_collapsed[writers_df_collapsed['Writers'].notna()]


directors_df_collapsed = directors_df.explode('Directors').fillna('').reset_index(drop=True)
directors_df_collapsed[['IMDb_ID', 'Directors']] = pd.DataFrame(directors_df_collapsed['Directors'].tolist(), index=directors_df_collapsed.index)
directors_df_collapsed = directors_df_collapsed[directors_df_collapsed['Directors'].notna()]



actors_df_collapsed = actors_df.explode('Actors').fillna('').reset_index(drop=True)
actors_df_collapsed.at[0, 'Actors'] = (None, None)
actors_df_collapsed[['IMDb_ID', 'Actors']] = pd.DataFrame(actors_df_collapsed['Actors'].tolist(), index=actors_df_collapsed.index)
actors_df_collapsed = actors_df_collapsed[actors_df_collapsed['Actors'].notna()]


country_df_collapsed = country_df.explode('Country of origin').fillna('').reset_index(drop=True)

writers_df_collapsed['Role'] = 'Writer'
directors_df_collapsed['Role'] = 'Director'
actors_df_collapsed['Role'] = 'Actor'


# создаем отдельные датасет Person
# сначала соединяем три отдельных датасета и удаляем повторения

df_writer = writers_df_collapsed.rename({'Writers': 'person_name'}, axis=1)
df_writer = df_writer[['person_name', 'IMDb_ID']].copy()
df_actor = actors_df_collapsed.rename({'Actors': 'person_name'}, axis=1)
df_actor = df_actor[['person_name', 'IMDb_ID']].copy()
df_director = directors_df_collapsed.rename({'Directors': 'person_name'}, axis=1)
df_director = df_director[['person_name', 'IMDb_ID']].copy()


# соединили
data_to_concat = [df_writer, df_actor, df_director]
persons_collapsed = pd.concat(data_to_concat, ignore_index=True)

# удалили дубликаты
unique_persons = persons_collapsed.drop_duplicates()

# присваиваем каждой личности ID

numb_for_per_id = list(map(str, list(range(1, unique_persons.shape[0] + 1))))
unique_persons['person_id'] = numb_for_per_id

def id_create_pers(value):
    if len(value) == 1:
        return "per000000" + value
    elif len(value) == 2:
        return "per00000" + value
    elif len(value) == 3:
        return "per0000" + value
    elif len(value) == 4:
        return "per000" + value
    elif len(value) == 5:
        return "per00" + value
    elif len(value) == 6:
        return "per0" + value
    elif len(value) == 7:
        return "per" + value

unique_persons['person_id'] = unique_persons['person_id'].map(id_create_pers)

# главный датасет Person

unique_persons


# Создаем соединительную таблицу, которая будет обеспечивать связи многое-ко-многим

# подгатавливаем датасеты для соединительной таблицы

writers_df_collapsed_pre = pd.merge(writers_df_collapsed, unique_persons[["person_id", 'IMDb_ID']], on="IMDb_ID", how="left")
writers_df_collapsed_pre = writers_df_collapsed_pre[['film_id', 'Role', 'person_id']].copy()

actors_df_collapsed_pre = pd.merge(actors_df_collapsed, unique_persons[["person_id", 'IMDb_ID']], on="IMDb_ID", how="left")
actors_df_collapsed_pre = actors_df_collapsed_pre[['film_id', 'Role', 'person_id']].copy()

directos_df_collapsed_pre = pd.merge(directors_df_collapsed, unique_persons[["person_id", 'IMDb_ID']], on="IMDb_ID", how="left")
directos_df_collapsed_pre = directos_df_collapsed_pre[['film_id', 'Role', 'person_id']].copy()


# Создаем соединительную таблицу, которая будет обеспечивать связи многое-ко-многим
# объединяем три подготовленные таблицы

data_to_concat_2 = [writers_df_collapsed_pre,
                    actors_df_collapsed_pre,
                    directos_df_collapsed_pre]

persons_collapsed_merge_df = pd.concat(data_to_concat_2, ignore_index=True)

# соединительный датасет для обеспечения связи многие-ко-многим готов!


persons_collapsed_merge_df = persons_collapsed_merge_df.reset_index(drop=True)
persons_collapsed_merge_df = persons_collapsed_merge_df[['person_id', 'film_id', 'Role']]

unique_persons = unique_persons.reset_index(drop=True)
unique_persons = unique_persons[['person_id', 'person_name', 'IMDb_ID']]

unique_persons.to_csv('Person.csv', index=False)
persons_collapsed_merge_df.to_csv('person_fo_film.csv', index=False)


# преодобрабатываем, что у нас пойдет в таблицу Film

# избаваляемся от лишних колонок в unique_title
df_to_merge_films = df_after_parsing[['film_id',
                                      'title (original)',
                                      'Year of Production',
                                      'Duration (min)',
                                      'IMDB id']]

# превращаем каждое значение года производтва в тип переменной int
for i in range(0, df_to_merge_films.shape[0]):
  if df_to_merge_films['Year of Production'][i] is not None:
    df_to_merge_films['Year of Production'][i] = int(df_to_merge_films['Year of Production'][i][0])

for i in range(0, df_to_merge_films.shape[0]):
  if df_to_merge_films['Duration (min)'][i] == 0:
    df_to_merge_films['Duration (min)'][i] = None

df_to_merge_films
# сохраняем в csv-файл
df_to_merge_films.to_csv('Film.csv', index=False)






