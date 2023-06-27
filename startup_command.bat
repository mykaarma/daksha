set "TEST_RESULT_DB=%TEST_RESULT_DB%"

@REM If the environment variable test_result_db is not set, we will directly run the server
if not defined TEST_RESULT_DB goto :runserver

@REM The parameter /i tells the cmd to do a insensitive case comparison
IF /i TEST_RESULT_DB==postgres (
python manage.py makimigrations engine
)

IF /i TEST_RESULT_DB==postgres (
python manage.py migrate
)

:runserver
python manage.py runserver