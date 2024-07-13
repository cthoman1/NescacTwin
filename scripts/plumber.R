#plumber.R

setwd("/Users/colinthoman/Desktop/racetimeanalytics")
library(plumber)
source("scripts/analysis.R")

#* @apiTitle Race Time Analytics API
#* @apiDescription API for interacting with race time analytics

#* athletes static list
#* @get /athletes
get_athletes <- function() {
  athletes_years_df <- cleaned_race_results %>%
    group_by(athlete_id, event) %>%
    filter(n() >= 3) %>%
    ungroup() %>%
    group_by(athlete_id) %>%
    summarize(
      first_year = min(format(race_date, format="%y")),
      last_year = max(format(race_date, format="%y"))
    ) %>%
    mutate(
      years_active = if_else(first_year == last_year,
                             paste0("'", first_year),
                             paste0("'", first_year, "-", last_year)
      )
    ) %>%
    select(-first_year, -last_year)
  athletes <- cleaned_athletes %>%
    left_join(athletes_years_df, by = "athlete_id") %>%
    filter(!is.na(years_active))
  return(athletes)
}

#* relevant events
#* @param id athlete_id
#* @get /relevant_events
relevant_events <- function(id) {
  events_subset <- cleaned_race_results %>%
    filter(athlete_id == id) %>%
    group_by(athlete_id) %>%
    filter(n()>=3) %>%
    pull(event) %>%
    unique()
  relevant_events <- sapply(events_subset, id2_to_event_name)
  class(relevant_events)
  return(relevant_events)
}

#* athlete trajectory
#* @param id1 athlete ID
#* @param id2 event code
#* @get /athlete_trajectory
athlete_trajectory <- function(id1,id2) {
  trajectory <- cleaned_race_results %>%
    filter(athlete_id == id1 & event == id2) %>%
    arrange(race_date) %>%
    select(-athlete_id, -athlete_id, -event) %>%
    filter(!contains_letters(result)) %>%
    mutate(result = as.numeric(result))
  return(trajectory)
}


#* Compare trajectory
#* @param id1 athlete ID
#* @param event_name event name
#* @param first_year start year
#* @param last_year end year
#* @param min_events minimum events
#* @param recency_bias a recency bias scalar
#* @get /compare_trajectory
compare_trajectory <- function(id1,id2,first_year=2005, last_year=2030, min_events=3,recency_bias=0) {
  id2 <- event_name_to_id2(event_name)
  event_subset <- cleaned_race_results %>%
    filter(event==id2) %>%
    group_by(athlete_id) %>%
    filter(!contains_letters(result)) %>%
    filter(n() >= min_events) %>%
    mutate(year = as.integer(substr(race_date, 1, 4))) %>%
    select(-race_date) %>%
    filter(year >= first_year & year <= last_year) %>%
    summarize() %>%
    pull("athlete_id")
  # This creates 'event_subset', a list of athlete_ids in the set with 3+ non-text results for the event.
  if (!(id1 %in% event_subset)) {
    print("The athlete ID given does not fit into the parameters given.")
  }
  else {
    event_subset <- data.frame(athlete_id = event_subset, index = NA, dist = NA, pos = NA, dists = NA)
    for (i in seq_along(event_subset$athlete_id)) {
      compare_results <- minimize_distance(
        athlete_trajectory(event_subset$athlete_id[i],id2)[,2],
        athlete_trajectory(id1,id2)[,2],
        recency_bias
      )
      event_subset$index[i] <- as.integer(compare_results[1])
      event_subset$dist[i] <- as.numeric(compare_results[2])
      event_subset$pos[i] <- as.integer(compare_results[3])
      event_subset$dists[i] <- as.vector(compare_results[4])
      # This creates a three-item list for each other athlete in the data set.
      # The three items are the three outputs from the distance minimization function.
      closest_trajectories <- event_subset %>%
        arrange(dist) %>%
        slice(2:11)
    }
    return(closest_trajectories)
    # This appends the three outputs from distance minimization to the IDs in 'event_subset'.
    # It then sorts them based on distance and takes the top ten (non-self) results.
  }
}

#* Name to ID
#* @param name Name
#* @get /name_to_id
name_to_id <- function(name) {
  match_idx <- match(name, cleaned_athletes$name)
  if (!is.na(match_idx)) {
    return(as.integer(cleaned_athletes$athlete_id[match_idx]))
  } else {
    return("Athlete with this name not found in the database") 
  }
}

#* ID to name
#* @param id ID
#* @get /id_to_name
id_to_name <- function(id) {
  match_idx <- match(id, cleaned_athletes$athlete_id)
  if (!is.na(match_idx)) {
    return(cleaned_athletes$name[match_idx])
  } else {
    return("Athlete with this ID not found in the database") 
  }
}

#* Event name to ID2
#* @param event_name name
#* @get /event_name_to_id
event_name_to_id2 <- function(event_name) {
  match_idx <- match(name, events$event_name)
  if (!is.na(match_idx)) {
    return(events$event_code)
      } else {
    return("Event with this name not found in the database") 
  }
}

#* ID2 to event name
#* @param id2 ID
#* @get /event_id_to_name
id2_to_event_name <- function(id2) {
  match_idx <- match(id2, events$event_code)
  if (!is.na(match_idx)) {
    return(events$event_name[match_idx])
  } else {
    return("Event with this ID not found in the database") 
  }
}




