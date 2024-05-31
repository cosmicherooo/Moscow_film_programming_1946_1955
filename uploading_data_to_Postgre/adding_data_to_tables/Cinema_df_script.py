from creating_db_template_in_postgres import *
from creating_tables_db import *
from creating_execution_commands import *
from def_filling_tables import *
import numpy as np

cinema_dataframe_to_load = pd.read_csv(
    '/Users/karnaukhovivan/Desktop/ВКР_!!!текст_текст/что будет на гите/предобработка/предобработка_кинотеатры/Cinema.csv',
    encoding='utf8')
cinema_dataframe_to_load = cinema_dataframe_to_load.replace(np.nan, None)

cinema_insertion_command = tables_insertion_commands.get("Cinema")

if __name__ == '__main__':
    statistics = filling_tables(hostname=hostname,
                                database=database,
                                username=username,
                                password=password,
                                port_id=port_id,
                                insert_script=cinema_insertion_command,
                                data_frame_to_upload=cinema_dataframe_to_load)

    statistics = list(statistics)
    statistics.append(filling_tables.total_time)
    print(statistics)