# ![Logo](https://raw.githubusercontent.com/Aerodlyn/mu/develop/static/images/logo-no-text.png "mu logo") mu - the simple forum
mu is a simple project that takes inspiration after traditional blogs and reddit. mu is powered by
[Django](https://www.djangoproject.com) and styled using [Bootstrap](https://www.getbootstrap.com).

## Set up
You will need [Python 3](https://www.python.org). I recommend using a virtual environment to avoid
any version conflicts with packages you might already have:
`python3 -m venv .venv && source .venv/bin/activate`.

Either way, you'll need to install the dependencies from `requirements.txt` using
`pip3 install -r requirements.txt`.

You will then need to create an `.env` file or pass the following attributes when running mu:
```
DEBUG=true
SECRET_KEY=...
```

Run `python3 manage.py migrate` and then finally `python3 manage.py runserver`. mu can then be
visted through `http://localhost:8000`.

## Name
I named mu after the noise one of my cats - Jack Jack - makes. Instead of a more traditional meow,
Jack Jack mews like a kitten, even though he's a 13-pound chonker.
