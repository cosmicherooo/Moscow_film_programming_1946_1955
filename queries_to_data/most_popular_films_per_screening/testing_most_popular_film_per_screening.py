from most_popular_films_per_screening import *


# Вызываем функцию, которая возвращает информацию о количестве
# экранодней для каждого фильма в 1946 году.
testing_query_1 = screenings_each_film(year = 1946)

print(testing_query_1)

testing_query_1.to_csv('testing_query_1.csv', index=False, encoding='utf-8')

# Вызываем функцию, которая возвращает информацию о количестве
# экранодней для каждого фильма в 1951 году.
testing_query_2 = screenings_each_film(year = 1951)

print(testing_query_2)

testing_query_2.to_csv('testing_query_2.csv', index=False, encoding='utf-8')

# Вызываем функцию, которая возвращает информацию о количестве
# экранодней для каждого фильма в 1955 году.
testing_query_3 = screenings_each_film(year = 1955)

print(testing_query_3)

testing_query_3.to_csv('testing_query_3.csv', index=False, encoding='utf-8')
