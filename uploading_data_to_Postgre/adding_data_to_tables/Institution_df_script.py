from creating_db_template_in_postgres import *
from creating_tables_db import *
from creating_execution_commands import *
from def_filling_tables import *
import numpy as np

institution_dataframe_to_load = pd.read_csv(
    'pre_processing/pre_processing_cinemas/Institution.csv',
    encoding='utf8')
institution_dataframe_to_load = institution_dataframe_to_load.replace(np.nan, None)

institution_insertion_command = tables_insertion_commands.get("Institution")

if __name__ == '__main__':
    filling_tables(hostname='localhost',
                   database='Film_Programming_Moscow_1946_1955',
                   username='postgres',
                   password='***********',
                   port_id=5432,
                   insert_script=institution_insertion_command,
                   data_frame_to_upload=institution_dataframe_to_load)

