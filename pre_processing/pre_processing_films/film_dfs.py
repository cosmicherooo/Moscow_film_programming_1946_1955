import pandas as pd
import math
import numpy as np
from ast import literal_eval

# преодобрабатываем, что у нас пойдет в таблицу Film

df_after_parsing = pd.read_csv("pre_processing/pre_processing_persons/df_after_parsing.csv")

df_after_parsing = df_after_parsing.replace(np.nan, None)

df_after_parsing['Writers'] = df_after_parsing['Writers'].map(lambda x: literal_eval(x) if type(x) == str else x)
df_after_parsing['Directors'] = df_after_parsing['Directors'].map(lambda x: literal_eval(x) if type(x) == str else x)
df_after_parsing['Actors'] = df_after_parsing['Actors'].map(lambda x: literal_eval(x) if type(x) == str else x)
df_after_parsing['Country of origin'] = df_after_parsing['Country of origin'].map(lambda x: literal_eval(x) if type(x) == str else x)
df_after_parsing['Year of Production'] = df_after_parsing['Year of Production'].map(lambda x: literal_eval(x) if type(x) == str else x)




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


df_to_merge_films['Duration (min)'] = df_to_merge_films['Duration (min)'].fillna(0).astype(int)    

df_to_merge_films = df_to_merge_films.replace(0, None)


# сохраняем в csv-файл
df_to_merge_films.to_csv('pre_processing/pre_processing_films/Film.csv', index=False)
