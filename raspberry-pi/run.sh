#!/bin/bash

# Run script1.py in the background
python monitoring/serial-comm.py &

# Run script3.py in the background
python stream-server/main.py &

# Wait for all background jobs to finish (optional)
wait

# Exit the script
exit 0
