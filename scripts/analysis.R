setwd("/Users/colinthoman/Desktop/racetimeanalytics")
load("data/cleaned/cleaned_race_results.rdata")
load("data/cleaned/cleaned_athletes.rdata")
load("data/cleaned/cleaned_events.rdata")
library(dplyr)
library(tidyr)
library(purrr)

contains_letters <- function(result) {
  grepl("[[:alpha:]]", result)
}
# Function to determine whether a result contains letters (DQ, DNF, etc).

euclidean_dist <- function(v1, v2) {
  if (length(v1) == length(v2)) {
    distance <- sqrt((v1-v2)^2)
    return(sum(distance))
  }
  else {
    print("The operation could not be completed because the vectors have differnet lengths.")
  }
}
# Finds point-by-point Euclidean distance between two vectors.

minimize_distance <- function(v1,v2) {
  if (length(v1) == length(v2)) {
    return(1)
  }
  if (length(v1) > length(v2)) {
    v1 <- v1
    v2 <- v2
    index <- 1
  } else {
    v1 <- v2
    v2 <- v1
    index <- 2
  }
  max_length <- length(v1)
  min_length <- length(v2)
  minimum_distance <- Inf
  for (i in 1:(length(v1) - length(v2) + 1)) {
    dist <- euclidean_dist(v2, v1[i:(i + (min_length - 1))])
    if (dist < minimum_distance) {
      minimum_distance <- dist
      pos <- i
    }
  }
  return(list(index,minimum_distance,pos))
}
# This function returns the position on the larger vector at which the smaller vector can be placed to minimize Euclidean distance.
# It also returns which of the two is the larger.

athlete_trajectory <- function(id1,id2) {
  trajectory <- cleaned_race_results %>%
    filter(athlete_id == id1 & event == id2) %>%
    arrange(race_date) %>%
    select(-athlete_id, -athlete_id, -event, -race_date) %>%
    mutate(result = as.numeric(result))
  return(trajectory[,1])
}
# Takes an athlete ID and event code and returns a vector of the athlete's results for that event.

compare_trajectory <- function(id1,id2) {
  event_subset <- cleaned_race_results %>%
    filter(event==id2) %>%
    group_by(athlete_id) %>%
    filter(n() > 2) %>%
    filter(!contains_letters(result)) %>%
    summarize() %>%
    pull("athlete_id")
  if (!(id1 %in% event_subset)) {
    print("There are not enough results for the given athlete-event combination (3>) to perform the operation.")
  }
  else {
    event_subset <- data.frame(athlete_id = event_subset, index = NA, dist = NA, pos = NA)
    for (i in event_subset) {
      compare_results <- minimize_distance(
        athlete_trajectory(i,id2),
        athlete_trajectory(id1,id2)
      )
      event_subset$index[i] <- compare_results[1]
      event_subset$dist[i] <- compare_results[2]
      event_subset$pos[i] <- compare_results[3]
    event_subset %>%
      arrange(dist) %>%
      head(10)
    }
    return(event_subset)
  }
}

compare_trajectory(7820846,13)
athlete_trajectory(7820846,10)
athlete_trajectory(7820844,10)
minimize_distance(athlete_trajectory(7820846,10),athlete_trajectory(7820844,10))


