---
title: "Виджеты"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/crm/platform/widgets-api
section: developers
---

В данном разделе описывается работа с виджетами через API.

### Оглавление

- [Список виджетов](#widgets-list)
- [Информация о виджете по его коду](#widget-detail)
- [Установка виджета в аккаунт](#widget-install)
- [Удаление установки виджета](#widget-uninstall)
- [Подтверждение выполнения блока виджета в Salesbot](#widget-continue)

### Список виджетов

#### Метод

GET /api/v4/widgets

#### Описание

Метод возвращает агрегированный список публичных виджетов, виджетов установленных в аккаунте, а также загруженным текущим пользователем.

#### Ограничения

Метод доступен всем пользователям.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| page | int | Страница выборки |
| limit | int | Количество возвращаемых сущностей за один запрос (Максимум – 250) |

#### Заголовок типа данных при успешном результате

Content-Type: application/hal+json

#### Заголовок типа данных при ошибке

Content-Type: application/problem+json

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выполнен успешно |
| 401 | Пользователь не авторизован |

#### Параметры ответа

Метод возвращает коллекцию моделей виджетов, рассмотрим ниже свойства модели.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID виджета |
| code | string | Код виджета |
| version | string | Версия виджета |
| rating | string/float | Рейтинг виджета |
| settings\_template | array | Поля доступные для настройки |
| settings\_template[0] | object | Поле для настройки |
| settings\_template[0][key] | string | Ключ значения поля в настройках виджета |
| settings\_template[0][name] | string | Название поля в настройках виджета |
| settings\_template[0][type] | string | Тип данных в настройках виджета (text, pass, custom, users или users\_lp) |
| settings\_template[0][is\_required] | bool | Является ли настройка обязательной |
| is\_lead\_source | bool | Доступен ли виджет в качестве источника сделок |
| is\_work\_with\_dp | bool | Доступен ли виджет в Digital Pipeline |
| is\_crm\_template | bool | Является ли виджет отраслевым решением |
| client\_uuid | string/null | UUID связанной с виджетом oAuth интеграции |
| is\_active\_in\_account | bool | Установлен ли виджет в аккаунте |
| pipeline\_id | int | ID воронки, в котором виджет установлен, как источник сделок |

#### Пример ответа

```json
{
"\_page": 1,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/widgets?limit=2&page=1"
},
"next": {
"href": "https://example.amocrm.ru/api/v4/widgets?limit=2&page=2"
}
},
"\_embedded": {
"widgets": [
{
"id": 742,
"code": "amo\_dropbox",
"version": "0.0.13",
"rating": "2,8",
"settings\_template": [
{
"key": "conf",
"name": "custom",
"type": "custom",
"is\_required": false
}
],
"is\_lead\_source": false,
"is\_work\_with\_dp": false,
"is\_crm\_template": false,
"client\_uuid": null,
"is\_active\_in\_account": false,
"pipeline\_id": null,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/widgets/amo\_dropbox"
}
}
},
{
"id": 796,
"code": "amo\_mailchimp",
"version": "1.1.12",
"rating": "3,4",
"settings\_template": [
{
"key": "api",
"name": "custom",
"type": "custom",
"is\_required": false
}
],
"is\_lead\_source": false,
"is\_work\_with\_dp": false,
"is\_crm\_template": false,
"client\_uuid": null,
"is\_active\_in\_account": false,
"pipeline\_id": null,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/widgets/amo\_mailchimp"
}
}
}
]
}
}
```

### Информация о виджете по его коду

#### Метод

GET /api/v4/widgets/{widget\_code}

#### Описание

Метод позволяет получить информацию о публичном или загруженном текущим пользователем виджете.

#### Ограничения

Метод доступен всем пользователям

#### Заголовок типа данных при успешном результате

Content-Type: application/hal+json

#### Заголовок типа данных при ошибке

Content-Type: application/problem+json

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Запрос выполнен успешно |
| 404 | Виджет не найден или недоступен |
| 401 | Пользователь не авторизован |

#### Параметры ответа

Метод возвращает модель виджета, рассмотрим ниже свойства модели.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID виджета |
| code | string | Код виджета |
| version | string | Версия виджета |
| rating | string/float | Рейтинг виджета |
| settings\_template | array | Поля доступные для настройки |
| settings\_template[0] | object | Поле для настройки |
| settings\_template[0][key] | string | Ключ значения поля в настройках виджета |
| settings\_template[0][name] | string | Название поля в настройках виджета |
| settings\_template[0][type] | string | Тип данных в настройках виджета (text, pass, custom, users или users\_lp) |
| settings\_template[0][is\_required] | bool | Является ли настройка обязательной |
| is\_lead\_source | bool | Доступен ли виджет в качестве источника сделок |
| is\_work\_with\_dp | bool | Доступен ли виджет в Digital Pipeline |
| is\_crm\_template | bool | Является ли виджет отраслевым решением |
| client\_uuid | string/null | UUID связанной с виджетом oAuth интеграции |
| is\_active\_in\_account | bool | Установлен ли виджет в аккаунте |
| pipeline\_id | int | ID воронки, в котором виджет установлен, как источник сделок |
| settings | array | Настройки виджета. Данный ключ возвращается только при запросе из под ключа, связанной с виджетом интеграции |

#### Пример ответа

```json
{
"id": 742,
"code": "amo\_dropbox",
"version": "0.0.13",
"rating": "2,8",
"settings\_template": [
{
"key": "conf",
"name": "custom",
"type": "custom",
"is\_required": false
}
],
"is\_lead\_source": false,
"is\_work\_with\_dp": false,
"is\_crm\_template": false,
"client\_uuid": null,
"is\_active\_in\_account": false,
"pipeline\_id": null,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/widgets/amo\_dropbox"
}
}
}
```

### Установка виджета в аккаунт

#### Метод

POST /api/v4/widgets/{widget\_code}

#### Описание

Метод позволяет устанавливать виджет в аккаунт.

#### Ограничения

Метод доступен с правами администратора аккаунта.

#### Заголовок запроса

Content-Type: application/json

#### Параметры запроса

Для установки виджета необходимо передать обязательные параметры в зависимости от доступных настроек виджета. Рассмотрим ниже доступные типы полей и их формат

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| text | string | Значение данного типа передается в виде простой строки |
| pass | string | Значение данного типа передается в виде простой строки |
| users | object | Объект, содержащий ID пользователя amoCRM как ключ и его добавочный номер как значение |
| users\_lp | object | Объект, содержащий ID пользователя amoCRM как ключ и объект к логином и паролем как значение |
| users\_lp[{user\_id}][login] | object | Логин пользователя |
| users\_lp[{user\_id}][password] | object | Пароль пользователя |

#### Пример запроса

В примере передадим необходимые поля для установки виджета amo\_asterisk.

Поле login и script\_path имеет тип text.  
Поле password имеет тип pass.

```json
{
"login": "example",
"password": "eXaMp1E",
"phones": {
"504141": "1039"
},
"script\_path": "https://example.com/"
}
```

#### Заголовок типа данных при успешном результате

Content-Type: application/hal+json

#### Заголовок типа данных при ошибке

Content-Type: application/problem+json

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 200 | Виджет был успешно установлен |
| 404 | Виджет не найден |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает объект виджета, который был установлен, а также настройки виджета. Свойства аналогичны тем, что приходят в методе получения виджета.

#### Пример ответа

```json
{
"id": 972,
"code": "amo\_asterisk",
"version": "1.1.6",
"rating": "2,7",
"settings\_template": [
{
"key": "login",
"name": "Логин",
"type": "text",
"is\_required": true
},
{
"key": "password",
"name": "Пароль",
"type": "pass",
"is\_required": true
},
{
"key": "phones",
"name": "Список телефонов",
"type": "users",
"is\_required": true
},
{
"key": "script\_path",
"name": "Путь к скрипту",
"type": "text",
"is\_required": true
}
],
"is\_lead\_source": false,
"is\_work\_with\_dp": false,
"is\_crm\_template": false,
"client\_uuid": null,
"is\_active\_in\_account": true,
"pipeline\_id": null,
"settings": {
"login": "example",
"password": "eXaMp1E",
"phones": {
"504141": "1039"
},
"script\_path": "https://example.com/"
},
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/widgets/amo\_asterisk"
}
}
}
```

### Удаление установки виджета

#### Метод

DELETE /api/v4/widgets/{widget\_code}

#### Описание

Метод позволяет отключить виджет по его коду.

#### Ограничения

Метод доступен только с правами администратора аккаунта.

#### Заголовок запроса

Content-Type: application/json

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 204 | Виджет был успешно отключен |
| 404 | Виджет не найден |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Пользователь не авторизован |

#### Параметры ответа

Метод не возвращает тело

### Подтверждение выполнения блока виджета в Salesbot

#### Метод

POST /api/v4/{salesbot|marketingbot}/{bot\_id}/continue/{continue\_id}

#### Описание

Метод принимает данные после выполнения отработки виджета в Salesbot’е и продолжает работу бота.  
Подробней о методе Salesbot widget\_request читайте – [тут.](https://www.amocrm.ru/developers/content/digital_pipeline/salesbot)

#### Ограничения

Метод доступен только с правами администратора аккаунта.  
Максимальное количество переданных хендлеров в параметре execute\_handlers: 10.  
Если передан в execute\_handler, хендлер с типом: show, то параметр value, не должен превышать 80 символов  
Максимальное количество переданных кнопок в execute\_handler: 25.

#### Заголовок запроса

Content-Type: application/json

#### Параметры запроса

Если виджету требуется передать какие либо данные, их нужно поместить в поле data в виде массива.Если виджету требуется выполнить дейсвтия до того, как бот продолжит работу, то вы можете передать список хендлеров в параметр: execute\_handlers. Переданные хендлеры выполняются по очереди.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| data | array | Данные для виджета, в коде бота можно получить их по ключу {{json.НАЗВАНИЯ\_КЛЮЧА\_МАССИВА}}, где НАЗВАНИЯ\_КЛЮЧА\_МАССИВА это имя поля переданного в data. Необязательный параметр. |
| execute\_handlers | array | На данный момент поддерживаются хендлеры следующих типов: show, goto. Необязательный параметр. |

#### Пример запроса

В примере передадим виджету поле status, в любом блоке после widget\_request по ключу {{json.status}} виджет сможет получить его значение: "success".  
Также передадим, чтобы бот виджета отобразил текст, кнопки, кнопки со ссылками и перешёл на 5 шаг бота виджета

```json
{
"data": {
"status": "success"
},
"execute\_handlers": [
{
"handler": "show",
"params": {
"type": "text",
"value": "Здесь текст"
}
},
{
"handler": "show",
"params": {
"type": "buttons",
"value": "Нажми на кнопку",
"buttons": [
"1ая кнопка",
"2ая кнопка",
"3ая кнопка",
"4ая кнопка",
...
"25ая кнопка"
]
}
},
{
"handler": "show",
"params": {
"type": "buttons\_url",
"value": "Кнопки со ссылками",
"buttons": [
"https://amocrm.ru",
"https://amocrm.com"
]
}
},
{
"handler": "goto",
"params": {
"type": "question|answer|finish",
"step": 5
}
}
]
}
```

#### HTTP коды ответа

| Код ответа | Условие |
| --- | --- |
| 202 | Виджет был успешно запущен |
| 400 | Переданы неверные данные |
| 404 | Запись о виджете ожидающем результата выполнения не найдена |
| 401 | Пользователь не авторизован |

#### Параметры ответа

Метод не возвращает тело