# book_master

Бот для покупки книг.\
bot: @book_king_bot

У бота есть функция авторизации по реферальной ссылке, либо ввода кода вручную.\
У бота есть админ-панель, а также django-админка.\
Доступ к функционалу бота есть только у пользователей прошедших авторизацию.

Список команд бота:\
  /start - Начать диалог.\
  /help - Получить справку.\
  /auth - Ввести код авторизации.\
  /books - Поиск и выбор интересующей вас книги.\
  /balance - Вывод текущего бонусного баланса и вашей уникальной реферальной ссылки.
   
Выбор книг доступен только через поиск в inline-режиме. Поиск ведётся по названиям книг совпадающим с введённым текстом. По умолчанию выводятся все книги в алфавитном порядке\
После выбора книги будет возможность ее купить. Для покупки используется тестовая карта(лимит на одну покупку 1000руб).

Есть встроенная админ панель, доступная админу по команде /admin_panel. Админ может добавить новую книгу, удалить и изменить имеющиеся книги.\
Также у бота есть django-админка с более полным функционалом.
