@echo off

set "TEST_RESULT_DB=%TEST_RESULT_DB%"

@REM If the environment variable TEST_RESULT_DB is not set, we will directly run the server
if not defined TEST_RESULT_DB goto :runserver

@REM The parameter /i tells the cmd to do a case-insensitive comparison
IF /i "%TEST_RESULT_DB%"=="postgres" (
    python manage.py makemigrations engine
    python manage.py migrate
)

:runserver
python manage.py runserver
