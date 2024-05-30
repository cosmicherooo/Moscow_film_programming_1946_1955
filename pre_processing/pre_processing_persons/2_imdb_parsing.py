

!pip install parsel
import os
from parsel import Selector
import re
import urllib.request as urllib2

import pandas as pd
import random
import time
import numpy as np

from MovieInfoIMDb import MovieInfoIMDb

unique_title = pd.read_csv("/content/df_for_imdb_parsing.csv")

unique_title = unique_title.replace(np.nan, None)

iterator = 0

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


    value = random.randint(0, 3)
    time.sleep(value)

  else:
    pass

  iterator += 1
  print(iterator)

unique_title.to_csv('df_after_parsing.csv', index=False)
