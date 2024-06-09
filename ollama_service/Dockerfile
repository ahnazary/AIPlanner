FROM ollama/ollama

WORKDIR /tmp

COPY Modelfile.txt Modelfile.txt
COPY ./run-ollama.sh run-ollama.sh

RUN chmod +x run-ollama.sh \
    && ./run-ollama.sh

EXPOSE 11434