#!/bin/bash

# # Start ollama in a new tmux session
# tmux new-session -d -s ollama serve

# #ollama run aiplanner

# # Output a message
# # echo "ollama is running in the terminal | start.sh"

# # Start the Python application
# python3 src/app.py

# ollama serve &
# ollama create aiplanner -f ./Modelfile.txt
# ollama list

ollama serve & python3 src/app.py
