FROM python:3.8-alpine

COPY ./* /home/app/

RUN apk add --no-cache python3-dev openssl-dev libffi-dev gcc linux-headers

RUN pip install --upgrade pip

RUN pip install -r /home/app/requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-b :5000", "landfill:app"]
