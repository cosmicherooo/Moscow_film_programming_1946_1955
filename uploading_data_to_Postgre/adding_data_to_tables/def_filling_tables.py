from creating_db_template_in_postgres import *
from creating_tables_db import *
from creating_execution_commands import *
import pandas as pd

sample_empty_df = pd.DataFrame()

def filling_tables(hostname='localhost',
                   database='Film_Programming_Moscow_1946_1955',
                   username='postgres',
                   password='85FibanironibI27',
                   port_id=5432,
                   insert_script='INSERT INTO Person(person_id, person_name, person_imdb_id) VALUES (?,?,?);',
                   data_frame_to_upload=sample_empty_df):

    try:
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password,
                                port=port_id)
        cur = conn.cursor()

        for i in range(0, data_frame_to_upload.shape[0]):
            try:
                cur.execute(insert_script, tuple(data_frame_to_upload.loc[i]))
                print(f'Your tuple has been successfully added into Database: {tuple(data_frame_to_upload.loc[i])}')
            except:
                print(f'Your tuple cannot be added into Database: {tuple(data_frame_to_upload.loc[i])}')
                print(error)

            conn.commit()

        cur.close()
        conn.close()

    except:
        print('Connection was unsuccessful!')
        print(error)



