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
  "SECRET_KEY": "<Django secret key>",
  "ALLOWED_HOSTS": [
    "<Hosts>"
  ],

  "DATABASES": {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "<host>",
        "PORT": 5432,
        "USER": "<user>",
        "PASSWORD": "<password>",
        "NAME": "<db name>"
    }
  },

  "AWS_ACCESS_KEY_ID": "<AWS_ACCESS_KEY_ID>",
  "AWS_SECRET_ACCESS_KEY": "<AWS_SECRET_ACCESS_KEY>",
  "AWS_STORAGE_BUCKET_NAME": "<AWS_STORAGE_BUCKET_NAME>",
  "AWS_DEFAULT_ACL": "private",
  "AWS_S3_REGION_NAME": "<AWS_S3_REGION_NAME>",
  "AWS_S3_SIGNATURE_VERSION": "<AWS_S3_SIGNATURE_VERSION>",

  "ADMIN_USERNAME": "<username>",
  "ADMIN_PASSWORD": "<password>",

  "SUPERUSER_USERNAME": "<username>",
  "SUPERUSER_PASSWORD": "<password>",
  "SUPERUSER_EMAIL": "<email>",

  "EMAIL_BACKEND" : "<email_backend>",
  "EMAIL_PORT" : "<port>",
  "EMAIL_HOST" : "<email_host>",
  "EMAIL_HOST_USER" : "<email_host_user>",
  "EMAIL_HOST_PASSWORD" : "<email_host_password>"
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
