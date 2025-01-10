FROM python:3.11.6

WORKDIR /usr/src/app

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJNAGO_SUPERUSER_EMAIL=admin@naver.com
ENV DJANGO_SUPERUSER_PASSWORD=admin1234!

WORKDIR ./LottoApp

RUN python manage.py makemigrations lottos
RUN python manage.py migrate
RUN python manage.py shell -c "from django.contrib.auth.models import User; \
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')"
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
