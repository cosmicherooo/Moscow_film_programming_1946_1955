from screenings_per_person import *
# На основе функции screenings_per_person строится функция, которая собирает
# и ранжирует по количеству экранодней, которые провели фильмы всех режиссеров
# за определенный год.

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        wrapper.total_time += duration
        print(f"Execution time: {duration}")
        return result

    wrapper.total_time = 0
    return wrapper

@timer
def screenings_each_person(role = 'Director',
                           year = 1946):

    try:
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password,
                                port=port_id)
        cur = conn.cursor()

    except:
        sys.exit('Unsuccessful connection!')

    try:
        cur.execute('''SELECT person_name
                       FROM person;''')
        list_of_persons = [item for item in cur.fetchall()]
        list_of_persons = sum(list_of_persons, ())

    except:
        sys.exit('Query to get all persons was unsuccessful')

    try:
        output_dataframe = screenings_per_person(role = role,
                                                 year = year,
                                                 person_name = list_of_persons)
    except:
        sys.exit('screenings_per_person function could not be started!')

    return output_dataframe[0]

if __name__ == '__main__':
    dataframe = screenings_each_person()[0]
    print(dataframe)