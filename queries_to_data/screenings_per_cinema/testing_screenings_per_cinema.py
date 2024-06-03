from screenings_per_cinema import *


# Вызываем функцию, которая возвращает
# колчество экранодней для кинотеатра Метрополь в 1950 году.


testing_query_1 = screenings_per_cinema(cinema_name='Метрополь',
                                        year=1950)

print(testing_query_1[0])
print(testing_query_1[1])

testing_query_1[0].to_csv('testing_query_1.csv', index=False, encoding='utf-8')


# Вызываем функцию, которая возвращает
# колчество экранодней для кинотеатра Экран в 1954 году.


testing_query_2 = screenings_per_cinema(cinema_name='Экран жизни',
                                        year=1950)

print(testing_query_2[0])
print(testing_query_2[1])

testing_query_2[0].to_csv('testing_query_2.csv', index=False, encoding='utf-8')
