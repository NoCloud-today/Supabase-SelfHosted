# Local Development

## Project Structure

* ![Admin Service](../admin)
* ![Deploy Configuration](../docker)  

## Building

Сервис админки включается в приложение в виде контейнера. Локально можно собирать во время запуска ```docker compose``` с опцией ```--build```.  
При коммите в ```main```, собирать очередной минорный релиз и публиковать в публичный ```container registry```, указывать с соответствующим с лейблом ```latest```: ```docker/docker-compose.yml:439```.
```shell
# из admin
docker build . -t <image-name>:<version>
docker tag <image-name>:<version> <image-name>:latest
docker push <image-name>:<version>
docker push <image-name>:latest
```

## Restarter

Функциональность рестарта осуществляется с помощью ```docker/restarter.sh``` - крутится на хосте в бесконечном цикле проверяет создание файла ```docker/restart.txt```, по обнаружению запускает ```docker compose up -d``` - поднимает целиком все приложение.  
Скрипт автоматически запускается при исполнении ```docker/start.py```.

## Supabase Auth

Какие переменные среды за что отвечают:
* ```SITE_URL, ADDITIONAL_REDIRECT_URLS``` - куда происходит переход после успешной авторизации пользователя
* ```SMTP_*``` - настройка почтового клиента для отправки пришлашений. Для тестирования можно использовать smtp-сервис яндекса: https://yandex.ru/support/mail/mail-clients/others.html. Сейчас есть бага: в письме с инвайтом ссылка ведет на http://kong/* вместо актуального домена, решение отложено до лучших времен.  

Подробнее про переменные для настройки GoTrue:
* https://github.com/supabase/auth - форк GoTrue от Supabase
* https://dev.to/chronsyn/self-hosting-with-supabase-1aii - с примерами для OAuth в сторонних сервисах
