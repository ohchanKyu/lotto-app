# lotto-app
OpensourceSW Homework2 - Lotto Application


## **Settings**
### Requirement install Docker
#### Ubuntu Bash Environment
```Bash
cd ~
```
```Bash
sudo apt update
sudo apt install git
```
```Bash
docker version
docker ps -a; docker images
```
```Bash
git clone https://github.com/ohchanKyu/lotto-app
cd ./lotto-app; ls
```
```Bash
docker image build . -t lotto_app
docker images
```
```Bash
docker container run -d -p 8000:8000 lotto_app
docker ps -a
```
URL - http://localhost:8000/lottos

## **Dockerfile**
```Dockerfile
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
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', 
    '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')"
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
```
## **Requirements.txt**
```Bash
django==5.1.4
```
