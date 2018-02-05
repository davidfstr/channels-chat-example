# channels-chat-example

This is a simple chat server implemented with Django Channels and WebSockets.

## Install

* Install Docker

* Install Python 3.5+

```
# Install pipenv to system Python, if not already done
pip3 install pipenv

# Create virtual environment for this project and install dependencies
pipenv install
```

## Run

```
docker run --name chat-redis -p 6379:6379 -d redis:2.8
pipenv run python3 manage.py runserver
```

Browse to: <http://127.0.0.1:8000/chat/>

## License

MIT.
