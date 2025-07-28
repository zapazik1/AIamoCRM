---
title: "Возможности"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/web/sdk/start
section: developers
---

**WEB SDK** позволяет дорабатывать amoCRM путем внедрения пользовательских скриптов и стилей, в терминологии системы мы называем эту возможность – "**виджеты**".

**Виджет** – это архив с JS, CSS файлами, а также файлами шаблонов Twig, который может быть загружен в [интеграцию](https://www.amocrm.ru/developers/content/integrations/intro). В таком случае JS файлы и верстка будет подгружена в браузер вместе с интерфейсом amoCRM, что даст возможность интегратору взаимодействовать с пользователем, взаимодействовать с API amoCRM или API собственного сервиса непосредственно из интерфейса amoCRM.

Виджеты могут работать как постоянно (с момента загрузки страницы и не прекращать свою работу, такие виджеты имеют флаг **"**[init\_once](https://www.amocrm.ru/developers/content/web_sdk/init_once)**"**), так и включаться в определенные моменты в указанных интерфейсах системы, эти определенные интерфейсы мы называем **"области подключения"** или **"locations"**.

Области подключения представляют из себя по сути перечисление мест интерфейса, где будет выполнен колбэк виджета, а виджет уже на своей стороне решает какую логику для данного колбэка выполнить. Более подробное описание работы каждой области подключения можно почитать по соответствующей ссылке в таблице ниже, но для начала давайте рассмотрим что из себя представляет минимальный виджет и разберемся с [механикой работы](https://www.amocrm.ru/developers/content/web_sdk/mechanics).

Список возможных областей подключения:

| Значение | Описание |
| --- | --- |
| lcard, cucard, ccard, comcard | [Карточки](https://www.amocrm.ru/developers/content/web_sdk/card) сделок, покупателей, контактов и компаний |
| llist, culist, clist, tlist | [Списки](https://www.amocrm.ru/developers/content/web_sdk/list) сделок, покупателей, контактов и задач |
| tline, tcalendar | Разделы задач в виде канбан и календаря, на данный момент используются для работы виджета в модальном [окне синхронизации задач](https://www.amocrm.ru/developers/content/web_sdk/todo_sync) |
| settings | Cтраница установки и [настройки](https://www.amocrm.ru/developers/content/web_sdk/settings) виджетов |
| advanced\_settings | Собственная страница [расширенных настроек](https://www.amocrm.ru/developers/content/web_sdk/settings) виджета |
| card\_sdk | Добавляет собственную [вкладку](https://www.amocrm.ru/developers/content/web_sdk/card) в левой части карточки (требует lcard, ccard, comcard для работы соответствующих сущностях) |
| catalogs | Позволяет изменять внешний вид карточки элемента сущности "[Списки](https://www.amocrm.ru/developers/content/web_sdk/list)" |
| digital\_pipeline | [Триггеры](https://www.amocrm.ru/developers/content/web_sdk/digital_pipeline) в Digital Pipeline |
| lead\_sources | [Источники сделок](https://www.amocrm.ru/developers/content/web_sdk/digital_pipeline) в Digital Pipeline |
| whatsapp\_modal | Модальное окно интеграций, работающих с [WhatsApp](https://www.amocrm.ru/developers/content/web_sdk/digital_pipeline) |
| everywhere | Виджет будет инициализироваться в любой из перечисленных областей видимости: lcard, cucard, ccard, comcard, llist, culist, clist, tlist. |