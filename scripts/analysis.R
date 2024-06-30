setwd("/Users/colinthoman/Desktop/racetimeanalytics")
load("data/cleaned/cleaned_race_results.rdata")
load("data/cleaned/cleaned_events.rdata")
library(dplyr)
library(tidyr)
library(purrr)

filtered_df <- cleaned_race_results %>%
  group_by(athlete_id, event) %>%
  filter(n() >= 3) %>%
  ungroup()

athlete_event_dfs <- filtered_df %>%
  group_by(athlete_id, event) %>%
  summarise(
    race_results = list(result),
    race_dates = list(format(race_date, "%m/%d/%y")),  # Ensure race_dates are stored as Date objects
    .groups = 'drop'
) 
  


