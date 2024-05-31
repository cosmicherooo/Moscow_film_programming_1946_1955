from creating_db_template_in_postgres import *
from creating_tables_db import *
from creating_execution_commands import *
from def_filling_tables import *
from delete_function import *
import numpy as np
import os
from subprocess import PIPE, run
import ast
import re

def testing_uploadind_and_deleting_data(path_to_uploading_script = '/Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/Cinema_df_script.py',
                                        path_to_deleting_script = '/Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/Cinema_delete_script.py',
                                        name_of_table = 'Cinema',
                                        path_to_upload_csv = '/Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/'):

    test_cinema_df_uploading = []
    test_cinema_df_deleting = []
    execution_num = 1
    for i in range(0, 10):
        command = ['python3', path_to_uploading_script]
        result_1 = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        string_1 = result_1.stdout
        x_1 = re.match(r"[^[]*(\[[^]]*\])", string_1).groups()[0]
        x_1 = ast.literal_eval(x_1)
        x_1.insert(0, execution_num)
        test_cinema_df_uploading.append(x_1)

        command_2 = ['python3', path_to_deleting_script]
        result_2 = run(command_2, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        string_2 = result_2.stdout
        x_2 = re.match(r"[^[]*(\[[^]]*\])", string_2).groups()[0]
        x_2 = ast.literal_eval(x_2)
        x_2.insert(0, execution_num)
        test_cinema_df_deleting.append(x_2)

        execution_num += 1

        print(f'Test №{execution_num} has been completed!')

        test_cinema_df_uploading_df = pd.DataFrame(test_cinema_df_uploading, columns=['execution_num',
                                                                                      'rows_added',
                                                                                      'rows_added_percantage',
                                                                                      'time_execution'])

        test_cinema_df_deleting_df = pd.DataFrame(test_cinema_df_deleting, columns=['execution_num',
                                                                                    'rows_undeleted',
                                                                                    'rows_undeleted_percantage',
                                                                                    'time_execution'])

        path_for_uploading_stats = path_to_upload_csv + name_of_table + '_uploading_stats.csv'
        path_for_deleting_stats = path_to_upload_csv + name_of_table + '_deleting_stats.csv'

        test_cinema_df_uploading_df.to_csv(path_for_uploading_stats,
                                           sep=',',
                                           index=False,
                                           encoding='utf-8')

        test_cinema_df_deleting_df.to_csv(path_for_deleting_stats,
                                          sep=',',
                                          index=False,
                                          encoding='utf-8')

        print('Uploading and deleting were tested!')


if __name__ == '__main__':
    testing_uploadind_and_deleting_data()

