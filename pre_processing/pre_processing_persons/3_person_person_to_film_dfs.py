
import pandas as pd
import math
import numpy as np
from ast import literal_eval

df_after_parsing = pd.read_csv("pre_processing/pre_processing_persons/df_after_parsing.csv")

df_after_parsing = df_after_parsing.replace(np.nan, None)

df_after_parsing['Writers'] = df_after_parsing['Writers'].map(lambda x: literal_eval(x) if type(x) == str else x)
df_after_parsing['Directors'] = df_after_parsing['Directors'].map(lambda x: literal_eval(x) if type(x) == str else x)
df_after_parsing['Actors'] = df_after_parsing['Actors'].map(lambda x: literal_eval(x) if type(x) == str else x)
df_after_parsing['Country of origin'] = df_after_parsing['Country of origin'].map(lambda x: literal_eval(x) if type(x) == str else x)
df_after_parsing['Year of Production'] = df_after_parsing['Year of Production'].map(lambda x: literal_eval(x) if type(x) == str else x)



directors_df = df_after_parsing[['film_id', 'title (original)', 'Directors']].copy()
writers_df = df_after_parsing[['film_id', 'title (original)', 'Writers']].copy()
actors_df = df_after_parsing[['film_id', 'title (original)', 'Actors']].copy()
duration_df = df_after_parsing[['film_id', 'title (original)', 'Duration (min)']].copy()
country_df = df_after_parsing[['film_id', 'title (original)', 'Country of origin']].copy()
year_of_production_df = df_after_parsing[['film_id', 'title (original)', 'Year of Production']].copy()


writers_df_collapsed = writers_df.explode('Writers').fillna('').reset_index(drop=True)
writers_df_collapsed[['IMDb_ID', 'Writers']] = pd.DataFrame(writers_df_collapsed['Writers'].tolist(), index=writers_df_collapsed.index)
writers_df_collapsed = writers_df_collapsed[writers_df_collapsed['Writers'].notna()]
writers_df_collapsed = writers_df_collapsed.reset_index(drop=True)


directors_df_collapsed = directors_df.explode('Directors').fillna('').reset_index(drop=True)
directors_df_collapsed[['IMDb_ID', 'Directors']] = pd.DataFrame(directors_df_collapsed['Directors'].tolist(), index=directors_df_collapsed.index)
directors_df_collapsed = directors_df_collapsed[directors_df_collapsed['Directors'].notna()]
directors_df_collapsed = directors_df_collapsed.reset_index(drop=True)



actors_df_collapsed = actors_df.explode('Actors').fillna('').reset_index(drop=True)
actors_df_collapsed.at[0, 'Actors'] = (None, None)
actors_df_collapsed[['IMDb_ID', 'Actors']] = pd.DataFrame(actors_df_collapsed['Actors'].tolist(), index=actors_df_collapsed.index)
actors_df_collapsed = actors_df_collapsed[actors_df_collapsed['Actors'].notna()]
actors_df_collapsed = actors_df_collapsed.reset_index(drop=True)


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

unique_persons.to_csv('pre_processing/pre_processing_persons/Person.csv', index=False)
persons_collapsed_merge_df.to_csv('pre_processing/pre_processing_persons/person_fo_film.csv', index=False)
