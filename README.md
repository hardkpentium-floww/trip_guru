# trip_guru


## setup virtualenv

```sh
pip install virtualenv
virtualenv .venv
```

## install requirements

```bash
pip install -r requirements_project.txt
pip install -r requirements_test.txt

# if you ran into any issue with kerbrose package install below system dependencies
sudo apt-get install krb5-config libkrb5-dev libssl-dev libsasl2-dev libsasl2-modules-gssapi-mit python3.7-dev python3-dev -y

```

## running django management commands & usage

```sh
source .venv/bin/activate
export DJANGO_SETTINGS_MODULE=trip_guru.settings.local
python manage.py build -a trip
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```