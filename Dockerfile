FROM python:3.14

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV TZ=Europe/Amsterdam

COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY /*.py /usr/src/app/

CMD [ "python", "-u", "waterstandtwitter.py" ]
