from screenings_per_film import *


# Вызываем функцию, которая возвращает
# колчество экранодней для фильма "Александр Невский" 1947 году.


testing_query_1 = screenings_per_film(film_name='Александр Невский',
                                      year=1947)

print(testing_query_1[0])
print(testing_query_1[1])

testing_query_1[0].to_csv('testing_query_1.csv', index=False, encoding='utf-8')


# Вызываем функцию, которая возвращает
# колчество экранодней для фильма 'Mágnás Miska' в 1950 году.


testing_query_2 = screenings_per_film(film_name='Mágnás Miska',
                                      year=1950)

print(testing_query_2[0])
print(testing_query_2[1])

testing_query_2[0].to_csv('testing_query_2.csv', index=False, encoding='utf-8')
