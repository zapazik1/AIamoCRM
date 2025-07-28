---
title: "Покупатели"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/crm/platform/customers-api
section: developers
---

В данном разделе описываются доступные методы для работы с сущностью покупателя

### Оглавление

- [Включение покупателей и смена их режима](#customers-mode)
- [Список покупателей](#customers-list)
- [Получение покупателя по ID](#customer-detail)
- [Добавление покупателей](#customers-add)
- [Редактирование покупателей](#customers-edit)
- [Список транзакций](#transactions-list)
- [Получение транзакции по ID](#transaction-detail)
- [Добавление транзакций к покупателю](#transactions-add)
- [Удаление транзакции](#transaction-delete)
- [Списание/начисление бонусных баллов покупателю](#customer–bonus-points-update)

### Включение покупателей и смена их режима

#### Метод

*PATCH /api/v4/customers/mode*

#### Описание

Метод позволяет включать/выключать функционал покупателей, а также менять режим функционала.

#### Ограничения

Метод доступен только с правами администратора аккаунта.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Обязательные поля – mode и is\_enabled

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| mode | string | Режим покупателей (segments – сегментация, periodicity – периодичность) |
| is\_enabled | bool | Включен ди функционал покупателей |

#### Пример запроса

```json
{
"mode": "segments",
"is\_enabled": true
}
```

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Режим покупателей успешно изменен |
| 402 | Тариф не позволяет включать покупателей |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает переданные свойства в случае успеха

#### Пример ответа

```json
{
"mode": "segments",
"is\_enabled": true
}
```

### Список покупателей

#### Метод

*GET /api/v4/customers*

#### Описание

Метод позволяет получить список покупателей в аккаунте.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| with | string | Данный параметр принимает строку, в том числе из нескольких значений, указанных через запятую. [Данный метод поддерживает следующие параметры.](#with-d9811dfd-a713-4799-8609-d4f2a895ad18-params) |
| page | int | Страница выборки |
| limit | int | Количество возвращаемых сущностей за один запрос (Максимум – 250) |
| query | string int | Поисковый запрос (Осуществляет поиск по заполненным полям сущности) |
| filter | object | Фильтр. Подробней про фильтры читайте в [отдельной статье](/developers/content/crm_platform/filters-api) |

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

Метод возвращает коллекцию моделей покупателей, рассмотрим ниже свойства модели.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID покупателя |
| name | string | Название покупателя |
| next\_price | int | Ожидаемая сумма покупки |
| next\_date | int | Ожидаемая дата следующей покупки. Данные в Unix Timestamp |
| responsible\_user\_id | int | ID пользователя, ответственного за покупателя |
| status\_id | int | ID статуса покупателя в аккаунте [подробнее здесь](https://www.amocrm.ru/developers/content/crm_platform/customers-statuses-api) |
| periodicity | int | Периодичность (данные необходимы для покупателей, при включенном функционале периодичности) |
| created\_by | int | ID пользователя, создавший покупателя |
| updated\_by | int | ID пользователя, изменивший покупателя |
| created\_at | int | Дата создания покупателя, передается в Unix Timestamp |
| updated\_at | int | Дата изменения покупателя, передается в Unix Timestamp |
| closest\_task\_at | int | Дата ближайшей задачи к выполнению, передается в Unix Timestamp |
| is\_deleted | bool | Удален ли покупатель |
| custom\_fields\_values | array null | Массив, содержащий информацию по значениям дополнительных полей, заданных для данного покупателя |
| ltv | int | Сумма покупок |
| purchases\_count | int | Количество |
| average\_check | int | Средний размер покупки |
| account\_id | int | ID аккаунта, в котором находится покупатель |
| \_embedded | object | Данные вложенных сущностей |
| \_embedded[segments] | array | Сегменты, в котором состоит покупатель |
| \_embedded[segments][0] | object | Модель сегмента |
| \_embedded[segments][0][id] | int | ID сегмента |
| \_embedded[tags] | array | Данные тегов, привязанных к покупателю |
| \_embedded[tags][0] | object | Модель тега, привязанного к покупателю |
| \_embedded[tags][0][id] | int | ID тега |
| \_embedded[tags][0][name] | string | Название тега |
| \_embedded[tags][0][color] | null | Цвет тега, доступен только для сделок |
| \_embedded[contacts] | array | **Требуется GET параметр with.** Данные контактов, привязанных к покупателю |
| \_embedded[contacts][0] | object | Данные контакта, привязанного к покупателю |
| \_embedded[contacts][0][id] | int | ID контакта, привязанного к покупателю |
| \_embedded[contacts][0][is\_main] | bool | Является ли контакт главным для покупателю |
| \_embedded[companies] | array | **Требуется GET параметр with.** Данные компании, привязанной к покупателю, в данном массиве всегда 1 элемент, так как у покупателя может быть только 1 компания |
| \_embedded[companies][0] | object | Данные компании, привязанного к покупателю |
| \_embedded[companies][0][id] | int | ID компании, привязанного к покупателю |
| \_embedded[catalog\_elements] | array | **Требуется GET параметр with.** Данные элементов списков, привязанных к покупателю |
| \_embedded[catalog\_elements][0] | object | Данные элемента списка, привязанного к покупателю |
| \_embedded[catalog\_elements][0][id] | int | ID элемента, привязанного к покупателю |
| \_embedded[catalog\_elements][0][metadata] | object | Мета-данные элемента |
| \_embedded[catalog\_elements][0][quantity] | int float | Количество элементов у покупателю |
| \_embedded[catalog\_elements][0][catalog\_id] | int | ID списка, в котором находится элемент |
| \_embedded[catalog\_elements][0][price\_id] | int | ID поля типа Цена, которое установлено для привязанного элемента в сущности |

#### Пример ответа

```json
{
"\_page": 1,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers?limit=2&with=contacts&page=1"
},
"next": {
"href": "https://example.amocrm.ru/api/v4/customers?limit=2&with=contacts&page=2"
}
},
"\_embedded": {
"customers": [
{
"id": 1,
"name": "1",
"next\_price": 214,
"next\_date": 1589058000,
"responsible\_user\_id": 504141,
"status\_id": 4740028,
"periodicity": 0,
"created\_by": 504141,
"updated\_by": 504141,
"created\_at": 1582117365,
"updated\_at": 1589651187,
"closest\_task\_at": null,
"is\_deleted": false,
"custom\_fields\_values": null,
"ltv": 1231454,
"purchases\_count": 11,
"average\_check": 111950,
"account\_id": 28805383,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/1"
}
},
"\_embedded": {
"segments": [
{
"id": 43,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/segments/43"
}
}
},
{
"id": 45,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/segments/45"
}
}
},
{
"id": 47,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/segments/47"
}
}
},
{
"id": 51,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/segments/51"
}
}
}
],
"tags": [],
"contacts": [
{
"id": 7143559,
"is\_main": false,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/contacts/7143559"
}
}
},
{
"id": 9820781,
"is\_main": true,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/contacts/9820781"
}
}
}
]
}
},
{
"id": 134923,
"name": "12412",
"next\_price": 0,
"next\_date": 1589403600,
"responsible\_user\_id": 504141,
"status\_id": 4740028,
"periodicity": 0,
"created\_by": 504141,
"updated\_by": 504141,
"created\_at": 1590943901,
"updated\_at": 1590943901,
"closest\_task\_at": null,
"is\_deleted": false,
"custom\_fields\_values": null,
"ltv": 0,
"purchases\_count": 0,
"average\_check": 0,
"account\_id": 28805383,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/134923"
}
},
"\_embedded": {
"segments": [],
"tags": [],
"contacts": [
{
"id": 3,
"is\_main": true,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/contacts/3"
}
}
}
]
}
}
]
}
}
```

#### Параметры для GET-параметра with

| Параметр | Описание |
| --- | --- |
| catalog\_elements | Добавляет в ответ связанные со покупателем элементы списков |
| contacts | Добавляет в ответ информацию о связанных с покупателем контактах |
| companies | Добавляет в ответ информацию о связанных с покупателем компаниях |

### Получение покупателя по ID

#### Метод

*GET /api/v4/customers/{id}*

#### Описание

Метод позволяет получить данные конкретного покупателя по ID.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| with | string | Данный параметр принимает строку, в том числе из нескольких значений, указанных через запятую. [Данный метод поддерживает следующие параметры.](#with-f2c232df-7b7c-48c9-9055-c4e05c5d1409-params) |

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выполнен успешно |
| 204 | Покупатель с указанным ID не существует |
| 401 | Пользователь не авторизован |

#### Параметры ответа

Метод возвращает модель покупателя, рассмотрим ниже её свойства.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID покупателя |
| name | string | Название покупателя |
| next\_price | int | Ожидаемая сумма покупки |
| next\_date | int | Ожидаемая дата следующей покупки. Данные в Unix Timestamp |
| responsible\_user\_id | int | ID пользователя, ответственного за покупателя |
| status\_id | int | ID статуса покупателя в аккаунте [подробнее здесь](https://www.amocrm.ru/developers/content/crm_platform/customers-statuses-api) |
| periodicity | int | Периодичность (данные необходимы для покупателей, при включенном функционале периодичности) |
| created\_by | int | ID пользователя, создавший покупателя |
| updated\_by | int | ID пользователя, изменивший покупателя |
| created\_at | int | Дата создания покупателя, передается в Unix Timestamp |
| updated\_at | int | Дата изменения покупателя, передается в Unix Timestamp |
| closest\_task\_at | int | Дата ближайшей задачи к выполнению, передается в Unix Timestamp |
| is\_deleted | bool | Удален ли покупатель |
| custom\_fields\_values | array null | Массив, содержащий информацию по значениям дополнительных полей, заданных для данного покупателя |
| ltv | int | Сумма покупок |
| purchases\_count | int | Количество |
| average\_check | int | Средний размер покупки |
| account\_id | int | ID аккаунта, в котором находится покупатель |
| \_embedded | object | Данные вложенных сущностей |
| \_embedded[segments] | array | Сегменты, в котором состоит покупатель |
| \_embedded[segments][0] | object | Модель сегмента |
| \_embedded[segments][0][id] | int | ID сегмента |
| \_embedded[tags] | array | Данные тегов, привязанных к покупателю |
| \_embedded[tags][0] | object | Модель тега, привязанного к покупателю |
| \_embedded[tags][0][id] | int | ID тега |
| \_embedded[tags][0][name] | string | Название тега |
| \_embedded[tags][0][color] | null | Цвет тега, доступен только для сделок |
| \_embedded[contacts] | array | **Требуется GET параметр with.** Данные контактов, привязанных к покупателю |
| \_embedded[contacts][0] | object | Данные контакта, привязанного к покупателю |
| \_embedded[contacts][0][id] | int | ID контакта, привязанного к покупателю |
| \_embedded[contacts][0][is\_main] | bool | Является ли контакт главным для покупателю |
| \_embedded[companies] | array | **Требуется GET параметр with.** Данные компании, привязанной к покупателю, в данном массиве всегда 1 элемент, так как у покупателя может быть только 1 компания |
| \_embedded[companies][0] | object | Данные компании, привязанного к покупателю |
| \_embedded[companies][0][id] | int | ID компании, привязанного к покупателю |
| \_embedded[catalog\_elements] | array | **Требуется GET параметр with.** Данные элементов списков, привязанных к покупателю |
| \_embedded[catalog\_elements][0] | object | Данные элемента списка, привязанного к покупателю |
| \_embedded[catalog\_elements][0][id] | int | ID элемента, привязанного к покупателю |
| \_embedded[catalog\_elements][0][metadata] | object | Мета-данные элемента |
| \_embedded[catalog\_elements][0][quantity] | int float | Количество элементов у покупателю |
| \_embedded[catalog\_elements][0][catalog\_id] | int | ID списка, в котором находится элемент |
| \_embedded[catalog\_elements][0][price\_id] | int | ID поля типа Цена, которое установлено для привязанного элемента в контексте сущности |

#### Пример ответа

```json
{
"id": 1,
"name": "покупатель",
"next\_price": 214,
"next\_date": 1589058000,
"responsible\_user\_id": 504141,
"status\_id": 4740028,
"periodicity": 0,
"created\_by": 504141,
"updated\_by": 504141,
"created\_at": 1582117365,
"updated\_at": 1589651187,
"closest\_task\_at": null,
"is\_deleted": false,
"custom\_fields\_values": null,
"ltv": 1231454,
"purchases\_count": 11,
"average\_check": 111950,
"account\_id": 28805383,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/1"
}
},
"\_embedded": {
"segments": [
{
"id": 43,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/segments/43"
}
}
},
{
"id": 45,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/segments/45"
}
}
},
{
"id": 47,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/segments/47"
}
}
},
{
"id": 51,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/segments/51"
}
}
}
],
"tags": []
}
}
```

#### Параметры для GET-параметра with

| Параметр | Описание |
| --- | --- |
| catalog\_elements | Добавляет в ответ связанные со покупателем элементы списков |
| contacts | Добавляет в ответ информацию о связанных с покупателем контактах |
| companies | Добавляет в ответ информацию о связанных с покупателем компаниях |

### Добавление покупателей

#### Метод

*POST /api/v4/customers*

#### Описание

Метод позволяет добавлять покупателей в аккаунт пакетно.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Обязательные поля – name и next\_date, если включен режим периодичности

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| name | string | Название покупателя |
| next\_price | int | Ожидаемая сумма покупки |
| next\_date | int | Ожидаемая дата следующей покупки. Данные в Unix Timestamp |
| responsible\_user\_id | int | ID пользователя, ответственного за покупателя |
| status\_id | int | ID статуса покупателя в аккаунте [подробнее здесь](https://www.amocrm.ru/developers/content/crm_platform/customers-statuses-api) |
| periodicity | int | Периодичность (данные необходимы для покупателей, при включенном функционале периодичности) |
| created\_by | int | ID пользователя, создавший покупателя |
| updated\_by | int | ID пользователя, изменивший покупателя |
| created\_at | int | Дата создания покупателя, передается в Unix Timestamp |
| updated\_at | int | Дата изменения покупателя, передается в Unix Timestamp |
| custom\_fields\_values | array null | Массив, содержащий информацию по значениям дополнительных полей, заданных для данного покупателя. [Примеры заполнения полей](/developers/content/crm_platform/custom-fields#cf-fill-examples) |
| tags\_to\_add | array | Массив тегов для добавления. |
| tags\_to\_add[0] | object | Модель тега для добавления. |
| tags\_to\_add[0][id] | array | ID тега для добавления. Важно передать или id или name. |
| tags\_to\_add[0][name] | array | Название тега для добавления. Важно передать или id или name. |
| \_embedded | object | Данные вложенных сущностей |
| \_embedded[tags] | array | Данные тегов, привязанных к покупателю |
| \_embedded[tags][0] | object | Модель тега, привязанного к покупателю |
| \_embedded[tags][0][id] | int | ID тега |
| \_embedded[tags][0][name] | string | Название тега |
| request\_id | string | Поле, которое вернется вам в ответе без изменений и не будет сохранено. Поле не является обязательным |

#### Пример запроса

В данном примере мы создадим 2 покупателя.  
Для первого мы зададим название, создателя – робота, тег, а также значение текстового поля.  
Для второго мы зададим название, добавим тег и добавим в сегмент.

```json
[
{
"name": "Покупатель для примера 1",
"created\_by": 0,
"custom\_fields\_values": [
{
"field\_id": 294479,
"values": [
{
"value": "Наш первый покупатель"
}
]
}
],
"tags\_to\_add": [
{
"id": 107721
}
]
},
{
"name": "Покупатель для примера 2",
"\_embedded": {
"tags": [
{
"name": "Важный покупатель"
}
],
"segments": [
{
"id": 81
}
]
}
}
]
```

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Покупатели были успешно созданы |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает коллекцию покупателей, которые были созданы.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID покупателя |
| request\_id | string | Строка переданная при запросе или порядковый указатель, если параметр не передан |

#### Пример ответа

```json
{
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers"
}
},
"\_embedded": {
"customers": [
{
"id": 134957,
"request\_id": "0"
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/134957"
}
}
},
{
"id": 134959,
"request\_id": "1",
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/134959"
}
}
}
]
}
}
```

### Редактирование покупателей

#### Метод

*PATCH /api/v4/customers*

#### Описание

Метод позволяет редактировать покупателей пакетно.  
Также вы можете добавить ID покупателя в метод для редактирования конкретного покупателя (/api/v4/customers/{id}).  
При редактировании пакетно передается массив из объектов-покупателей, при редактировании одного покупателя, передается просто модель.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Обязательных полей нет

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| name | string | Название покупателя |
| next\_price | int | Ожидаемая сумма покупки |
| next\_date | int | Ожидаемая дата следующей покупки. Данные в Unix Timestamp |
| responsible\_user\_id | int | ID пользователя, ответственного за покупателя |
| status\_id | int | ID статуса покупателя в аккаунте [подробнее здесь](https://www.amocrm.ru/developers/content/crm_platform/customers-statuses-api) |
| periodicity | int | Периодичность (данные необходимы для покупателей, при включенном функционале периодичности) |
| created\_by | int | ID пользователя, создавший покупателя |
| updated\_by | int | ID пользователя, изменивший покупателя |
| created\_at | int | Дата создания покупателя, передается в Unix Timestamp |
| updated\_at | int | Дата изменения покупателя, передается в Unix Timestamp |
| custom\_fields\_values | array null | Массив, содержащий информацию по значениям дополнительных полей, заданных для данного покупателя. [Примеры заполнения полей](/developers/content/crm_platform/custom-fields#cf-fill-examples) |
| tags\_to\_add | array | Массив тегов для добавления. |
| tags\_to\_add[0] | object | Модель тега для добавления. |
| tags\_to\_add[0][id] | array | ID тега для добавления. Важно передать или id или name. |
| tags\_to\_add[0][name] | array | Название тега для добавления. Важно передать или id или name. |
| tags\_to\_delete | array | Массив тегов для удаления. |
| tags\_to\_delete[0] | object | Модель тега для удаления. |
| tags\_to\_delete[0][id] | array | ID тега для удаления. Важно передать или id или name. |
| tags\_to\_delete[0][name] | array | Название тега для удаления. Важно передать или id или name. |
| \_embedded | object | Данные вложенных сущностей |
| \_embedded[tags] | array | Данные тегов, привязанных к покупателю |
| \_embedded[tags][0] | object | Модель тега, привязанного к покупателю |
| \_embedded[tags][0][id] | int | ID тега |
| \_embedded[tags][0][name] | string | Название тега |
| request\_id | string | Поле, которое вернется вам в ответе без изменений и не будет сохранено. Поле не является обязательным |

#### Пример запроса

```json
[
{
"id": 1299433,
"name": "Новое название покупателя",
"\_embedded": {
"tags": [
{
"name": "Тег 125"
}
]
}
}
]
```

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Покупатели были успешно изменены |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает коллекцию покупателей, которые были изменены.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID покупателя |
| updated\_at | int | Unix Timestamp изменения покупателя |
| request\_id | string | Строка переданная при запросе или порядковый указатель, если параметр не передан |

#### Пример ответа

```json
{
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers"
}
},
"\_embedded": {
"leads": [
{
"id": 1299433,
"updated\_at": 1589556420,
"request\_id": "0",
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/1299433"
}
}
}
]
}
}
```

### Список транзакций

#### Метод

*GET /api/v4/customers/transactions*

#### Описание

Метод позволяет получить список транзакций в аккаунте.  
Также вы можете получить транзакции конкретного покупателя обратившись к методу /api/v4/customers/{customer\_id}/transactions.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| page | int | Страница выборки |
| limit | int | Количество возвращаемых сущностей за один запрос (Максимум – 250) |
| filter | object | Фильтр |
| filter[id] | int array | Фильтр по ID транзакций |

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

Метод возвращает коллекцию моделей транзакций, рассмотрим ниже свойства модели.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID транзакции |
| comment | string | Комментарий к покупке |
| price | int | Сумма покупки |
| completed\_at | int | Когда транзакция была проведена. Данные в Unix Timestamp |
| customer\_id | int | ID покупателя, в котором находится транзакция |
| created\_by | int | ID пользователя, создавший транзакцию |
| updated\_by | int | ID пользователя, изменивший транзакцию |
| created\_at | int | Дата создания транзакции, передается в Unix Timestamp |
| updated\_at | int | Дата изменения транзакции, передается в Unix Timestamp |
| is\_deleted | bool | Удалена ли транзакция |
| account\_id | int | ID аккаунта, в котором находится транзакция |
| \_embedded | object | Данные вложенных сущностей |
| \_embedded[customer] | object | Покупатель, в котором находится транзакция |
| \_embedded[customer][id] | int | ID покупателя |
| \_embedded[catalog\_elements] | array | Данные элементов списков, привязанных к транзакции |
| \_embedded[catalog\_elements][0] | object | Данные элемента списка, привязанного к транзакции |
| \_embedded[catalog\_elements][0][id] | int | ID элемента, привязанного к транзакции |
| \_embedded[catalog\_elements][0][metadata] | object | Мета-данные элемента |
| \_embedded[catalog\_elements][0][quantity] | int | Количество элементов у транзакции |
| \_embedded[catalog\_elements][0][catalog\_id] | int | ID списка, в котором находится элемент |

#### Пример ответа

```json
{
"\_page": 1,
"\_links": {
"self": {
"href": "http://example.amocrm.ru/api/v4/customers/transactions?filter%5Bid%5D%5B0%5D=134643&page=1&limit=50"
},
"next": {
"href": "http://example.amocrm.ru/api/v4/customers/transactions?filter%5Bid%5D%5B0%5D=134643&page=2&limit=50"
}
},
"\_embedded": {
"transactions": [
{
"id": 134643,
"price": 123,
"comment": null,
"completed\_at": 1591005900,
"customer\_id": 1000000158,
"created\_by": 939801,
"updated\_by": 939801,
"created\_at": 1591005900,
"updated\_at": 1591005900,
"is\_deleted": false,
"account\_id": 17079858,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/1000000158/transactions/134643"
}
},
"\_embedded": {
"customer": {
"id": 1000000158,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/1000000158"
}
}
},
"catalog\_elements": [
{
"id": 1677,
"metadata": {
"catalog\_id": 1079,
"quantity": 10
}
}
]
}
}
]
}
}
```

### Получение транзакции по ID

#### Метод

*GET /api/v4/customers/transactions/{id}*

#### Описание

Метод позволяет получить транзакцию в аккаунте.  
Также вы можете получить транзакцию конкретного покупателя обратившись к методу /api/v4/customers/{customer\_id}/transactions/{id}.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

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

Метод возвращает модель транзакций, рассмотрим ниже свойства модели.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID транзакции |
| comment | string | Комментарий к покупке |
| price | int | Сумма покупки |
| completed\_at | int | Когда транзакция была проведена. Данные в Unix Timestamp |
| customer\_id | int | ID покупателя, в котором находится транзакция |
| created\_by | int | ID пользователя, создавший транзакцию |
| updated\_by | int | ID пользователя, изменивший транзакцию |
| created\_at | int | Дата создания транзакции, передается в Unix Timestamp |
| updated\_at | int | Дата изменения транзакции, передается в Unix Timestamp |
| is\_deleted | bool | Удалена ли транзакция |
| account\_id | int | ID аккаунта, в котором находится транзакция |
| \_embedded | object | Данные вложенных сущностей |
| \_embedded[customer] | object | Покупатель, в котором находится транзакция |
| \_embedded[customer][id] | int | ID покупателя |
| \_embedded[catalog\_elements] | array | Данные элементов списков, привязанных к транзакции |
| \_embedded[catalog\_elements][0] | object | Данные элемента списка, привязанного к транзакции |
| \_embedded[catalog\_elements][0][id] | int | ID элемента, привязанного к транзакции |
| \_embedded[catalog\_elements][0][metadata] | object | Мета-данные элемента |
| \_embedded[catalog\_elements][0][quantity] | int | Количество элементов у транзакции |
| \_embedded[catalog\_elements][0][catalog\_id] | int | ID списка, в котором находится элемент |

#### Пример ответа

```json
{
"id": 14755,
"price": 123124,
"comment": "Транзакция",
"completed\_at": 1589025179,
"customer\_id": 1,
"created\_by": 504141,
"updated\_by": 504141,
"created\_at": 1589025179,
"updated\_at": 1589025179,
"is\_deleted": false,
"account\_id": 28805383,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/1/transactions/14755"
}
},
"\_embedded": {
"customer": {
"id": 1,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/1"
}
}
}
}
}
```

### Добавление транзакций к покупателю

#### Метод

*POST /api/v4/customers/{customer\_id}/transactions*

#### Описание

Метод позволяет добавлять транзакции к конкретному покупателю в аккаунт пакетно.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Обязательное поле – price

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| comment | string | Комментарий к покупке |
| price | int | Сумма покупки |
| completed\_at | int | Когда транзакция была проведена. Данные в Unix Timestamp |
| next\_price | int | Ожидаемая сумма следующей покупки у покупателя |
| next\_date | int | Ожидаемая дата следующей покупки у покупателя. Данные в Unix Timestamp |
| created\_by | int | ID пользователя, создавший транзакцию |
| \_embedded[catalog\_elements] | array | Данные элементов списков, привязанных к транзакции |
| \_embedded[catalog\_elements][0] | object | Данные элемента списка, привязанного к транзакции |
| \_embedded[catalog\_elements][0][id] | int | ID элемента, привязанного к транзакции |
| \_embedded[catalog\_elements][0][metadata] | object | Мета-данные элемента |
| \_embedded[catalog\_elements][0][quantity] | int | Количество элементов у транзакции |
| \_embedded[catalog\_elements][0][catalog\_id] | int | ID списка, в котором находится элемент |
| request\_id | string | Поле, которое вернется вам в ответе без изменений и не будет сохранено. Поле не является обязательным |

#### Пример запроса

```json
[
{
"price":123,
"created\_by":0,
"comment":"Комментарий",
"\_embedded":{
"catalog\_elements":[
{
"id":1677,
"metadata":{
"catalog\_id":1079,
"quantity":10
}
}
]
}
}
]
```

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Транзакции были успешно созданы |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает коллекцию транзакций, которые были созданы.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID транзакции |
| customer\_id | int | ID покупател |
| request\_id | string | Строка переданная при запросе или порядковый указатель, если параметр не передан |

#### Пример ответа

```json
{
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers"
}
},
"\_embedded": {
"customers": [
{
"id": 134957,
"request\_id": "0",
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/134957"
}
}
},
{
"id": 134959,
"request\_id": "1",
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/customers/134959"
}
}
}
]
}
}
```

### Удаление транзакции

#### Метод

*DELETE /api/v4/customers/transactions/{id}*

#### Описание

Метод позволяет удалить транзакцию в аккаунте.  
Также вы можете получить удалить транзакцию конкретного покупателя обратившись к методу /api/v4/customers/{customer\_id}/transactions/{id}.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### Заголовок запроса

*Content-Type: application/json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 204 | Транзакция была успешно удалена |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод не возвращает тело

### Списание/начисление бонусных баллов покупателю

#### Метод

*POST /api/v4/customers/{id}/bonus\_points*

#### Описание

Метод позволяет списывать/начислять бонусные баллы покупателю по ID. Взаимодействует с системой [карт лояльности amoCRM](https://www.amocrm.ru/support/customers/loyalty_card).

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Если покупателю нужно списать баллы обязательное поле redeem, если начислить, то earn. Оба поля передавать запрещено

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| redeem | int | Указывает сколько бонусных баллов нужно списать |
| earn | int | Указывает сколько бонусных баллов нужно начислить |

#### Пример запроса

В данном примере мы начислим покупателю 500 бонусных баллов.

```json
{
"earn": 500
}
```

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Бонусные баллы успешно начислены/списаны |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает обновленное значение бонусных баллов покупателя

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| bonus\_points | int | Количество бонусных баллов покупателя после запроса |

#### Пример ответа

```json
{
"bonus\_points": 534
}
```