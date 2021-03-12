# Test Assignment by idaproject
Service based on Django framework, which allows users to upload images straight from their PC or from URL. It can also resize each image based on provided width/height.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for testing purposes.

### Prerequisites

Get the latest version of Python at https://www.python.org/downloads/ or with your operating system’s package manager. This project uses SQLite, which is included with Python.

Get the package from the source code:
```
git clone https://github.com/RubikonZ/DjangoTest.git
```
### Installation
Set up your development environment:
```
python3 -m virtualenv venv
```
To activate and work in newly created environment:
```
source venv/bin/activate
```
Install required modules:
```
python install -r requirements.txt
```

Make sure you have migrations up-to-date:
```
python manage.py check
```

If they aren't (and they should be), write next commands:
```
python manage.py makemigrations
python manage.py migrate
```

Now you can start web application:
```
python manage.py runserver
```

By default this web application uses port 8000. You can connect to it with these links:
```
http://127.0.0.1:8000/
http://localhost:8000/
```
