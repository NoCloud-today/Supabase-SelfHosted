# Supabase-SelfHosted

### Локальный запуск:
```shell
git clone --depth 1 https://github.com/MhlvDenis/Self-Hosted_Supabase
cd docker
cp .env.example .env
docker compose pull
docker compose up -d # в фоне
# docker compose up # с логами
```

Доступ к дашборду: http://localhost:8000

Дефолтные логин и пароль из .env:
- supabase
- this_password_is_insecure_and_should_be_updated  

TODO:  
 /-- Поправить шаблон для   приглашения пользователя по электронной почте - ссылка с подтверждением начинается с http://kong