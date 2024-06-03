from filtering_films import *
import re

# Вызываем функцию, которая возвращает информацию о всех фильмах, где Юлий Райзман был режиссером

"""
testing_query_1 = filtering_films(person_name = ('Yuli Raizman',),
                                 is_actor = False,
                                 is_writer = False
                                 )
print(testing_query_1[0])
print(testing_query_1[1])

testing_query_1[0].to_csv('testing_query_1.csv', index=False, encoding='utf-8')
"""

"""
# Выызываем информаци о кинокартинах, которые вышли на советских экранах между 1946 и 1955 гг.
# и были произведены до 1941 года
testing_query_2 = filtering_films(year_of_prod_max = 1941)

print(testing_query_2[0])
print(testing_query_2[1])

testing_query_2[0].to_csv('testing_query_2.csv', index=False, encoding='utf-8')

"""

"""
# Вызываем функцию, которая демонстрирует, в каких картинах Сергей Эйзенштейн был режиссером, и они были произведены
# после 1944 года.
testing_query_3 = filtering_films(person_name = ('Sergei Eisenstein',),
                                  is_actor = False,
                                  is_writer = False,
                                  year_of_prod_min = 1944)
                      
print(testing_query_3[0])
print(testing_query_3[1])

testing_query_3[0].to_csv('testing_query_3.csv', index=False, encoding='utf-8')
"""
"""
# вызываем функцию, которая выводит информацию о кинокартинах, продолдительность которых была меньше или равна 1 часу (60 минутам)
testing_query_4 = filtering_films(duration_max = 60)
print(testing_query_4[0])
print(testing_query_4[1])

testing_query_4[0].to_csv('testing_query_4.csv', index=False, encoding='utf-8')
"""





# вызываем функцию, которая выводит инфомрацию о фильмах, в съемках которых принимали участие и Mikhail Vitukhnovsky, и Yakov Yaluner

testing_query_5 = filtering_films(person_name = ('Mikhail Vitukhnovsky', 'Yakov Yaluner'),
                                  and_pers_operator= True )
print(testing_query_5[0])
print(testing_query_5[1])

testing_query_5[0].to_csv('testing_query_5.csv', index=False, encoding='utf-8')


                      





