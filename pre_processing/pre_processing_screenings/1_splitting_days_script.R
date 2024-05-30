library('dplyr')
library('tidyr')
library("knitr")
library(lubridate)
library(data.table)
library(tidyverse)
install.packages('berryFunctions')
library ("berryFunctions")
library(tibble)
install.packages('janitor')
library('janitor')

#Выгружаем датасет

data_cinema <- read.csv('Dataset_Moscow_1946-1955_UPD_Film Programming, 1946–1955.csv')
data_cinema <- as_tibble(data_cinema)


# Превращаем даты первого показа в данные типа "date" (вид даты: год-месяц-день)

data_cinema <- data_cinema |>
  mutate(first.day.of.screening = dmy(first.day.of.screening))

data_cinema <- data_cinema |> 
  filter(row_number() <= n()-1)

data_cinema = subset(data_cinema, select = c("cinema..ID.", "first.day.of.screening", 
                                             "screening.days",
                                             "title..source.",
                                             "title..transliteration.",
                                             "title..original.",
                                             "IMDB.id",
                                             "country.of.origin",
                                             "source"))


# Делим датасет на все даты показа определенного фильма. 
# Соответственно значение во всех ячейках First.day.of.screening - 1.
# Также добавляем, какой день недели в отдульную колонку

data_cinema <- data_cinema |>
  mutate(rn = row_number()) |>
  rowwise() |>
  slice(rep(1, screening.days)) |>
  group_by(rn) |>
  mutate(first.day.of.screening = seq(first.day.of.screening[1], by = "day", length.out = n())) |>
  ungroup() |>
  mutate(screening.days = 1,
         Day_of_the_week = wday(first.day.of.screening))



write.csv(data_cinema,"pre_processing/pre_processing_screenings/screenings_split.csv", row.names = FALSE)
