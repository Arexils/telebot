## Структура для сдачи ДЗ телеграм ботов

* Бот [@arexils_innopolis_bot](https://t.me/arexils_innopolis_bot) - кто желает, можете во время занятия потыкать
* [Документация API telegram](https://core.telegram.org/bots/api)
* [pythonanywhere хостинг бота](https://www.pythonanywhere.com/)
* [Ngrok](https://ngrok.com/)
* [Railway](https://railway.app)
* [Goorm.io](https://ide.goorm.io/)

### Примеры ботов

* [Polling](https://github.com/Arexils/telebot/tree/master)
* [Webhook](https://github.com/Arexils/telebot/tree/webhook)
* [API](https://github.com/Arexils/telebot/tree/api)

## Запуск и установка бота

1. Вы должны создать в корне проекта файла `.env`
2. В него написать `TOKEN=` после знака `=` вставить ваш токен.
3. Корректный `.gitignore` смотрите в этом репозитории.
4. Да и вообще файлы | структуру можно посмотреть в этом репозитории.

Содержание файла `.env`

```dotenv
TOKEN=
NGROK=
WEATHER_API=
```

___

1. Вы должны убедиться что вы находитесь в **виртуальном окружении** вашего проекта.
2. Как это проверить?
    * Командная строка начинается с `(venv)` и затем идет путь к вашему проекту.
    * Если это отсутствует, то вам необходимо войти в виртуальное окружение (или создать его если отсутствует в проекте папка `venv`)
        * Создать виртуальное окружение с помощью команды `python -m venv venv`
    * Активация виртуального окружения:
        * Linux / MacOS : `source venv/bin/activate`
        * Windows: `venv\Scripts\activate`
            * ❗ Если у вас в консоле ошибка с выполнениями скриптов [Ссылка на решение проблемы](https://ru.stackoverflow.com/a/1041525) и сама команда на всякий случай `Set-ExecutionPolicy Unrestricted`
3. После того как вы зашли в виртуальное окружение `venv`, вы должны установить зависимости из файла `requirements.txt`. Каждая новая зависимость должна начинаться с новой строки.
4. Команда установки `pip install -r requirements.txt`
5. Команда запуска бота `python main.py` - т.к. у меня называется файл `main.py`

___

## Как сдавать проект?

❗❗❗ Перед отправкой убедитесь, что вы не отправляете `TOKEN` публично, он должен оставаться только у вас.

### 1. ❗ БЕЗ ❗ [gitlab.com](https://gitlab.com/)

+ Все выполняет в одном файле `bot.py`
+ У вас должен быть отдельно файл `config.py`, где будет содержаться ваш токен, который вы импортирует в `bot.py`
+ ❗Перед отправкой проверяйте запуская (работает) ваш бот, правильно ли работает?
+ На сайт отправляете только файл `bot.py`

### 2. ❗ ДЛЯ ❗ [gitlab.com](https://gitlab.com/)

+ Проверьте правильность вашего `.gitignore`, так же репозиторий не дожен содержать лишнее файла и папки: `venv`, `__pycache__`, `.git` и тд.
+ От основной ветки `master` вы создаёте новую ветку `dev` и в ней выполняете работу.
+ Вы делаете полноценную архитектуру проекта разбивая на файлы.
+ В файле `config.py` вы токен получаете из переменных окружения, которые описаны в файле `.env`.
+ ❗❗❗Файл `.env` **НЕЛЬЗЯ** отправлять на [gitlab.com](https://gitlab.com/)
+ Для проверки вашей работы вы делаете MR (merge request), а именно изменения из `dev` в `master`, и ожидаете пока проверю.
    + После успешной проверки MR, не забудьте сделать `git pull` для получения изменений с [gitlab.com](https://gitlab.com/) к вам локально.
+ На сайт вы прикрепляете файл `bot.py`, где **в самом верху** ввиде комментария находится ссылка на ваш [gitlab.com](https://gitlab.com/) репозиторий бота (не профиль).

___

Если остались вопросы - задавайте в телеграмме.