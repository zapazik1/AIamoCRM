---
title: "Уведомление о звонке"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/telephony/call/event
section: developers
---

С помощью метода API можно добавлять уведомление о том, что в данный момент происходит звонок по определенному номеру телефона.

![](https://i.postimg.cc/mkS16pm7/phone-call.png)

При этом система автоматически найдет контакт или компанию с этим номером телефона, а также все связанные сущнонсти и покажет в уведомлении одну из них со следующим приоритетом:

- если у контакта/компании есть одна активная сделка, и нет связанных покупателей то будет показана сделка
- если у контакта/компании есть один покупатель и нет активных сделок, то будет показан покупатель
- в случае если у контакта/компании более одной активной сделки/покупателя или связанные сущности отсутствуют, то будет показана карточка контакта/компании

Если же такого номера в системе еще нет, то в уведомлении будет предложено создать контакт с этим номером.

Этот способ уведомления о звонке позволит не делать лишних запросов на поиск сущностей по номеру телефона через API. Что значительно оптимизирует работу интегрируемых телефоний. Теперь достаточно создать запрос через бэкэнд к данному API методу, передав номер телефона и список пользователей, которые сразу в аккаунте получат уведомление о звонке. И также по описанному выше алгоритму, получат в уведомлении наиболее актуальную в данный момент сущность, связанную с переданным номером телефона.

##### URL метода

*POST /api/v2/events/*

#### Параметры

| Параметр | Тип | Описание |
| --- | --- | --- |
| type *require* | string | Тип уведомления – phone\_call |
| users | array | int | string | Id пользователей для которых будет отправлено уведомление. Если не передавать этот параметр, то уведомление будет отправлено для всех пользователей |
| phone\_number *require* | string | Номер телефона на который поступает звонок. Можно передавать в любом формате |

#### Пример запроса

Приведём пример запроса на добавление уведомления.

```json
{
add: [
{
type: "phone\_call",
phone\_number: "+79998885533",
users: [88888, 99999]
}
]
}
```

#### Описание параметров ответа

| Параметр | Тип | Описание |
| --- | --- | --- |
| element\_id | int | null | Уникальный идентификатор сущности для которой было вызвано уведомление, если сущность не была найдена то вернется null |
| element\_type | int | null | Тип сущности для которой было вызвано уведомление, если сущность не была найдена то вернется null |
| uid | string | Уникальный идентификатор уведомления |
| phone\_number | string | Номер телефона по которому вызвано уведомление |

Response Headeres содержит следующие заголовки:

- Content-Type:application/hal+json

#### Пример ответа

```json
{
\_links: {
self: {
href: "/api/v2/events",
method: "post"
}
},
\_embedded: {
items: [
{
element\_id: 1234565,
element\_type: 2,
uid: "0e3455ff-67aa-4779-bebe-66ddc038a4ee",
phone\_number: "+79998885533"
}
]
}
}
```

Приведём пример запроса для добавления уведомлений о звонке.

#### Пример интеграции на фронтенде

```js
define(['jquery'], function($){
// Пример виджета, добавляющего уведомления о звонке при рендере
var CustomWidget = function () {
var self = this,
data = {
add: [{
type: "phone\_call", //тип уведомления
phone\_number: "+78005553535", //номер, на который поступает звонок
users: [Object.keys(APP.constant('account').users)[0]]
// id пользователей, которым придет уведомление. Если не указывать, то придет всем пользователям в аккаунте
// Получить массив id пользователей аккаунта следующим образом: Object.keys(APP.constant('account').users)
}]
};
this.callbacks = {
render: function() {
$.ajax({
url: '/api/v2/events/',
type: 'POST',
contentType: "application/json; charset=utf-8",
dataType: "json",
data: JSON.stringify(data)
}).then(function(res) {
// res.element\_id - уникальный id сущности, для которой было вызвано уведомление
// res.element\_type - тип сущности для которой было вызвано уведомление
// res.uid - id уведомления
// res.phone\_number - номер телефона, по которому вызвано уведомление
});
return true;
},
init: function() {
console.log('init');
return true;
},
settings: function($modal\_body) {
return true;
},
onSave: function(){
console.log('click');
return true;
}
};
return this;
};
return CustomWidget;
});
```

#### Пример интеграции на бэкенде

```php
$calls\_event['add'] = [
[
'phone\_number' => '+79998885533',
'users' => [88888, 99999],
'type' => 'phone\_call'
]
];
#Формируем ссылку для запроса
$link = 'https://mysubdomain.amocrm.ru/api/v2/events';
$curl = curl\_init(); #Сохраняем дескриптор сеанса cURL
#Устанавливаем необходимые опции для сеанса cURL
curl\_setopt($curl, CURLOPT\_POST, TRUE);
curl\_setopt($curl, CURLOPT\_RETURNTRANSFER, TRUE);
curl\_setopt($curl, CURLOPT\_USERAGENT, 'amoCRM-API-client/1.0');
curl\_setopt($curl, CURLOPT\_HEADER, FALSE);
curl\_setopt($curl, CURLOPT\_TIMEOUT, 10);
curl\_setopt($curl, CURLOPT\_SSL\_VERIFYPEER, 0);
curl\_setopt($curl, CURLOPT\_SSL\_VERIFYHOST, 0);
curl\_setopt($curl, CURLOPT\_URL, $link);
curl\_setopt($curl, CURLOPT\_POSTFIELDS, http\_build\_query($calls\_event));
$out = curl\_exec($curl); #Инициируем запрос к API и сохраняем ответ в переменную
$code = curl\_getinfo($curl, CURLINFO\_HTTP\_CODE);
$code = (int)$code;
$response = json\_decode($out, TRUE);
if (count($response ['\_embedded'] ['items']) > 0 ) {
$output .= 'Успешно добавленные звонки:' . PHP\_EOL;
foreach ($response ['\_embedded'] ['items'] as $v) {
$output .= $v . PHP\_EOL;
}
}
```