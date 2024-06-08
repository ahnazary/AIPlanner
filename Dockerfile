FROM python:3.10

WORKDIR /app

# Install ollama
RUN apt-get update && apt-get install -y coreutils
RUN curl -fsSL https://ollama.com/install.sh | sh

# Confirm installation
RUN ollama --version

# Create a new model
COPY Modelfile.txt Modelfile.txt
COPY run-ollama.sh run-ollama.sh

RUN chmod +x run-ollama.sh && ./run-ollama.sh

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ai_planner/ ai_planner/

EXPOSE 5050

# Start ollama in the background and then start the Flask app
CMD ["sh", "-c", "ollama & sleep 5 && python ai_planner/src/app.py"]
