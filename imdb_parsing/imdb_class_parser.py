!pip install parsel
import os 
from parsel import Selector
import re
import urllib.request as urllib2

class MovieInfoIMDb:

  """Class representing a Movie on IMDb"""

  def __init__(self, db_movie_id, imdb_url):

    self.db_movie_id = db_movie_id
    self.imdb_url = imdb_url
    self.actors_names = 0
    self.writers_names = 0
    self.directors_names = 0
    self.country_of_origin = 0
    self.duration = 0
    self.sel_obj = 0
    self.str_html_obj = 0



  def reading_html(self):

    url_to_read = self.imdb_url
    req = urllib2.Request(url_to_read, None, {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
    response = str(urllib2.urlopen(req).read())
    sel = Selector(response)

    self.sel_obj = sel
    self.str_html_obj = response

  def writing_html_into_txt(self, save_path):


    try:

      name_of_file = os.path.join(save_path, str(self.db_movie_id) + '_html_str' + '.txt')

    except:

      print("There is an error: check your class objects")

    with open(name_of_file, "w") as file:

      file.write(self.str_html_obj)

      print(f'{name_of_file} is created!')



  def add_actors_names(self):

    try:
      actors_names_list = list(set(re.findall('href=[\'"]?/name/([^\'" >]+)/\?ref_=tt_cl_t_.{1,2}[\'"] class="sc-bfec09a1-1 gCQkeh">(.*?)</a>', self.str_html_obj)))
    except:
      print('Xpath-finder cannot be a appleid to yuor object!')

    try:
      self.actors_names = actors_names_list
    except:
      print('Actors-object cannot be added to a class properly!')




  def add_writers_names(self):

    try:
      writers_names_list = list(set(re.findall('href=[\'"]?/name/([^\'" >]+)/\?ref_=tt_ov_wr">(.*?)</a>', self.str_html_obj)))
    except:
      print('Xpath-finder cannot be a appleid to yuor object!')


    try:
      self.writers_names = writers_names_list
    except:

      print('Writers-object cannot be added to a class properly!')




  def add_directors_names(self):
    try:
      directors_names_list = list(set(re.findall('href=[\'"]?/name/([^\'" >]+)/\?ref_=tt_ov_dr">(.*?)</a>', self.str_html_obj)))
    except:
      print('Xpath-finder cannot be a appleid to yuor object!')

    try:
      self.directors_names = directors_names_list
    except:
      print('Direcots-object cannot be added to a class properly!')




  def add_country_of_origin(self):

    if type(self.str_html_obj) == str:

      try:
        country_of_origin_list = re.findall('country_of_origin=(.*?)&amp', self.str_html_obj)
      except:
        print('Cannot find country of origin in HTML-file!')

      try:
        self.country_of_origin = country_of_origin_list
      except:
        print('Country-of-origin-object cannot be added to a class properly!')

    else:
      print('You need to convert your data type to str-type!')


  def add_film_duration(self):

    if type(self.str_html_obj) == str:

      try:

        time_list = (re.findall('<meta property="og:description" content="(.{0,2}?h)?( )?(.{0,2}?m)?', self.str_html_obj))[0]

        hours = re.findall('[0-9][0-9]?', time_list[0])
        mins = re.findall('[0-9][0-9]?', time_list[2])

        hours_zero = False
        mins_zero = False

        if len(hours) == 1:
          hours = int(hours[0])

        elif len(hours) == 0:

          hours = 0
          hours_zero = True

        else:
          hours_zero = True
          print("Hours were not written correctly")


        if len(mins) == 1:
          mins = int(mins[0])

        elif len(mins) == 0:

          mins = 0
          mins_zero = True

        else:

          mins_zero = True
          print("Minutes were not written correctly")


        if mins_zero & hours_zero == True:

          overall_mins = 0
          print("Film duration is not accessible, it assigned to zero!")

        else:

          overall_mins = hours*60 + mins


      except:
        print('Cannot find country of origin in HTML-file!')

      try:
        self.duration = overall_mins
      except:
        print('Duration-object cannot be added to a class properly!')

    else:
      print('You need to convert your data type to str-type!')



