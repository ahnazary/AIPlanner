FROM python:3.10

# install ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# confirm installation
RUN ollama --version