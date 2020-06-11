# Mind Palace

Mind palace: mnemonic note taking system.

This is a web application built with Django and React.

## Running in production

```
gunicorn mind_palace.mind_palace_site.wsgi -w 2 --log-level debug
```