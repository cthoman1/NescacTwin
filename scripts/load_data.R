library(DBI)
library(RSQLite)

if (!dir.exists("data/processed")) {
  dir.create("data/processed", recursive = TRUE)
}

db_path <- "data/raw/nescactf.db"
conn <- dbConnect(RSQLite::SQLite(), db_path)

tables <- dbListTables(conn)
print(tables)

race_results <- dbReadTable(conn, "race_results")
athletes <- dbReadTable(conn, "athletes")
events <- dbReadTable(conn, "events")

dbDisconnect(conn)

save(race_results, file = "data/processed/race_results.RData")
save(athletes, file = "data/processed/athletes.RData")
save(events, file = "data/processed/events.RData")


