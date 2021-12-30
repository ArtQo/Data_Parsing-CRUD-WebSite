# В лабораторной работе №3 реализованы CRUD-функции с улучшенным интерфейсом веб-сайта, а также парсер новостей (https://russian.rt.com)

1. ___Парсер новостей:___
Состоит из библиотек (selenium, beautifulsoup, requests)
Сначала, с помощью автоматизированого ПО, мы погружаем дополнительные статьи, количество пролистывания можно настроить в коде, так как сайт является динамическим. Дальше код парсера, по определённым элементам, собирает нужную нам информацию (Название статьи, описание и ссылку). С помощью библиотеки (requests), добавляем собранные данные в базу mysql, используя функцию (post, которая находится в CRUD директории).

2. ___CRUD-функции:___
Состоит из библиотек(bottle, pymysql, configparser) В данной папке реализованы функции (поиска информации по 'id' в базе данных 'mysql', вывод всех данных из базы, редактирование, удаление записей, а также поиск по слову/словосочетнию и функция поиска через оператор ___LIKE___ и логических опреторов). Также данные доступа к базе данных скрыты с помощью (configparser), который читает файл (pymysql.ini) и автоматически выполняет подключение.

3. ___Сайт:___
Написан на html и немного JavaScript. Сделан веб-интерфейс для взаимодействия с ___CRUD-функциями___.

Скриншот ___"Главное меню"___:
<img width="366" alt="Главное" src="https://user-images.githubusercontent.com/95654540/147759796-4bdf8e73-0b4c-4476-9c22-e0ce4de65ad2.png">

Скриншот ___"Поиск в Базе данных"___:
<img width="490" alt="Поиск" src="https://user-images.githubusercontent.com/95654540/147759844-38a2b40c-6d0b-46ff-b5c9-faa022b6e16d.png">

Сриншот ___"Функция Show All"___:
<img width="892" alt="БД" src="https://user-images.githubusercontent.com/95654540/147759912-a3c19b02-79ff-4b32-8bcd-1e7277ffa630.png">


## Для запуска нам нужно:

* Указать путь к chromedriver (в коде parserDB)
* Запустить локальный сервер (mysql)
* Создать таблицу в mysql с атрибутами (таблица: news_data_RT; атрибуты: ID, Article, Pre_Body, Link)
* Запустить сначала серверную часть (директория CRUD)
* Запустить парсер и добавление данных с сайта в базу (директория ParserDB)
* Перейти на указанную ссылку локального сайта (Она отображается при запуске кода 'директория CRUD')
* Наслаждаться! 🙂

## На выходе:
123
