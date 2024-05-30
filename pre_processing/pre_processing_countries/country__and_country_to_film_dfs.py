import pandas as pd
import math
import numpy as np
from ast import literal_eval

# создаем таблицу со странами и соединительную таблицу между странами и фильмами
# преобразуем изначальный датасет, где уже были указания на место произвоства фильмов
film_programming_df = pd.read_csv("Dataset_Moscow_1946-1955_UPD_Film Programming, 1946–1955.csv")
df_to_merge_films = pd.read_csv("pre_processing/pre_processing_cinemas/Film.csv")
get_countries = film_programming_df[['title (original)', 'country of origin']]
# удаляем дубликаты
get_countries = get_countries.drop_duplicates()
get_countries.drop(get_countries.tail(1).index,inplace=True)
get_countries = get_countries.reset_index(drop=True)
get_countries = pd.merge(get_countries, df_to_merge_films[['film_id', 'title (original)']], on="title (original)", how="left")


get_countries['country of origin'] = get_countries['country of origin'].apply(lambda x: [i for i in x.split(',')])
get_countries = get_countries.explode('country of origin').fillna('').reset_index(drop=False)
get_countries = get_countries.replace('Unknown', None)
get_countries = get_countries.dropna()
get_countries = get_countries.applymap(lambda x: x.strip() if isinstance(x, str) else x)


# Создаем датасет Country

data_country = [['ctr000001', 'Soviet Union', 'SU'],
                ['ctr000002', 'United States', 'US'],
                ['ctr000003', 'Great Britian', 'GB'],
                ['ctr000004', 'East Germany', 'DD'],
                ['ctr000005', 'Mongolia', 'MN'],
                ['ctr000006', 'Bulgaria', 'BG'],
                ['ctr000007', 'West Germany', 'DE'],
                ['ctr000008', 'Romania', 'RO'],
                ['ctr000009', 'Czechoslovakia', 'CS'],
                ['ctr000010', 'France', 'FR'],
                ['ctr000011', 'Italy', 'IT'],
                ['ctr000012', 'Poland', 'PL'],
                ['ctr000013', 'Austria', 'AT'],
                ['ctr000014', 'Albania', 'AL'],
                ['ctr000015', 'Idnia', 'IN'],
                ['ctr000016', 'China', 'CN'],
                ['ctr000017', 'Mexico', 'MX'],
                ['ctr000018', 'North Korea', 'KP'],
                ['ctr000019', 'Finland', 'FI'],
                ['ctr000020', 'Vietnam', 'VN'],
                ['ctr000021', 'Japan', 'JP'],
                ['ctr000022', 'Argentina', 'AR'],
                ['ctr000023', 'Yugoslavia', 'YU'],
                ['ctr000024', 'Norway', 'NO'],
                ['ctr000025', 'Hungary', 'HU']]

# Отдельная таблица Country готова!
country_df = pd.DataFrame(data_country, columns=['country_id',
                                                 'country_name',
                                                 'ISO_3166_1_alpha_2'])
country_df.to_csv('Country.csv', index=False)


# Теперь создаем соединительную таблицу Country_to_film
get_countries = get_countries.rename(columns={'country of origin': 'ISO_3166_1_alpha_2'})

country_to_film = pd.merge(country_df, get_countries[["ISO_3166_1_alpha_2", 'film_id']], on="ISO_3166_1_alpha_2", how="left")

# соединительная таблица готова!
country_to_film = country_to_film[['film_id', 'country_id']]

country_to_film.to_csv('pre_processing/pre_processing_countries/country_to_film.csv', index=False)
