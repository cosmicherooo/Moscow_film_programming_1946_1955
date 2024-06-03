from creating_db_template_in_postgres import *
from creating_tables_db import *
from creating_execution_commands import *
from def_filling_tables import *
import numpy as np

screening_dataframe_to_load = pd.read_csv(
    '/Users/karnaukhovivan/Desktop/ВКР_!!!текст_текст/что будет на гите/предобработка/предобработка_кинопоказ/Screening.csv',
    encoding='utf8')

screening_dataframe_to_load = screening_dataframe_to_load.replace(np.nan, None)
screening_dataframe_to_load["day_of_screening"] = pd.to_datetime(screening_dataframe_to_load["day_of_screening"],
                                                                 format='%Y-%m-%d').dt.date
screening_dataframe_to_load["is_programme"] = screening_dataframe_to_load["is_programme"].values.astype(str)

screening_dataframe_to_load_insertion_command = tables_insertion_commands.get("Screening")


if __name__ == '__main__':
    statistics = filling_tables(hostname=hostname,
                                database=database,
                                username=username,
                                password=password,
                                port_id=port_id,
                                insert_script=screening_dataframe_to_load_insertion_command,
                                data_frame_to_upload=screening_dataframe_to_load)

    statistics = list(statistics)
    statistics.append(filling_tables.total_time)
    print(statistics)


