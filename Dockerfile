FROM python:3.10.1

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN mkdir /daksha

# Set the working directory to /ui_automation_engine
WORKDIR /daksha

# Copy the current directory contents into the container at /ui_automation_engine
ADD . /daksha/

# Install any needed packages specified in requirements.txt
RUN pip install -r ./requirements.txt

# start server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "daksha.wsgi"]
