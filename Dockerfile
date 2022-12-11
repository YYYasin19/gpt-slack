FROM mambaorg/micromamba

WORKDIR /app
COPY . /app

RUN micromamba create -y -f environment.yml
ENTRYPOINT [ "micromamba", "run", "-n", "slack-gpt", "python", "main.py" ]
