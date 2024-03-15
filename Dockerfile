FROM python:3.12-alpine3.19

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY main.py .

ENV discord_token=SET_ME

ENTRYPOINT [ "python3", "main.py" ]
