---
title: "Подписка на уведомления"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/notifications/js-subscribe
section: developers
---

В amoCRM доступен функционал подписки на получение уведомлений.

Он доступен только для виджетов, у которых в manifest.json указан параметр – [init\_once: ‘Y’](https://www.amocrm.ru/developers/content/integrations/areas).

##### Название метода

APP.addNotificationCallback(widget\_code, callback(data))

#### Параметры

| Параметр | Обязательный | Описание |
| --- | --- | --- |
| widget\_code | Да | Код виджета, который подписывается на уведомления |
| callback(data) | Да | Функция для обработки входящих событий |

#### Пример

```
APP.addNotificationCallback('test', function (data) {
console.log(data);
});
```

#### Пример переданного параметра в callback

```
{
"id": "6ea1aaa1-2633-5832-8550-4665242fc155",
"entity": null,
"linked\_entity": null,
"created\_at": 1566922308,
"updated\_at": 1566922308,
"is\_read": false,
"silent": false,
"body": {
"title": "Звонок",
"icon": {
"call": true,
"value": "/frontend/images/interface/inbox/notifications\_call.svg"
},
"rows": [
{
"style": "default",
"text": "+79999999999",
"class\_height": "h3"
}
],
"actions": {
"click": {
"url": "/contacts/add/?phone=+79999999999"
},
"buttons": [
{
"url": "/contacts/add/?phone=+79999999999",
"title": "+79999999999",
"web\_link": "/contacts/add/?phone=+79999999999",
"absolute\_link": false
}
],
"read\_on\_show": true
}
},
"uuid": "ca6e2205-a591-40d0-bfc6-b48f31bd12fd",
"notification\_id": "6ea1aaa1-2633-5832-8550-4665242fc155",
"click": {
"type": "url",
"value": "/contacts/add/?phone=+79999999999"
},
"web\_link": "/contacts/add/?phone=+79999999999",
"absolute\_link": false,
"buttons": [
{
"url": "/contacts/add/?phone=+79999999999",
"title": "+79999999999",
"web\_link": "/contacts/add/?phone=+79999999999",
"absolute\_link": false
}
],
"notification": true
}
```