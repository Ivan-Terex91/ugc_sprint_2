# Проектная работа 9 спринта

# Запуск проекта

1. Скопировать переменные окружения командой `make copy_env_file`.
2. Запустить `docker-compose up -d --build`
3. Выполнить команду `bash up_mongo.sh`


[Сервис хранения, обработки и предоставления пользовательских данных о фильмах](https://github.com/Ivan-Terex91/ugc_sprint_2/pull/6)
1. Было добавлено хранение лайков пользователей к каждому фильму, рецензий к фильмам, закладкок пользователя (отложенные на потом фильмы).
2. Были добавлены методы api и views лайков, рецензий, закладкок.

P.S. В последствии было принято решение отказаться от кластера Монги и использовать один инстанс пока что.


[CI/CD](https://github.com/Ivan-Terex91/ugc_sprint_2/pull/5)
1. Был добавлен функционал CI/CD согласно заданию к спринту


[Настройка логгирования сервисов](https://github.com/Ivan-Terex91/ugc_sprint_2/pull/7)
1. Была добавлена настройка Sentry, настройка ELK.
2. Было добавлено логгирование в сервис auth и сервис UGC.
