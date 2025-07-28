---
title: "Salesbot"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/web/sdk/salesbot-2
section: developers
---

В amoCRM есть возможность автоматизировать рутинные процессы с помощью создания ботов и, конечно же, мы даем возможность расширения функциональности ботов с помощью виджетов. Для работы виджета в конструкторе ботов необходимо выполнить следующие шаги:

Указать локейшн конструктора ботов в **manifest.json**:

```
{
...
"locations": [
"salesbot\_designer"
],
...
}
```

Также в **manifest.json** добавить объект **salesbot\_designer**. Данный объект описывает поля для отображения интерфейса настроек виджета в конструкторе:

```
{
...
"salesbot\_designer": {
"logo": "/widgets/testWidgetShruk/images/shrek.jpg",
"handler\_sms": {
"name": "settings.handler\_sms",
"settings": {
"phone": {
"name": "settings.phone",
"default\_value": "+7 912 345 67 89",
"type": "text"
},
}
},
"handler\_email": {
"name": "settings.handler\_email",
"settings": {
"email": {
"name": "settings.email",
"default\_value": "example@email.com",
"type": "text"
},
}
}
},
...
}
```

Как мы видим, один виджет может предоставлять несколько вариантов использования в рамках конструктора, например, виджет может иметь возможность отправить СМС или E-mail как в примере выше.

У полей в свойстве **settings** могут быть следующие варианты type:

- **text** – текстовые поля
- **numeric** – числовые поля
- **url** – ссылка

Если данные настройки указаны верно, то виджет появится в модальном окне виджетов конструктора.

![](https://i.postimg.cc/W3L3Y7XM/image1-5.png)

При нажатии пользователем на кнопку добавить под виджетом отработает колбэк **salesbotDesignerSettings**. С помощью данного колбэка вы можете изменить внешний вид кубика своего виджета в конструкторе. На вход колбэк принимает следующие параметры:

- body – jQuery-объект кубика виджета
- renderRow – функция, которая в параметр получает название поля, и возвращает разметку поля в стилях конструктора

Пример реализации данного колбэка:

```
this.callbacks = {
...
salesbotDesignerSettings: function ($body, renderRow) {
$body.find('[data-field-name="sms"]')
.replaceWith(
$(renderRow('SMS'))
.append('Кастомная разметка здесь')
);
return {
exits: [
{ code: 'success', title: 'При успешном выполнении' },
{ code: 'fail', title: 'При ошибке' }
]
};
},
...
}
```

Виджета может иметь как один, так и несколько вариантов результата выполнения (например, выполнение может завершиться с ошибкой и бота надо направить по альтернативному сценарию), колбэк **salesbotDesignerSettings** должен возвращать объект с ключом exits, как в примере выше. Выглядеть это будет так:

![](https://i.postimg.cc/QtJX4ZB3/image2-2.png)

После того, как пользователь настроил свою цепочку в конструкторе и нажал на кнопку “Сохранить” в виджете выполяется колбэк **onSalesbotDesignerSave**, который должен генерировать код для виджета с учетом данных кодов выходов из бота. Пример:

```
onSalesbotDesignerSave: function (handler\_code, params) {
var request\_data = {
message: params.message,
amouser: '{{admin.login}}'
};
if (APP.getBaseEntity() === 'customers') {
request\_data.customer = '{{customer.id}}';
} else {
request\_data.lead = '{{lead.id}}';
}
return JSON.stringify([
{
question: [
{
handler: 'request',
params: {
url: send\_sms\_url,
method: 'POST',
json: false,
data: request\_data
}
},
{
handler: 'goto',
params: {
type: 'question',
step: 1
}
}
]
},
{
question: [
{
handler: 'conditions',
params: {
logic: 'and',
conditions: [
{
term1: '{{json.status}}',
term2: 'success',
operation: '='
}
],
result: [
{
handler: 'exits',
params: {
value: 'success'
}
}
]
}
},
{
handler: 'exits',
params: {
value: 'fail'
}
}
]
}
]);
}
```

В данном примере виджет отправки смс отправляет запрос к себе в сервис для отправки сообщения, при получении ответа идет в блок с условием и если статус ответа равен успеху, то идет в выход succes, если же отправка не удалась и пришла ошибка, то идет в fail и если у пользователя в боте настроена цепочка на ошибку (например, если не смогли отправить смс, то отправим клиенту email), то бот пойдет по ней.