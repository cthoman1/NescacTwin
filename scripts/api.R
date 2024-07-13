library(plumber)
setwd("/Users/colinthoman/Desktop/racetimeanalytics")
pr("scripts/plumber.R") %>% pr_run(port = 8000)
print("API is running on port 8000.")
