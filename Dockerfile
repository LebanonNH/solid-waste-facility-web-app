FROM python:3.8-alpine

WORKDIR /home/app

COPY . /home/app/

RUN apk add --no-cache musl-dev python3-dev openssl-dev libffi-dev gcc 

RUN pip install --upgrade pip

RUN pip install -r /home/app/requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-b :5000", "landfill:app"]
