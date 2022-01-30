FROM python:3.9

WORKDIR /spotyfree

COPY ./requirements.txt /spotyfree/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /spotyfree/requirements.txt

RUN apt-get update && apt-get -y install ffmpeg

COPY ./app /spotyfree/app

COPY ./log.txt /spotyfree/log.txt

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]