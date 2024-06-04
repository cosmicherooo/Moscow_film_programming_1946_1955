from popstat_per_film import *

# Вызываем функцию, которая возвращает POPSTAT для фильма Весна, Далекая
# Невеста и Поезд идет на Восток за 1948 год.
testing_query_1 = screenings_per_film(film_name=('Весна',
                                                 'Далекая невеста',
                                                 'Поезд идет на Восток'),
                                      start_date=(1948, 1, 1),
                                      end_date=(1948, 12, 31),
                                      is_cinema = False,
                                      by_year = False)

print(testing_query_1)

testing_query_1.to_csv('testing_query_1.csv', index=False, encoding='utf-8')


# Вызываем функцию, которая возвращает POPSTAT для фильма Кубанские казаки, Секретная миссия
# и Смелые людт за 1950 год  с уточнением по кинотеатрам.
testing_query_2 = screenings_per_film(film_name=('Кубанские казаки',
                                                 'Секретная миссия',
                                                 'Смелые люди'),
                                      start_date=(1950, 1, 1),
                                      end_date=(1950, 12, 31),
                                      is_cinema = True,
                                      by_year = False)

print(testing_query_2)

testing_query_2.to_csv('testing_query_2.csv', index=False, encoding='utf-8')



# Вызываем функцию, которая возвращает POPSTAT для фильмов Awaara, Анна на шее
# и La edad del amor за 1954 и 1955 годы с уточнением по кинотеатрам и по годам.
testing_query_3 = screenings_per_film(film_name=('Awaara',
                                                 'Анна на шее',
                                                 'La edad del amor'),
                                      start_date=(1954, 1, 1),
                                      end_date=(1955, 12, 31),
                                      is_cinema=True,
                                      by_year=True)

print(testing_query_3)

testing_query_3.to_csv('testing_query_3.csv', index=False, encoding='utf-8')

# Считаем POPSTAT для всех фильмов за каждый из годов по отдельности

for year in range(1946, 1956):

    POPSTAT = screenings_per_film(film_name=True,
                                  start_date=(year, 1, 1),
                                  end_date=(year, 12, 31),
                                  is_cinema=False,
                                  by_year=False)
    print(POPSTAT)
    POPSTAT.to_csv('POPSTAT' + '_' + str(year) +'.csv', index=False, encoding='utf-8')

# Считаем POPSTAT для всех фильмов в целом по всей БД
POPSTAT_overall = screenings_per_film(film_name=True,
                                      start_date=(1946, 1, 1),
                                      end_date=(1955, 12, 31),
                                      is_cinema=False,
                                      by_year=False)
print(POPSTAT_overall)

POPSTAT_overall.to_csv('POPSTAT_overall.csv', index=False, encoding='utf-8')

