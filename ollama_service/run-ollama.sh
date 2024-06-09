#!/usr/bin/env bash

ollama serve &
ollama list
ollama pull llama3
ollama create aiplanner -f ./Modelfile.txt