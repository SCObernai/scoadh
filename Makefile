run:
    python manage.py runserver 0.0.0.0:8000 --settings=sco.local_settings

sh:
    python manage.py shell_plus --settings=sco.local_settings

mig:
    python manage.py migrate --settings=sco.local_settings

dep:
    npm install
    pip install -r requirements.txt