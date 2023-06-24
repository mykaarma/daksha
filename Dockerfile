FROM python:3.10

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN mkdir /daksha

# Set the working directory to /ui_automation_engine
WORKDIR /daksha

# Copy the current directory contents into the container at /ui_automation_engine
ADD . /daksha/

# Copy the script file for startup
# COPY startup_command.sh /daksha/

#gives required premissions
RUN chmod og+x -R /daksha

# Install any needed packages specified in requirements.txt
RUN pip install -r ./requirements.txt

#Ubuntu releases are only supported for 9 months. LTS (Long Term Support) releases have support for 5 years.
# Once support is cut for the version you're using, you'll see error messages. 
#Ubuntu moves the repositories to another server and the defined URL to reach the sources are no longer available on default location

#We use the sed command to update the sources in /etc/apt/sources.list file to the new location for 
#old package repositories.
#RUN sed -i 's/stable\/updates/stable-security\/updates/' /etc/apt/sources.list
#RUN sed -i 's/stable\/updates/stable-security\/updates/' /etc/apt/sources.list.d/debian.sources

COPY startup_command.sh /usr/local/bin/startup_command.sh

RUN chmod +x /usr/local/bin/startup_command.sh

# Update the package files
RUN apt-get update 

# Install the cron package
RUN apt-get install -y cron

# start server
CMD ["startup_command.sh"]
