
echo "performing migrations"
python manage.py makemigrations engine 

echo " migrating"
python manage.py migrate 

echo "starting the server"
python manage.py runserver 0.0.0.0:8000