FROM python:3.8-alpine

COPY ./* /home/app/

RUN apk install gcc 

RUN pip install -r /home/app/requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-b :5000", "landfill:app"]
