from screenings_per_person import *


# Вызываем функцию, которая возвращает
# колчество экранодней для фильмов, в которых режиссером был Юлий Райзман в 1946 году.


testing_query_1 = screenings_per_person(role = 'Director',
                                        year = 1946,
                                        person_name = 'Yuli Raizman')

print(testing_query_1[0])
print(testing_query_1[1])

testing_query_1[0].to_csv('testing_query_1.csv', index=False, encoding='utf-8')


# Вызываем функцию, которая возвращает
# колчество экранодней для фильмов, в которых актером был Алексей Дикий в 1949 году.


testing_query_2 = screenings_per_person(role = 'Actor',
                                        year = 1949,
                                        person_name = 'Aleksei Dikij')

print(testing_query_2[0])
print(testing_query_2[1])

testing_query_2[0].to_csv('testing_query_2.csv', index=False, encoding='utf-8')


# Вызываем функцию, которая возвращает
# колчество экранодней для фильмов, в которых сценаристом был Петр Павленко в 1950 году.


testing_query_3 = screenings_per_person(role = 'Writer',
                                        year = 1950,
                                        person_name = 'Pyotr Pavlenko')

print(testing_query_3[0])
print(testing_query_3[1])

testing_query_3[0].to_csv('testing_query_3.csv', index=False, encoding='utf-8')
