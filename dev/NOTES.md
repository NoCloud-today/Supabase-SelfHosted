# Заметки для разработки

## Supabase Auth

Какие переменные среды за что отвечают:
* ```SITE_URL, ADDITIONAL_REDIRECT_URLS``` - куда происходит переход после успешной авторизации пользователя
* ```SMTP_*``` - настройка почтового клиента для отправки пришлашений. Для тестирования можно использовать smtp-сервис яндекса: https://yandex.ru/support/mail/mail-clients/others.html. Сейчас есть бага: в письме с инвайтом ссылка ведет на http://kong/* вместо актуального домена, решение отложено до лучших времен.  

Подробнее про переменные для настройки GoTrue:
* https://github.com/supabase/auth - форк GoTrue от Supabase
* https://dev.to/chronsyn/self-hosting-with-supabase-1aii - с примерами для OAuth в сторонних сервисах
