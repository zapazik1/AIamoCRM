---
title: "Связи сущностей"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/crm/platform/entity-links-api
section: developers
---

В данном разделе описываются доступные методы для работы со связями контактов, компаний, сделок и покупателей

### Оглавление

- [Общая информация](#common-info)
- [Список связанных сущностей](#links-list)
- [Привязка сущностей](#links-link)
- [Отвязка сущностей](#links-unlink)
- [Массовый список связанных сущностей](#mass-links-list)
- [Массовая привязка сущностей](#mass-links-link)
- [Массовая отвязка сущностей](#mass-links-unlink)

### Общая информация

Возможные связи различаются для разных типов сущностей

- Для сделок доступны: контакты, компании, элементы списков
- Для контактов доступны: компании, покупатели, элементы списков
- Для компаний доступны: контакты, сделки, покупатели, элементы списков
- Для покупателей доступны: контакты, компании, элементы списков

### Список связанных сущностей

#### Метод

GET /api/v4/leads/{entity\_id}/links

GET /api/v4/contacts/{entity\_id}/links

GET /api/v4/companies/{entity\_id}/links

GET /api/v4/customers/{entity\_id}/links

#### Описание

Метод позволяет получить связанные сущности по ID основной сущности.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| filter | object | Фильтр |
| filter[to\_entity\_id] | int | Фильтр по ID связанной сущности, передается вместе с фильтром filter[to\_entity\_type] |
| filter[to\_entity\_type] | string | Фильтр по типу связанной сущности, передается вместе с фильтром filter[to\_entity\_id] |
| filter[to\_catalog\_id] | int | Фильтр по ID каталога связанной сущности |

#### Заголовок типа данных при успешном результате

Content-Type: application/hal+json

#### Заголовок типа данных при ошибке

Content-Type: application/problem+json

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выполнен успешно |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает коллекцию моделей связей. Рассмотрим ниже свойства моделей

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| to\_entity\_id | int | ID связанной сущности |
| to\_entity\_type | string | Тип связанной сущности (leads, contacts, companies, customers, catalog\_elements) |
| metadata | object/null | Метаданные связанной сущности |
| metadata[main\_contact] | bool | Является ли привязанный контакт главным |
| metadata[quantity] | int/float | Количество прикрепленных элементов каталогов |
| metadata[catalog\_id] | int | ID каталога |
| metadata[price\_id] | int/null | ID поля типа Цена, которое установлено для привязанного элемента в контексте сущности |

#### Пример ответа

```json
{
"\_total\_items": 4,
"\_links": {
"self": {
"href": "https://shard151.amocrm.ru/api/v4/leads/7593303/links?page=1&limit=50"
}
},
"\_embedded": {
"links": [
{
"to\_entity\_id": 597393,
"to\_entity\_type": "catalog\_elements",
"metadata": {
"quantity": 1,
"catalog\_id": 4521
}
},
{
"to\_entity\_id": 11069775,
"to\_entity\_type": "contacts",
"metadata": {
"main\_contact": true
}
},
{
"to\_entity\_id": 11271233,
"to\_entity\_type": "contacts",
"metadata": {
"main\_contact": false
}
},
{
"to\_entity\_id": 11271229,
"to\_entity\_type": "companies",
"metadata": null
}
]
}
}
```

### Привязка сущностей

#### Метод

POST /api/v4/leads/{entity\_id}/link

POST /api/v4/contacts/{entity\_id}/link

POST /api/v4/companies/{entity\_id}/link

POST /api/v4/customers/{entity\_id}/link

#### Описание

Метод позволяет прикреплять сущности к основной сущности.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### Заголовок запроса

Content-Type: application/json

#### Параметры запроса

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| to\_entity\_id | int | ID связанной сущности |
| to\_entity\_type | string | Тип связанной сущности (leads, contacts, companies, customers, catalog\_elements) |
| metadata | object/null | Метаданные связанной сущности |
| metadata[catalog\_id] | int | ID каталога |
| metadata[quantity] | int/float | Количество прикрепленных элементов каталогов |
| metadata[is\_main] | bool | Является ли контакт главным |
| metadata[updated\_by] | int | ID пользователя, от имени которого осуществляется прикрепление |
| metadata[price\_id] | int/null | ID поля типа Цена, которое будет установлено для привязанного элемента в сущности |

#### Пример запроса

```json
[
{
"to\_entity\_id": 10,
"to\_entity\_type": "catalog\_elements",
"metadata": {
"quantity": 1,
"catalog\_id": 1026
}
},
{
"to\_entity\_id": 457282,
"to\_entity\_type": "contacts",
"metadata": {
"is\_main": true
}
}
]
```

#### Заголовок типа данных при успешном результате

Content-Type: application/hal+json

#### Заголовок типа данных при ошибке

Content-Type: application/problem+json

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Сущности привязаны успешно |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает коллекцию моделей привязанных сущностей. Параметры аналогичны тем, что возвращаются при запросе списка связей.

#### Пример ответа

```json
{
"\_total\_items": 2,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/14158851/links"
}
},
"\_embedded": {
"links": [
{
"entity\_id": 14158851,
"entity\_type": "leads",
"to\_entity\_id": 10,
"to\_entity\_type": "catalog\_elements",
"metadata": {
"quantity": 1,
"catalog\_id": 1026
}
},
{
"entity\_id": 14158851,
"entity\_type": "leads",
"to\_entity\_id": 457282,
"to\_entity\_type": "contacts",
"metadata": {
"main\_contact": true
}
}
]
}
}
```

### Отвязка сущностей

#### Метод

POST /api/v4/leads/{entity\_id}/unlink

POST /api/v4/contacts/{entity\_id}/unlink

POST /api/v4/companies/{entity\_id}/unlink

POST /api/v4/customers/{entity\_id}/unlink

#### Описание

Метод позволяет открепить сущности у основной сущности.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### Заголовок запроса

Content-Type: application/json

#### Параметры запроса

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| to\_entity\_id | int | ID связанной сущности |
| to\_entity\_type | string | Тип связанной сущности (leads, contacts, companies, customers, catalog\_elements) |
| metadata | object/null | Метаданные связанной сущности |
| metadata[catalog\_id] | int | ID каталога |
| metadata[updated\_by] | int | ID пользователя, от имени которого осуществляется открепление |

#### Пример запроса

```json
[
{
"to\_entity\_id": 10,
"to\_entity\_type": "catalog\_elements",
"metadata": {
"catalog\_id": 1026
}
},
{
"to\_entity\_id": 457282,
"to\_entity\_type": "contacts"
}
]
```

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 204 | Сущности отвязаны успешно |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод не возвращает тело

### Массовый список связанных сущностей

#### Метод

GET /api/v4/leads/links

GET /api/v4/contacts/links

GET /api/v4/companies/links

GET /api/v4/customers/links

#### Описание

Метод позволяет получить связанные сущности по ID-ам основных сущностей.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| filter | object | Фильтр |
| filter[entity\_id] | array | Фильтр по ID главных сущностей, обязательный параметр |
| filter[to\_entity\_id] | int | Фильтр по ID связанной сущности, передается вместе с фильтром filter[to\_entity\_type] |
| filter[to\_entity\_type] | string | Фильтр по типу связанной сущности, передается вместе с фильтром filter[to\_entity\_id] |
| filter[to\_catalog\_id] | int | Фильтр по ID каталога связанной сущности |

#### Заголовок типа данных при успешном результате

Content-Type: application/hal+json

#### Заголовок типа данных при ошибке

Content-Type: application/problem+json

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выполнен успешно |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает коллекцию моделей связей. Рассмотрим ниже свойства моделей

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| entity\_id | int | ID главной сущности |
| entity\_type | string | Тип главной сущности (leads, contacts, companies, customers) |
| to\_entity\_id | int | ID связанной сущности |
| to\_entity\_type | string | Тип связанной сущности (leads, contacts, companies, customers, catalog\_elements) |
| metadata | object/null | Метаданные связанной сущности |
| metadata[main\_contact] | bool | Является ли привязанный контакт главным |
| metadata[quantity] | int/float | Количество прикрепленных элементов каталогов |
| metadata[catalog\_id] | int | ID каталога |
| metadata[price\_id] | int/null | ID поля типа Цена, которое установлено для привязанного элемента в контексте сущности |

#### Пример ответа

```json
{
"\_total\_items": 4,
"\_links": {
"self": {
"href": "https://shard151.amocrm.ru/api/v4/leads/links?filter[entity\_id][]=7593303&filter[entity\_id][]=7593305"
}
},
"\_embedded": {
"links": [
{
"entity\_id": 7593303,
"entity\_type": "leads"
"to\_entity\_id": 597393,
"to\_entity\_type": "catalog\_elements",
"metadata": {
"quantity": 1,
"catalog\_id": 4521
}
},
{
"entity\_id": 7593303,
"entity\_type": "leads"
"to\_entity\_id": 11069775,
"to\_entity\_type": "contacts",
"metadata": {
"main\_contact": true
}
},
{
"entity\_id": 7593305,
"entity\_type": "leads"
"to\_entity\_id": 11271233,
"to\_entity\_type": "contacts",
"metadata": {
"main\_contact": false
}
},
{
"entity\_id": 7593305,
"entity\_type": "leads"
"to\_entity\_id": 11271229,
"to\_entity\_type": "companies",
"metadata": null
}
]
}
}
```

### Массовая привязка сущностей

#### Метод

POST /api/v4/leads/link

POST /api/v4/contacts/link

POST /api/v4/companies/link

POST /api/v4/customers/link

#### Описание

Метод позволяет прикреплять сущности к нескольким сущностям.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### Заголовок запроса

Content-Type: application/json

#### Параметры запроса

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| entity\_id | int | ID главной сущности |
| to\_entity\_id | int | ID связанной сущности |
| to\_entity\_type | string | Тип связанной сущности (leads, contacts, companies, customers, catalog\_elements) |
| metadata | object/null | Метаданные связанной сущности |
| metadata[catalog\_id] | int | ID каталога |
| metadata[quantity] | int/float | Количество прикрепленных элементов каталогов |
| metadata[is\_main] | bool | Является ли контакт главным |
| metadata[updated\_by] | int | ID пользователя, от имени которого осуществляется прикрепление |
| metadata[price\_id] | int/null | ID поля типа Цена, которое будет установлено для привязанного элемента в контексте сущности |

#### Пример запроса

```json
[
{
"entity\_id": 14158851,
"to\_entity\_id": 10,
"to\_entity\_type": "catalog\_elements",
"metadata": {
"quantity": 1,
"catalog\_id": 1026
}
},
{
"entity\_id": 14158852,
"to\_entity\_id": 457282,
"to\_entity\_type": "contacts",
"metadata": {
"is\_main": true
}
}
]
```

#### Заголовок типа данных при успешном результате

Content-Type: application/hal+json

#### Заголовок типа данных при ошибке

Content-Type: application/problem+json

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Сущности привязаны успешно |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает коллекцию моделей привязанных сущностей. Параметры аналогичны тем, что возвращаются при запросе списка связей.

#### Пример ответа

```json
{
"\_total\_items": 2,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/links"
}
},
"\_embedded": {
"links": [
{
"entity\_id": 14158851,
"entity\_type": "leads",
"to\_entity\_id": 10,
"to\_entity\_type": "catalog\_elements",
"metadata": {
"quantity": 1,
"catalog\_id": 1026
}
},
{
"entity\_id": 14158852,
"entity\_type": "leads",
"to\_entity\_id": 457282,
"to\_entity\_type": "contacts",
"metadata": {
"main\_contact": true
}
}
]
}
}
```

### Массовая отвязка сущностей

#### Метод

POST /api/v4/leads/unlink

POST /api/v4/contacts/unlink

POST /api/v4/companies/unlink

POST /api/v4/customers/unlink

#### Описание

Метод позволяет открепить сущности у основных сущностей.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### Заголовок запроса

Content-Type: application/json

#### Параметры запроса

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| entity\_id | int | ID главной сущности |
| to\_entity\_id | int | ID связанной сущности |
| to\_entity\_type | string | Тип связанной сущности (leads, contacts, companies, customers, catalog\_elements) |
| metadata | object/null | Метаданные связанной сущности |
| metadata[catalog\_id] | int | ID каталога |
| metadata[updated\_by] | int | ID пользователя, от имени которого осуществляется открепление |

#### Пример запроса

```json
[
{
"entity\_id": 14158851,
"to\_entity\_id": 10,
"to\_entity\_type": "catalog\_elements",
"metadata": {
"catalog\_id": 1026
}
},
{
"entity\_id": 14158853,
"to\_entity\_id": 457282,
"to\_entity\_type": "contacts"
}
]
```

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 204 | Сущности отвязаны успешно |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод не возвращает тело