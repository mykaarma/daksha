#!/usr/bin/env bash

# The reason for this is that Cron sets up a minimalistic environment and doesn't read the environment variables
# that you may have already had set. We solve it by giving cron access to environment variables we need.
export >> ~/.bash_profile

# Convert TEST_RESULT_DB to lowercase
TEST_RESULT_DB=$(echo "$TEST_RESULT_DB" | tr '[:upper:]' '[:lower:]')

if [ "$TEST_RESULT_DB" == "postgres" ]; then
    echo "Making Migrations to database"
    python manage.py makemigrations engine
    echo "================================="
fi

if [ "$TEST_RESULT_DB" == "postgres" ]; then
    echo "Applying Migrations"
    python manage.py migrate
    echo "================================="
fi

# Convert CRON_ENABLED to lowercase
CRON_ENABLED=$(echo "$CRON_ENABLED" | tr '[:upper:]' '[:lower:]')

if [ "$CRON_ENABLED" == "true" ]; then
    echo "Starting Cron Service"
    service cron start
    echo "================================="
fi

if [ "$CRON_ENABLED" == "true" ]; then
    echo "Adding the listed cron jobs"
    python manage.py crontab add
    echo "================================="
fi

if [ "$CRON_ENABLED" == "true" ]; then
    echo "The Cron Jobs registered are :-"
    python manage.py crontab show
    echo "================================="
fi

echo "Starting the server"
gunicorn --bind 0.0.0.0:8000 daksha.wsgi