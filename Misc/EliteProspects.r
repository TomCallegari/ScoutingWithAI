#
# EliteProspects

setwd("D://Analytics/EliteProspects/")

# Load Libraries
library(tidyverse)
library(Hmisc)
library(DataExplorer)
library(viridis)
library(gridExtra)

raw_yearly <- read.csv("yearly_player_stats_test.csv",
                  header = T,
                  stringsAsFactors = F)

yearly <- raw_yearly %>%
  mutate(league = as.factor(league))

raw_meta <- read.csv("meta_stats_test.csv",
                      header = T,
                      stringsAsFactors = F)

meta <- raw_meta %>%
  mutate(position = as.factor(position),
         date_of_birth = as.Date(date_of_birth),
         shoots = as.factor(shoots))

scaler0_1 <- function(x) (x-min(x))/(max(x)-min(x))
scaler0_100 <- function(x) (x-min(x))/(max(x)-min(x)) * 100

str(raw_yearly)
str(raw_meta)

raw_meta %>%
  ggplot() +
  geom_histogram(aes(height),
                 binwidth=1)
raw_meta %>%
  ggplot() +
  geom_histogram(aes(weight),
                 binwidth=1)

yearly %>%
  ggplot() +
  geom_bar(aes(league))

meta %>%
  ggplot() +
  geom_bar(aes(position))

yearly %>%
  ggplot() +
  geom_histogram(aes(plus_minus),
                 binwidth=1)

meta %>%
  ggplot() +
  geom_histogram(aes(date_of_birth))

yearly %>%
  ggplot() +
  geom_bar(aes(season))

meta %>%
  ggplot() +
  geom_bar(aes(shoots))
