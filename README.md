docker-compose down

docker-compose up --build

docker-compose run web python manage.py makemigrations

docker-compose run web python manage.py populate_db

docker-compose run web python manage.py migrate