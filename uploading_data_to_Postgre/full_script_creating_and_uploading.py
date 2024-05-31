import os

if __name__ == "__main__":
    command_to_create_template = 'python3 /Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/creating_db_template_in_postgres.py'
    os.system(command_to_create_template)

    print("Database has been successfully created!")

    command_to_create_tables = 'python3 /Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/creating_tables_db.py'
    os.system(command_to_create_tables)

    print("Tables has been successfully created!")

    command_to_create_execution_commands = 'python3 /Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/creating_execution_commands.py'
    os.system(command_to_create_execution_commands)

    print("Execution commands have been successfully compilated!")

    command_to_upload_cinema = 'python3 /Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/Cinema_df_script.py'
    os.system(command_to_upload_cinema)

    print("Cinema dataframe has been loaded with data successfully!")

    command_to_upload_cinema_info = 'python3 /Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/Cinema_info_df_script.py'
    os.system(command_to_upload_cinema_info)

    print("Cinema_info dataframe has been loaded with data successfully!")

    command_to_upload_country = 'python3 /Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/country_df_script.py'
    os.system(command_to_upload_country)

    print("Country dataframe has been loaded with data successfully!")

    command_to_upload_country_to_film = 'python3 /Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/country_to_film_df_script.py'
    os.system(command_to_upload_country_to_film)

    print("Country_to_film dataframe has been loaded with data successfully!")

    command_to_upload_film = 'python3 /Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/Film_df_script.py'
    os.system(command_to_upload_film)

    print("Film dataframe has been loaded with data successfully!")

    command_to_upload_institution = 'python3 /Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/Institution_df_script.py'
    os.system(command_to_upload_institution)

    print("Institution dataframe has been loaded with data successfully!")

    command_to_upload_periodic = 'python3 /Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/Periodic_df_script.py'
    os.system(command_to_upload_periodic)

    print("Periodic dataframe has been loaded with data successfully!")

    command_to_upload_periodic_ref = 'python3 /Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/periodic_ref_df_script.py'
    os.system(command_to_upload_periodic_ref)

    print("Periodic_ref dataframe has been loaded with data successfully!")

    command_to_upload_person = 'python3 /Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/Person_df_script.py'
    os.system(command_to_upload_person)

    print("Person dataframe has been loaded with data successfully!")

    command_to_upload_person_to_film = 'python3 /Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/Person_to_film_db_script.py'
    os.system(command_to_upload_person_to_film)

    print("Person_to_film dataframe has been loaded with data successfully!")

    command_to_upload_screening = 'python3 /Users/karnaukhovivan/PycharmProjects/pythonProject5/venv/Screening_df_script.py'
    os.system(command_to_upload_screening)

    print("Screening dataframe has been loaded with data successfully!")

