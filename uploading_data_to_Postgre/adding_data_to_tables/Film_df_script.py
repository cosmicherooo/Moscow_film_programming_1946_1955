from creating_db_template_in_postgres import *
from creating_tables_db import *
from creating_execution_commands import *
from def_filling_tables import *
import numpy as np


film_dataframe_to_load = pd.read_csv('/Users/karnaukhovivan/Desktop/ВКР_!!!текст_текст/что будет на гите/предобработка/предобработка_фильмы/Film.csv',
                                       encoding='utf8')
film_dataframe_to_load = film_dataframe_to_load.replace(np.nan, None)


person_insertion_command = tables_insertion_commands.get("Film")


if __name__ == '__main__': 
    statistics = filling_tables(hostname=hostname,
                                database=database,
                                username=username,
                                password=password,
                                port_id=port_id,
                                insert_script=person_insertion_command,
                                data_frame_to_upload=film_dataframe_to_load)

    statistics = list(statistics)
    statistics.append(filling_tables.total_time)
    print(statistics)
