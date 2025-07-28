---
title: "Методы API"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/files/files-api
section: developers
---

В данном разделе описываются доступные методы для работы с API файлов в amoCRM.

Через методы API файлов интеграция может загружать файлы, удалять их, создавать версии файлов, связывать файлы с сущностями.

Интеграция идентифицируется посредством проверки переданного Access Token в заголовке `Authorization: Bearer ACCESS_TOKEN`.

Большинство методов API файлов доступны только через отдельный домен сервиса файлов.

**Важно учесть, что при добавлении файла по общему адресу, некоторые функции, например поиск этого файла, могут быть доступны с задержкой.  
Для получения адреса сервиса, который обслуживает текущий аккаунт, можно запросить [свойства аккаунта](https://www.amocrm.ru/developers/content/crm_platform/account-info) с флагом `with=drive_url`.**

### Оглавление

- [Требования к работе с API файлов](#Требования-к-работе-с-API-файлов)
- [Создание сессии загрузки файла](#Создание-сессии-загрузки-файла)
- [Загрузка части файла](#Загрузка-части-файла)
- [Получение файлов](#Получение-файлов)
- [Получение файла по UUID](#Получение-файла-по-UUID)
- [Редактирование файла](#Редактирование-файла)
- [Удаление файлов](#Удаление-файлов)
- [Восстановление файлов](#Восстановление-файлов)
- [Получение версий файла](#Получение-версий-файла)
- [Получение файлов связанных с сущностью](#Получение-файлов-связанных-с-сущностью)
- [Привязка файлов к сущности](#Привязка-файлов-к-сущности)
- [Отвязка файлов от сущности](#Отвязка-файлов-от-сущности)
- [Получение сущностей связанных с файлом](#Получение-сущностей-связанных-с-файлом)

### Требования к работе с API файлов

Для работы с API файлов у интеграции должен быть установлен scope – Доступ к файлам. Для удаления файлов у интеграции дополнительно должен быть установлен scope – Удаление файлов.

### Создание сессии загрузки файла

#### Метод

*POST /v1.0/sessions*

#### Описание

Метод позволяет создать сессию для загрузки файла или версии файла. Если метод используется для загрузки новой версии файла, то загруженная версия автоматически станет активной версией файла. Запрос должен отправляться на хост сервиса файлов.

#### Ограничения

Метод доступен интеграциям у которых установлен scope – Доступ к файлам.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Обязательные поля – file\_name и file\_size

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| file\_name | string | Имя загружаемого файла |
| file\_size | int | Размер загружаемого файла |
| file\_uuid | string | UUID файла, для которого загружается новая версия файла. Если UUID не задан, то будет создан новый файл. |
| content\_type | string | MIME-тип файла |
| with\_preview | bool | При установке данного флага для файла будет сгенерировано превью |

#### Пример запроса

```json
{
"file\_name": "aaa",
"file\_size": 3435,
"content\_type": "image/jpeg",
"file\_uuid": "367b9f38-5f01-4cea-947e-dfab47aea522"
}
```

#### Заголовок типа данных при успешном результате

*Content-Type: application/json*

#### Заголовок типа данных при ошибке

*Content-Type: application/json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Сессия загрузки успешно создана |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Неудачная аутентификация |
| 400 | Переданы некорректные данные |

#### Параметры ответа

Метод возвращает модель сессии, рассмотрим ниже её свойства.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| session\_id | int | ID сессии |
| upload\_url | string | URL по которому должна быть закачена первая часть файла |
| max\_file\_size | int | Максимальный размер файла |
| max\_part\_size | int | Максимальные размер загружаемой части файла |

#### Пример ответа

```json
{
"max\_file\_size": 314572800,
"max\_part\_size": 524288,
"session\_id": 26136001,
"upload\_url": "https://drive-b.amocrm.ru/v1.0/sessions/upload/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjc0MTg3MzYwMCwiaWF0Ijo3NDE4NzM2MDAsIm5iZiI6NzQxODczNjAwLCJhY2NvdW50X2lkIjo3Nzc3Nzc3Nywic2Vzc2lvbl9pZCI6Nzc3Nzc3NzcsInVzZXJfaWQiOjc3Nzc3NzcsInVzZXJfdHlwZSI6ImludGVybmFsIiwicGFydF9udW0iOjF9.8sdJVTZJ\_MjuHhMGDkU7\_eSi2q1u1EG-au\_TZhmmXK8"
}
```

### Загрузка части файла

#### Метод

*POST /v1.0/sessions/upload/{session\_token}*

#### Описание

Метод позволяет загрузить часть файла. Запрос должен отправляться на хост сервиса файлов.  
Полная ссылка с указанием session\_token возвращается при открытии сессии.

#### Заголовок типа данных при успешном результате

*Content-Type: application/json*

#### Заголовок типа данных при ошибке

*Content-Type: application/json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выполнен успешно |
| 404 | Сессия загрузки не найдена |

#### Параметры ответа

Метод возвращает ссылку для загрузки следующей части файла.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| session\_id | int | ID сессии |
| next\_url | string | URL для загрузки следующей части файла |

#### Пример ответа

```json
{
"next\_url": "https://drive-b.amocrm.ru/v1.0/sessions/upload/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjc0MTg3MzYwMCwiaWF0Ijo3NDE4NzM2MDAsIm5iZiI6NzQxODczNjAwLCJhY2NvdW50X2lkIjo3Nzc3Nzc3Nywic2Vzc2lvbl9pZCI6Nzc3Nzc3NzcsInVzZXJfaWQiOjc3Nzc3NzcsInVzZXJfdHlwZSI6ImludGVybmFsIiwicGFydF9udW0iOjF9.8sdJVTZJ\_MjuHhMGDkU7\_eSi2q1u1EG-au\_TZhmmXK8",
"session\_id": 26434413
}
```

#### Параметры ответа при загрузке последней части файла

Метод возвращает модель загруженного файла.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| uuid | string | UUID файла |
| type | string | Тип файла. Возможные параметры – image, video, audio, document, file |
| is\_trashed | bool | Удален ли файл |
| name | string | Имя файла |
| sanitized\_name | string | Имя файла в ASCII кодировке |
| size | int | Размер файла в байтах |
| source\_id | int|null | Идентификатор источника из которого пришел файл |
| version\_uuid | string | Идентификатор версии файла |
| has\_multiple\_versions | bool | Имеет ли файл множество версий |
| created\_at | int | Время создания файла Unix Timestamp |
| created\_by | object | Пользователь создавший файл |
| created\_by[id] | int | ID пользователя создавшего файла |
| created\_by[type] | string | Тип пользователя создавшего файла |
| updated\_at | int | Время последнего обновления файла Unix Timestamp |
| updated\_by | object | Пользователь обновивший файл |
| deleted\_at | int|null | Время удаления файла Unix Timestamp |
| deleted\_by | object|null | Пользователь удаливший файл |
| metadata | object|null | Метаданные файла |
| metadata[extension] | string | Расширение файла |
| metadata[mime\_type] | string | MIME-тип файла |
| previews | array|null | Массив превью для файла |
| previews[0] | object | Превью файла |
| previews[0][download\_link] | string | URL для загрузки превью |
| previews[0][width] | int | Ширина превью |
| previews[0][height] | int | Высота превью |

#### Пример ответа при загрузке последней части файла

```json
{
"\_links": {
"download": {
"href": "https://drive-b.amocrm.ru/download/aff5603a-28b1-4c17-8e98-16e473b323b3/367b9f38-5f01-4cea-947e-dfab47aea522/picture.png"
},
"download\_version": {
"href": "https://drive-b.amocrm.ru/download/aff5603a-28b1-4c17-8e98-16e473b323b3/367b9f38-5f01-4cea-947e-dfab47aea522/43de3be7-307b-4766-a23e-5e88211b9a8d/picture.png"
},
"self": {
"href": "https://drive-b.amocrm.ru/v1.0/files/367b9f38-5f01-4cea-947e-dfab47aea522"
}
},
"created\_at": 1671687247,
"created\_by": { "type": "internal", "id": 7758337 },
"deleted\_at": null,
"deleted\_by": null,
"has\_multiple\_versions": false,
"is\_trashed": false,
"metadata": { "extension": "png", "mime\_type": "image/png" },
"name": "product",
"previews": null,
"sanitized\_name": "product",
"session\_id": 26136001,
"size": 7526,
"source\_id": null,
"type": "file",
"updated\_at": 1671687247,
"updated\_by": { "type": "internal", "id": 7758337 },
"uuid": "367b9f38-5f01-4cea-947e-dfab47aea522",
"version\_uuid": "43de3be7-307b-4766-a23e-5e88211b9a8d"
}
```

### Получение файлов

#### Метод

*GET /v1.0/files*

#### Описание

Метод позволяет получить файлы аккаунта удовлетворяющие указанному фильтру. Запрос должен отправляться на хост сервиса файлов.

#### Ограничения

Метод доступен интеграциям у которых установлен scope – Доступ к файлам.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| filter[uuid] | string | Массив UUID’ов файлов, перечисленных через запятую |
| filter[name] | string | Имя файла |
| filter[extensions][] | string | Расширение файла |
| filter[term] | string | Подстрока содержащаяся в имение файла или имени какой-то из связанных сущностей |
| filter[source\_id] | int | Идентификатор источника из которого был получен файл |
| filter[deleted] | null | Если параметр передан, то будут выведены удалённые файлы |
| filter[size][unit] | int | Количество байт в единице размера файла (по умолчанию 1 байт) |
| filter[size][from] | int | Минимальный размер файла |
| filter[size][to] | int | Максимальный размер файла |
| filter[date][type] | string | Тип события по которому производится фильтрация. Возможные значения – created\_at, updated\_at |
| filter[date][date\_preset] | string | Пресет для задания временного диапазона. Возможные значения – day, tomorrow, yesterday, week, previous\_week, next\_week, month, next\_month, previous\_month, quarter, previous\_quarter, next\_quarter, last\_3\_days, next\_3\_days, last\_6\_month, year |
| filter[date][from] | int | Время после которого произошло событие Unix Timestamp |
| filter[date][to] | int | Время до которого произошло событие Unix Timestamp |
| filter[created\_by][] | int | Создатель файла. Возможные значения: -1 – клиент, 0 – робот, {id} – внутренний пользователь |
| filter[updated\_by][] | int | Пользователь последний обновивший файл. Возможные значения: -1 – клиент, 0 – робот, {id} – внутренний пользователь |

#### Заголовок типа данных при успешном результате

*Content-Type: application/json*

#### Заголовок типа данных при ошибке

*Content-Type: application/json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выполнен успешно |
| 204 | Файлов не найдено |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Неудачная аутентификация |
| 400 | Переданы некорректные данные |

#### Параметры ответа

Метод возвращает массив моделей файлов.

#### Пример ответа

```json
{
"\_count": 25,
"\_embedded": {
"files": [
{
"\_links": {
"download": {
"href": "https://drive-b.amocrm.ru/download/367b9f38-5f01-4cea-947e-dfab47aea522/26ec7266-d953-433b-8bc5-737eb70da87a/8Z5PQ3D7wbS6Doz-svQ0zYdWXeTq8HqfSQzjM-aDY2cI5uM3wcRZ0dD8nLV8TUcX.jpg"
},
"download\_version": {
"href": "https://drive-b.amocrm.ru/download/367b9f38-5f01-4cea-947e-dfab47aea522/26ec7266-d953-433b-8bc5-737eb70da87a/0244c437-1637-4cdf-887a-e574f55eb114/8Z5PQ3D7wbS6Doz-svQ0zYdWXeTq8HqfSQzjM-aDY2cI5uM3wcRZ0dD8nLV8TUcX.jpg"
},
"self": {
"href": "https://drive-b.amocrm.ru/v1.0/files/26ec7266-d953-433b-8bc5-737eb70da87a"
}
},
"created\_at": 1671871033,
"created\_by": { "type": "internal", "id": 7758337 },
"deleted\_at": null,
"deleted\_by": null,
"has\_multiple\_versions": false,
"is\_trashed": false,
"metadata": { "extension": "jpg", "mime\_type": "image/jpeg" },
"name": "8Z5PQ3D7wbS6Doz-svQ0zYdWXeTq8HqfSQzjM-aDY2cI5uM3wcRZ0dD8nLV8TUcX",
"previews": null,
"sanitized\_name": "8Z5PQ3D7wbS6Doz-svQ0zYdWXeTq8HqfSQzjM-aDY2cI5uM3wcRZ0dD8nLV8TUcX",
"size": 38635,
"source\_id": null,
"type": "image",
"updated\_at": 1671871033,
"updated\_by": { "type": "internal", "id": 7758337 },
"uuid": "26ec7266-d953-433b-8bc5-737eb70da87a",
"version\_uuid": "0244c437-1637-4cdf-887a-e574f55eb114"
},
{
"\_links": {
"download": {
"href": "https://drive-b.amocrm.ru/download/367b9f38-5f01-4cea-947e-dfab47aea522/9403badc-5690-4c7d-a999-be09f8c57566/-96.png"
},
"download\_version": {
"href": "https://drive-b.amocrm.ru/download/367b9f38-5f01-4cea-947e-dfab47aea522/9403badc-5690-4c7d-a999-be09f8c57566/2a93e2a2-7c09-4f0d-b8ee-f0228e890307/-96.png"
},
"self": {
"href": "https://drive-b.amocrm.ru/v1.0/files/9403badc-5690-4c7d-a999-be09f8c57566"
}
},
"created\_at": 1671814907,
"created\_by": { "type": "internal", "id": 2647957 },
"deleted\_at": null,
"deleted\_by": null,
"has\_multiple\_versions": false,
"is\_trashed": false,
"metadata": { "extension": "png", "mime\_type": "image/png" },
"name": "\_96",
"previews": null,
"sanitized\_name": "-96",
"size": 5230,
"source\_id": null,
"type": "image",
"updated\_at": 1671814907,
"updated\_by": { "type": "internal", "id": 2647957 },
"uuid": "9403badc-5690-4c7d-a999-be09f8c57566",
"version\_uuid": "2a93e2a2-7c09-4f0d-b8ee-f0228e890307"
},
...
]
},
"\_links": {
"next": {
"href": "https://drive-b.amocrm.ru/v1.0/files?filter%5Bextensions%5D%5B%5D=bmp&filter%5Bextensions%5D%5B%5D=jpeg&filter%5Bextensions%5D%5B%5D=jpg&filter%5Bextensions%5D%5B%5D=png&filter%5Bis\_filter%5D=true&filter%5Bsize%5D%5Bunit%5D=1000000&limit=25&page=2"
},
"self": {
"href": "https://drive-b.amocrm.ru/v1.0/files?filter%5Bextensions%5D%5B%5D=bmp&filter%5Bextensions%5D%5B%5D=jpeg&filter%5Bextensions%5D%5B%5D=jpg&filter%5Bextensions%5D%5B%5D=png&filter%5Bis\_filter%5D=true&filter%5Bsize%5D%5Bunit%5D=1000000&limit=25&page=1"
}
}
}
```

### Получение файла по UUID

#### Метод

*GET /v1.0/files/{file\_uuid}*

#### Описание

Метод позволяющий получать файл аккаунта. Запрос должен отправляться на хост сервиса файлов.

#### Ограничения

Метод доступен интеграциям у которых установлен scope – Доступ к файлам.

#### Заголовок типа данных при успешном результате

*Content-Type: application/json*

#### Заголовок типа данных при ошибке

*Content-Type: application/json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выолнен успешно |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Неудачная аутентификация |
| 404 | Файл не найден |

#### Параметры ответа

Метод возвращает модель файла.

#### Пример ответа

```json
{
"\_links": {
"download": {
"href": "https://drive-b.amocrm.ru/download/aff5603a-28b1-4c17-8e98-16e473b323b3/367b9f38-5f01-4cea-947e-dfab47aea522/picture.png"
},
"download\_version": {
"href": "https://drive-b.amocrm.ru/download/aff5603a-28b1-4c17-8e98-16e473b323b3/367b9f38-5f01-4cea-947e-dfab47aea522/43de3be7-307b-4766-a23e-5e88211b9a8d/picture.png"
},
"self": {
"href": "https://drive-b.amocrm.ru/v1.0/files/367b9f38-5f01-4cea-947e-dfab47aea522"
}
},
"created\_at": 1671687247,
"created\_by": { "type": "internal", "id": 7758337 },
"deleted\_at": null,
"deleted\_by": null,
"has\_multiple\_versions": false,
"is\_trashed": false,
"metadata": { "extension": "png", "mime\_type": "image/png" },
"name": "product",
"previews": null,
"sanitized\_name": "product",
"session\_id": 26136001,
"size": 7526,
"source\_id": null,
"type": "file",
"updated\_at": 1671687247,
"updated\_by": { "type": "internal", "id": 7758337 },
"uuid": "367b9f38-5f01-4cea-947e-dfab47aea522",
"version\_uuid": "43de3be7-307b-4766-a23e-5e88211b9a8d"
}
```

### Редактирование файла

#### Метод

*PATCH /v1.0/files/{file\_uuid}*

#### Описание

Метод позволяет редактировать файл. При редактировании файла можно изменить его имя или активную версию. Запрос должен отправляться на хост сервиса файлов.

#### Ограничения

Метод доступен интеграциям у которых установлен scope – Доступ к файлам.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Обязательных полей нет. Поля name и version\_uuid не могут быть заданны одновременно.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| name | string | Новое имя файла |
| version\_uuid | string | UUID версии файла, которая должна быть установлена как активная версия файла |

#### Пример запроса

```json
{
"name": "Новое имя файла"
}
{
"version\_uuid": "367b9f38-5f01-4cea-947e-dfab47aea522"
}
```

#### Заголовок типа данных при успешном результате

*Content-Type: application/json*

#### Заголовок типа данных при ошибке

*Content-Type: application/json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Файл был успешно изменен |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Неудачная аутентификация |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |
| 404 | Файл не найден |

#### Параметры ответа

Метод возвращает модель файла.

#### Пример ответа

```json
{
"\_links": {
"download": {
"href": "https://drive-b.amocrm.ru/download/aff5603a-28b1-4c17-8e98-16e473b323b3/367b9f38-5f01-4cea-947e-dfab47aea522/picture.png"
},
"download\_version": {
"href": "https://drive-b.amocrm.ru/download/aff5603a-28b1-4c17-8e98-16e473b323b3/367b9f38-5f01-4cea-947e-dfab47aea522/43de3be7-307b-4766-a23e-5e88211b9a8d/picture.png"
},
"self": {
"href": "https://drive-b.amocrm.ru/v1.0/files/367b9f38-5f01-4cea-947e-dfab47aea522"
}
},
"created\_at": 1671687247,
"created\_by": { "type": "internal", "id": 7758337 },
"deleted\_at": null,
"deleted\_by": null,
"has\_multiple\_versions": false,
"is\_trashed": false,
"metadata": { "extension": "png", "mime\_type": "image/png" },
"name": "product",
"previews": null,
"sanitized\_name": "product",
"session\_id": 26136001,
"size": 7526,
"source\_id": null,
"type": "file",
"updated\_at": 1671687247,
"updated\_by": { "type": "internal", "id": 7758337 },
"uuid": "367b9f38-5f01-4cea-947e-dfab47aea522",
"version\_uuid": "43de3be7-307b-4766-a23e-5e88211b9a8d"
}
```

### Удаление файлов

#### Метод

*DELETE /v1.0/files*

#### Описание

Метод позволяет удалить файлы аккаунта. Запрос должен отправляться на хост сервиса файлов.

#### Ограничения

Метод доступен интеграциям у которых установлен scope – Удаление файлов.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Тело запроса должно содержать массив объектов с полем uuid.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| uuid | string | UUID файла |

#### Пример запроса

```json
[
{
"uuid": "367b9f38-5f01-4cea-947e-dfab47aea522"
},
{
"uuid": "bf1097fb-58fe-42c1-b385-ac443228ddd0"
}
]
```

#### Заголовок типа данных при успешном результате

*Content-Type: application/json*

#### Заголовок типа данных при ошибке

*Content-Type: application/json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 204 | Файлы успешно удалены |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Неудачная аутентификация |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод не возвращает тело ответа при успешном запросе.

### Восстановление файлов

#### Метод

*POST /v1.0/files/restore*

#### Описание

Метод позволяет восстановить файлы аккаунта. Запрос должен отправляться на хост сервиса файлов.

#### Ограничения

Метод доступен интеграциям у которых установлен scope – Доступ к файлам.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Тело запроса должно содержать массив объектов с полем uuid.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| uuid | string | UUID файла |

#### Пример запроса

```json
[
{
"uuid": "367b9f38-5f01-4cea-947e-dfab47aea522"
},
{
"uuid": "bf1097fb-58fe-42c1-b385-ac443228ddd0"
}
]
```

#### Заголовок типа данных при успешном результате

*Content-Type: application/json*

#### Заголовок типа данных при ошибке

*Content-Type: application/json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Файлы были успешно восстановлен |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Неудачная аутентификация |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает коллекцию восстановленых файлов.

#### Пример ответа

```json
{
"\_count": 2,
"\_embedded": {
"files": [
{
"\_links": {
"download": {
"href": "https://drive-b.amocrm.ru/download/367b9f38-5f01-4cea-947e-dfab47aea522/26ec7266-d953-433b-8bc5-737eb70da87a/8Z5PQ3D7wbS6Doz-svQ0zYdWXeTq8HqfSQzjM-aDY2cI5uM3wcRZ0dD8nLV8TUcX.jpg"
},
"download\_version": {
"href": "https://drive-b.amocrm.ru/download/367b9f38-5f01-4cea-947e-dfab47aea522/26ec7266-d953-433b-8bc5-737eb70da87a/0244c437-1637-4cdf-887a-e574f55eb114/8Z5PQ3D7wbS6Doz-svQ0zYdWXeTq8HqfSQzjM-aDY2cI5uM3wcRZ0dD8nLV8TUcX.jpg"
},
"self": {
"href": "https://drive-b.amocrm.ru/v1.0/files/26ec7266-d953-433b-8bc5-737eb70da87a"
}
},
"created\_at": 1671871033,
"created\_by": { "type": "internal", "id": 7758337 },
"deleted\_at": null,
"deleted\_by": null,
"has\_multiple\_versions": false,
"is\_trashed": false,
"metadata": { "extension": "jpg", "mime\_type": "image/jpeg" },
"name": "8Z5PQ3D7wbS6Doz-svQ0zYdWXeTq8HqfSQzjM-aDY2cI5uM3wcRZ0dD8nLV8TUcX",
"previews": null,
"sanitized\_name": "8Z5PQ3D7wbS6Doz-svQ0zYdWXeTq8HqfSQzjM-aDY2cI5uM3wcRZ0dD8nLV8TUcX",
"size": 38635,
"source\_id": null,
"type": "image",
"updated\_at": 1671871033,
"updated\_by": { "type": "internal", "id": 7758337 },
"uuid": "26ec7266-d953-433b-8bc5-737eb70da87a",
"version\_uuid": "0244c437-1637-4cdf-887a-e574f55eb114"
},
{
"\_links": {
"download": {
"href": "https://drive-b.amocrm.ru/download/367b9f38-5f01-4cea-947e-dfab47aea522/9403badc-5690-4c7d-a999-be09f8c57566/-96.png"
},
"download\_version": {
"href": "https://drive-b.amocrm.ru/download/367b9f38-5f01-4cea-947e-dfab47aea522/9403badc-5690-4c7d-a999-be09f8c57566/2a93e2a2-7c09-4f0d-b8ee-f0228e890307/-96.png"
},
"self": {
"href": "https://drive-b.amocrm.ru/v1.0/files/9403badc-5690-4c7d-a999-be09f8c57566"
}
},
"created\_at": 1671814907,
"created\_by": { "type": "internal", "id": 2647957 },
"deleted\_at": null,
"deleted\_by": null,
"has\_multiple\_versions": false,
"is\_trashed": false,
"metadata": { "extension": "png", "mime\_type": "image/png" },
"name": "\_96",
"previews": null,
"sanitized\_name": "-96",
"size": 5230,
"source\_id": null,
"type": "image",
"updated\_at": 1671814907,
"updated\_by": { "type": "internal", "id": 2647957 },
"uuid": "9403badc-5690-4c7d-a999-be09f8c57566",
"version\_uuid": "2a93e2a2-7c09-4f0d-b8ee-f0228e890307"
}
]
}
}
```

### Получение версий файла

#### Метод

*GET /v1.0/files/{file\_uuid}/versions*

#### Описание

Метод позволяющий получать версии файлов. Запрос должен отправляться на хост сервиса файлов.

#### Ограничения

Метод доступен интеграциям у которых установлен scope – Доступ к файлам.

#### Заголовок типа данных при успешном результате

*Content-Type: application/json*

#### Заголовок типа данных при ошибке

*Content-Type: application/json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выполнен успешно |
| 404 | Файл не найден |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Неудачная аутентификация |
| 400 | Переданы некорректные данные |

#### Параметры ответа

Метод возвращает коллекцию версий файла.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| uuid | string | UUID версии файла |
| file\_uuid | string | UUID файла |
| type | string | Тип версии файла. Возможные параметры – image, video, audio, document, file |
| name | string | Имя версии файла |
| sanitized\_name | string | Имя версии файла в ASCII кодировке |
| size | int | Размер версии файла в байтах |
| is\_main | bool | Является ли данная версия активной версией файла |
| source\_id | int|null | Идентификатор источника из которого пришла версия файла |
| created\_at | int | Время создания версии файла Unix Timestamp |
| created\_by | object | Пользователь создавший версию файла |
| created\_by[id] | int | ID пользователя создавшего версию файла |
| created\_by[type] | string | Тип пользователя создавшего версию файла |
| updated\_at | int | Время последнего обновления версии файла Unix Timestamp |
| updated\_by | object | Пользователь обновивший версию файла |
| metadata | object|null | Метаданные файла |
| metadata[extension] | string | Расширение файла |
| metadata[mime\_type] | string | MIME-тип файла |
| previews | array|null | Массив превью для файла |
| previews[0] | object | Превью файла |
| previews[0][download\_link] | string | URL для загрузки превью |
| previews[0][width] | int | Ширина превью |
| previews[0][height] | int | Высота превью |

#### Пример ответа

```json
{
"\_count": 2,
"\_embedded": {
"versions": [
{
"\_links": {
"download": {
"href": "https://drive-b.amocrm.ru/download/21c0e773-0b10-57ac-96d1-c0b97ba6a3f7/89a61e7b-ba30-476f-b2f6-705a964e85c6/fd8401e1-c1db-4033-851c-1df68d40f579/source.jpeg"
},
"self": {
"href": "https://drive-b.amocrm.ru/v1.0/files/89a61e7b-ba30-476f-b2f6-705a964e85c6/versions/fd8401e1-c1db-4033-851c-1df68d40f579"
}
},
"created\_at": 1671995440,
"created\_by": { "type": "internal", "id": 7758337 },
"file\_uuid": "89a61e7b-ba30-476f-b2f6-705a964e85c6",
"is\_main": true,
"metadata": { "extension": "jpeg", "mime\_type": "image/jpeg" },
"name": "source",
"previews": null,
"sanitized\_name": "source",
"size": 93425,
"source\_id": null,
"type": "image",
"updated\_at": 1671995440,
"updated\_by": { "type": "internal", "id": 7758337 },
"uuid": "fd8401e1-c1db-4033-851c-1df68d40f579"
},
{
"\_links": {
"download": {
"href": "https://drive-b.amocrm.ru/download/21c0e773-0b10-57ac-96d1-c0b97ba6a3f7/89a61e7b-ba30-476f-b2f6-705a964e85c6/17006a5b-aa43-4b2f-a380-e851786b9a57/consoleText.txt"
},
"self": {
"href": "https://drive-b.amocrm.ru/v1.0/files/89a61e7b-ba30-476f-b2f6-705a964e85c6/versions/17006a5b-aa43-4b2f-a380-e851786b9a57"
}
},
"created\_at": 1663233556,
"created\_by": { "type": "internal", "id": 7758337 },
"file\_uuid": "89a61e7b-ba30-476f-b2f6-705a964e85c6",
"is\_main": false,
"metadata": { "extension": "txt", "mime\_type": "" },
"name": "consoleText",
"previews": null,
"sanitized\_name": "consoleText",
"size": 7347,
"source\_id": null,
"type": "file",
"updated\_at": 1670599185,
"updated\_by": { "type": "internal", "id": 7758337 },
"uuid": "17006a5b-aa43-4b2f-a380-e851786b9a57"
}
]
},
"\_links": {
"self": {
"href": "https://drive-b.amocrm.ru/v1.0/files/89a61e7b-ba30-476f-b2f6-705a964e85c6/versions"
}
}
}
```

### Получение файлов связанных с сущностью

#### Метод

*GET /api/v4/leads/{entity\_id}/files*

*GET /api/v4/contacts/{entity\_id}/files*

*GET /api/v4/companies/{entity\_id}/files*

*GET /api/v4/customers/{entity\_id}/files*

#### Описание

Метод позволяет получить файлы связанные с сущностью.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### GET параметры

Обязательных полей нет

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| limit | int | Количество возвращаемых связей за один запрос |
| before\_id | int | Вернутся связи с ID меньше заданного |

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выполнен успешно |
| 204 | У сущности нет связанных файлов |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Неудачная аутентификация |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |
| 404 | Сущность не найдена |

#### Параметры ответа

Метод возвращает массив объектов, содержащих идентификатор файлов.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| file\_uuid | string | UUID файла |
| id | int | ID связи сущность-файл |

#### Пример ответа

```json
{
"\_links": {
"self": {
"href": "https://wombat.amocrm.ru/ajax/v4/leads/18437733/files?limit=50"
}
},
"\_embedded": {
"files": [
{ "file\_uuid": "50ca4b6b-0b88-4ece-9f89-d48961579ae0", "id": 2140857 },
{ "file\_uuid": "5ef222cd-bce4-4df8-8466-3dee7d16e70d", "id": 2128681 }
]
}
}
```

### Привязка файлов к сущности

#### Метод

*PUT /api/v4/leads/{entity\_id}/files*

*PUT /api/v4/contacts/{entity\_id}/files*

*PUT /api/v4/companies/{entity\_id}/files*

*PUT /api/v4/customers/{entity\_id}/files*

#### Описание

Метод позволяет привязывать файл к сущности.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

Тело запроса содержит массив объектов с указанием UUID’ов привязываемых файлов.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| file\_uuid | string | UUID привязываемого файла |

#### Пример запроса

```json
[
{
"file\_uuid": "50ca4b6b-0b88-4ece-9f89-d48961579ae0"
},
{
"file\_uuid": "367b9f38-5f01-4cea-947e-dfab47aea522"
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
| 202 | Файлы успешно привязаны |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Неудачная аутентификация |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |
| 404 | Сущность не найдена |

#### Параметры ответа

Метод не возвращает тело ответа при успешном запросе.

### Отвязка файлов от сущности

#### Метод

*DELETE /api/v4/leads/{entity\_id}/files*

*DELETE /api/v4/contacts/{entity\_id}/files*

*DELETE /api/v4/companies/{entity\_id}/files*

*DELETE /api/v4/customers/{entity\_id}/files*

#### Описание

Метод позволяет отвязать файл от сущности.

#### Ограничения

Метод доступен в соответствии с правами пользователя.

#### Параметры запроса

Тело запроса содержит массив объектов с указанием UUID’ов отвязываемых файлов.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| file\_uuid | string | UUID отвязываемого файла |

#### Заголовок типа данных при успешном результате

*Content-Type: application/hal+json*

#### Заголовок типа данных при ошибке

*Content-Type: application/problem+json*

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 202 | Запрос выполнен успешно |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Неудачная аутентификация |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |
| 404 | Сущность не найдена |

#### Параметры ответа

Метод не возвращает тело ответа при успешном запросе.

### Получение сущностей связанных с файлом

#### Метод

*GET /api/v4/files/{file\_uuid}/links*

#### Описание

Метод позволяет получить сущности связанные с файлом.

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
| 403 | Не хватает прав для вызова данного метода |
| 401 | Неудачная аутентификация |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает объект, содержащий UUID файла и массив связанных с ним сущностей.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| file\_uuid | string | UUID файла |
| entities | array | Массив связанных с файлом сущностей |
| entities[0] | object | Связанная с файлом сущность |

#### Пример ответа

```json
{
"file\_uuid": "5ef222cd-bce4-4df8-8466-3dee7d16e70d",
"entities": [
{
"id": 22859207,
"name": "Сделка #22859207",
"created\_by": 0,
"main\_user\_id": 7758337,
"date\_create": 1669372247,
"price": 20,
"pipeline\_id": 3858604,
"date\_update": 1672060100,
"updated\_by": 7758337,
"entity\_type": "leads",
"status\_id": 37066879,
"closest\_task\_at": null
},
{
"id": 19229439,
"name": "Сделка #19229439",
"created\_by": 0,
"main\_user\_id": 7758337,
"date\_create": 1651773549,
"price": 20,
"pipeline\_id": 3858604,
"date\_update": 1662404148,
"updated\_by": null,
"entity\_type": "leads",
"status\_id": 37066876,
"closest\_task\_at": null
}
]
}
```