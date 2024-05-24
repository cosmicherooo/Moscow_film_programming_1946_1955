Despite an immense ampunt of work my collegues and me put into data collection, cleaning and oraganazing, we are still
yet to enrich it with extra infromation, namely: 
- directors' names
- writers' names
- actors' names
- films' duration.

Code that is published here is to to solve this problem. 

После запуска скрипта parser_script было получено несколько датасетов: 
- actors_df.csv (в Google Sheets добавлена колонка role, где для всех указана роль в фильме - actor, для дальнейшей предобработки - создание соединительной таблицы)
- country_df.csv (не использован, так как в изначальном датасете уже присутствовали указания на страны производства)
- directors_df.csv (в Google Sheets добавлена колонка role, где для всех указана роль в фильме - director, для дальнейшей предобработки - создание соединительной таблицы)
- duration_df.csv
- writers_df.csv (в Google Sheets добавлена колонка role, где для всех указана роль в фильме - writer, для дальнейшей предобработки - создание соединительной таблицы)
