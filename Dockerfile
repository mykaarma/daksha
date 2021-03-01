FROM python:3.7

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN mkdir /ui_automation_engine

# Set the working directory to /ui_automation_engine
WORKDIR /ui_automation_engine

# Copy the current directory contents into the container at /ui_automation_engine
ADD . /ui_automation_engine/

# Install any needed packages specified in requirements.txt
RUN pip install -r ./requirements.txt