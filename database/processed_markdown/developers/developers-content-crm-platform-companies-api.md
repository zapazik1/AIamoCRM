---
title: "Компании"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/crm/platform/companies-api
section: developers
---

В данном разделе описываются доступные методы для работы с сущностью компании

### Оглавление

- [Список компаний](#companies-list)
- [Получение компании по ID](#company-detail)
- [Добавление компаний](#companies-add)
- [Редактирование компаний](#companies-edit)

### Список компаний

#### Метод

*GET /api/v4/companies*

#### Описание

Метод позволяет получить список компаний в аккаунте.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| with | string | Данный параметр принимает строку, в том числе из нескольких значений, указанных через запятую. [Данный метод поддерживает следующие параметры.](#with-1bcd09db-6db3-4625-94b9-0d443e753631-params) |
| page | int | Страница выборки |
| limit | int | Количество возвращаемых сущностей за один запрос (Максимум – 250) |
| query | string int | Поисковый запрос (Осуществляет поиск по заполненным полям сущности) |
| filter | object | Фильтр. Подробней про фильтры читайте в [отдельной статье](/developers/content/crm_platform/filters-api) |
| order | object | Сортировка результатов списка. Доступные поля для сортировки: updated\_at, id. Доступные значения для сортировки: asc, desc. Пример: /api/v4/companies?order[updated\_at]=asc |

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выполнен успешно |
| 401 | Пользователь не авторизован |
| 402 | Аккаунт не оплачен |

#### Параметры ответа

Метод возвращает коллекцию моделей компании, рассмотрим ниже её свойства.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID компании |
| name | string | Название компании |
| responsible\_user\_id | int | ID пользователя, ответственного за компанию |
| group\_id | int | ID группы, в которой состоит ответственны пользователь за компанию |
| created\_by | int | ID пользователя, создавший компанию |
| updated\_by | int | ID пользователя, изменивший компанию |
| created\_at | int | Дата создания компании, передается в Unix Timestamp |
| updated\_at | int | Дата изменения компании, передается в Unix Timestamp |
| closest\_task\_at | int | Дата ближайшей задачи к выполнению, передается в Unix Timestamp |
| custom\_fields\_values | array null | Массив, содержащий информацию по значениям дополнительных полей, заданных для данной компании |
| is\_deleted | bool | Удален ли элемент |
| account\_id | int | ID аккаунта, в котором находится компания |
| \_embedded | object | Данные вложенных сущностей |
| \_embedded[tags] | array | Данные тегов, привязанных к компании |
| \_embedded[tags][0] | object | Модель тега, привязанного к компании |
| \_embedded[tags][0][id] | int | ID тега |
| \_embedded[tags][0][name] | string | Название тега |
| \_embedded[tags][0][color] | null | Цвет тега, доступен только для сделок |
| \_embedded[contacts] | array | **Требуется GET параметр with.** Данные контактов, привязанных к компании. |
| \_embedded[contacts][0] | object | Данные контакта |
| \_embedded[contacts][0][id] | int | ID контакта |
| \_embedded[customers] | array | **Требуется GET параметр with.** Данные покупателей, привязанных к компании |
| \_embedded[customers][0] | object | Данные покупателя |
| \_embedded[customers][0][id] | int | ID покупателя |
| \_embedded[leads] | array | **Требуется GET параметр with.** Данные сделок, привязанных к компании |
| \_embedded[leads][0] | object | Данные сделки |
| \_embedded[leads][0][id] | int | ID сделки |
| \_embedded[catalog\_elements] | array | **Требуется GET параметр with.** Данные элементов списков, привязанных к компании |
| \_embedded[catalog\_elements][0] | object | Данные элемента списка, привязанного к компании |
| \_embedded[catalog\_elements][0][id] | int | ID элемента, привязанного к компании |
| \_embedded[catalog\_elements][0][metadata] | object | Мета-данные элемента |
| \_embedded[catalog\_elements][0][quantity] | int float | Количество элементов у компании |
| \_embedded[catalog\_elements][0][catalog\_id] | int | ID списка, в котором находится элемент |
| \_embedded[catalog\_elements][0][price\_id] | int | ID поля типа Цена, которое установлено для привязанного элемента в сущности |

#### Пример ответа

```json
{
"\_page": 1,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/companies?limit=2&page=1"
},
"next": {
"href": "https://example.amocrm.ru/api/v4/companies?limit=2&page=2"
}
},
"\_embedded": {
"companies": [
{
"id": 7767077,
"name": "Компания Васи",
"responsible\_user\_id": 504141,
"group\_id": 0,
"created\_by": 504141,
"updated\_by": 504141,
"created\_at": 1586359618,
"updated\_at": 1586359618,
"closest\_task\_at": null,
"custom\_fields\_values": null,
"account\_id": 28805383,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/companies/7767077"
}
},
"\_embedded": {
"tags": []
}
},
{
"id": 7767457,
"name": "Example",
"responsible\_user\_id": 504141,
"group\_id": 0,
"created\_by": 504141,
"updated\_by": 504141,
"created\_at": 1586360394,
"updated\_at": 1586360394,
"closest\_task\_at": null,
"custom\_fields\_values": null,
"account\_id": 28805383,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/companies/7767457"
}
},
"\_embedded": {
"tags": []
}
}
]
}
}
```

#### Параметры для GET-параметра with

| Параметр | Описание |
| --- | --- |
| catalog\_elements | Добавляет в ответ связанные с компанией элементы списков |
| leads | Добавляет в ответ связанные с компанией сделки |
| customers | Добавляет в ответ связанных с компанией покупателей |
| contacts | Добавляет в ответ связанные с компанией контакты |

### Получение компании по ID

#### Метод

*GET /api/v4/companies/{id}*

#### Описание

Метод позволяет получить данные конкретной компании по ID.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| with | string | Данный параметр принимает строку, в том числе из нескольких значений, указанных через запятую. [Данный метод поддерживает следующие параметры.](#with-bf1e4aa2-96b3-43e2-bb4d-16b6f6e1cb0d-params) |

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выполнен успешно |
| 204 | Контакт с указанным ID не существует |
| 401 | Пользователь не авторизован |

#### Параметры ответа

Метод возвращает модель компании, рассмотрим ниже её свойства.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID компании |
| name | string | Название компании |
| responsible\_user\_id | int | ID пользователя, ответственного за компанию |
| group\_id | int | ID группы, в которой состоит ответственны пользователь за компанию |
| created\_by | int | ID пользователя, создавший компанию |
| updated\_by | int | ID пользователя, изменивший компанию |
| created\_at | int | Дата создания компании, передается в Unix Timestamp |
| updated\_at | int | Дата изменения компании, передается в Unix Timestamp |
| closest\_task\_at | int | Дата ближайшей задачи к выполнению, передается в Unix Timestamp |
| is\_deleted | bool | Удален ли элемент |
| custom\_fields\_values | array null | Массив, содержащий информацию по значениям дополнительных полей, заданных для данной компании |
| account\_id | int | ID аккаунта, в котором находится компания |
| \_embedded | object | Данные вложенных сущностей |
| \_embedded[tags] | array | Данные тегов, привязанных к компании |
| \_embedded[tags][0] | object | Модель тега, привязанного к компании |
| \_embedded[tags][0][id] | int | ID тега |
| \_embedded[tags][0][name] | string | Название тега |
| \_embedded[tags][0][color] | null | Цвет тега, доступен только для сделок |
| \_embedded[contacts] | array | **Требуется GET параметр with.** Данные контактов, привязанных к компании. |
| \_embedded[contacts][0] | object | Данные контакта |
| \_embedded[contacts][0][id] | int | ID контакта |
| \_embedded[customers] | array | **Требуется GET параметр with.** Данные покупателей, привязанных к компании |
| \_embedded[customers][0] | object | Данные покупателя |
| \_embedded[customers][0][id] | int | ID покупателя |
| \_embedded[leads] | array | **Требуется GET параметр with.** Данные сделок, привязанных к компании |
| \_embedded[leads][0] | object | Данные сделки |
| \_embedded[leads][0][id] | int | ID сделки |
| \_embedded[catalog\_elements] | array | **Требуется GET параметр with.** Данные элементов списков, привязанных к компании |
| \_embedded[catalog\_elements][0] | object | Данные элемента списка, привязанного к компании |
| \_embedded[catalog\_elements][0][id] | int | ID элемента, привязанного к компании |
| \_embedded[catalog\_elements][0][metadata] | object | Мета-данные элемента |
| \_embedded[catalog\_elements][0][quantity] | int float | Количество элементов у компании |
| \_embedded[catalog\_elements][0][catalog\_id] | int | ID списка, в котором находится элемент |
| \_embedded[catalog\_elements][0][price\_id] | int | ID поля типа Цена, которое установлено для привязанного элемента в сущности |

#### Пример ответа

```json
{
"id": 1,
"name": "АО Рога и копыта",
"responsible\_user\_id": 504141,
"group\_id": 0,
"created\_by": 504141,
"updated\_by": 504141,
"created\_at": 1582117331,
"updated\_at": 1586361223,
"closest\_task\_at": null,
"custom\_fields\_values": [
{
"field\_id": 3,
"field\_name": "Телефон",
"field\_code": "PHONE",
"field\_type": "multitext",
"values": [
{
"value": "123213",
"enum\_id": 1,
"enum": "WORK"
}
]
}
],
"account\_id": 28805383,
"\_links": {
"self": {
"href": "https://exmaple.amocrm.ru/api/v4/companies/1"
}
},
"\_embedded": {
"tags": []
}
}
```

#### Параметры для GET-параметра with

| Параметр | Описание |
| --- | --- |
| catalog\_elements | Добавляет в ответ связанные с компанией элементы списков |
| leads | Добавляет в ответ связанные с компанией сделки |
| customers | Добавляет в ответ связанных с компанией покупателей |
| contacts | Добавляет в ответ связанные с компанией контакты |

### Добавление компаний

#### Метод

*POST /api/v4/companies*

#### Описание

Метод позволяет добавлять компании в аккаунт пакетно.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Обязательных полей для добавления нет

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| name | string | Название компании |
| responsible\_user\_id | int | ID пользователя, ответственного за компанию |
| created\_by | int | ID пользователя, создавшего компанию |
| updated\_by | int | ID пользователя, изменившего компанию |
| created\_at | int | Дата создания компании, передается в Unix Timestamp |
| updated\_at | int | Дата изменения компании, передается в Unix Timestamp |
| custom\_fields\_values | array | Массив, содержащий информацию по значениям дополнительных полей, заданных для данной компании. [Примеры заполнения полей](/developers/content/crm_platform/custom-fields#cf-fill-examples) |
| tags\_to\_add | array | Массив тегов для добавления. |
| tags\_to\_add[0] | object | Модель тега для добавления. |
| tags\_to\_add[0][id] | array | ID тега для добавления. Важно передать или id или name. |
| tags\_to\_add[0][name] | array | Название тега для добавления. Важно передать или id или name. |
| \_embedded | object | Данные вложенных сущностей |
| \_embedded[tags] | array | Данные тегов, привязанных к компании |
| \_embedded[tags][0] | object | Модель тега, привязанного к компании |
| \_embedded[tags][0][id] | int | ID тега |
| \_embedded[tags][0][name] | string | Название тега |
| request\_id | string | Поле, которое вернется вам в ответе без изменений и не будет сохранено. Поле не является обязательным |

#### Пример запроса

```json
[
{
"name": "АО Рога и Копыта",
"custom\_fields\_values": [
{
"field\_code": "PHONE",
"values": [
{
"value": "+7912322222",
"enum\_code": "WORK"
}
]
}
]
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
| 200 | Компании были успешно созданы |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает коллекцию компаний, которые были созданы.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID компании |
| request\_id | string | Строка переданная при запросе или порядковый указатель, если параметр не передан |

#### Пример ответа

```json
{
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/companies"
}
},
"\_embedded": {
"companies": [
{
"id": 11090825,
"request\_id": "0",
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/companies/11090825"
}
}
}
]
}
}
```

### Редактирование компаний

#### Метод

*PATCH /api/v4/companies*

#### Описание

Метод позволяет редактировать компании пакетно.  
Также вы можете добавить ID компании в метод для редактирования конкретной компании (/api/v4/companies/{id}).  
При редактировании пакетно передается массив из объектов-компаний, при редактировании одной компании, передается просто модель компании.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Обязательных полей для добавления нет

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| name | string | Название компании |
| responsible\_user\_id | int | ID пользователя, ответственного за контакт |
| created\_by | int | ID пользователя, создавший контакт |
| updated\_by | int | ID пользователя, изменивший контакт |
| created\_at | int | Дата создания контакта, передается в Unix Timestamp |
| updated\_at | int | Дата изменения контакта, передается в Unix Timestamp |
| custom\_fields\_values | array | Массив, содержащий информацию по значениям дополнительных полей, заданных для данной компании. [Примеры заполнения полей](/developers/content/crm_platform/custom-fields#cf-fill-examples) |
| tags\_to\_add | array | Массив тегов для добавления. |
| tags\_to\_add[0] | object | Модель тега для добавления. |
| tags\_to\_add[0][id] | array | ID тега для добавления. Важно передать или id или name. |
| tags\_to\_add[0][name] | array | Название тега для добавления. Важно передать или id или name. |
| tags\_to\_delete | array | Массив тегов для удаления. |
| tags\_to\_delete[0] | object | Модель тега для удаления. |
| tags\_to\_delete[0][id] | array | ID тега для удаления. Важно передать или id или name. |
| tags\_to\_delete[0][name] | array | Название тега для удаления. Важно передать или id или name. |
| \_embedded | object | Данные вложенных сущностей |
| \_embedded[tags] | array | Данные тегов, привязанных к компании |
| \_embedded[tags][0] | object | Модель тега, привязанного к компании |
| \_embedded[tags][0][id] | int | ID тега |
| \_embedded[tags][0][name] | string | Название тега |

#### Пример запроса

```json
[
{
"id": 11090825,
"name": "Новое название компании",
"custom\_fields\_values": [
{
"field\_code": "EMAIL",
"values": [
{
"value": "test@example.com",
"enum\_code": "WORK"
}
]
}
]
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
| 200 | Компании были успешно изменены |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает коллекцию компаний, которые были изменены.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID сделки |
| updated\_at | int | Unix Timestamp изменения сделки |

#### Пример ответа

```json
{
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/companies"
}
},
"\_embedded": {
"companies": [
{
"id": 11090825,
"name": "Новое название компании",
"updated\_at": 1590998669,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/companies/11090825"
}
}
}
]
}
}
```