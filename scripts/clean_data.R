setwd("/Users/colinthoman/Desktop/racetimeanalytics")
load("data/processed/race_results.rdata")
load("data/processed/events.rdata")

contains_only_letters <- function(x) {
  grepl("^[[:alpha:]]+$", x)  # Matches strings with only letters
}
race_results <- race_results[!sapply(race_results$result, contains_only_letters), ]
race_results <- race_results[!is.na(race_results$result) & trimws(race_results$result) != "", ]
# Removes DNFs, DQs, DNS's, NMs (Fouls), and NHs.

remove_letters <- function(text) {
  # Remove all letters from the input text using regex
  cleaned_text <- gsub("[[:alpha:]]", "", text)
  return(cleaned_text)
}
race_results$result <- remove_letters(race_results$result)
# Removes letters that found their way into results. 

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
for (i in seq_along(race_results$result)) {
  race_results$result[i] <- trimws(race_results$result[i])
  race_results$result[i] <- time_to_seconds(race_results$result[i])
}
# Changes all times to seconds only. 

remove_trailing_dots <- function(vec) {
  cleaned_vec <- sub("\\.$", "", vec)
  return(cleaned_vec)
}
race_results$result <- remove_trailing_dots(race_results$result)
# Removes trailing dots

race_results$result <- as.numeric(race_results$result)
race_results$race_date <- as.Date(race_results$race_date, format = "%m/%d/%y")


