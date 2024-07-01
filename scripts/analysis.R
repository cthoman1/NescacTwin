setwd("/Users/colinthoman/Desktop/racetimeanalytics")
load("data/cleaned/cleaned_race_results.rdata")
load("data/cleaned/cleaned_athletes.rdata")
load("data/cleaned/cleaned_events.rdata")
library(dplyr)
library(tidyr)
library(purrr)
filtered_df <- cleaned_race_results %>%
  group_by(athlete_id, event) %>%
  filter(n() >= 3) %>%
  ungroup()
# Selects only those results for which the athlete has done it 3 or more times.
# Any less and the trajectories would not be very meaningful.

contains_letters <- function(result) {
  grepl("[[:alpha:]]", result)
}
#Function to determine whether a result contains letters (DQ, DNF, etc).

trajectory_tables <- filtered_df %>%
  group_by(athlete_id, event) %>%
  arrange(race_date) %>%
  summarise(
    results = list(result),
    race_dates = list(format(race_date, "%m/%d/%y")),  
    .groups = 'drop') 
# Uses the filtered database to create chronological result lists for each athlete-event pairing.

filtered_trajectory_tables <- trajectory_tables %>%
  rowwise() %>%
  mutate(
    results = list(as.numeric(results[!contains_letters(results)])),
    race_dates = list(race_dates[!contains_letters(results)])
  ) %>%
  ungroup() %>%
  filter(map_int(results, length) > 2) 
# Returns the trajectory tables but including only numeric results.


write.csv(events,file="events.csv")