from creating_db_template_in_postgres import *
from creating_tables_db import *
from creating_execution_commands import *
from def_filling_tables import *
import numpy as np

periodic_ref_dataframe_to_load = pd.read_csv(
    'pre_processing/pre_rpocessing_periodics/periodic_ref.csv',
    encoding='utf8')
periodic_ref_dataframe_to_load = periodic_ref_dataframe_to_load.replace(np.nan, None)
periodic_ref_dataframe_to_load["is_programme"] = periodic_ref_dataframe_to_load["is_programme"].values.astype(str)

periodic_ref_insertion_command = tables_insertion_commands.get("periodic_ref")

if __name__ == '__main__':
    filling_tables(hostname='localhost',
                   database='Film_Programming_Moscow_1946_1955',
                   username='postgres',
                   password=str(input()),
                   port_id=5432,
                   insert_script=periodic_ref_insertion_command,
                   data_frame_to_upload=periodic_ref_dataframe_to_load)

