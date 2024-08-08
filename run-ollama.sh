#!/usr/bin/env bash

ollama serve &
ollama list
# ollama pull llama3
# ollama pull moondream
ollama create aiplanner -f ./Modelfile.txt