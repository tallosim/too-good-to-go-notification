FROM python:3.9-alpine

COPY requirements.txt /app/
COPY *.py /app/

WORKDIR /app

RUN pip install -r requirements.txt


ARG EMAIL_ADDRESS
RUN echo "Email sent to the $EMAIL_ADDRESS."
RUN python create_credtentials.py -e $EMAIL_ADDRESS

CMD python send_notification.py -i 30