FROM ollama/ollama

WORKDIR /app

# Clear the base image entrypoint
ENTRYPOINT []

COPY Modelfile.txt Modelfile.txt
COPY ./run-ollama.sh run-ollama.sh

RUN chmod +x run-ollama.sh \
    && ./run-ollama.sh \
    apt-get update && apt-get install -y \
    coreutils \
    python3-pip \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y python3.10 python3.10-venv python3.10-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ai_planner/src src

EXPOSE 11434
EXPOSE 5050

# Run the ollama server and the python app
CMD ollama serve & python3 src/app.py