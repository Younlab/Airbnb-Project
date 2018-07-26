# Airbnb Project

## Requirements

- Python (3.6)
- pipenv
- Django (2.0)

### Secrets

#### `.secrets/secrets.json`

- PostgreSQL을 사용, DATABASES 설정이 필요

```json
{
  "SECRET_KEY": "<Django secret key>"
}
```

## Running

```
# Move project's directory
pipenv install
pipenv shell
cd app
`export DJANGO_SETTINGS_MODULE=config.settings.local`
`./manage.py runserver`
```
