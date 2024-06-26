# часть предобработки, после которой появляются датасеты для загрузки в базу данных:
# -- periodic_ref.csv
# -- periodic.csv

import math
import pandas as pd
import numpy as np

# Дальнейшая предобрабокта, после которой появился столбец is_programme, где отмечено, какие номера газет содержат афиши
# 1 -- содержат, 0 -- не содежрат

all_issues_VM_1946_1955_df = pd.read_csv('pre_processing/pre_rpocessing_periodics/is_prog_periodic_ref.csv')

# присваиваем каждому выпуску газеты уникальный идентификатор

numb_for_prd_ref_id = list(map(str, list(range(1, all_issues_VM_1946_1955_df.shape[0] + 1))))
all_issues_VM_1946_1955_df['periodic_ref_id'] = numb_for_prd_ref_id

def id_create_prd_ref(value):
    if len(value) == 1:
        return "prd000000" + value
    elif len(value) == 2:
        return "prd00000" + value
    elif len(value) == 3:
        return "prd0000" + value
    elif len(value) == 4:
        return "prd000" + value
    elif len(value) == 5:
        return "prd00" + value
    elif len(value) == 6:
        return "prd0" + value
    elif len(value) == 7:
        return "prd" + value

all_issues_VM_1946_1955_df['periodic_ref_id'] = all_issues_VM_1946_1955_df['periodic_ref_id'].map(id_create_prd_ref)



# создаем таблицу Periodic, там будет только один кортеж - Вечерняя Москва

data_periodic = [['prd000001',
                  'Вечерняя Москва',
                  'Vecherniaia Moskva']]




# Отдельная таблица Country готова!
periodic_df = pd.DataFrame(data_periodic, columns=['periodic_id',
                                                   'periodic_name_original',
                                                   'periodic_name_trans'])

# присоединяем колонку внешний ключ, связывающий таблицу priodic_df с periodic_ref

numb_for_prd_ref_id = list(map(str, list(range(1, all_issues_VM_1946_1955_df.shape[0] + 1))))
all_issues_VM_1946_1955_df['periodic_ref_id'] = numb_for_prd_ref_id

def id_create_prd_ref(value):
    if len(value) == 1:
        return "iss000000" + value
    elif len(value) == 2:
        return "iss00000" + value
    elif len(value) == 3:
        return "iss0000" + value
    elif len(value) == 4:
        return "iss000" + value
    elif len(value) == 5:
        return "iss00" + value
    elif len(value) == 6:
        return "iss0" + value
    elif len(value) == 7:
        return "iss" + value

all_issues_VM_1946_1955_df['periodic_ref_id'] = all_issues_VM_1946_1955_df['periodic_ref_id'].map(id_create_prd_ref)

all_issues_VM_1946_1955_df['periodic_id'] = periodic_df['periodic_id'][0]

all_issues_VM_1946_1955_df = all_issues_VM_1946_1955_df[['periodic_ref_id', 'periodic_issue', 'periodic_url',
                                                         'periodic_url_programme',
                                                         'periodic_date', 'is_programme','periodic_id']]


all_issues_VM_1946_1955_df['is_programme'].replace({0: False, 1: True}, inplace=True)


# сохраняем таблицы в отдельные csv-файлы, предобработка двух таблиц для загрузки закончена

periodic_df.to_csv('pre_processing/pre_rpocessing_periodics/periodic.csv', sep=',', index=False, encoding='utf-8')
all_issues_VM_1946_1955_df.to_csv('pre_processing/pre_rpocessing_periodics/periodic_ref.csv', sep=',', index=False, encoding='utf-8')
