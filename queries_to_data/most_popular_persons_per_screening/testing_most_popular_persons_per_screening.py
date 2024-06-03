from most_popular_persons_per_screening import *


# Вызываем функцию, которая возвращает информацию о количестве
# экранодней для каждого режиссера, чей фильмы демонстрировался в 1950 году.
testing_query_1 = screenings_each_person(role = 'Director',
                                         year = 1950)

print(testing_query_1)

testing_query_1.to_csv('testing_query_1.csv', index=False, encoding='utf-8')

# Вызываем функцию, которая возвращает информацию о количестве
# экранодней для каждого актера, чей фильмы демонстрировался в 1954 году.
testing_query_2 = screenings_each_person(role = 'Actor',
                                         year = 1954)

print(testing_query_2)

testing_query_2.to_csv('testing_query_2.csv', index=False, encoding='utf-8')

# Вызываем функцию, которая возвращает информацию о количестве
# экранодней для каждого cценариста (важно отметить, что в качестве сценаристов
# на IMDB, откуда были скачаны данные могут указывать авторы оригинальных произведений,
# на основе которых был снят тот или иной фильм),
# чей фильмы демонстрировался в 1948 году.
testing_query_3 = screenings_each_person(role = 'Writer',
                                         year = 1948)

print(testing_query_3)

testing_query_3.to_csv('testing_query_3.csv', index=False, encoding='utf-8')