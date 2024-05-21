import pandas as pd
import random
import time
from imdb_class_parser import MovieInfoIMDb

folder_to_save = '/'

url = 'https://github.com/cosmicherooo/Moscow_film_programming_1946_1955/blob/main/imdb_parsing/film_test.csv'
test_df = pd.read_csv(url, index_col=0)

test_df["Directors"] = None
test_df["Writers"] = None
test_df["Actors"] = None
test_df["Country of origin"] = None
test_df["Duration (min)"] = None

for i in range(0, test_df.shape[0]):

  imdb_url = test_df['IMDB_id'][i]
  film_id = test_df['film_id'][i]

  film_in_cycle = MovieInfoIMDb(film_id, imdb_url)
  film_in_cycle.reading_html()
  film_in_cycle.writing_html_into_txt(folder_to_save)

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


  value = random.randint(0, 10)
  time.sleep(value)

test_df.to_csv('enriched.csv', index=False)  
