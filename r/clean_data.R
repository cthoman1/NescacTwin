setwd("/Users/colinthoman/Desktop/racetimeanalytics")
load("data/processed/race_results.rdata")
load("data/processed/events.rdata")
load("data/processed/athletes.rdata")
library(dplyr)

cleaned_race_results <- race_results %>%
  select(-id)
# Removes the primary key "id" column, making it easier to spot duplicates.
# Duplicates may arise from running the Python script for a school multiple times.

contains_number <- function(x) {
  grepl("[0-9]", x)
}
remove_letters <- function(text) {
  cleaned_text <- gsub("[[:alpha:]]", "", text)
  return(cleaned_text)
}
# Remove all letters from the input text using regex
for (i in seq_along(race_results$result)) {
  if (contains_number(race_results$result[i])) {
    cleaned_race_results$result[i] <- remove_letters(cleaned_race_results$result[i])
  }
}
# Removes letters that found their way into numeric results (happens on sprints). 

extract_first_four_letters <- function(x) {
  if (grepl("^[[:alpha:]]", x)) {
    return(substr(x, 1, 4))
  } else {
    return(x)  
  }
}
for (i in seq_along(cleaned_race_results$result)) {
  cleaned_race_results$result[i] <- extract_first_four_letters(cleaned_race_results$result[i])
}
#This will fix the odd formatting for certain "Foul" and "NM" results.
time_to_seconds <- function(time_str) {
  # Check if the input time string contains a colon
  if (grepl(":", time_str)) {
      time_parts <- as.numeric(strsplit(time_str, ":")[[1]])
      if (length(time_parts) == 2) {
        return(time_parts[1] * 60 + time_parts[2])
      }
  }
  return(time_str)
}
for (i in seq_along(cleaned_race_results$result)) {
  cleaned_race_results$result[i] <- trimws(cleaned_race_results$result[i])
  cleaned_race_results$result[i] <- time_to_seconds(cleaned_race_results$result[i])
}
# Changes all times to seconds only. 

remove_trailing_dots <- function(vec) {
  cleaned_vec <- sub("\\.$", "", vec)
  return(cleaned_vec)
}
cleaned_race_results$result <- remove_trailing_dots(cleaned_race_results$result)
# Removes trailing dots

cleaned_race_results$race_date <- as.Date(cleaned_race_results$race_date, format = "%m/%d/%y")
cleaned_race_results$event <- as.integer(cleaned_race_results$event)
# Assigns the proper data classes to race results, event codes, and dates.

cleaned_athletes <- athletes
cleaned_athletes$name<- gsub("  ", " ", cleaned_athletes$name)
#Fixes double spaces in athlete names

cleaned_race_results <- cleaned_race_results %>%
  distinct()
# Removes duplicates from the results table.

cleaned_events <- events
#Doesn't seem like there is any cleaning to do on the events file. 

save(cleaned_race_results, file = "data/cleaned/cleaned_race_results.rdata")
save(cleaned_athletes, file = "data/cleaned/cleaned_athletes.rdata")
save(events, file = "data/cleaned/cleaned_events.rdata")



