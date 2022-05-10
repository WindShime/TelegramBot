# TelegramBot для трекинга доходов и расходов.


В данном проекте используются такие файлы как:
server.py - основной запускаемый файл. Содержит в себе запуск функций по командам.
categories.py - работа с категориями sqlite3
createdb.sql - создание базы данных finance.db по определенным критериям
db.py - работа с базой данных sqlite3 (insert, fetchall, delete)
exceptions.py - различные эксепты
expenses.py - работа с получением расходов, их обработкой и последующим внесением в БД
incomes.py - работа с получением доходов, их обработкой и последующим внесением в БД


В данной проекте используются такие модули как:
yarl
aiogram
multidict
Babel
async-timeout
certifi
idna
aiohttp
pytz
chardet
attrs

База данных находится в файле finance.db
