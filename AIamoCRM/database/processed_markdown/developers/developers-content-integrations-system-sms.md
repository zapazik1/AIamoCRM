---
title: "Отправка системных SMS"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/integrations/system/sms
section: developers
---

### Возможности и принципы работы системных SMS

Начиная с релиза “Осень 2020”, мы вводим понятие, как отправка системных SMS сообщений. Сейчас виджеты с поддержкой этой возможности могут быть использованы для отправки SMS с кодами авторизации в личном кабинете. В будущем могут появиться новые места, где необходимо будет использовать SMS.

#### Начало работы

Чтобы существующий или новый виджет начал поддерживать функционал системных SMS, вам необходимо добавить новый объект sms и указать дополнительный location sms в [файле manifest.json](/developers/content/integrations/structure#manifest).

**Location sms** говорит о том, что виджет готов к работе в роли отправителя системных SMS. **Объект sms со строковым свойством endpoint** должен иметь в себе адрес, на который будет отправлен **POST** запрос c информацией, которая необходима для отправки SMS. Информация придет с заголовком “Content-Type: application/x-www-form-urlencoded”. Адрес должен быть валидным и доступным уже в момент загрузки архива виджета.

#### Пример manifest.json

```
{
"widget": {
"interface\_version": 2,
"init\_once": false,
"locale": [
"ru"
],
"installation": true
},
"locations": [
"lcard-1",
"digital\_pipeline",
"settings",
"sms"
],
"settings": {
"login": {
"name": "settings.login",
//указывает на файл локализации, в папке i18n
"type": "text",
//тип: текстовое поле
"required": false
},
"password": {
"name": "settings.password",
//указывает на файл локализации, в папке i18n
"type": "pass",
//тип: пароль
"required": false
}
},
"dp": {
"settings": {
"message": {
"name": "settings.message",
"type": "text",
"required": true
}
},
"action\_multiple": false
},
"sms": {
"endpoint": "https://example.com/sms\_endpoint"
}
}
```

#### Параметры отправляемого запроса

В теле запроса будет передан массив, содержащий 3 ключа: text, phone и token. Ниже рассмотрим данных этого массива:

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| text | string | Подготовленный текст для отправки в сообщении |
| phone | string | Подготовленный номер в международном формате, на который необходимо отправить SMS сообщение |
| token | string | JWT токен, который позволит идентифицировать аккаунт, из которого сделан запрос. Используется токен, описание которого доступно в [статье](/developers/content/oauth/disposable-tokens). Обязательно валидируйте подпись полученного токена, это позволит быть уверенными, что запрос пришел из amoCRM. |

#### Пример тела запроса

```
{
"text": "Код для входа в личный кабинет - 834622",
"phone": "+79123456789",
"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkV4YW1wbGUgYW1vQ1JNIFRPS0VOIiwiaWF0IjoxNjA4MjQxNjU4fQ.GkL8yEXAAQ4yaM1M9gpY01zVJur9FJ9Nfed63vxN\_J4"
}
```