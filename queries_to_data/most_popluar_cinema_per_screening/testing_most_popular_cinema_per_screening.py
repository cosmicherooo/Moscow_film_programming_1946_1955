from most_popluar_cinema_per_screening import *


# Вызываем функцию, которая возвращает информацию о количестве
# экранодней для каждого кинотеатра в 1950 году.
testing_query_1 = screenings_each_cinema(year = 1950)

print(testing_query_1)

testing_query_1.to_csv('testing_query_1.csv', index=False, encoding='utf-8')

# Вызываем функцию, которая возвращает информацию о количестве
# экранодней для каждого кинотеатра в 1946 году.
testing_query_2 = screenings_each_cinema(year = 1955)

print(testing_query_2)

testing_query_2.to_csv('testing_query_2.csv', index=False, encoding='utf-8')

# Вызываем функцию, которая возвращает информацию о количестве
# экранодней для каждого кинотеатра в 1955 году.
testing_query_3 = screenings_each_cinema(year = 1945)

print(testing_query_3)

testing_query_3.to_csv('testing_query_3.csv', index=False, encoding='utf-8')