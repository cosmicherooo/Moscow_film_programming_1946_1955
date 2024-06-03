from screenings_per_cinema import *

# На основе функции screenings_per_cinema строится функция, которая собирает
# и ранжирует по количеству экранодней, которые провели фильмы в каждом из кинотеатров
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
def screenings_each_cinema(year = 1946):

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
        cur.execute('''SELECT cinema_name_source
                       FROM cinema;''')

        list_of_cinemas = [item for item in cur.fetchall()]
        list_of_cinemas = sum(list_of_cinemas, ())

    except:
        sys.exit('Query to get all cinemas was unsuccessful')

    try:
        output_dataframe = screenings_per_cinema(year = year,
                                                 cinema_name = list_of_cinemas)
    except:
        sys.exit('screenings_per_cinema function could not be started!')

    return output_dataframe[0]

if __name__ == '__main__':
    dataframe = screenings_each_cinema()
    print(dataframe)
