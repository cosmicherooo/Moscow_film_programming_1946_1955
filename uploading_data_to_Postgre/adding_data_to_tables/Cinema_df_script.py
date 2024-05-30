from creating_db_template_in_postgres import *
from creating_tables_db import *
from creating_execution_commands import *
from def_filling_tables import *
import numpy as np

cinema_dataframe_to_load = pd.read_csv(
    'pre_processing/pre_processing_cinemas/Cinema.csv',
    encoding='utf8')
cinema_dataframe_to_load = cinema_dataframe_to_load.replace(np.nan, None)

cinema_insertion_command = tables_insertion_commands.get("Cinema")

if __name__ == '__main__':
    filling_tables(hostname='localhost',
                   database='Film_Programming_Moscow_1946_1955',
                   username='postgres',
                   password='85FibanironibI27',
                   port_id=5432,
                   insert_script=cinema_insertion_command,
                   data_frame_to_upload=cinema_dataframe_to_load)

