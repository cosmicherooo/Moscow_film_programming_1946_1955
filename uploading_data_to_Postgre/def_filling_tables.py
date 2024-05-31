from creating_db_template_in_postgres import *
from creating_tables_db import *
from creating_execution_commands import *
import pandas as pd
from functools import wraps
import time
import sys


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


sample_empty_df = pd.DataFrame()


@timer
def filling_tables(hostname=hostname,
                   database=database,
                   username=username,
                   password=password,
                   port_id=port_id,
                   insert_script='INSERT INTO Person(person_id, person_name, person_imdb_id) VALUES (?,?,?);',
                   data_frame_to_upload=sample_empty_df,
                   path_to_file='/Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/',
                   name_of_a_table='Cinema'):


    try:
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password,
                                port=port_id)
        cur = conn.cursor()


        unsuccessful_tuples = []

        for i in range(0, data_frame_to_upload.shape[0]):
            try:
                cur.execute(insert_script, tuple(data_frame_to_upload.loc[i]))
            except:
                unsuccessful_tuples.append(tuple(data_frame_to_upload.loc[i]))
                print(f'Your tuple cannot be added into Database: {tuple(data_frame_to_upload.loc[i])}')
                print(error)

            conn.commit()

        cur.close()
        conn.close()

        creating_path = path_to_file + name_of_a_table + '_adding' + '.txt'
        file = open(creating_path, 'w')

        if len(unsuccessful_tuples) == 0:
            num_tuples_added = data_frame_to_upload.shape[0]
            print(f'{num_tuples_added} has been added to your dataframe! All successful tuples have been added!')
            file.write(f'All rows ({num_tuples_added}) were successfully added to your database!' + "\n")
            file.close()
        else:
            num_tuples_added = data_frame_to_upload.shape[0] - len(unsuccessful_tuples)
            print(
                f'Certain rows {num_tuples_added} could not be added to your dataframe! Look them up in output txt-file!\n'
                f'Path to your file is:{creating_path}')
            for item in unsuccessful_tuples:
                file.write('These rows could not be added to your dataframe!\n')
                file.write(item + "\n")
            file.close()

    except:
        print('Connection was unsuccessful!')
        print(error)

    return num_tuples_added, (str((num_tuples_added/data_frame_to_upload.shape[0]) * 100) + ' %')

