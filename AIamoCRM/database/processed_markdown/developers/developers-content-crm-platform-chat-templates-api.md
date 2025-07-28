---
title: "Шаблоны ответов в чаты"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/crm/platform/chat-templates-api
section: developers
---

В данном разделе описываются доступные методы для работы с шаблонами ответов в чаты.

Шаблоны ответов в чаты могут быть использованы в карточке, а также в боте. Контент шаблона может содержать в себе маркеры.  
[Подробнее о доступных маркерах.](https://www.amocrm.ru/developers/content/digital_pipeline/salesbot#salesbot-markers)

Также шаблон может содержать в себе информацию о кнопках, которые будут отправлены вместе с ним.

Загрузка файлов в шаблоны, в данный момент не доступна.

**Важным ограничение данного API является то, что методы работают только с теми шаблонами, которые были созданы текущей интеграцией**

### Оглавление

- [Список шаблонов](#Список-шаблонов)
- [Получение шаблона по ID](#Получение-шаблона-по-ID)
- [Добавление шаблона](#Добавление-шаблона)
- [Редактирование шаблонов](#Редактирование-шаблонов)
- [Отправка шаблона WhatsApp на модерацию](#Отправка-шаблона-WhatsApp-на-модерацию)
- [Редактирование статуса шаблона WhatsApp](#Редактирование-статуса-шаблона-WhatsApp)
- [Удаление шаблонов](#Удаление-шаблонов)

### Список шаблонов

#### Метод

*GET /api/v4/chats/templates*

#### Описание

Метод позволяет получить список шаблонов в аккаунте.

#### Ограничения

- Метод возвращает только те шаблоны, которые были созданы текущей интеграцией
- Метод доступен в соответствии только администратору аккаунта

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| page | int | Страница выборки |
| limit | int | Количество возвращаемых сущностей за один запрос (Максимум – 50) |
| filter[external\_id] | string или array | Фильтр по внешнему идентификатору. Можно передать 1 строкой, или массив из нескольких идентификаторов |
| with | string | Данный параметр принимает строку. Данный метод поддерживает только параметр reviews |

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выполнен успешно |
| 204 | Шаблоны не найдены |
| 401 | Пользователь не авторизован |

#### Параметры ответа

Метод возвращает коллекцию моделей шаблонов, рассмотрим ниже свойства модели.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID шаблона |
| account\_id | int | ID аккаунта, которому принадлежит шаблон |
| name | string | Название шаблона |
| content | string | Тело шаблона, сообщение, которое отправляется пользователю |
| is\_editable | bool | Может ли пользователь редактировать шаблон в интерфейсе amoCRM |
| type | string | Тип шаблона. Возможны 2 варианта: amocrm и waba |
| buttons | array | Массив объектов кнопок |
| buttons[][type] | string | Тип кнопки, доступные варианты: `inline` (обычная текстовая кнопка), `url` (кнопка ссылка) |
| buttons[][text] | string | Текст, отображаемый в кнопке |
| buttons[][url] | string | Ссылка кнопки, доступно только для кнопки типа `url` |
| attachment | object|null | Объект добавленного файла в шаблон |
| attachment[id] | string | UUID файла, прикрепленного к шаблону |
| attachment[name] | string | Название файла, прикрепленного к шаблону, которое будет передано в мессенджер |
| attachment[type] | string | Тип прикрепленного файла. Возможные типы – picture, file, document, video |
| attachment[is\_external] | bool | Показатель, что файл из сервиса файлов. Для всех шаблонов добавляемых с весны 2022 – true |
| created\_at | int | Timestamp создания шаблона |
| updated\_at | int | Timestamp последнего изменения шаблона |
| external\_id | string | Внешний идентификатор шаблона. ID шаблона в вашей системе |
| review\_status | string|null | Статус шаблона WhatsApp: approved review paused rejected. Требуется GET параметр with |
| is\_on\_review | null|bool | Находится ли шаблон на проверке. Требуется GET параметр with |
| waba\_footer | string | Футер шаблона WhatsApp |
| waba\_category | string | Категоря шаблона WhatsApp. Доступны следующие категории: UTILITY AUTHENTICATION MARKETING |
| waba\_language | string | Язык шаблона WhatsApp |
| waba\_examples | object | Примеры замены маркеров шаблона WhatsApp. Пример "waba\_examples":{"{{lead.name}}":"qwerty"} |
| waba\_header | string|null | Хедер шаблона WhatsApp с лимитом до 60 символов. Необязательный параметр |
| waba\_header\_type | string | Тип хедера шаблона WhatsApp. Доступные варианты: `text` (WhatsApp шаблон с хедером), `media` (WhatsApp шаблон с медиа хедером, должно быть вложение под ключом attachment). Необязательный параметр |
| \_embedded | object | Объект содержащий информацию прилегающую к запросу |
| \_embedded.reviews | array | Массив статусов шаблона WhatsApp. Требуется GET параметр with |
| reviews[][id] | int | id статуса шаблона WhatsApp. Требуется GET параметр with |
| reviews[][source\_id] | int | id источника статуса шаблона WhatsApp. Требуется GET параметр with |
| reviews[][reject\_reason] | string | Причина отказа в одобрении шаблона WhatsApp. Требуется GET параметр with |
| reviews[][status] | string | Статус шаблона WhatsApp. Требуется GET параметр with |

#### Пример ответа

```json
{
"\_page": 1,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/chats/templates?page=1&limit=50"
},
"next": {
"href": "https://example.amocrm.ru/api/v4/chats/templates?page=2&limit=50"
}
},
"\_embedded": {
"chat\_templates": [
{
"id": 7349,
"account\_id": 29420107,
"name": "Test template",
"content": "New content. Contact name - {{contact.name}}",
"created\_at": 1640360627,
"updated\_at": 1640360627,
"buttons": [
{
"text": "кнопка 1",
"type": "inline"
},
{
"text": "кнопка 2",
"type": "inline"
}
],
"attachment": null,
"is\_editable": false,
"external\_id": "my\_external\_id",
"type": "waba",
"waba\_footer": "my footer",
"waba\_category": "UTILITY",
"waba\_language": "en",
"waba\_examples": {
"{{contact.name}}": "My contact"
},
"waba\_header": "Header example",
"waba\_header\_type": "text",
"review\_status": "review",
"is\_on\_review": true,
"\_embedded": {
"reviews": [
{
"id": 367,
"source\_id": 13234480,
"status": "review",
"reject\_reason": ""
}
]
},
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/chats/templates/7349"
}
}
}
]
}
}
```

### Получение шаблона по ID

#### Метод

*GET /api/v4/chats/templates/{id}*

#### Описание

Метод позволяет получить данные конкретного шаблона по ID.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| with | string | Данный параметр принимает строку. Данный метод поддерживает только параметр reviews |

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выполнен успешно |
| 404 | Шаблон с указанным ID не существует |
| 401 | Пользователь не авторизован |

#### Параметры ответа

Метод возвращает модель шаблона, рассмотрим ниже её свойства.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID шаблона |
| account\_id | int | ID аккаунта, которому принадлежит шаблон |
| name | string | Название шаблона |
| content | string | Тело шаблона, сообщение, которое отправляется пользователю |
| is\_editable | bool | Может ли пользователь редактировать шаблон в интерфейсе amoCRM |
| type | string | Тип шаблона. Возможны 2 варианта: amocrm и waba |
| buttons | array | Массив объектов кнопок |
| buttons[][type] | string | Тип кнопки, доступные варианты: `inline` (обычная текстовая кнопка), `url` (кнопка ссылка) |
| buttons[][text] | string | Текст, отображаемый в кнопке |
| buttons[][url] | string | Ссылка кнопки, доступно только для кнопки типа `url` |
| attachment | object|null | Объект добавленного файла в шаблон |
| attachment[id] | string | UUID файла, прикрепленного к шаблону |
| attachment[name] | string | Название файла, прикрепленного к шаблону, которое будет передано в мессенджер |
| attachment[type] | string | Тип прикрепленного файла. Возможные типы – picture, file, document, video |
| attachment[is\_external] | bool | Показатель, что файл из сервиса файлов. Для всех шаблонов добавляемых с весны 2022 – true |
| created\_at | int | Timestamp создания шаблона |
| updated\_at | int | Timestamp последнего изменения шаблона |
| external\_id | string | Внешний идентификатор шаблона. ID шаблона в вашей системе |
| review\_status | string|null | Статус шаблона WhatsApp: approved review paused rejected. Требуется GET параметр with |
| is\_on\_review | null|bool | Находится ли шаблон на проверке. Требуется GET параметр with |
| waba\_footer | string | Футер шаблона WhatsApp |
| waba\_category | string | Категоря шаблона WhatsApp. Доступны следующие категории: UTILITY AUTHENTICATION MARKETING |
| waba\_language | string | Язык шаблона WhatsApp |
| waba\_examples | object | Примеры замены маркеров шаблона WhatsApp. Пример "waba\_examples":{"{{lead.name}}":"qwerty"} |
| waba\_header | string|null | Хедер шаблона WhatsApp с лимитом до 60 символов. Необязательный параметр |
| waba\_header\_type | string | Тип хедера шаблона WhatsApp. Доступные варианты: `text` (WhatsApp шаблон с хедером), `media` (WhatsApp шаблон с медиа хедером, должно быть вложение под ключом attachment). Необязательный параметр |
| \_embedded | object | Объект содержащий информацию прилегающую к запросу |
| \_embedded.reviews | array | Массив статусов шаблона WhatsApp. Требуется GET параметр with |
| reviews[][id] | int | id статуса шаблона WhatsApp. Требуется GET параметр with |
| reviews[][source\_id] | int | id источника статуса шаблона WhatsApp. Требуется GET параметр with |
| reviews[][reject\_reason] | string | Причина отказа в одобрении шаблона WhatsApp. Требуется GET параметр with |
| reviews[][status] | string | Статус шаблона WhatsApp. Требуется GET параметр with |

#### Пример ответа

```json
{
"id": 7349,
"account\_id": 29420107,
"name": "Test template",
"content": "New content. Contact name - {{contact.name}}",
"created\_at": 1640360627,
"updated\_at": 1640360627,
"buttons": [
{
"text": "кнопка 1",
"type": "inline"
},
{
"text": "кнопка 2",
"type": "inline"
}
],
"attachment": {
"id": "5ee9417d-afb8-46eb-9388-0490c75d5ea1",
"name": "Название файла",
"type": "picture",
"is\_external": true
},
"is\_editable": false,
"external\_id": "my\_external\_id",
"type": "waba",
"waba\_footer": "my footer",
"waba\_category": "UTILITY",
"waba\_language": "en",
"waba\_examples": {
"{{contact.name}}": "My contact"
},
"waba\_header": null,
"waba\_header\_type": "media",
"review\_status": "approved",
"is\_on\_review": false,
"\_embedded": {
"reviews": [
{
"id": 367,
"source\_id": 13234480,
"status": "approved",
"reject\_reason": ""
}
]
},
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/chats/templates/7349"
}
}
}
```

### Добавление шаблона

#### Метод

*POST /api/v4/chats/templates*

#### Описание

Метод позволяет добавлять шаблоны в аккаунт пакетно.

#### Ограничения

Метод доступен только администратору.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Обязательные поля – name, content

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| name | string | Название шаблона |
| content | string | Тело шаблона, сообщение, которое отправляется пользователю. Можно использовать маркеры Salesbot. |
| is\_editable | bool | Может ли пользователь редактировать шаблон в интерфейсе amoCRM. По умолчанию – false |
| type | string | Тип шаблона. Возможны 2 варианта: amocrm и waba |
| buttons | array | Массив объектов кнопок |
| buttons[][type] | string | Тип кнопки, доступные варианты: `inline` (обычная текстовая кнопка), `url` (кнопка ссылка) |
| buttons[][text] | string | Текст, отображаемый в кнопке |
| buttons[][url] | string | Ссылка кнопки, доступно только для кнопки типа `url` |
| attachment | object|null | Объект добавленного файла в шаблон |
| attachment[id] | string | UUID файла из API файлов, прикрепленного к шаблону |
| attachment[name] | string | Название файла, прикрепленного к шаблону, которое будет передано в мессенджер |
| attachment[type] | string | Тип прикрепленного файла. Возможные типы – picture, file, document, video |
| external\_id | string | Внешний идентификатор шаблона. ID шаблона в вашей системе |
| request\_id | string | Поле, которое вернется вам в ответе без изменений и не будет сохранено. Необязательный параметр |
| waba\_footer | string | Футер шаблона WhatsApp |
| waba\_category | string | Категоря шаблона WhatsApp. Доступны следующие категории: UTILITY AUTHENTICATION MARKETING |
| waba\_language | string | Язык шаблона WhatsApp |
| waba\_examples | object | Примеры замены маркеров шаблона WhatsApp. Пример "waba\_examples":{"{{lead.name}}":"qwerty"} |
| waba\_header | string|null | Хедер шаблона WhatsApp с лимитом до 60 символов. Необязательный параметр |
| waba\_header\_type | string | Тип хедера шаблона WhatsApp. Доступные варианты: `text` (WhatsApp шаблон с хедером), `media` (WhatsApp шаблон с медиа хедером, должно быть вложение под ключом attachment). Необязательный параметр |

#### Пример запроса

```json
[
{
"name": "Hello template",
"content": "Hello {{contact.name}}",
"external\_id": "my\_external\_id\_for\_hello",
"buttons": [
{
"type": "inline",
"text": "button 1"
},
{
"type": "inline",
"text": "button 2"
}
],
"attachment": {
"id": "c2b77f70-d0d6-484a-8f6e-583f70a08cce",
"name": "Название изображения",
"type": "picture"
},
"type": "waba",
"waba\_footer": "my footer",
"waba\_category": "UTILITY",
"waba\_language": "en",
"waba\_examples": {
"{{contact.name}}": "My contact"
},
"waba\_header": null,
"waba\_header\_type": "media"
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
| 200 | Шаблоны были успешно созданы |
| 422 | Запрос не может быть обработан, превышен лимит шаблонов |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает коллекцию шаблонов, которые были созданы.

Метод возвращает модель шаблона, рассмотрим ниже её свойства.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID шаблона |
| account\_id | int | ID аккаунта, которому принадлежит шаблон |
| name | string | Название шаблона |
| content | string | Тело шаблона, сообщение, которое отправляется пользователю |
| is\_editable | bool | Может ли пользователь редактировать шаблон в интерфейсе amoCRM |
| type | string | Тип шаблона. Возможны 2 варианта: amocrm и waba |
| buttons | array | Массив объектов кнопок |
| buttons[][type] | string | Тип кнопки, доступные варианты: `inline` (обычная текстовая кнопка), `url` (кнопка ссылка) |
| buttons[][text] | string | Текст, отображаемый в кнопке |
| buttons[][url] | string | Ссылка кнопки, доступно только для кнопки типа `url` |
| attachment | object|null | Объект добавленного файла в шаблон |
| attachment[id] | string | UUID файла из API файлов, прикрепленного к шаблону |
| attachment[name] | string | Название файла, прикрепленного к шаблону, которое будет передано в мессенджер |
| attachment[type] | string | Тип прикрепленного файла. Возможные типы – picture, file, document, video |
| created\_at | int | Timestamp создания шаблона |
| updated\_at | int | Timestamp последнего изменения шаблона |
| external\_id | string | Внешний идентификатор шаблона. ID шаблона в вашей системе |
| waba\_footer | string | Футер шаблона WhatsApp |
| waba\_category | string | Категоря шаблона WhatsApp. Доступны следующие категории: UTILITY AUTHENTICATION MARKETING |
| waba\_language | string | Язык шаблона WhatsApp |
| waba\_examples | object | Примеры замены маркеров шаблона WhatsApp. Пример "waba\_examples":{"{{lead.name}}":"qwerty"} |
| waba\_header | string|null | Хедер шаблона WhatsApp с лимитом до 60 символов. Необязательный параметр |
| waba\_header\_type | string | Тип хедера шаблона WhatsApp. Доступные варианты: `text` (WhatsApp шаблон с хедером), `media` (WhatsApp шаблон с медиа хедером, должно быть вложение под ключом attachment). Необязательный параметр |

#### Пример ответа

```json
{
"\_total\_items": 1,
"\_embedded": {
"chat\_templates": [
{
"id": 7351,
"account\_id": 29420107,
"name": "Hello template",
"content": "Hello {{contact.name}}",
"created\_at": 1640362536,
"updated\_at": 1640362536,
"buttons": [
{
"type": "inline",
"text": "button 1"
},
{
"type": "inline",
"text": "button 2"
}
],
"attachment": {
"id": "c2b77f70-d0d6-484a-8f6e-583f70a08cce",
"name": "Название изображения",
"type": "picture"
},
"type": "waba",
"waba\_footer": "my footer",
"waba\_category": "UTILITY",
"waba\_language": "en",
"waba\_examples": {
"{{contact.name}}": "My contact"
},
"waba\_header": null,
"waba\_header\_type": "media",
"is\_editable": false,
"external\_id": "my\_external\_id\_for\_hello",
"request\_id": "0",
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/chats/templates/7351"
}
}
}
]
}
}
```

### Редактирование шаблонов

#### Метод

*PATCH /api/v4/chats/templates*  
*PATCH /api/v4/chats/templates/{id}*

#### Описание

Метод позволяет редактировать шаблоны пакетно.  
Также вы можете добавить ID шаблоны в метод для редактирования конкретного шаблона (/api/v4/chats/templates/{id}).  
При редактировании пакетно передается массив из объектов, при редактировании одного шаблона, передается просто модель.  
Шаблоны типа waba можно редактировать только в статусе draft

#### Ограничения

Метод доступен только администраторам аккаунта

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Обязательные поля отсутствуют

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID шаблона |
| name | string | Название шаблона |
| content | string | Тело шаблона, сообщение, которое отправляется пользователю. Можно использовать маркеры Salesbot. |
| is\_editable | bool | Может ли пользователь редактировать шаблон в интерфейсе amoCRM. По умолчанию – false |
| type | string | Тип шаблона. Возможны 2 варианта: amocrm и waba |
| buttons | array | Массив объектов кнопок |
| buttons[][type] | string | Тип кнопки, доступные варианты: `inline` (обычная текстовая кнопка), `url` (кнопка ссылка) |
| buttons[][text] | string | Текст, отображаемый в кнопке |
| buttons[][url] | string | Ссылка кнопки, доступно только для кнопки типа `url` |
| attachment | object|null | Объект добавленного файла в шаблон |
| attachment[id] | string | UUID файла из API файлов, прикрепленного к шаблону |
| attachment[name] | string | Название файла, прикрепленного к шаблону, которое будет передано в мессенджер |
| attachment[type] | string | Тип прикрепленного файла. Возможные типы – picture, file, document, video |
| external\_id | string | Внешний идентификатор шаблона. ID шаблона в вашей системе |
| request\_id | string | Поле, которое вернется вам в ответе без изменений и не будет сохранено. Необязательный параметр |
| waba\_footer | string | Футер шаблона WhatsApp |
| waba\_category | string | Категоря шаблона WhatsApp. Доступны следующие категории: UTILITY AUTHENTICATION MARKETING |
| waba\_language | string | Язык шаблона WhatsApp |
| waba\_examples | object | Примеры замены маркеров шаблона WhatsApp. Пример "waba\_examples":{"{{lead.name}}":"qwerty"} |
| waba\_header | string|null | Хедер шаблона WhatsApp с лимитом до 60 символов. Необязательный параметр |
| waba\_header\_type | string | Тип хедера шаблона WhatsApp. Доступные варианты: `text` (WhatsApp шаблон с хедером), `media` (WhatsApp шаблон с медиа хедером, должно быть вложение под ключом attachment). Необязательный параметр |

#### Пример запроса

```json
[
{
"id": 7351,
"name": "My new name",
"content": "My new content",
"buttons": [
{
"type": "inline",
"text": "кнопка 1"
},
{
"type": "inline",
"text": "кнопка 2"
}
],
"attachment": {
"id": "c2b77f70-d0d6-484a-8f6e-583f70a08cce",
"name": "Название изображения",
"type": "picture"
},
"type": "amocrm",
"is\_editable": true
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
| 200 | Шаблон были успешно изменены |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает коллекцию шаблонов, которые были изменены.  
Если происходило редактирование конкретного шаблона, то вернется модель шаблона.

#### Пример ответа

```json
{
"\_total\_items": 1,
"\_embedded": {
"chat\_templates": [
{
"id": 7351,
"account\_id": 29420107,
"name": "My new name",
"content": "My new content",
"created\_at": 1640362536,
"updated\_at": 1640363257,
"buttons": [
{
"type": "inline",
"text": "кнопка 1"
},
{
"type": "inline",
"text": "кнопка 2"
}
],
"attachment": {
"id": "c2b77f70-d0d6-484a-8f6e-583f70a08cce",
"name": "Название изображения",
"type": "picture"
},
"is\_editable": true,
"external\_id": "my\_external\_id\_for\_hello",
"type": "amocrm",
"waba\_footer": "",
"waba\_category": "",
"waba\_language": "",
"waba\_examples": [],
"waba\_header": null,
"waba\_header\_type": null,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/chats/templates/7351"
}
}
}
]
}
}
```

### Отправка шаблона WhatsApp на модерацию

#### Метод

*POST /api/v4/chats/templates/{id}/review*

#### Описание

Метод позволяет отправлять шаблон WhatsApp на модерацию.

#### Ограничения

Метод доступен только администраторам аккаунта

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Параметры запроса отсутствуют

#### Пример запроса

```json
{}
```

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Шаблона WhatsApp был успешно отправлен на модерацию |
| 401 | Пользователь не авторизован |

#### Параметры ответа

Метод возвращает коллекцию статусов шаблона WhatsApp

#### Пример ответа

```json
{
"\_embedded": {
"reviews": [
{
"id" :367,
"source\_id" :13234480,
"status": "review",
"reject\_reason":""
}
]
}
}
```

### Редактирование статуса шаблона WhatsApp

#### Метод

*POST /api/v4/chats/templates/{id}/review/{review\_id}*

#### Описание

Метод позволяет редактировать статус шаблона WhatsApp.

#### Ограничения

Метод доступен только администраторам аккаунта

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Обязательные поля отсутствуют

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| status | string | Возможные значения: approved – одобрен, paused – шаблон на паузе, rejected – шаблон отклонен |
| reject\_reason | string | Причина отказа – произвольная строка длинной до 65535 символов |

#### Пример запроса

```json
{
"status": "rejected",
"reject\_reason": "Не прошёл внутреннюю проверку"
}
```

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Статус шаблона WhatsApp был успешно изменен |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает модель статуса шаблона WhatsApp

#### Пример ответа

```json
{
"id": 7351,
"source\_id": 29420107,
"status": "rejected",
"reject\_reason": "Не прошёл внутреннюю проверку"
}
```

### Удаление шаблонов

#### Метод

*DELETE /api/v4/chats/templates*  
*DELETE /api/v4/chats/templates/{id}*

#### Описание

Метод позволяет удалить шаблон в аккаунте.  
Можно удалить, как конкретный шаблон, так и несколько шаблонов сразу.  
Если файл, прикреплённый к шаблону больше нигде не использовался, или все сущности, где он использовался, удалены, то файл будет удалён вместе с шаблоном, иначе файл не будет удалён и будет доступен в общем списке файлов.

#### Ограничения

- Метод доступен только с правами администратора аккаунта

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

При удалении конкретного шаблона, тело запроса не нужно передавать.

При удалении нескольких шаблонов, нужно передать объекты для удаления с ID шаблонов.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID шаблона |

#### Пример запроса

```json
[
{
"id": 7351
}
]
```

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 204 | Шаблоны была успешно удалены |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод не возвращает тело