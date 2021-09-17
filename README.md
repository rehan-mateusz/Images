# Images


Features:
- Creating users with django admin
- Creating plans with django admin
- Users can upload images via HTTP request
- Users can get list of their images
- Users can see details of their image - amount of information received by user depends on user's plan (links to original image and thumbnails)
- Users can create a temporary link to a detail view that is valid for 30-30000 seconds and can be accessed by anonymous user. The guest will same amount of information as user that created the link



# How to use
- Download the repository
```
git clone https://github.com/rehan-mateusz/Images/
```

- Create .env file in Library/imagesproject/imagesproject/ it should contain:
```
SECRET_KEY=your_SECRET_KEY
DEBUG=on
```

- Start with docker:

cd to /Images and use docker-compose by typing in console
```
docker-compose up
```
- Start with Python:

Preferably create a virtual environment.

cd to /Images
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages.
```
pip install -r requirements.txt
```
With requirements installed you can run the app:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

# Tests
- With docker-compose:
Go into docker-compose.yml file, remove:
```
"python manage.py makemigrations &&
 python manage.py migrate &&
 python manage.py runserver 0:8000"
 ```
and put in pytest command:
 ```
 command: |
      sh -c "pytest"
 ```
next just cd to /Images and use docker-compose by typing in console
 ```
 docker-compose up
 ```
- With python:
After installing app and requirements.txt simply go into /Images/imagesproject and type into console:
  ```
pytest
  ```
