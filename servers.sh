#!/bin/bash

# Setting the working directory to the project directory
cd /Users/colinthoman/Desktop/racetimeanalytics

#Start plumber API
Rscript r/api.R &

#Go back to project directory
cd web

#Start node.js server
npx nodemon server.js 

# Wait for background processes to complete.
wait
