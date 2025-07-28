---
title: "Интеграция виджета в Salesbot"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/integrations/salesbot/widget
section: developers
---

# *Файл manifest.json*

**1.** Указать интерфейс в области видимости

#### Пример:

```javascript
"locations":[
"salesbot\_designer"
],
```

**2.** В сам манифест добавляется объект salesbot\_designer Данный объект описывает поля для отображения интерфейса настроек виджета в конфигураторе

#### Пример:

```javascript
"salesbot\_designer": {
"logo": "/widgets/testWidgetShrek/images/shrek.jpg",
"handler\_name": {
"name": "settings.handler\_name",
"settings": {
"text": {
"name": "settings.text",
"default\_value": "Hello, i am Salesbot!",
"type": "text", // В зависимости от указанного типа будут
// предложены для выбора поля разного типа. numeric - текстовые и числовые
// поля, text - текстовые поля, url - поля типа текст и ссылка
"manual": true, // true - пользователь должен ввести значение,
// false - пользователь выбирает значение поля
},
"link\_to": {
"name": "settings.link",
"default\_value": "www.amocrm.com",
"type": "url",
}
}
}
}
```

![](https://i.postimg.cc/pXp83zcS/new-salesbot.png)

### *Файл script.js*

Настройки каждого из handler’ов прописываются в файле manifest.json, а затем уже в готовом виде используются в коде salesbot

Все допустимые параметры handler размещены здесь – [Обработчики Salesbot](https://www.amocrm.ru/developers/content/digital_pipeline/salesbot#handlers)

События в callbacks:

#### onSalesbotDesignerSave

Метод срабатывает, когда пользователь в конструкторе Salesbot размещает один из хендлеров, описанных в manifest.json Метод должен вернуть строку вида JSON кода salesbot’а

Принимает на вход:

- handler\_code – Код хендлера объекта в объекте salesbot\_designer
- params – Передаются настройки виджета формата

```javascript
{
"text": "Hello, i am Salesbot!",
"link\_to": "www.amocrm.com"
}
```

#### Пример работы метода

```javascript
onSalesbotDesignerSave: function (handler\_code, params) {
var salesbot\_source = {
question: [],
require: [],
},
values = [];
salesbot\_source.question.push({ type: 'text' });
$.each(params, (param) => {
values.push(param);
});
salesbot\_source.question.push({
values: values,
});
salesbot\_source.question.push({ accept\_unsorted: 'false' });
return JSON.stringify([salesbot\_source]);
};
```

#### salesbotDesignerSettings

Метод рендера содержимого окна настроек виджета, вызываемого из конфигуратора salesbot’a. Метод может вернуть объект с ключом exists, в котором будут содержаться возможные выходы из блока виджета в боте. В массиве exists должны содержаться объекты с ключами code (код выхода) и title (Название выхода).

Принимает на вход:

- body – Объект DOM
- renderRow – Функция описана ниже
- params – Настройки уже созданного хендлера

```javascript
function(caption) {
return twig({
ref: '/tmpl/salesbot\_designer/controls/widget\_param.twig',
}).render({
caption: caption,
is\_widget: true,
});
}
```

#### Пример c jQuery

```javascript
salesbotDesignerSettings: function ($body, renderRow, params) {
var use\_catalog =
$body
.find('[data-field-name="invoice\_catalog"][name = "value\_manual"]')
.val() == 'true',
$catalog\_switcher = $(renderRow())
.append(self.langs.invoice\_catalog)
.append(
self.render(
{
ref: '/tmpl/controls/switcher.twig',
},
{
checked: use\_catalog,
custom\_class\_name: 'switcher\_blue',
id: 'stripe\_invoice\_catalog',
},
),
);
return {
exits: [
{ code: 'success', title: self.i18n('salesbot').success\_callback\_title },
{ code: 'fail', title: self.i18n('salesbot').fail\_callback\_title },
],
};
}
```

#### Пример интеграции с хуками для Salesbot

```javascript
salesbotDesignerSettings: function ($body, rowTemplate, params) {
// Логика рендера
return {
exits: [
{ code: 'success', title: self.i18n('salesbot').success\_callback\_title },
{ code: 'fail', title: self.i18n('salesbot').fail\_callback\_title },
],
};
},
onSalesbotDesignerSave: function (handler\_code, params) {
var request\_data = {
message: params.message,
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
handler: 'widget\_request',
params: {
url: 'https://example.com/webhook',
data: request\_data,
},
},
{
handler: 'goto',
params: {
type: 'question',
step: 1,
},
},
],
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
operation: '=',
},
],
result: [
{
handler: 'exits',
params: {
value: 'success',
},
},
],
},
},
{
handler: 'exits',
params: {
value: 'fail',
},
},
],
},
]);
},
```