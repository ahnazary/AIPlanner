#!/usr/bin/env bash

ollama serve &
ollama list
ollama create aiplanner -f ./Modelfile.txt