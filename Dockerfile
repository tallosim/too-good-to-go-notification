FROM python:3.12-alpine

# Set the working directory to /usr/app
WORKDIR /usr/app

# Copy the current directory contents into the container at /usr/app
COPY requirements.txt /usr/app/
COPY tgtg-notification.py /usr/app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run app.py when the container launches
CMD python -u tgtg-notification.py
