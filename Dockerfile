FROM ollama/ollama

WORKDIR /app

# Clear the base image entrypoint
ENTRYPOINT []

COPY Modelfile.txt Modelfile.txt
COPY ./run-ollama.sh run-ollama.sh

# RUN chmod +x run-ollama.sh \
#     && ./run-ollama.sh


RUN apt-get update && apt-get install -y \
    coreutils \
    python3-pip

# Install Python 3.10
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y python3.10 python3.10-venv python3.10-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure python3 points to python3.10
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ai_planner/src src

COPY start.sh start.sh

EXPOSE 11434
EXPOSE 5050

# # Add this line to ensure the script has executable permissions
RUN chmod +x /app/start.sh

# # Use CMD to run the script
# CMD ["./start.sh"]

# run ollama serve & python src/app.py
CMD ["./start.sh"]