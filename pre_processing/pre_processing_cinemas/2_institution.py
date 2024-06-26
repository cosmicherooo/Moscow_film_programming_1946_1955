import pandas as pd
import math
import numpy as np
from ast import literal_eval

# Создаем датасет Institution

# Загружаем необходимые датасеты
cinemas_initial_df = pd.read_csv("Cinemas, 1946–1955.csv")

# оставляем только нужные колонки
institution = cinemas_initial_df[['affiliation']].drop_duplicates().reset_index(drop=True)

# присваиваем институциям ID

institution_id = list(map(str, list(range(1, institution.shape[0] + 1))))
institution['institution_id'] = institution_id

def id_create_institution(value):
    if len(value) == 1 and value != 'nan':
        return "ins000000" + value
    elif len(value) == 2 and value != 'nan':
        return "ins00000" + value
    elif len(value) == 3 and value != 'nan':
        return "ins0000" + value
    elif len(value) == 4 and value != 'nan':
        return "ins000" + value
    elif len(value) == 5 and value != 'nan':
        return "ins00" + value
    elif len(value) == 6 and value != 'nan':
        return "ins0" + value
    elif len(value) >= 7 and value != 'nan':
        return "ins" + value

institution['institution_id'] = institution['institution_id'].map(id_create_institution)

# Добавляем новые колонки

institution['address_inst'] = None
institution['city'] = 'Moscow'
institution['country_id'] = 'ctr000001'


# переименовываем колонки
"institution_name"

institution = institution.rename(columns={'affiliation': 'institution_name'})

# расставляем колонки в нужной последовательности

institution = institution[['institution_id',
                           'institution_name',
                           'address_inst',
                           'city',
                           'country_id']]


 # Сохраняем в датасет Institution для последующей загрузки в базу
institution.to_csv('pre_processing/pre_processing_cinemas/Institution.csv', sep=',', index=False, encoding='utf-8')
