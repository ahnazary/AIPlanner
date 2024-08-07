FROM ollama/ollama

WORKDIR /app

# Clear the base image entrypoint
ENTRYPOINT []

RUN apt-get update && apt-get install -y coreutils

COPY Modelfile.txt Modelfile.txt
COPY ./run-ollama.sh run-ollama.sh

# Install Python 3.10
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-venv python3.10-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure python3 points to python3.10
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Check python version
RUN python3 --version

# Install pip
RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN chmod +x run-ollama.sh \
    && ./run-ollama.sh

COPY ai_planner/src src

EXPOSE 11434
EXPOSE 5050

CMD ["python3", "src/app.py"]
