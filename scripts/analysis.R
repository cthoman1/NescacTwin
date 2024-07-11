# analysis.R
setwd("/Users/colinthoman/Desktop/racetimeanalytics")
load("data/cleaned/cleaned_race_results.rdata")
load("data/cleaned/cleaned_athletes.rdata")
load("data/cleaned/cleaned_events.rdata")

suppressPackageStartupMessages({
library(dplyr)
library(tidyr)
library(purrr)
})

contains_letters <- function(result) {
  grepl("[[:alpha:]]", result)
}
# Function to determine whether a result contains letters (DQ, DNF, etc).

euclidean_dist <- function(v1, v2, recency_bias) {
  if (length(v1) == length(v2)) {
    n <- length(v1)
    if (recency_bias != 0) {
      weights <- (1:n) ^ -recency_bias
      weights <- weights / sum(weights)
    } else {
      weights <- rep(n^-1, n)
    }
  
    distance <- sqrt((v1-v2)^2)
    weighted_distance <- distance * weights
    return(list(weighted_distance, sum(weighted_distance)/n))
  } else {
    print("The operation could not be completed because the vectors have different lengths.")
  }
}
# Finds point-by-point Euclidean distance between two vectors.
# It also applies a power law distribution based on the recency_bias input.
# It returns a vector of the point-by-point distances and the average.

minimize_distance <- function(v1,v2,recency_bias) {
  if (length(v1) >= length(v2)) {
    index <- 1
    V1 <- v1
    V2 <- v2
  } else {
    V1 <- v2
    V2 <- v1
    index <- 2
  }
  max_length <- length(V1)
  min_length <- length(V2)
  minimum_distance <- Inf
  pos <- 0
  
  for (i in 1:(length(V1) - length(V2) + 1)) {
    dist <- euclidean_dist(V2, V1[i:(i + (min_length - 1))], recency_bias)[[2]]
    if (dist < minimum_distance) {
      minimum_distance <- dist
      pos <- i
      dists <- euclidean_dist(V2, V1[i:(i + (min_length - 1))], recency_bias)[[1]]
    }
  }
  return(list(index,minimum_distance,pos,dists))
}
# This function takes two vectors and returns a three-item list.
# It also applies recency bias on a scale of 0 (none) to extreme (3).
# The recency bias uses a power law distribution.
# The first item in the list is which of the two is larger. 1 for the first (or for equal lengths), 2 for the second.
# The second is the summed point-by-point Euclidean distance between the two divided by the number of races on which they're being compared.
# In effect, the second is the average distance between points in the two vectors.
# The third is the position on which (if applicable) the smaller vector "fits" into the larger one.
# The fourth is the point-by-point weighted distances.

athlete_trajectory <- function(id1,id2) {
  trajectory <- cleaned_race_results %>%
    filter(athlete_id == id1 & event == id2) %>%
    arrange(race_date) %>%
    select(-athlete_id, -athlete_id, -event) %>%
    filter(!contains_letters(result)) %>%
    mutate(result = as.numeric(result))
  return(trajectory)
}
# This an athlete ID and event code and returns a vector of the athlete's results for that event.

compare_trajectory <- function(id1,id2,first_year=2005, last_year=2030, min_events=3,recency_bias=0) {
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
# This function takes a few inputs.
# id1 and id2 correspond to athlete_id and event code respectively.
# first_year and last_year set the time range of athletes surveyed.
# min_events sets a minimum for length of the vectors compared.
# recency_bias determines to what extent recent events are favored on a power-law scale.
# It outputs a table of the ten closest non-self trajectories with index, dist, pos, and dists.

name_to_id <- function(name) {
  match_idx <- match(name, cleaned_athletes$name)
  if (!is.na(match_idx)) {
    return(list(cleaned_athletes$athlete_id[match_idx],cleaned_athletes$school[match_idx]))
  } else {
    return("Athlete with this name not found in the database") 
  }
}
# Takes a name, responds with the athlete ID. Case sensitive.

id_to_name <- function(id) {
  match_idx <- match(id, cleaned_athletes$athlete_id)
  if (!is.na(match_idx)) {
    return(cleaned_athletes$name[match_idx])
  } else {
    return("Athlete with this ID not found in the database") 
  }
}
# Takes an athlete ID, responds with the name.

