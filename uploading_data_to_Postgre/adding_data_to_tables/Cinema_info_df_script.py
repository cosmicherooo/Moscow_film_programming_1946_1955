from creating_db_template_in_postgres import *
from creating_tables_db import *
from creating_execution_commands import *
from def_filling_tables import *
import numpy as np
from psycopg2.extensions import register_adapter, AsIs

cinema_info_dataframe_to_load = pd.read_csv(
    '/Users/karnaukhovivan/Desktop/ВКР_!!!текст_текст/что будет на гите/предобработка/предобработка_кинотеатры/Cinema_info.csv',
    encoding='utf8')
cinema_info_dataframe_to_load = cinema_info_dataframe_to_load.replace(np.nan, None)
cinema_info_dataframe_to_load["reconstruction"] = cinema_info_dataframe_to_load["reconstruction"].values.astype(str)
register_adapter(np.int64, AsIs)


cinema_info_insertion_command = tables_insertion_commands.get("Cinema_info")

if __name__ == '__main__':
    filling_tables(hostname='localhost',
                   database='Film_Programming_Moscow_1946_1955',
                   username='postgres',
                   password='85FibanironibI27',
                   port_id=5432,
                   insert_script=cinema_info_insertion_command,
                   data_frame_to_upload=cinema_info_dataframe_to_load)

