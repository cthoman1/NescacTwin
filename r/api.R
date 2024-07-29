library(plumber)
setwd("/Users/colinthoman/Desktop/racetimeanalytics")
pr("r/plumber.R") %>% pr_run(port = 8000)
print("API is running on port 8000.")
