```
$ cp config/settings/local_settings.default.py config/settings/local_settings.py
```

```
$ docker-compose build
$ docker-compose run --rm web python3 manage.py migrate
$ docker-compose up
```
