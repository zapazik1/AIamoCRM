---
title: "Параметры аккаунта"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/crm/platform/account-info
section: developers
---

### Параметры аккаунта

#### Метод

*GET /api/v4/account*

#### Описание

Метод позволяет получить необходимую информацию по аккаунту, например: ID, название, справочник типов задач, группы пользователей и другие параметры.

#### Ограничения

Метод доступен всем пользователям аккаунта.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| with | string | Данный параметр принимает строку, в том числе из нескольких значений, указанных через запятую. [Данный метод поддерживает следующие параметры.](#with-b030cba4-f35c-42c2-b9fd-24bdfebebfb6-params) |

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выполнен успешно |
| 401 | Пользователь не авторизован |

#### Параметры ответа

Метод возвращает модель данных аккаунта, рассмотрим ниже свойства.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID аккаунта |
| name | string | Название аккаунта |
| subdomain | string | Субдомен аккаунта |
| current\_user\_id | int | ID текущего пользователя |
| country | string | Страна, указанная в настройках аккаунта |
| customers\_mode | string | Режим покупателей. Возможные варианты: unavailable (функционал недоступен), disabled (функцонал отключен), segments (сегментация), dynamic (deprecated), periodicity (периодические покупки) |
| is\_unsorted\_on | bool | Включен ли функционал “Неразобранного” в аккаунте |
| is\_loss\_reason\_enabled | bool | Включен ли функционал причин отказа |
| is\_helpbot\_enabled | bool | Включен ли функционал Типовых вопросов (доступен только на профессиональном тарифе) |
| is\_technical\_account | bool | Является ли данный аккаунт техническим |
| contact\_name\_display\_order | int | Порядок отображения имен контактов (1 – Имя, Фамилия; 2 – Фамилия, Имя) |
| amojo\_id | string | **Требуется GET параметр with.** Уникальный идентификатор аккаунта для работы с сервисом чатов amoJo |
| version | int | **Требуется GET параметр with.** Текущая версия amoCRM |
| drive\_url | string | **Требуется GET параметр with.** Адрес сервиса файлов для конкретного аккаунта |
| is\_api\_filter\_enabled | bool | **Требуется GET параметр with.** Включена ли API фильтрация для аккаунта |
| entity\_names | object | **Требуется GET параметр with.** Настройки названия сущностей |
| invoices\_settings | object | **Требуется GET параметр with.** Настройки счетов-покупок |
| invoices\_settings[lang] | string | **Требуется GET параметр with.** Язык счетов-покупок и PayWall. |
| invoices\_settings[invoices\_catalog\_id] | int | **Требуется GET параметр with.** ID списка счетов-покупок |
| \_embedded[amojo\_rights] | object | **Требуется GET параметр with.** Объект настроек чатов |
| \_embedded[amojo\_rights][can\_direct] | object | **Требуется GET параметр with.** Доступны ли внутренние чаты |
| \_embedded[amojo\_rights][can\_create\_groups] | object | **Требуется GET параметр with.** Доступна ли возможность создавать групповые чаты |
| \_embedded[users\_groups] | array | **Требуется GET параметр with.** Массив объектов групп пользователей аккаунта |
| \_embedded[users\_groups][0][id] | int | **Требуется GET параметр with.** ID группы пользователей |
| \_embedded[users\_groups][0][name] | string | **Требуется GET параметр with.** Название группы пользователей |
| \_embedded[task\_types] | array | **Требуется GET параметр with.** Типы задач, доступные в аккаунте |
| \_embedded[task\_types][0][id] | int | **Требуется GET параметр with.** ID типа задач |
| \_embedded[task\_types][0][name] | string | **Требуется GET параметр with.** Название типа задач |
| \_embedded[task\_types][0][color] | string | **Требуется GET параметр with.** Цвет типа задач |
| \_embedded[task\_types][0][icon\_id] | int | **Требуется GET параметр with.** ID иконки типа задач |
| \_embedded[task\_types][0][code] | string | **Требуется GET параметр with.** Код типа задач |
| \_embedded[datetime\_settings] | object | **Требуется GET параметр with.** Настройки и форматы даты и времени в аккаунте |

#### Пример ответа

```json
{
"id": 1231414,
"name": "example",
"subdomain": "example",
"current\_user\_id": 581651,
"country": "RU",
"customers\_mode": "segments",
"is\_unsorted\_on": true,
"is\_loss\_reason\_enabled": true,
"is\_helpbot\_enabled": false,
"is\_technical\_account": false,
"is\_api\_filter\_enabled": true,
"contact\_name\_display\_order": 1,
"amojo\_id": "f3c6340d-410e-4ad1-9f7e-c5e663599909",
"uuid": "824f3a59-6154-4edf-ba90-0b5593715d07",
"drive\_url": "https://drive-b.amocrm.ru"
"version": 16,
"entity\_names": {
"leads": {
"ru": {
"gender": "m",
"plural\_form": {
"dative": "клиентам",
"default": "клиенты",
"genitive": "клиентов",
"accusative": "клиентов",
"instrumental": "клиентами",
"prepositional": "клиентах"
},
"singular\_form": {
"dative": "клиенту",
"default": "клиент",
"genitive": "клиента",
"accusative": "клиента",
"instrumental": "клиентом",
"prepositional": "клиенте"
}
},
"en": {
"singular\_form": {
"default": "lead"
},
"plural\_form": {
"default": "leads"
},
"gender": "f"
},
"es": {
"singular\_form": {
"default": "acuerdo"
},
"plural\_form": {
"default": "acuerdos"
},
"gender": "m"
}
}
},
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/account"
}
},
"\_embedded": {
"amojo\_rights": {
"can\_direct": true,
"can\_create\_groups": true
},
"users\_groups": [
{
"id": 0,
"name": "Отдел продаж",
"uuid": null
}
],
"task\_types": [
{
"id": 1,
"name": "Связаться",
"color": null,
"icon\_id": null,
"code": "FOLLOW\_UP"
},
{
"id": 2,
"name": "Встреча",
"color": null,
"icon\_id": null,
"code": "MEETING"
}
],
"datetime\_settings": {
"date\_pattern": "d.m.Y H:i",
"short\_date\_pattern": "d.m.Y",
"short\_time\_pattern": "H:i",
"date\_formant": "d.m.Y",
"time\_format": "H:i:s",
"timezone": "Europe/Moscow",
"timezone\_offset": "+03:00"
}
}
}
```

#### Параметры для GET-параметра with

| Параметр | Описание |
| --- | --- |
| amojo\_id | Добавляет в ответ ID аккаунта в сервисе чатов |
| amojo\_rights | Добавляет в ответ информацию о доступности функционала создания групповых и использования директ чатов пользователями |
| users\_groups | Добавляет в ответ информацию о доступных группах пользователей аккаунта |
| task\_types | Добавляет в ответ информацию о доступных типах задач в аккаунте |
| version | Добавляет в ответ информацию о текущей версии amoCRM |
| entity\_names | Добавляет в ответ названия сущностей с их переводами и формами чисел |
| datetime\_settings | Добавляет в ответ информацию о текущих настройках форматов даты и времени аккаунта |
| drive\_url | Добавляет в ответ адрес сервиса файлов для запрашиваемого аккаунта |
| is\_api\_filter\_enabled | Добавляет в ответ флаг, включена ли Альфа-фильтрация для аккаунта |
| invoices\_settings | Добавляет в ответ информацию о настройки счетов-покупок |