# Сменить email суперадмина в PostgreSQL

Выполняйте на сервере под пользователем с доступом к БД (часто `postgres`).

**Если старый email ещё `admin@example.com`:**

```bash
sudo -u postgres psql -d streaming -c "UPDATE users SET email = 'fylhtq25508@mail.ru' WHERE email = 'admin@example.com' AND role = 'SUPERADMIN';"
```

Если такой строки нет (email уже меняли), сначала посмотрите учётки:

```bash
sudo -u postgres psql -d streaming -c "SELECT email, role FROM users WHERE role = 'SUPERADMIN';"
```

и подставьте нужный `WHERE`.

**Показать интерактивное знакомство снова** (после прохождения онбординга):

```bash
sudo -u postgres psql -d streaming -c "UPDATE users SET onboarding_completed = false WHERE email = 'fylhtq25508@mail.ru';"
```

Дальше войдите под новым email и паролем.
