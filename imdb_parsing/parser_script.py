import pandas as pd
import random
import time
from imdb_class_parser import MovieInfoIMDb

folder_to_save = '/'

url = 'https://github.com/cosmicherooo/Moscow_film_programming_1946_1955/blob/main/imdb_parsing/film_test.csv'
test_df = pd.read_csv(url, index_col=0)


for i in range(0, test_df.shape[0]):

  imdb_url = test_df['IMDB_id'][i]
  film_id = test_df['film_id'][i]

  film_in_cycle = MovieInfoIMDb(film_id, imdb_url)
  film_in_cycle.reading_html()
  #film_in_cycle.writing_html_into_txt(folder_to_save)

  film_in_cycle.add_actors_names()
  film_in_cycle.add_country_of_origin()
  film_in_cycle.add_directors_names()
  film_in_cycle.add_film_duration()
  film_in_cycle.add_writers_names()

  test_df['Directors'][i] = film_in_cycle.directors_names
  test_df['Writers'][i] = film_in_cycle.writers_names
  test_df['Actors'][i] = film_in_cycle.actors_names
  test_df['Country of origin'][i] = film_in_cycle.country_of_origin
  test_df['Duration (min)'][i] = film_in_cycle.duration


  value = random.randint(0, 5)
  time.sleep(value)



directors_df = test_df[['film_id', 'title (source)', 'Directors']].copy()
writers_df = test_df[['film_id', 'title (source)', 'Writers']].copy()
actors_df = test_df[['film_id', 'title (source)', 'Actors']].copy()
duration_df = test_df[['film_id', 'title (source)', 'Duration (min)']].copy()
country_df = test_df[['film_id', 'title (source)', 'Country of origin']].copy()


writers_df_collapsed = writers_df.explode('Writers').fillna('').reset_index(drop=True)
writers_df_collapsed[['IMDb_ID','Writers']] = pd.DataFrame(writers_df_collapsed['Writers'].tolist(), index=writers_df_collapsed.index)


directors_df_collapsed = directors_df.explode('Directors').fillna('').reset_index(drop=True)
directors_df_collapsed[['IMDb_ID','Directors']] = pd.DataFrame(directors_df_collapsed['Directors'].tolist(), index=directors_df_collapsed.index)

actors_df_collapsed = actors_df.explode('Actors').fillna('').reset_index(drop=True)
actors_df_collapsed[['IMDb_ID','Actors']] = pd.DataFrame(actors_df_collapsed['Actors'].tolist(), index=actors_df_collapsed.index)


country_df_collapsed = country_df.explode('Country of origin').fillna('None').reset_index(drop=True)


writers_df_collapsed.to_csv('writers_df', sep=',', index=False, encoding='utf-8')
directors_df_collapsed.to_csv('directors_df', sep=',', index=False, encoding='utf-8')
actors_df_collapsed.to_csv('actors_df', sep=',', index=False, encoding='utf-8')
country_df_collapsed.to_csv('country_df', sep=',', index=False, encoding='utf-8')
duration_df.to_csv('duration_df', sep=',', index=False, encoding='utf-8')




