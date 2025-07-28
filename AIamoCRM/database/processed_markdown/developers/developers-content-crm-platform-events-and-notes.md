---
title: "События и Примечания"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/crm/platform/events-and-notes
section: developers
---

В данном разделе описывается работа со списком событий и примечаниями сущностей

### Оглавление

- [Общая информация о событиях](#events-common-info)
- [Список событий](#events-list)
- [Получение события по ID](#events-detail)
- [Значения для фильтра по значению до/после](#events-filter-params)
- [Структуры данных в полях value\_after и value\_before](#events-params)
- [Типы событий](#events-types)
- [Получение типов событий](#event-types)
- [Особенности фильтрации событий по связанным сущностям](#events-peculiarities)
- [Общая информация о примечаниях](#notes-common-info)
- [Типы примечаний](#notes-types)
- [Список примечаний по типу сущности](#notes-list)
- [Список примечаний по конкретной сущности, по ID сущности](#notes-entity-list)
- [Получение примечания по ID](#note-detail)
- [Добавление примечаний](#notes-add)
- [Редактирование примечаний](#notes-edit)

### Общая информация о событиях

Список событий – это набор информации о происходящих действиях в вашем аккаунте. С помощью API списка событий вы можете получить информацию о различных действиях в аккаунте.

### Список событий

#### Метод

*GET /api/v4/events*

#### Описание

Метод позволяет получить список событий.

#### Ограничения

Метод доступен всем пользователям аккаунта. Возвращаемые данные зависят от прав на сущность.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| with | string | Данный параметр принимает строку, в том числе из нескольких значений, указанных через запятую. Данный метод поддерживает [следующие параметры.](#with-e2e4c901-fcb2-463f-b8bf-fcdf1643963d-params) |
| page | int | Страница выборки |
| limit | int | Количество возвращаемых сущностей за один запрос (Максимум – 100) |
| filter | object | Фильтр |
| filter[id] | string|array | Фильтр по ID событий. Можно передать как один ID, так и массив из нескольких ID |
| filter[created\_at] | int|array | Фильтр по дате создания события (когда оно произошло). Можно передать timestamp, в таком случае будут возвращены события, которые были созданы после переданного значения. |
| filter[created\_by] | int|array | Фильтр по пользователю, передаются до 10-ти ID пользователей, состоящих в аккаунте, в виде массива. Например, filter[created\_by][]=956328&filter[created\_by][]=504141 |
| filter[entity] | string|array | Фильтр по типу сущности, передаются в виде массива. Возможные параметры – lead, contact, company,customer, task, catalog\_{CATALOG\_ID}. Например, filter[entity][]=lead&filter[entity][]=contact&filter[entity][]=catalog\_1075 |
| filter[entity\_id] | int|array | Фильтр по ID сущности, передаются до 10-ти ID в виде массива. Для использования данного фильтра обязательна передача фильтра filter[entity] и не более 1 сущности в нём. Например,filter[entity]=lead&filter[entity\_id][]=648533 |
| filter[type] | string|array | Фильтр по типу событий. Типы перечисляются в виде массива, [подробней о возможных типах](#events-types) |
| filter[value\_before] | string|array | Фильтр по значению до. Подробней о возможных значения и ограничениях читайте – [тут](#events-filter-params) |
| filter[value\_after] | string|array | Фильтр по значению до. Подробней о возможных значения и ограничениях читайте – [тут](#events-filter-params) |

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

Метод возвращает коллекцию моделей событий, рассмотрим ниже свойства события.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | string | ID события |
| type | string | Тип события |
| entity\_id | int | ID сущности события |
| entity\_type | string | Сущность события |
| created\_by | int | ID пользователя, создавший событие |
| created\_at | int | Дата создания события, передается в Unix Timestamp |
| value\_after | array | Массив с изменениями по событию. Подробней о свойствах изменения читайте [тут](#events-params) |
| value\_before | array | Массив с изменениями по событию. Подробней о свойствах изменения читайте [тут](#events-params) |
| account\_id | int | ID аккаунта, в котором находится событие |

#### Пример ответа

```json
{
"\_page": 1,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/events?limit=1&page=1"
},
"next": {
"href": "https://example.amocrm.ru/api/v4/events?limit=1&page=2"
}
},
"\_embedded": {
"events": [
{
"id": "01pz58t6p04ymgsgfbmfyfy1mf",
"type": "lead\_added",
"entity\_id": 26060763,
"entity\_type": "lead",
"created\_by": 939801,
"created\_at": 1888888888,
"value\_after": [
{
"note": {
"id": 42743871
}
}
],
"value\_before": [],
"account\_id": 17079858,
"\_links": {
"self": {
"href": https://example.amocrm.ru/api/v4/events/01pz58t6p04ymgsgfbmfyfy1mf"
}
},
"\_embedded": {
"entity": {
"id": 26060763,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/26060763"
}
}
}
}
}
]
}
}
```

#### Параметры для GET-параметра with

| Параметр | Описание |
| --- | --- |
| contact\_name | Если сущностью события является контакт, то помимо его ID, вы получите и название |
| lead\_name | Если сущностью события является сделка, то помимо её ID, вы получите и название |
| company\_name | Если сущностью события является компания, то помимо её ID, вы получите и название |
| catalog\_element\_name | Если сущностью события является элемент каталога, то помимо его ID, вы получите и название |
| customer\_name | Если сущностью события является покупатель, то помимо его ID, вы получите и название |
| catalog\_name | Если сущностью события является элемент каталога, то помимо ID каталога, к которому он относится, вы получите и название каталога |

### Получение события по ID

#### Метод

*GET /api/v4/events/{id}*

#### Описание

Метод позволяет получить данные конкретного события по ID.

#### Ограничения

Метод доступен всем пользователям аккаунта. Возвращаемые данные зависят от прав на сущность.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| with | string | Данный параметр принимает строку, в том числе из нескольких значений, указанных через запятую. Данный метод поддерживает [следующие параметры.](#with-4330ca9b-11f2-4afb-858f-6e90d14bef43-params) |

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

Метод возвращает модель события, рассмотрим ниже свойства события.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | string | ID события |
| type | string | Тип события |
| entity\_id | int | ID сущности события |
| entity\_type | string | Сущность события |
| created\_by | int | ID пользователя, создавший событие |
| created\_at | int | Дата создания события, передается в Unix Timestamp |
| value\_after | array | Массив с изменениями по событию. Подробней о свойствах изменения читайте [тут](#events-params) |
| value\_before | array | Массив с изменениями по событию. Подробней о свойствах изменения читайте [тут](#events-params) |
| account\_id | int | ID аккаунта, в котором находится событие |

#### Пример ответа

```json
{
"id": "01pz58t6p04ymgsgfbmfyfy1mf",
"type": "lead\_added",
"entity\_id": 26060763,
"entity\_type": "lead",
"created\_by": 939801,
"created\_at": 1888888888,
"value\_after": [
{
"note": {
"id": 42743871
}
}
],
"value\_before": [],
"account\_id": 17079858,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/events/01pz58t6p04ymgsgfbmfyfy1mf"
}
},
"\_embedded": {
"entity": {
"id": 26060763,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/26060763"
}
}
}
}
}
```

#### Параметры для GET-параметра with

| Параметр | Описание |
| --- | --- |
| catalog\_elements | Добавляет в ответ связанные со сделками элементы списков |
| is\_price\_modified\_by\_robot | Добавляет в ответ свойство, показывающее, изменен ли в последний раз бюджет сделки роботом |
| loss\_reason | Добавляет в ответ расширенную информацию по причине отказа |
| contacts | Добавляет в ответ информацию о связанных со сделкой контактах |
| only\_deleted | Если передать данный параметр, то в ответе на запрос метода, вернутся удаленные сделки, которые еще находятся в корзине. В ответ вы получите модель сделки, у которой доступны дату изменения, ID пользователя сделавшего последнее изменение, её ID и параметр is\_deleted = true. |

### Значения для фильтра по значению до/после

В данный момент для фильтра по значению до/после доступны следующие значения:

- [leads\_statuses](#value_after_before_filter_leads_statuses) – фильтр по статусу сделки, доступен для события lead\_status\_changed
- [customers\_statuses](#value_after_before_filter_customers_statuses) – фильтр по статусу покупателя, доступен для события customer\_status\_changed
- [responsible\_user\_id](#value_after_before_filter_responsible_user_id) – фильтр по ответственному пользователю, доступен для события entity\_responsible\_changed
- [custom\_field\_values](#value_after_before_filter_custom_field_values) – фильтр по enum значению поля, доступен для события custom\_field\_{FIELD\_ID}\_value\_changed, в одном запросе должно передаваться не более 1 типа события.
- [value](#value_after_before_filter_value) – фильтр по точному значению, доступен для событий nps\_rate\_added, sale\_field\_changed, name\_field\_changed, ltv\_field\_changed, custom\_field\_value\_changed

##### Описание фильтра по значению до/после – leads\_statuses

Данный фильтр позволяет передать ID статусов и их воронок, чтобы получить только необходимые события смены статуса сделки.

Запрос должен быть составлен следующим образом:

```json
filter[value\_after][leads\_statuses][0][pipeline\_id]=13513&filter[value\_after][leads\_statuses][0][status\_id]=17079863
```

В примере мы получим все события смены статуса этапа сделки, где сделка перешла в этап 17079863 воронки 13513.

Вы можете передать несколько значений в фильтр. Ниже приведен пример по формированию такого фильтра используя язык PHP:

```php
$filter = [
'filter' => [
'value\_after' => [
'leads\_statuses' => [
[
'pipeline\_id' => 13513,
'status\_id' => 17079863,
],
[
'pipeline\_id' => 13513,
'status\_id' => 17079860,
],
],
],
],
];
$filterUri = http\_build\_query($filter);
//filter%5Bvalue\_after%5D%5Bleads\_statuses%5D%5B0%5D%5Bpipeline\_id%5D=13513&filter%5Bvalue\_after%5D%5Bleads\_statuses%5D%5B0%5D%5Bstatus\_id%5D=17079863&filter%5Bvalue\_after%5D%5Bleads\_statuses%5D%5B1%5D%5Bpipeline\_id%5D=13513&filter%5Bvalue\_after%5D%5Bleads\_statuses%5D%5B1%5D%5Bstatus\_id%5D=17079860
```

##### Описание фильтра по значению до/после – customers\_statuses

Данный фильтр позволяет передать ID статусов, чтобы получить только необходимые события смены статуса покупателя.

Запрос должен быть составлен следующим образом:

```json
filter[value\_after][customers\_statuses][0][status\_id]=135751
```

В примере мы получим все события смены статуса этапа покупателя, где покупатель перешел в этап 135751.

Вы можете передать несколько значений в фильтр. Ниже приведен пример по формированию такого фильтра используя язык PHP:

```php
$filter = [
'filter' => [
'value\_after' => [
'customers\_statuses' => [
[
'status\_id' => 135751,
],
[
'status\_id' => 135754,
],
],
],
],
];
$filterUri = http\_build\_query($filter);
//filter%5Bvalue\_after%5D%5Bcustomers\_statuses%5D%5B0%5D%5Bstatus\_id%5D=135751&filter%5Bvalue\_after%5D%5Bcustomers\_statuses%5D%5B1%5D%5Bstatus\_id%5D=135754
```

##### Описание фильтра по значению до/после – responsible\_user\_id

Данный фильтр позволяет передать ID пользователей, состоящих в аккаунте, через запятую, чтобы получить только необходимые события смены ответственного пользователя.

Запрос должен быть составлен следующим образом:

```php
filter[value\_after][responsible\_user\_id]=32321
```

В примере мы получим все события смены ответственного пользователя, где ID пользователя 448292.

Вы можете передать несколько значений в фильтр. Ниже приведен пример по формированию такого фильтра используя язык PHP:

```php
$filter = [
'filter' => [
'value\_after' => [
'responsible\_user\_id' => '3231,412314',
],
],
];
$filterUri = http\_build\_query($filter);
//filter%5Bvalue\_after%5D%5Bresponsible\_user\_id%5D=3221%2C412314
```

##### Описание фильтра по значению до/после – custom\_field\_values

Фильтр по **enum** значению поля, доступен для события custom\_field\_{FIELD\_ID}\_value\_changed, в одном запросе должно передаваться не более 1 типа события.

Данный фильтр позволяет передать **enum** значений поля, чтобы получить только необходимые события изменения значения поля.

Запрос должен быть составлен следующим образом:

```json
filter[value\_after][custom\_field\_values]=145&filter[type]=custom\_field\_57832\_value\_changed
```

В примере мы получим все события смены значения поля с ID 57832, где ID **enum** равен 145.

Вы можете передать несколько значений в фильтр. Ниже приведен пример по формированию такого фильтра используя язык PHP:

```php
$filter = [
'filter' => [
'value\_after' => [
'custom\_field\_values' => '145,157,202',
],
'type' => 'custom\_field\_57832\_value\_changed',
],
];
$filterUri = http\_build\_query($filter);
filter%5Bvalue\_after%5D%5Bcustom\_field\_values%5D=145%2C157%2C202&filter%5Btype%5D=custom\_field\_57832\_value\_changed
```

##### Описание фильтра по значению до/после – value

Данный фильтр позволяет передать значение до/после. Он работает только со следующими типами событий: nps\_rate\_added, sale\_field\_changed, name\_field\_changed, ltv\_field\_changed, custom\_field\_value\_changed.

Запрос должен быть составлен следующим образом:

```json
filter[value\_after][value]=155&filter[type]=sale\_field\_changed&filter[entity]=lead
```

В примере мы получим все события смены изменения бюджета, где бюджет сделок стал равен 155.

Ниже приведен пример по формированию такого фильтра используя язык PHP:

```php
$filter = [
'filter' => [
'value\_after' => [
'value' => '155',
],
'type' => 'sale\_field\_changed',
'entity' => 'lead',
],
];
$filterUri = http\_build\_query($filter);
//filter%5Bvalue\_after%5D%5Bvalue%5D=155&filter%5Btype%5D=sale\_field\_changed&filter%5Bentity%5D=lead
```

### Структуры данных в полях value\_after и value\_before

Структура данных в полях value\_after и value\_before зависит от типа события и может принимать разные значения.

Тип событий: **lead\_deleted, lead\_restored, contact\_deleted, contact\_restored, company\_deleted, company\_restored, customer\_deleted, entity\_merged, task\_added, task\_deleted, task\_completed**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after|value\_before | array | Пустой массив |

```json
{
"value\_after": [],
"value\_before": []
}
```

Тип события: **task\_text\_changed**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after|value\_before | array | Массив с изменениями по событию (у данного типа всегда только одно изменение в массиве) |
| value\_after|value\_before[0] | object | Объект с данными изменения |
| value\_after|value\_before[0][task] | object | Объект с данными изменения задачи |
| value\_after|value\_before[0][task][text] | string | Текст задачи |

```json
{
"value\_after": [
{
"task": {
"text": "задача"
}
}
],
"value\_before": [
{
"task": {
"text": "задача old"
}
}
],
}
```

Тип событий: **robot\_replie и intent\_identified**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after | array | Массив с изменениями по событию (у данного типа всегда только одно изменение в массиве) |
| value\_after[0] | object | Объект с данными изменения |
| value\_after[0][helpbot] | object | Объект с данными интента, который сработал |
| value\_after[0][helpbot][id] | int | ID интента |

```json
{
"value\_after": [
{
"helpbot": {
"id": 145
}
}
]
}
```

Тип события: **transaction\_added**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after | array | Массив с изменениями по событию (у данного типа всегда только одно изменение в массиве) |
| value\_after[0] | object | Объект с данными изменения |
| value\_after[0][transaction] | object | Объект с данными транзакции |
| value\_after[0][transaction][id] | int | ID транзакции |

```json
{
"value\_after": [
{
"transaction": {
"id": 33675
}
}
]
}
```

Тип событий: **lead\_added, contact\_added, company\_added, customer\_added, common\_note\_added, common\_note\_deleted, attachment\_note\_added, targeting\_in\_note\_added, targeting\_out\_note\_added, geo\_note\_added, service\_note\_added, site\_visit\_note\_added, message\_to\_cashier\_note\_added, incoming\_call, outgoing\_call, incoming\_sms, outgoing\_sms, link\_followed, task\_result\_added**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after | array | Массив с изменениями по событию (у данного типа всегда только одно изменение в массиве) |
| value\_after[0] | object | Объект с данными изменения |
| value\_after[0][note] | object | Объект с данными примечания |
| value\_after[0][note][id] | int | ID примечания |

```json
{
"value\_after": [
{
"note": {
"id": 7422564
}
}
]
}
```

Тип события: **nps\_rate\_added**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after | array | Массив с изменениями по событию (у данного типа всегда только одно изменение в массиве) |
| value\_after[0] | object | Объект с данными изменения |
| value\_after[0][nps] | object | Объект с данными оценки |
| value\_after[0][nps][rate] | int | Оценка от 0 до 10 |

```json
{
"value\_after": [
{
"nps": {
"rate": 7
}
}
]
}
```

Тип событий: **incoming\_chat\_message, outgoing\_chat\_message, entity\_direct\_message**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after | array | Массив с изменениями по событию (у данного типа всегда только одно изменение в массиве) |
| value\_after[0] | object | Объект с данными изменения |
| value\_after[0][message] | object | Объект с данными сообщения |
| value\_after[0][message][id] | string | ID сообщения |

```json
{
"value\_after": [
{
"message": {
"id": "1508b51c-aab0-428e-9322-611d847ae747"
}
}
]
}
```

Тип событий: **entity\_tag\_added и entity\_tag\_deleted**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after|value\_before | array | Массив с изменениями по событию |
| value\_after|value\_before[0] | object | Объект с данными изменения |
| value\_after|value\_before[0][tag] | object | Объект с данными тега |
| value\_after|value\_before[0][tag][name] | string | Название тега |

```json
{
"value\_after": [
{
"tag": {
"name": "тег1"
}
}
],
"value\_before": [
{
"tag": {
"name": "тег2"
}
},
{
"tag": {
"name": "тег2"
}
}
]
}
```

Тип события: **lead\_status\_changed**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after|value\_before | array | Массив с изменениями по событию |
| value\_after|value\_before[0] | object | Объект с данными изменения (у данного типа всегда только одно изменение в массиве) |
| value\_after|value\_before[0][lead\_status] | object | Объект с данными статуса |
| value\_after|value\_before[0][lead\_status][id] | int | ID статуса |
| value\_after|value\_before[0][lead\_status][pipeline\_id] | int | ID воронки |

```json
{
"value\_after": [
{
"lead\_status": {
"id": 5233224,
"pipeline\_id": 437642,
}
}
],
"value\_before": [
{
"lead\_status": {
"id": 5233224,
"pipeline\_id": 437642,
}
}
]
}
```

Тип события: **customer\_status\_changed**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after|value\_before | array | Массив с изменениями по событию |
| value\_after|value\_before[0] | object | Объект с данными изменения (у данного типа всегда только одно изменение в массиве) |
| value\_after|value\_before[0][customer\_status] | object | Объект с данными статуса |
| value\_after|value\_before[0][customer\_status][id] | int | ID статуса |

```json
{
"value\_after": [
{
"customer\_status": {
"id": 43832
}
}
],
"value\_before": [
{
"customer\_status": {
"id": 53791
}
}
]
}
```

Тип событий: **customer\_linked, customer\_unlinked, company\_linked, company\_unlinked, contact\_linked, contact\_unlinked, lead\_linked, lead\_unlinked, entity\_linked, entity\_unlinked**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after|value\_before | array | Массив с изменениями по событию (у данного типа всегда только одно изменение в массиве) |
| value\_after|value\_before[0] | object | Объект с данными изменения |
| value\_after|value\_before[0][link|unlink] | object | Объект с данными cобытия |
| value\_after|value\_before[0][link|unlink][entity] | object | Объект с сущностью |
| value\_after|value\_before[0][link|unlink][entity][type] | string | Тип сущности |
| value\_after|value\_before[0][link|unlink][entity][id] | int | ID сущности |

```json
{
"value\_after": [
{
"link": {
"entity": {
"type": "lead",
"id": 6232965
}
}
}
],
"value\_before": []
}
```

Тип события: **entity\_responsible\_changed**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after|value\_before | array | Массив с изменениями по событию |
| value\_after|value\_before[0] | object | Объект с данными изменения (у данного типа всегда только одно изменение в массиве) |
| value\_after|value\_before[0][responsible\_user] | object | Объект с данными пользователя |
| value\_after|value\_before[0][responsible\_user][id] | int | ID пользователя |

```json
{
"value\_after": [
{
"responsible\_user": {
"id": 504329
}
}
],
"value\_before": [
{
"responsible\_user": {
"id": 37268
}
}
]
}
```

Тип события: **task\_deadline\_changed**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after|value\_before | array | Массив с изменениями по событию |
| value\_after|value\_before[0] | object | Объект с данными изменения (у данного типа всегда только одно изменение в массиве) |
| value\_after|value\_before[0][task\_deadline] | object | Объект с данными срока выполнения задачи |
| value\_after|value\_before[0][task\_deadline][timestamp] | int | Timestamp срока выполнения задачи |

```json
{
"value\_after": [
{
"task\_deadline": {
"timestamp": 1573595900
}
}
],
"value\_before": [
{
"task\_deadline": {
"timestamp": 1573578700
}
}
]
}
```

Тип события: **task\_type\_changed**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after|value\_before | array | Массив с изменениями по событию |
| value\_after|value\_before[0] | object | Объект с данными изменения (у данного типа всегда только одно изменение в массиве) |
| value\_after|value\_before[0][task\_type] | object | Объект с данными типа задачи |
| value\_after|value\_before[0][task\_type][id] | int | ID типа задачи |

```json
{
"value\_after": [
{
"task\_type": {
"id": 504329
}
}
],
"value\_before": [
{
"task\_type": {
"id": 37268
}
}
]
}
```

Тип события: **custom\_field\_value\_changed**

| Параметр | Тип | Описание |
| --- | --- | --- |
| value\_after|value\_before | array | Массив с изменениями по событию |
| value\_after|value\_before[0] | object | Объект с данными изменения |
| value\_after|value\_before[0][custom\_field\_value] | object | Объект с данными изменения поля |
| value\_after|value\_before[0][custom\_field\_value][field\_id] | int | ID измененого поля |
| value\_after|value\_before[0][custom\_field\_value][field\_type] | int | Тип измененого поля |
| value\_after|value\_before[0][custom\_field\_value][enum\_id] | int|null | ID enum значения поля, null, если у поля нет enum значений |
| value\_after|value\_before[0][custom\_field\_value][text] | string | Текст значения поля |

```json
{
"value\_after": [
{
"custom\_field\_value": {
"field\_id": 53728,
"field\_type": 8,
"enum\_id": 2352876,
"text": "example1@test.com"
}
},
{
"custom\_field\_value": {
"field\_id": 53728,
"field\_type": 8,
"enum\_id": 2352876,
"text": "example@test.com"
}
}
],
"value\_before": [
{
"custom\_field\_value": {
"field\_id": 53728,
"field\_type": 8,
"enum\_id": 193200,
"text": "example@test.com"
}
}
]
}
```

### Типы событий

#### Возможные типы событий

| Значение | Описание |
| --- | --- |
| lead\_added | Новая сделка |
| lead\_deleted | Сделка удалена |
| lead\_restored | Сделка восстановлена |
| lead\_status\_changed | Изменение этапа продажи |
| lead\_linked | Прикрепление сделки |
| lead\_unlinked | Открепление сделки |
| contact\_added | Новый контакт |
| contact\_deleted | Контакт удален |
| contact\_restored | Контакт восстановлен |
| contact\_linked | Прикрепление контакта |
| contact\_unlinked | Открепление контакта |
| company\_added | Новая компания |
| company\_deleted | Компания удалена |
| company\_restored | Компания восстановлена |
| company\_linked | Прикрепление компании |
| company\_unlinked | Открепление компании |
| customer\_added | Новый покупатель |
| customer\_deleted | Покупатель удален |
| customer\_status\_changed | Изменение этапа покупателя |
| customer\_linked | Прикрепление покупателя |
| customer\_unlinked | Открепление покупателя |
| task\_added | Новая задача |
| task\_deleted | Задача удалена |
| task\_completed | Завершение задачи |
| task\_type\_changed | Изменение типа задачи |
| task\_text\_changed | Изменение текста задачи |
| task\_deadline\_changed | Изменение даты исполнения задачи |
| task\_result\_added | Результат по задаче |
| incoming\_call | Входящий звонок |
| outgoing\_call | Исходящий звонок |
| incoming\_chat\_message | Входящее сообщение |
| outgoing\_chat\_message | Исходящее сообщение |
| entity\_direct\_message | Сообщение внутреннего чата |
| incoming\_sms | Входящее SMS |
| outgoing\_sms | Исходящее SMS |
| entity\_tag\_added | Теги добавлены |
| entity\_tag\_deleted | Теги убраны |
| entity\_linked | Прикрепление |
| entity\_unlinked | Открепление |
| sale\_field\_changed | Изменение поля “Бюджет” |
| name\_field\_changed | Изменение поля “Название” |
| ltv\_field\_changed | Сумма покупок |
| custom\_field\_value\_changed | Изменение поля |
| entity\_responsible\_changed | Ответственный изменен |
| robot\_replied | Ответ робота |
| intent\_identified | Тема вопроса определена |
| nps\_rate\_added | Новая оценка NPS |
| link\_followed | Переход по ссылке |
| transaction\_added | Добавлена покупка |
| common\_note\_added | Новое примечание |
| common\_note\_deleted | Примечание удалено |
| attachment\_note\_added | Добавлен новый файл |
| targeting\_in\_note\_added | Добавление в ретаргетинг |
| targeting\_out\_note\_added | Удаление из ретаргетинга |
| geo\_note\_added | Новое примечание с гео-меткой |
| service\_note\_added | Новое системное примечание |
| site\_visit\_note\_added | Заход на сайт |
| message\_to\_cashier\_note\_added | LifePay: Сообщение кассиру |
| key\_action\_completed | Ключевое действие |
| entity\_merged | Выполнено объединение |
| custom\_field\_{FIELD\_ID}\_value\_changed | Изменение поля c переданным ID. Если вы передаете данный тип, то другие типы не могут быть переданы. |

### Получение типов событий

#### Метод

*GET /api/v4/events/types*

#### Описание

Метод позволяет получить все доступные для аккаунта типы событий.

#### Ограничения

Метод доступен всем пользователям аккаунта. Возвращаемые данные зависят от прав на сущность.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| language\_code | string | Код языка, в котором вернутся названия типов событий. Если не передан, то вернется в языке пользователя, под которым происходит запрос. Возможные параметры – en, es, ru, pt. |

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

Метод возвращает коллекцию моделей типов событий, рассмотрим ниже свойства.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| key | string | Код типа события |
| type | int | Идентификатор типа события |
| lang | string | Локализованное название события |

#### Пример ответа

```json
{
"\_total\_items": 35,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/events/types?limit=6"
}
},
"\_embedded": {
"events\_types": [
{
"key": "lead\_added",
"type": 1,
"lang": "Новая сделка"
},
{
"key": "lead\_deleted",
"type": 7,
"lang": "Сделка удалена"
},
...
]
}
}
```

### Особенности фильтрации событий по связанным сущностям

При фильтрации событий с типами:

- outgoing\_chat\_message
- incoming\_chat\_message

Если существует связанная с этим событием беседа, событие будет возвращаться с типом сущности lead или customer и включать поле linked\_talk\_contact\_id, которое содержит идентификатор связанного контакта.  
Если сделка/покупатель удалены, событие будет возвращаться с типом сущности contact.

**Важное замечание**  
Для корректной работы фильтра по этим типам событий стоит использовать значение contact в параметре фильтрации entity.  
То есть, возникаем известная нам неточность, фильтруем по контакту, а получаем данные с указанием другой сущности. В данный момент такое поведение является техническим нюансом.

Пример запроса:  
*GET /api/v4/events?filter[entity][]=contact*

### Общая информация о примечаниях

Примечания предоставляют возможность хранить дополнительную структурированную или неструктурированную информацию к сущности.  
Примечания отображаются в виде событий в карточке сущности. Они могут быть добавлены к следующим сущностям: сделка, контакт, компания и покупатель.  
Чаще всего примечания используются виджетами для добавления дополнительной информации, которая имеет привязку ко времени.  
Они всегда отображаются в хронологическом порядке в ленте и, если ваша информация привязана к дате (хронологии), то мы рекомендуем использовать именно примечания.  
Примечания бывают разных типов: системные (исходящее/входящее смс, исходящий/входящий звонок, счет оплачен, контакт создан и т.д.), созданные пользователем (текстовые примечания, файлы).  
В amoCRM существует 10 типов примечаний, которые можно редактировать.

### Типы примечаний

#### Возможные типы примечаний

| Тип | Название |
| --- | --- |
| common | Текстовое примечание |
| call\_in | Входящий звонок |
| call\_out | Исходящий звонок |
| service\_message | Системное сообщение (добавляется интеграциями) |
| message\_cashier | Сообщение кассиру |
| geolocation | Текстовое примечание с гео-координатами (добавляются мобильным приложением) |
| sms\_in | Входящее SMS |
| sms\_out | Исходящее SMS |
| extended\_service\_message | Расширенное системное сообщение (поддерживает больше текста и сворачивается в интерфейсе) |
| attachment | Примечание с файлом |

#### Типы примечаний, для которых обязателен массив params

```json
Тип примечания - common
"params": {
"text": "Обычное примечание"
}
Тип примечания - call\_in
"params": {
"uniq": "8f52d38a-5fb3-406d-93a3-a4832dc28f8b",
"duration": 60,
"source": "onlinePBX",
"link": "https://example.com",
"phone": "+79999999999",
"call\_responsible": "Василий"
}
Тип примечания - call\_out
"params": {
"uniq": "8f52d38a-5fb3-406d-93a3-a4832dc28f8b",
"duration": 60,
"source": "onlinePBX",
"link": "https://example.com",
"phone": "+79999999999",
"call\_responsible": 504141
}
Тип примечания - service\_message и extended\_service\_message
"params": {
"service": "Сервис для примера",
"text": "Текст для примечания"
}
Тип примечания - message\_cashier
"params": {
// Статус может быть один из следующих:
// - created
// - shown
// - canceled
"status": "created",
"text": "Текст для примечания"
}
Тип примечания - geolocation
"params": {
"text": "Геолокация",
"address": "ул. Пушкина, дом Колотушкина",
// долгота
"longitude": "-13",
// широта
"latitude": "32"
}
Тип примечания - sms\_in
"params": {
"text": "Новое входящие сообщение",
"phone": "+79999999999"
}
Тип примечания - sms\_out
"params": {
"text": "Новое исходящие сообщение",
"phone": "+79999999999"
}
Тип примечания - attachment
"params": {
"version\_uuid": "5e316440-4122-4cad-b121-9709882b4cc1", // версия файла, можно не передавать, будет использована последняя версия
"file\_uuid": "9905db7c-3a29-4d30-8953-bac68c05e8e8",
"file\_name": "изображение.png", // название файла, которое будет отображаться в примечании
}
```

### Список примечаний по типу сущности

#### Метод

*GET /api/v4/{entity\_type}/notes*

#### Описание

Метод позволяет получить примечания по типу сущности.

#### Ограничения

Метод доступен всем пользователям аккаунта. Возвращаемые данные зависят от прав на сущность.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| page | int | Страница выборки |
| limit | int | Количество возвращаемых сущностей за один запрос (Максимум – 250) |
| filter | object | Фильтр |
| filter[id] | int|array | Фильтр по ID примечаний. Можно передать как один ID, так и массив из нескольких ID |
| filter[entity\_id] | array | Фильтр по ID сущности. Можно передать массив из нескольких ID |
| filter[note\_type] | string|array | Фильтр по типу примечания. |
| filter[updated\_at] | int|object | Фильтр по дате последнего изменения примечания.  Можно передать timestamp, в таком случае будут возвращены примечания, которые были изменены после переданного значения.  Также можно передать массив вида filter[updated\_at][from]=… и filter[updated\_at][to]=…, для фильтрации по значениям ОТ и ДО. |
| order | object | Сортировка результатов списка. Доступные поля для сортировки: updated\_at, id. Доступные значения для сортировки: asc, desc. Пример: /api/v4/leads/notes?order[updated\_at]=asc |

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

Метод возвращает коллекцию моделей примечаний, рассмотрим ниже свойства примечаний.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID примечания |
| entity\_id | int | ID родительской сущности примечания |
| created\_by | int | ID пользователя, создавший примечание |
| updated\_by | int | ID пользователя, изменивший примечание последним |
| created\_at | int | Дата создания примечания, передается в Unix Timestamp |
| updated\_at | int | Дата изменения примечания, передается в Unix Timestamp |
| responsible\_user\_id | int | ID пользователя, ответственного за примечание |
| group\_id | int | ID группы, в которой состоит ответственны пользователь за примечание |
| note\_type | string | Тип примечания |
| params | object | Свойства примечания, зависят от типа примечания. Подробней о свойствах читайте [тут](#notes-params-info) |
| account\_id | int | ID аккаунта, в котором находится примечание |

#### Пример ответа

```json
{
"\_page": 1,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/notes?filter%5Bid%5D%5B0%5D=42709325&filter%5Bid%5D%5B1%5D=42709842&page=1&limit=50"
},
"next": {
"href": "https://example.amocrm.ru/api/v4/leads/notes?filter%5Bid%5D%5B0%5D=42709325&filter%5Bid%5D%5B1%5D=42709842&page=2&limit=50"
}
},
"\_embedded": {
"notes": [
{
"id": 42709325,
"entity\_id": 26050861,
"created\_by": 940088,
"updated\_by": 940088,
"created\_at": 1540407495,
"updated\_at": 1540408317,
"responsible\_user\_id": 939801,
"group\_id": 0,
"note\_type": "common",
"params": {
"text": "Текст примечания"
},
"account\_id": 17079858,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/26050861/notes/42709325"
}
}
},
{
"id": 42709842,
"entity\_id": 26053794,
"created\_by": 939801,
"updated\_by": 939801,
"created\_at": 1548280113,
"updated\_at": 1548280115,
"responsible\_user\_id": 939801,
"group\_id": 0,
"note\_type": "attachment",
"params": {
"is\_drive\_attachment": true,
"text": "Снимок экрана 2022-12-12 в 20.11.45 (1).jpg",
"original\_name": "Снимок экрана 2022-12-12 в 20.11.45 (1).jpg",
"file\_uuid": "6905db7c-3a29-4d30-8953-bac68c05e8e8",
"version\_uuid": "4e316440-4122-4cad-b121-9709882b4cc1",
"file\_name": "Snimok\_ekrana\_2022-12-12\_v\_20.11.45\_1\_.jpg"
},
"account\_id": 17079858,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/26053794/notes/42709842"
}
}
}
]
}
}
```

### Список примечаний по конкретной сущности, по ID сущности

#### Метод

*GET /api/v4/{entity\_type}/{entity\_id}/notes*

#### Описание

Метод позволяет получить примечания по ID родительской сущности.

#### Ограничения

Метод доступен всем пользователям аккаунта. Возвращаемые данные зависят от прав на сущность.

#### GET параметры

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| page | int | Страница выборки |
| limit | int | Количество возвращаемых сущностей за один запрос (Максимум – 250) |
| filter | object | Фильтр |
| filter[id] | int|array | Фильтр по ID примечаний. Можно передать как один ID, так и массив из нескольких ID |
| filter[note\_type] | string|array | Фильтр по типу примечания. |
| filter[updated\_at] | int|object | Фильтр по дате последнего изменения примечания.  Можно передать timestamp, в таком случае будут возвращены примечания, которые были изменены после переданного значения.  Также можно передать массив вида filter[updated\_at][from]=… и filter[updated\_at][to]=…, для фильтрации по значениям ОТ и ДО. |
| order | object | Сортировка результатов списка. Доступные поля для сортировки: updated\_at, id. Доступные значения для сортировки: asc, desc. Пример: /api/v4/leads/notes?order[updated\_at]=asc |

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

Метод возвращает коллекцию моделей примечаний, рассмотрим ниже свойства примечаний.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID примечания |
| entity\_id | int | ID родительской сущности примечания |
| created\_by | int | ID пользователя, создавший примечание |
| updated\_by | int | ID пользователя, изменивший примечание последним |
| created\_at | int | Дата создания примечания, передается в Unix Timestamp |
| updated\_at | int | Дата изменения примечания, передается в Unix Timestamp |
| responsible\_user\_id | int | ID пользователя, ответственного за примечание |
| group\_id | int | ID группы, в которой состоит ответственны пользователь за примечание |
| note\_type | string | Тип примечания |
| params | object | Свойства примечания, зависят от типа примечания. Подробней о свойствах читайте [тут](#notes-params-info) |
| account\_id | int | ID аккаунта, в котором находится примечание |

#### Пример ответа

```json
{
"\_page": 1,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/26050861/notes?limit=2&page=1"
},
"next": {
"href": "https://example.amocrm.ru/api/v4/leads/26050861/notes?limit=2&page=2"
}
},
"\_embedded": {
"notes": [
{
"id": 42709325,
"entity\_id": 26050861,
"created\_by": 940088,
"updated\_by": 940088,
"created\_at": 1540407495,
"updated\_at": 1540408317,
"responsible\_user\_id": 939801,
"group\_id": 0,
"note\_type": "common",
"params": {
"text": "Текст примечания 2"
},
"account\_id": 17079858,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/26050861/notes/42709325"
}
}
},
{
"id": 42736075,
"entity\_id": 26050861,
"created\_by": 939801,
"updated\_by": 939801,
"created\_at": 1587555198,
"updated\_at": 1587555199,
"responsible\_user\_id": 939801,
"group\_id": 0,
"note\_type": "common",
"params": {
"text": "Текст примечания"
},
"account\_id": 17079858,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/26050861/notes/42736075"
}
}
}
]
}
}
```

### Получение примечания по ID

#### Метод

*GET /api/v4/{entity\_type}/notes/{id}*

*GET /api/v4/{entity\_type}/{entity\_id}/notes/{id}*

#### Описание

Метод позволяет получить данные конкретного примечания по ID.

#### Ограничения

Метод доступен всем пользователям аккаунта. Возвращаемые данные зависят от прав на сущность.

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

Метод возвращает модель примечания, рассмотрим ниже свойства примечания.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID примечания |
| entity\_id | int | ID родительской сущности примечания |
| created\_by | int | ID пользователя, создавший примечание |
| updated\_by | int | ID пользователя, изменивший примечание последним |
| created\_at | int | Дата создания примечания, передается в Unix Timestamp |
| updated\_at | int | Дата изменения примечания, передается в Unix Timestamp |
| responsible\_user\_id | int | ID пользователя, ответственного за примечание |
| group\_id | int | ID группы, в которой состоит ответственны пользователь за примечание |
| note\_type | string | Тип примечания |
| params | object | Свойства примечания, зависят от типа примечания. Подробней о свойствах читайте [тут](#notes-params-info) |
| account\_id | int | ID аккаунта, в котором находится примечание |

#### Пример ответа

```json
{
"id": 42709325,
"entity\_id": 26050861,
"created\_by": 940088,
"updated\_by": 940088,
"created\_at": 1540407495,
"updated\_at": 1540408317,
"responsible\_user\_id": 939801,
"group\_id": 0,
"note\_type": "common",
"params": {
"text": "Текст примечания"
},
"account\_id": 17079858,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/26050861/notes/42709325"
}
}
}
```

### Добавление примечаний

#### Метод

*POST /api/v4/{entity\_type}/notes*

*POST /api/v4/{entity\_type}/{entity\_id}/notes*

#### Описание

Метод позволяет добавлять примечания в аккаунт пакетно.

#### Ограничения

Метод доступен всем пользователям аккаунта. Успешность выполнения действия зависит от прав на сущность.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| entity\_id | int | ID сущности, в которую добавляется примечание. Обязателен при использовании метода создания примечания в сущности, если создание идет через метод /api/v4/{entity\_type}/{entity\_id}/notes, то данный параметр передавать не нужно |
| created\_by | int | ID пользователя, от имени которого добавляется примечание. При добавлении звонка, в таймлайне карточки, пользователь будет отображен как автор звонка или как принимающий, в зависимости от типа звонка |
| note\_type | string | Тип примечания. [Возможные типы примечаний](#notes-types) |
| responsible\_user\_id | int | ID пользователя, ответственного за примечание. Необязательный параметр. |
| params | object | Свойства примечания, зависят от типа примечания. Подробней о свойствах читайте [тут](#notes-params-info) |
| request\_id | string | Поле, которое вернется вам в ответе без изменений и не будет сохранено. Необязательный параметр |
| is\_need\_to\_trigger\_digital\_pipeline | bool | Нужно ли отправлять события в Digital Pipeline. Необязательный параметр. Если флаг не передан или передан со значением true, триггеры Digital Pipeline отрабатывать будут, если передано false – не будут. Влияет такие триггеры: счет оплачен, звонок соверешен и другие, которые запускаются при добавлении примечания. |

#### Пример запроса

```json
[
{
"entity\_id": 167353,
"note\_type": "call\_in",
"responsible\_user\_id": 8238874,
"params": {
"uniq": "8f52d38a-5fb3-406d-93a3-a4832dc28f8b",
"duration": 60,
"source": "onlinePBX",
"link": "https://example.com",
"phone": "+79999999999"
}
},
{
"entity\_id": 167353,
"note\_type": "call\_out",
"responsible\_user\_id": 8238874,
"params": {
"uniq": "8f52d38a-5fb3-406d-93a3-a4832dc28f8b",
"duration": 60,
"source": "onlinePBX",
"link": "https://example.com",
"phone": "+79999999999"
}
},
{
"entity\_id": 167353,
"note\_type": "geolocation",
"responsible\_user\_id": 8238874,
"params": {
"text": "Примечание с геолокацией",
"address": "ул. Пушкина, дом Колотушкина, квартира Вольнова",
"longitude": "53.714816",
"latitude": "91.423146"
}
}
]
```

#### Пример запроса для отображения в разделе "Аналитика" для примечаний типа call\_in и call\_out.

Для того, чтобы в разделе "Аналитика" по указанному user\_id отображались звонки, необходимо передавать следующие параметры.  
При этом responsible\_user\_id и created\_by **должны быть одинаковыми**

```json
[
{
"note\_type": "call\_in",
"created\_by": 32321,
"responsible\_user\_id": 32321,
"params": {
"uniq": "8f52d38a-5fb3-406d-93a3-a4832dc28f8b",
"duration": 60,
"source": "onlinePBX",
"link": "https://example.com",
"phone": "+79999999999"
}
},
{
"note\_type": "call\_out",
"created\_by": 32321,
"responsible\_user\_id": 32321,
"params": {
"uniq": "8f52d38a-5fb3-406d-93a3-a4832dc28f8b",
"duration": 60,
"source": "onlinePBX",
"link": "https://example.com",
"phone": "+79999999999"
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
| 200 | Примечания были успешно созданы |
| 403 | Не хватает прав для вызова данного метода |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает коллекцию примечаний, которые были созданы.

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| id | int | ID примечания |
| entity\_id | int | ID сущности, в которое было добавлено примечание |
| request\_id | string | Строка переданная при запросе или порядковый указатель, если параметр не передан |

#### Пример ответа

```json
{
"\_links": {
"self": {
"href": "http://example.amocrm.ru/api/v4/leads/notes"
}
},
"\_embedded": {
"notes": [
{
"id": 76787983,
"entity\_id": 167353,
"request\_id": "0",
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/167353/notes/76787983"
}
}
},
{
"id": 76787985,
"entity\_id": 167353,
"request\_id": "1",
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/167353/notes/76787985"
}
}
},
{
"id": 76787987,
"entity\_id": 167353,
"request\_id": "2",
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/167353/notes/76787987"
}
}
},
{
"id": 76787989,
"entity\_id": 167353,
"request\_id": "3",
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/167353/notes/76787989"
}
}
}
]
}
}
```

### Редактирование примечаний

#### Метод

*PATCH /api/v4/{entity\_type}/notes*

*PATCH /api/v4/{entity\_type}/{entity\_id}/notes*

*PATCH /api/v4/{entity\_type}/{entity\_id}/notes/{id}*

#### Описание

Метод позволяет редактировать примечания пакетно.  
Также вы можете добавить ID примечания в метод для редактирования конкретного примечания (/api/v4/{entity\_type}/{entity\_id}/notes/{id}).  
При редактировании пакетно передается массив из объектов-примечаний, при редактировании одного примечания, передается просто модель.

#### Ограничения

Метод доступен всем пользователям аккаунта. Успешность выполнения действия зависит от прав на сущность.

#### Заголовок запроса

*Content-Type: application/json*

#### Параметры запроса

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| entity\_id | int | ID сущности, в которую добавляется примечание. Обязателен при использовании метода создания примечания в сущности, если создание идет через метод /api/v4/{entity\_type}/{entity\_id}/notes, то данный параметр передавать не нужно |
| note\_type | string | Тип примечания. [Возможные типы примечаний](#notes-types) |
| params | object | Свойства примечания, зависят от типа примечания. Подробней о свойствах читайте [тут](#notes-params-info) |

#### Пример запроса

```json
[
{
"id": 76610421,
"note\_type": "sms\_in",
"params": {
"text": "Новое входящие SMS",
"phone": "+79999999999"
}
},
{
"id": 76610423,
"note\_type": "sms\_out",
"params": {
"text": "Новое исходящие SMS",
"phone": "+79999999999"
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
| 200 | Списки были успешно изменены |
| 401 | Пользователь не авторизован |
| 400 | Переданы некорректные данные. Подробности доступны в теле ответа |

#### Параметры ответа

Метод возвращает коллекцию или модель списка, которые были изменены. Параметры аналогичны тем, что возвращаются при создании примечания.

#### Пример ответа

```json
{
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/notes"
}
},
"\_embedded": {
"notes": [
{
"id": 76610421,
"entity\_id": 167353,
"updated\_at": 1588841241,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/167353/notes/76610421"
}
}
},
{
"id": 76610423,
"entity\_id": 167353,
"updated\_at": 1588841241,
"\_links": {
"self": {
"href": "https://example.amocrm.ru/api/v4/leads/167353/notes/76610423"
}
}
}
]
}
}
```