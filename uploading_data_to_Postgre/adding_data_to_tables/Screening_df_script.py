from creating_db_template_in_postgres import *
from creating_tables_db import *
from creating_execution_commands import *
from def_filling_tables import *
import numpy as np

screening_dataframe_to_load = pd.read_csv(
    'pre_processing/pre_processing_screenings/Screening.csv',
    encoding='utf8')
screening_dataframe_to_load = screening_dataframe_to_load.replace(np.nan, None)
screening_dataframe_to_load["day_of_screening"] = pd.to_datetime(screening_dataframe_to_load["day_of_screening"],
                                                                 format='%Y-%m-%d').dt.date
screening_dataframe_to_load["is_programme"] = screening_dataframe_to_load["is_programme"].values.astype(str)


screening_dataframe_to_load_insertion_command = tables_insertion_commands.get("Screening")


if __name__ == '__main__':
    filling_tables(hostname='localhost',
                   database='Film_Programming_Moscow_1946_1955',
                   username='postgres',
                   password='85FibanironibI27',
                   port_id=5432,
                   insert_script=screening_dataframe_to_load_insertion_command,
                   data_frame_to_upload=screening_dataframe_to_load)



