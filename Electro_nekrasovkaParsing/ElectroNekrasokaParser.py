!pip install parsel

import requests
from parsel import Selector
import re
import urllib.request as urllib2

import math
import pandas as pd
import random
import time
import itertools
import numpy as np


class ElectroNekrasokaParser:

  """Class to download images from ElectroNekrasovka web-site"""

  def __init__(self, edition_name, edition_number, list_of_years):

    """edition_name in latin how you want to write it"""
    """edition_number could be found on ElectroNekrasovka edition pages in its url in its end& https://electro.nekrasovka.ru/editions/45 -- here it is 45"""
    """vectors_of_years -- years of edition you want to look through"""

    self.edition_name = edition_name
    self.edition_number = edition_number
    self.list_of_years = list(map(str, list_of_years))
    self.main_url = 'https://electro.nekrasovka.ru/editions/'

    self.url_to_edtition = 0
    self.urls_to_pages = 0
    self.all_urls_per_year = 0
    self.list_of_issues_images = 0


  def creating_url_to_edition(self):

    """
    This function is creating url-link to the main page of the edition on the website
    """

    url_to_edition = self.main_url + self.edition_number + '/'

    self.url_to_edtition = url_to_edition

    return url_to_edition

  def creating_urls_to_year_pages(self, flag = True):

    """
    This function returns list of links to each page of the edition sorted by years based on the list_of_years arguement.
    If flag value is True function calls creating_url_to_edition first.
    If it is False, it references self.url_to_edition value that youhave already filled
    """

    if flag is True:

      main_url = self.creating_url_to_edition()

    else:

      main_url = self.url_to_edtition


    years_to_parse = self.list_of_years
    list_of_year_urls = [main_url + i for i in years_to_parse]

    self.urls_to_pages = list_of_year_urls

    return list_of_year_urls


  def reading_html(self, url_to_read):

    """
    This function is reading html of a certain url and returns it as an html-string.
    """

    url = url_to_read

    headers = requests.utils.default_headers()

    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
            }
        )

    try:
      response = requests.get(url, headers=headers)

      print(f'Your url: {url} has been read properly.')

    except:

      print(f'Your url: {url} cannot be read properly.')

    html_string = response.text

    return html_string


  def urls_to_each_page_per_year(self, flag = True):

    """
    This function returns list of links to each page of the edition of the each page where certain issues of the edition are listed.
    If flag value is True function calls creating_urls_to_year_pages first.
    If it is False, it references self.urls_to_pages value that youhave already filled.
    """

    list_of_pages_per_year = []


    if flag is True:

      url_per_years = self.creating_urls_to_year_pages()

    else:

      url_per_years = self.urls_to_pages


    for i in url_per_years:


      html_text = self.reading_html(i)

      page_counter = re.findall('"count":([0-9]{1,2}?),', html_text)
      page_counter = list(map(int, list(page_counter)))
      page_counter = math.ceil(sum(page_counter) / 12)
      page_counter = list(map(str, list(range(1, page_counter+1))))

      list_of_pages_per_year.append(page_counter)

      value = random.randint(0, 5)
      time.sleep(value)

      print('urls_to_each_page_per_year function is executing')


    for i in range(0, len(url_per_years)):
      url_per_years[i] = [url_per_years[i] + '?page=' + s for s in list_of_pages_per_year[i]]


    url_per_years = list(itertools.chain(*url_per_years))

    self.all_urls_per_year = url_per_years


    return url_per_years


  def links_to_images(self, page_num, flag = True):

    """
    This function returns list of lists.
    Each list consists of name of the issue (first list object),
    url-link to the page where isssue is located (second list object),
    url-link to the imapge of the certain page of the each issue based on the page_num arguement (third list object).
    If flag value is True function calls urls_to_each_page_per_year first.
    If it is False, it references self.all_urls_per_year value that youhave already filled.
    """

    page_num = page_num

    iter = 0


    if flag is True:

      all_links = self.urls_to_each_page_per_year()

    else:

      all_links = self.all_urls_per_year

    for i in range(0, len(all_links)):

      try_string = self.reading_html(all_links[i])

      if iter == 0:

        all_names = re.findall('{"title":"([^"]+)","image":"[^"]+","url":"([^"]+)","is_public":1,"is_active":1}', try_string)
        all_names = [list(tup) for tup in all_names]
        all_names_final = all_names

      else:

        all_names = re.findall('{"title":"([^"]+)","image":"[^"]+","url":"([^"]+)","is_public":1,"is_active":1}', try_string)
        all_names = [list(tup) for tup in all_names]
        all_names_final = all_names_final + all_names

      value = random.randint(0, 5)
      time.sleep(value)

      iter += 1
      print(iter)

      print('links_to_images function is executing')

    for i in range(0, len(all_names_final)):

      link_to_picture = 'https://api.electro.nekrasovka.ru/api' + all_names_final[i][1] +'/pages/' + page_num + '/img/original'
      all_names_final[i][1] = 'https://electro.nekrasovka.ru' + all_names_final[i][1] +'/pages/1'
      all_names_final[i].append(link_to_picture)


    self.list_of_issues_images = all_names_final

    return all_names_final
