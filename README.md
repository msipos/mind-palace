# Mind Palace

Mind palace: mnemonic note taking system.

This is a web application built with Django and React. You can host it yourself.

![Screen Recording](mind-palace.gif)

Pull requests welcome.

## Features

* Notes are written in Markdown and collected into collections
* You can search/view/edit/archive/delete notes.
* Notes can be *repeated* whereby they will pop up on the "Repeat" page on a schedule until bounced off to a later time
* Each note has its own repetition schedule, and a learning schedule
* 3 possible repeating schedules:
   - no repeating
   - repeat every N hours
   - repeat every N days (in the morning or evening)
* 2 possible learning schedules:
   - fixed
   - exponential (repetition period changes by factors of 50%/100%/150%/200%).
* Notes are composed of multiple cards, each written in Markdown. Cards can be "hidden". This can be used for e.g.
  language learning
* Notes can contain EJS templates. This allows dynamic content, for example 
* Multi-user support, one hosted system can have multiple users with their own collections 
* Can be hosted at a sub-URL, e.g. /this-is-my-url/mind-palace/ 
* Import and export into JSON

## TODOs

* Collection editing is currently done through the admin UI, mostly out of laziness, as it's rarely done.
* Static asset management system will allow pictures and attachments

## Roadmap

* Embed-an-image sections
* Embed-a-PDF sections
* Local / client-side encryption
* Better spaced repetition algorithms
* Collect data on repetitions

## Getting started locally

* With poetry:

```
poetry install
```

* Install frontend dependencies:

```
cd frontend
npm install
``` 

* Create your `LOCAL_ENV.dev`, populate the entries and source it

```
cp LOCAL_ENV.dev.template LOCAL_ENV.dev
source LOCAL_ENV.dev
```

* Run a build and collect static files

```
poetry run inv collectstatic  # or collectstatic-release
```

* Create the database 

```
poetry run python manage.py migrate
```

* Create a superuser

```
poetry run python manage.py createsuperuser
```

* Run your server for development

```
poetry run python manage.py runserver
```

## Running in production

Roughly the above steps, but instead of `runserver`:

```
poetry run gunicorn mind_palace.mind_palace_site.wsgi -w 2 --log-level debug
```

You will want to proxy via a gateway load balancer such as Caddy or Nginx.


## Docker (WIP)

Build package:

```
docker build -t mind_palace:dev -f docker/Dockerfile.build .
```

Test package (WIP):
```
docker run -it --rm mind_palace:dev /bin/bash
```

Retag package:

```
docker tag mind_palace:dev msiposdocker/mind_palace:0.0.X
docker push msiposdocker/mind_palace:0.0.X
```
