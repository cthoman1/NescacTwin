setwd("/Users/colinthoman/Desktop/racetimeanalytics")
load("data/cleaned/cleaned_race_results.rdata")
load("data/cleaned/cleaned_events.rdata")
library(dplyr)
library(tidyr)

if (exists('filtered_df')) {
  rm(filtered_df)
}

if (exists('athlete_event_dfs')) {
rm(athlete_event_dfs)
}

if (exists('filtered_df')) {
  print("Filtered database already exists.")
} else {
filtered_df <- cleaned_race_results %>%
  group_by(athlete_id, event) %>%
  filter(n() >= 3) %>%
  ungroup()
}


if (exists('athlete_event_dfs')) {
  print("Filtered database already exists.")
} else {
athlete_event_dfs <- filtered_df %>%
  group_by(athlete_id, event) %>%
  group_split()
}

names(athlete_event_dfs) <- filtered_df %>%
  group_by(athlete_id, event) %>%
  group_keys() %>%
  unite("athlete_event", athlete_id, event, sep = "_") %>%
  pull(athlete_event)

athlete_event_dfs <- lapply(athlete_event_dfs, function(df) {
  df %>% select(-athlete_id, -event)
})
