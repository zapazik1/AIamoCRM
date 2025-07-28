---
title: "JS-Виджет"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/integrations/script/js
section: developers
---

#### Разработка script.js

Разберем общую структуру script.js:

Данная часть виджета состоит из основных обязательных частей, которые мы рассмотрим. Так же script.js может содержать дополнительные функции. Разберем начальный каркас данного файла.

Весь виджет представляется в виде объекта. Когда система загружает виджеты, она расширяет существующий системный объект Widget функционалом описанным в script.js. Таким образом объект CustomWidget наследует свойства и методы, которые будут полезны для работы и разобраны далее. Объект имеет функции обратного вызова, которые вызываются при определенных условиях. Данные функции перечислены в таблице после примера кода script.js.

#### Общий вид **script.js**

```
define(['jquery'], function ($) {
var CustomWidget = function () {
var self = this, // для доступа к объекту из методов
system = self.system(), //Данный метод возвращает объект с переменными системы.
langs = self.langs; //Объект локализации с данными из файла локализации (папки i18n)
this.callbacks = {
settings: function () {},
init: function () {
return true;
},
bind\_actions: function () {
return true;
},
render: function () {
return true;
},
dpSettings: function () {},
advancedSettings: function () {},
destroy: function () {},
contacts: {
selected: function () {}
},
onSalesbotDesignerSave: function (handler\_code, params) {},
leads: {
selected: function () {}
},
todo: {
selected: function () {}
},
onSave: function () {},
onAddAsSource: function (pipeline\_id) {}
};
return this;
};
return CustomWidget;
});
```

#### Функции обратного вызова, объект callbacks

| Функция | Описание |
| --- | --- |
| render: | При сборке виджета первым вызывается callbacks.render. В этом методе обычно описываются действия для отображения виджета. Виджет будет отображаться самостоятельно только в меню настроек (settings), для отображения виджета в других областях, например в правой колонке, необходимо использовать специальные методы в этой функции, например методы объекта render() и/или render\_template(), которые разобраны далее. **Необходимо чтобы callbacks.render вернул true**. Это важно, т.к. без этого, не запустятся методы callbacks.init и callbacks.bind\_actions. |
| init: | Запускается сразу после callbacks.render одновременно с callbacks.bind\_actions. Метод init() обычно используется для сбора необходимой информации и других действий, например связи со сторонним сервером и авторизации по API, если виджет используется для передачи или запроса информации стороннему серверу. В самом простом случае он может, к примеру, определять текущую локацию, где находится пользователь. **callbacks.init должен возвращать true** для дальнейшей работы. |
| bind\_actions: | Метод callbacks.bind\_actions используется для навешивания событий на действия предпринимаемые пользователем, например нажатие пользователя на кнопку. **callbacks.bind\_actions должен возвращать true**. |
| settings: | Метод callbacks.settings вызывается при щелчке на иконку виджета в области настроек. Может использоваться для добавления на страницу модального окна, подробнее это рассмотрено далее.   Публичные виджет не должны никак скрывать/влиять на рейтинг и отзывы виджета. |
| dpSettings: | Метод callbacks.dpSettings аналогичен callbacks.settings, но вызывается в области видимости digital\_pipeline (подробнее [Digital pipeline](/developers/content/digital_pipeline/integrations)) |
| advancedSettings: | Метод callbacks.advancedSettings вызывается на странице расширенных настроек виджета. Для функционирования данного callback’a необходимо указать область подключения виджета advanced\_settings. |
| onSave: | callbacks.onSave вызывается при щелчке пользователя на кнопке “Установить/Сохранить” в настройках виджета. Можно использовать для отправки введенных в форму данных и смены статуса виджета. Так же этот метод срабатывает при отключении виджета. Сначала срабатывает onSave, затем destroy. |
| leads:selected | Данная функция вызывается в случае выбора элементов списка сделок, с использованием checkbox, и последующем нажатии на имя виджета в добавочном меню. Используется, когда нужно предпринять какие-либо действия с выделенными объектами. Примеры рассмотрены далее. |
| contacts:selected | Данная функция вызывается в случае выбора элементов списка контактов, с использованием checkbox, и последующем нажатии на имя виджета в добавочном меню. Используется, когда нужно предпринять какие-либо действия с выделенными объектами. Примеры рассмотрены далее. |
| todo:selected | Данная функция вызывается в случае выбора элементов списка задач, с использованием checkbox, и последующем нажатии на имя виджета в добавочном меню. Используется, когда нужно предпринять какие-либо действия с выделенными объектами. Примеры рассмотрены далее. |
| destroy: | Данная функция вызывается при отключении виджета через меню его настроек. Например, нужно удалить из DOM все элементы виджета, если он был отключен, или предпринять еще какие-либо действия. Так же данный метод срабатывает при переходе между областями отображения виджета. |
| onSource: | Данная функция определяет логику работы источника и вызывается если был использован какой-то источник. Например, если пользователь отправил sms. |
| onSalesbotDesignerSave: | Данная функция определяет логику работы действия виджета в Salesbot и вызывается, если был добавлен виджет в конструкторе Salesbot, при сохранении. |
| onAddAsSource: | Данная функция вызывается при добавлении виджета как источника в настройках воронки. |

#### Пример JS-кода виджета:

Приведенный ниже пример демонстрирует варианты использования объекта функций обратного вызова с дополнительными функциями, а так же применение некоторых функций объекта виджет. Все эти функции рассмотрены в примерах далее. Советуем просто просмотреть данный код, а за подробностями обратиться к описанию функций объекта widget.

Данный виджет будет выбирать из листа контактов отмеченные контакты и передавать телефоны и e-mail адреса на сторонний сервер.

Функции, используемые в данном примере разобраны более подробно далее. В первую очередь стоит обратить внимание на объект callbacks.

```
define(['jquery'], function ($) {
var CustomWidget = function () {
var self = this,
system = self.system;
this.get\_ccard\_info = function () //Сбор информации из карточки контакта
{
if (self.system().area == 'ccard') {
var phones = $('.card-cf-table-main-entity .phone\_wrapper input[type=text]:visible'),
emails = $('.card-cf-table-main-entity .email\_wrapper input[type=text]:visible'),
name = $('.card-top-name input').val(),
data = [],
c\_phones = [], c\_emails = [];
data.name = name;
for (var i = 0; i  0) {
c\_phones[i] = $(phones[i]).val();
}
}
data['phones'] = c\_phones;
for (var i = 0; i  0) {
c\_emails[i] = $(emails[i]).val();
}
}
data['emails'] = c\_emails;
console.log(data)
return data;
} else {
return false;
}
};
this.sendInfo = function (person\_name, settings) { // Отправка собранной информации
self.crm\_post(
'http://example.com/index.php',
{
// Передаем POST данные
name: person\_name['name'],
phones: person\_name['phones'],
emails: person\_name['emails']
},
function (msg) {
},
'json'
);
};
this.callbacks = {
settings: function () {
},
dpSettings: function () {
},
init: function () {
if (self.system().area == 'ccard') {
self.contacts = self.get\_ccard\_info();
}
return true;
},
bind\_actions: function () {
if (self.system().area == 'ccard' || 'clist') {
$('.ac-form-button').on('click', function () {
self.sendInfo(self.contacts);
});
}
return true;
},
render: function () {
var lang = self.i18n('userLang');
w\_code = self.get\_settings().widget\_code; //в данном случае w\_code='new-widget'
if (typeof (APP.data.current\_card) != 'undefined') {
if (APP.data.current\_card.id == 0) {
return false;
} // не рендерить на contacts/add || leads/add
}
self.render\_template({
caption: {
class\_name: 'js-ac-caption',
html: ''
},
body: '',
render: '\
\
\
\
\
\
SEND\
\
\
'
});
return true;
},
contacts: {
selected: function () { //Здесь описано поведение при мультивыборе контактов и клике на название виджета
var c\_data = self.list\_selected().selected;
$('#js-sub-lists-container').children().remove(); //Контейнер очищается затем в контейнер собираются элементы, выделенные в списке.контейнер - div блок виджета, отображается в правой колонке.
var names = [], // Массив имен
length = c\_data.length; // Количество выбранных id (отсчет начинается с 0)
for (var i = 0; i Email:' + names[i].emails + ' Phone:' + names[i].phones + '');
}
$(self.contacts).remove(); //очищаем переменную
self.contacts = names;
}
},
leads: {
selected: function () {
}
},
onSave: function () {
return true;
}
};
return this;
};
return CustomWidget;
});
```

Содержание файла **new\_widget.css**, который может находиться в папке с виджетом

```
.card-widgets\_\_widget-new\_widget .card-widgets\_\_widget\_\_body {
padding: 0 10px 0px;
padding-bottom: 5px;
background-color: grey;
}
.ac-form {
padding: 5px 15px 15px;
margin-bottom: 10px;
background: #fff;
}
.js-ac-caption {
display: block;
margin: auto;
background-color: grey;
}
.lists\_amo\_ac ul li span {
color: #81868f;
}
.ac-form-button {
padding: 5px 0;
background: #fafafb;
text-align: center;
font-weight: bold;
text-transform: uppercase;
border: 1px solid rgba(0, 0, 0, 0.09);
-webkit-box-shadow: 0 1px 0 0 rgba(0, 0, 0, 0.15);
box-shadow: 0 1px 0 0 rgba(0, 0, 0, 0.15);
-webkit-border-radius: 2px;
border-radius: 2px;
font-size: 13px;
cursor: pointer;
}
.ac-form-button:active {
background: grey;
}
.ac-already-subs {
position: absolute;
width: 245px;
bottom: 10px;
right: 15px;
cursor: pointer;
color: #f37575;
background: #fff;
}
#js-ac-sub-lists-container, #js-ac-sub-subs-container {
min-height: 38px;
}
```

### Методы объекта widget

#### Метод render()

Метод render() используется, для работы с шаблонами шаблонизатора twig.js, который удобен в использовании, ознакомиться с документацией можно по [ссылке](https://github.com/justjohn/twig.js/wiki).

Метод является оборачивающим для twig.js и принимает в качестве параметров информацию по шаблону(data) и данные для рендеринга данного шаблона (params). render(data, params). Метод возвращает отрендеренный шаблон. result = twig(data).render(params).

#### Разберем простой Пример:

```
var params = [
{
name: 'name1',
id: 'id1'
},
{
name: 'name2',
id: 'id2'
},
{
name: 'name3',
id: 'id3'
}
]; //массив данных, передаваемых для шаблона
var template = '' + '{% for person in names %}' +
'Name : {{ person.name }}, id: {{ person.id }}' +
'{% endfor %}' + '';
console.log(self.render({data: template}, // передаем шаблон
{names: params}));
```

В результате мы получим разметку:

- Name : name1, id: id1
- Name : name2, id: id2
- Name : name3, id: id3

Можно передать функции один из шаблонов нашей системы, для этого в передаваемом объекте data нужно указать ссылку на шаблон: ref: ‘/tmpl/controls/#TEMPLATE\_NAME#.twig. Например, для создания раскрывающегося списка используем существующий шаблон:

```
m\_data = [
{
option: 'option1',
id: 'id1'
},
{
option: 'option2',
id: 'id2'
},
{
option: 'option3',
id: 'id3'
}
]; //массив данных, передаваемых для шаблона
var data = self.render(
{ref: '/tmpl/controls/select.twig'}, // объект data в данном случае содержит только ссылку на шаблон
{
items: m\_data, //данные
class\_name: 'subs\_w', //указание класса
id: w\_code + '\_list' //указание id
});
```

Чтобы посмотреть на разметку data, надо добавить data в DOM. Разметка раскрывающегося списка выполнена в стиле нашей системы.

Ознакомится с полным списком шаблонов, вы можете пройдя по [ссылке](/static/assets/developers/files/templates/twigs.zip). Для использования других системных шаблонов нужно поменять параметр ref, общий вид: ref: ‘/tmpl/controls/#TEMPLATE\_NAME#.twig’

- textarea
- suggest
- select
- radio
- multiselect
- date\_field
- checkbox
- checkboxes\_dropdown
- file
- button
- cancel\_button
- delete\_button
- input

Методу render() можно передавать не только системные существующие шаблоны, но и ссылки на собственные шаблоны. Для этого надо передавать объект data с рядом параметров. Необходимо создать папку templates в папке нашего виджета и положить в нее шаблон template.twig. Рассмотрим пример:

```
var params = {}; //пустые данные
var callback = function (template) { //функция обратного вызова, вызывается если шаблон загружен, ей передается объект шаблон.
var markup = template.render(params); //
/\*
\* далее код для добавления разметки в DOM
\*/
};
var s = self.render({
href: 'templates/template.twig', //путь до шаблона
base\_path: self.params.path, //базовый путь до директории с виджетом
load: callback //вызов функции обратного вызова произойдет только если шаблон существует и загружен
},
params
); //параметры для шаблона
```

Если шаблон существует по адресу ссылки, то вызывается переданная функция callback, и ей передается объект шаблон, который содержит метод render, передаем render параметры для рендеринга. В данном примере вызов функции обратного вызова произойдет, если шаблон существует в папке.

#### Пример функции для загрузки шаблонов по из папки templates

Для удобства обращения создадим функцию. В нее будем передавать параметры: template – имя шаблона который лежит в папке с виджетом в папке template, params – объект параметров для шаблона, callbacks – функция обратного вызова, которая будет вызываться после загрузки шаблона, в данном случае будем добавлять шаблон в модальное окно. Про объект модальное окно можно почитать в разделе [JS методы и объекты для работы с amoCRM](/developers/content/integrations/js_sdk#jssdk_modal).

#### Общий пример работы с функцией self.getTemplate

```
self.getTemplate = function (template, params, callback) {
params = (typeof params == 'object') ? params : { } ;
template = template || '';
return self.render({
href: '/templates/' + template + '.twig',
base\_path: self.params.path, //тут обращение к объекту виджет вернет /widgets/#WIDGET\_NAME#
load: callback //вызов функции обратного вызова
}, params); //параметры для шаблона
};
```

#### Пример использования self.getTemplate в callbacks.settings

```
settings: function ( ) {
self.getTemplate ( //вызов функции
'login\_block', //указываем имя шаблона, который лежит у нас в папке с виджетом в папке templates
{}, /\* пустые данные для шаблона, т.к мы сначала запросим шаблон, если он существует, то функция обр.вызова вызовет уже функцию для добавления данных к шаблону, см.ниже \*/
function (template) {
template.render ({
widget\_code: self.params.widget\_code, //параметры для шаблона.
lang: self.i18n ( 'settings' )}));
}};
```

#### Добавление тура в модальное окно виджета

Для добавления тура в модальное окно виджета необходимо добавить свойство tour в manifest.json. Подробней об этом читайте в [этой статье.](https://www.amocrm.ru/developers/content/integrations/structure#manifest_example)

Пример описания свойства в manifest.json:

```
"tour": {
"is\_tour": true,
"tour\_images": {
"ru": [
"/images/tour\_1\_ru.png",
"/images/tour\_2\_ru.png",
"/images/tour\_3\_ru.png"
],
"en": [
"/images/tour\_1\_en.png",
"/images/tour\_2\_en.png",
"/images/tour\_3\_en.png"
],
"es": [
"/images/tour\_1\_es.png",
"/images/tour\_2\_es.png",
"/images/tour\_3\_es.png"
]
},
"tour\_description": "widget.tour\_description"
},
```

#### Метод render\_template()

Метод render\_template() оборачивает переданную ему разметку или шаблон в стандартную для виджетов оболочку (разметку) и помещает полученную разметку в правую колонку виджетов

Можно передавать данной функции html разметку или шаблон с данными для рендеринга, так же как в случае с методом render().

Функция дополняет переданную ей разметку своей, хранящейся в переменной template\_element объекта widget.

```
/\*html\_data хранит разметку, которую необходимо поместить в правую колонку виджетов.\*/
var html\_data = '' + '' + '' + 'BUTTON' + ''; self.render\_template({ caption: { class\_name: 'new\_widget', //имя класса для обертки разметки }, body: html\_data, //разметка render: '' //шаблон не передается });
```

Был показан самый простой пример без использования шаблона, но метод render\_template() так же может принимать шаблон и данные для шаблона в качестве параметров. Так же можно передавать сылку на шаблон, аналогично методу render().

```
/\*Здесь в качестве параметров передается шаблон и данные для шаблона.\*/
var render\_data = '' +
'' +
'' +
'' +
'' +
'' +
'' +
'' +
'{{b\_name}}' +
'';
self.render\_template(
{
caption: {
class\_name: 'new\_widget'
},
body: '',
render: render\_data
},
{
name: "widget\_name",
w\_code: self.get\_settings().widget\_code,
b\_name: "BUTTON" // в данном случае лучше передать ссылку на lang через self.i18n()
}
);
```

Получаем в правой колонке виджет, созданный по шаблону.

Объект widget имеет еще ряд полезных функций, которые можно вызывать для решения разных задач.

Описание и примеры приведены ниже.

#### Функция set\_lang()

Функция set\_lang() позволяет изменять параметры, установленные по умолчанию файлами из папки i18n

Текущий объект lang хранится в переменной langs объекта widget

```
langs = self.langs; //Вызываем текущий объект
langs.settings.apiurl = 'apiurl\_new' //меняем имя поля
self.set\_lang(langs); //меняем текущий объект на объект с измененным полем
console.log(self.langs); //выводим в консоль, чтобы убедиться, что название изменилось
```

#### Функция set\_settings()

Функция set\_settings() позволяет добавлять виджету свойства.

```
self.set\_settings({par1: "text"}); //создается свойство с именем par1 и значением text
self.get\_settings(); // в ответ придет массив с уже созданным свойством
```

#### Функция list\_selected()

Функция list\_selected() возвращает выделенные галочками контакты/сделки из таблицы контактов/сделок в виде массива объектов: count\_selected и selected. Один из объектов selected содержит массив выделенных галочками объектов со свойствами emails, id, phones, type.

```
console.log(self.list\_selected().selected); //Возвращает два объекта, выбираем объект selected
//Результат:
/\*0: Object
emails: Array[1]
id: #id#
phones: Array[1]
type: "contact" \*/
```

#### Функция widgetsOverlay()

Функция widgetsOverlay() (true/false) включает или отключает оверлей, который появляется при вызове виджета из списка контактов или сделок.

```
//Пример:
self.widgetsOverlay(true);
```

#### Функция add\_action()

При работе пользователя в области список контактов и компаний, можно обеспечить вызов какой-либо функции, при щелчке на номер телефона или e-mail адрес контакта.

Функции add\_action() передаются параметры (type,action), где type – “e-mail” или “phone”, action – функция, которая будет вызываться при щелчке на номере телефона или адресе e-mail.

```
self.add\_action("phone", function () {
/\*
\* код взаимодействия с виджетом телефонии
\*/
});
```

#### Функция add\_source()

Позволяет указать новый источник, который будет отображаться в контроле в нижней части фида карточки сделки, покупателя, контакта или компании.

На данный момент можно указать только один тип источника – sms

Функции add\_source() передаются параметры (source\_type, handler), где source\_type – “sms”, handler – функция, которая будет вызываться при клике на кнопку “отправить”.

Функция “handler” всегда должна возвращать объект Promise

```
// пример
self.add\_source("sms", function (params) {
/\*
params - это объект в котором будут необходимые параметры для отправки смс
{
"phone": 75555555555, // телефон получателя
"message": "sms text", // сообщение для отправки
"contact\_id": 12345 // идентификатор контакта, к которому привязан номер телефона
}
\*/
return new Promise(function (resolve, reject) {
// тут будет описываться логика для отправки смс
$.ajax({
url: '/widgets/' + self.system().subdomain + '/loader/' + self.get\_settings().widget\_code + '/send\_sms',
method: 'POST',
data: params,
success: function () {
// при успешном завершении будет автоматически создано примечание типа 'sms'
resolve();
},
error: function () {
reject();
}
});
});
});
```

#### Метод crm\_post(url, data, callback, type)

Метод используется для отправки запроса на ваш удаленный сервер через прокси-сервер amoCRM. Его использование необходимо, т.к. при работе с amoCRM пользователь работает по защищенному SSL протоколу и браузер может блокировать кросс-доменные запросы. Лучшим решением является наличие подписанного SSL-сертификата на стороне внутренней системы и работа по HTTPS. Функция аналогична jQuery post().

Описание метода

| Параметр | Тип | Описание |
| --- | --- | --- |
| url | Строка | Ссылка на скрипт обрабатывающий данные |
| data  *optional* | Javascript объект | Пары ключ:значение, которые будут отосланы на сервер |
| callback   *optional* | Функция | Функция, вызывающаяся после каждого успешного выполнения (в случае передачи type=text or html, выполняется всегда). |
| type  *optional* | Строка | Тип данных, который возвращается функции: “xml”, “html”, “script”, “json”, “jsonp”, или “text”. |

#### Пример запроса

```
self.crm\_post(
'http://www.test.ru/file.php',
{
// Передаем POST данные с помощью объектной модели Javascript
name: 'myname',
login: 'mylogin',
password: 'mypassword'
},
function (msg) {
alert('It\'s all OK');
},
'text',
function () {
alert('Error');
}
)
```

#### Метод self.get\_settings()

Данный метод необходим, для того, чтобы получить данные, которые ввел пользователь при подключении виджета. Данные возвращаются в виде объекта javascript

#### Пример ответа:

```
{
login: "ZABRTEST" ,
password: "test" ,
maybe: "Y"
}
```

#### Метод self.get\_version()

Данный метод вернет номер версии виджета, можно использовать для того, чтобы кэш статики сбрасывался после обновления. Данные возвращаются в виде строки.

#### Пример ответа:

```
0.0.1
```

#### Метод self.get\_install\_status()

Данный метод вернет статус установки виджета. Данные возвращаются в виде строки. Возможные значения – installed (виджет установлен), install (виджет не установлен), not\_configured (тур виджета пройден, но настройки не заполнены)

#### Пример ответа:

```
not\_configured
```

#### Метод self.system()

Данный метод необходим, для того, чтобы получить системные данные. Данные возвращаются в виде объекта javascript

| Параметр | Описание |
| --- | --- |
| area | Область на которой воспроизводится виджет в данный момент |
| amouser\_id | Id пользователя |
| amouser | Почта пользователя |
| amohash | Ключ для авторизации API |

#### Пример ответа:

```
{
area: "ccard" ,
amouser\_id: "103586" ,
amouser: "testuser@amocrm.ru" ,
amohash: "d053abd66063225fa8b763afz6496da8"
}
```

#### Метод self.i18n(objname)

Данные метод позволяет, получить объект из языковых файлов, в котором будут сообщения на языковых локалях, используемые пользователем  
В objname передается имя объекта, который необходимо вытащить

Например, вызываем функцию `self.i18n('userLang')`

#### Пример ответа:

```
{
firstWidgetText: "Кликни на кнопку, чтобы переслать данные на сторонний сервер:",
textIntoTheButton: "Отправить данные",
responseMessage: "Ответ сервера :",
responseError: "Ошибка"
}
```

Таким образом, имея простой инструмент для взаимодействия с DOM и выполнения кроссдоменных запросов, вы можете помимо создания простых текстовых виджетов, менять дизайн элементов страницы, создавать собственные информационные блоки на основе внешних данных, или наоборот, пересылать данные во внешние сервисы, причем все это работает сразу для всех пользователей вашего аккаунта.

#### Метод проверки согласия на передачу данных в виджете.

Данное решение не является единственно возможным.

1. В manifest.json в параметр settings добавляется кастомное поле, обязательное для заполнения, например, **oferta**

```
"oferta": {
"name": "settings.oferta",
"type": "custom",
"required": true
}
```

Данное поле будет скрыто(по умолчанию). При нажатии на “Установить” установка не произойдёт, так как это поле является незаполненным на данном этапе. Далее необходимо вставить блок с чекбоксом (вёрстка) в правую часть модального окна виджета и при отметке чекбокса записывать в поле **oferta** произвольное значение, а при снятии галочки чекбокса, очищать значение. Кроме того, следует информировать пользователя о необходимости дать согласие на передачу данных до начала установки виджета. Если пользователь нажимает кнопку “Установить” не дав согласие, выводить предупреждающее сообщение. Для примера вы можете воспользоваться следующим кодом.

Вёрстку с чекбоксом расположим в шаблоне templates/oferta.twig

#### templates/oferta.twig

```

Подтвердите согласие на передачу данных аккаунта на сторонний сервер

Необходимо дать согласие

```

#### Script.js

```
define(['jquery'], function ($) {
var CustomWidget = function () {
var self = this;
// Добавим метод получения шаблонов twig
self.getTemplate = function (template, params, callback) {
params = (typeof params == 'object') ? params : {};
template = template || '';
return self.render({
href: '/templates/' + template + '.twig', // путь до шаблона
base\_path: self.params.path, //тут обращение к объекту виджет вернет /widgets/#WIDGET\_NAME#
load: callback //вызов функции обратного вызова
}, params); //параметры для шаблона
}
this.callbacks = {
render: function () {
return true;
},
init: function () {
return true;
},
bind\_actions: function () {
return true;
},
settings: function ($modal\_body) { //$modal\_body - jquery-объект блока правой части модального окна виджета
self.getTemplate(
'oferta',
{},
function (template) {
$modal\_body.find('input[name="oferta"]').val(''); // очищаем принудительно поле oferta
$modal\_body.find('.widget\_settings\_block').append(template.render()); // отрисовываем шаблон и добавляем в блок настроек виджета
var $install\_btn = $('button.js-widget-install'),
$oferta\_error = $('div.oferta\_error');
$modal\_body.find('input[name="oferta\_check"]').on('change', function (e) {
var $checkbox = $(e.currentTarget);
if ($checkbox.prop('checked')) {
$modal\_body.find('input[name="oferta"]').val('1'); //заполняем поле oferta, если чекбокс отмечен
$oferta\_error.addClass('hidden'); // скрываем предупреждение, если оно отображено
} else {
$modal\_body.find('input[name="oferta"]').val(''); // очищаем поле oferta, если не отмечен чекбокс
}
});
//при нажатии на кнопку "Установить", если не отмечен чекбокс, отображаем предупреждение
$install\_btn.on('click', function () {
if (!$modal\_body.find('input[name="oferta"]').val()) {
$oferta\_error.removeClass('hidden');
}
});
}
);
return true;
},
onSave: function () {
return true;
},
destroy: function () {
return true;
},
contacts: {
selected: function () {
return true;
}
},
leads: {
selected: function () {
return true;
}
},
tasks: {
selected: function () {
return true;
}
}
};
return this;
};
return CustomWidget;
});
```

### Получение настроек виджета вне script.js

Для примера с получением настроек виджета в дочернем модуле рассмотрим следующий кейс. Виджет при инициализации проверяет логин на корректность и если логин не подходит по каким-то критериям, то мы должны показать пользователю модальное окно с ошибкой.

Состав нашего виджета будет следующим:

- script.js – обработчик виджета
- ./lib/settings\_helper.js – наш хелпер, который будет хранилищем настроек
- ./lib/error.js – вспомогательная библиотека для отображения ошибок, в ней нам надо получить логин пользователя из настроек виджета

Как видим в примере, в конструкторе виджета мы запоминаем настройки виджета в нашем специализированным хелпере, до того как виджет выполнит какой-либо из системных колбэков.

Таким образом мы можем получить хоть код виджета, хоть любой другой параметр, который находится в объекте, возвращаемом от **get\_settings**.

#### script.js

```
define(['jquery', './lib/settings\_helper.js', './lib/error.js'], function($, settings\_helper, error\_lib) {
var CustomWidget = function() {
var self = this;
// еще в конструкторе виджета запомним его настройки в хелпере
settings\_helper.set(self.get\_settings());
this.callbacks = {
settings: function() {},
init: function() {
var in\_case\_of\_login\_error = true;
if (in\_case\_of\_login\_error) {
error\_lib.showLoginError();
}
return true;
},
bind\_actions: function() {
return true;
},
render: function() {
return true;
},
dpSettings: function() {},
advancedSettings: function() {},
destroy: function() {},
contacts: {
selected: function() {}
},
leads: {
selected: function() {}
},
onSave: function() {}
};
return this;
};
return CustomWidget;
});
```

#### lib/settings\_helper.js

```
define([], function() {
var settings = {};
return {
set: function(widget\_settings) {
settings = widget\_settings;
},
get: function() {
return settings;
}
};
});
```

#### lib/error.js

```
define(['lib/components/base/modal', './lib/settings\_helper.js'], function(Modal, settings\_helper) {
return {
showLoginError: function() {
var widget\_settings = settings\_helper.get();
new Modal().\_showError(widget\_settings.login + ' is incorrect!');
}
};
});
```

### Подключение файла style.css

Для избежания случаев кэширования файла style.css необходимо при подключении файла css передавать параметром версию виджета

Ниже пример подключения файла css:

#### script.js

```
define(['jquery'], function ($) {
var CustomWidget = function () {
var self = this, // для доступа к объекту из методов
system = self.system(), //Данный метод возвращает объект с переменными системы.
langs = self.langs; //Объект локализации с данными из файла локализации (папки i18n)
this.callbacks = {
settings: function () {},
init: function () {
// Возвращаем настройки виджета
var settings = self.get\_settings();
// Проверяем подключен ли наш файл css
if ($('link[href="' + settings.path + '/style.css?v=' + settings.version +'"').length ');
}
return true;
},
bind\_actions: function () {
return true;
},
render: function () {
return true;
},
dpSettings: function () {},
advancedSettings: function () {},
destroy: function () {},
contacts: {
selected: function () {}
},
leads: {
selected: function () {}
},
onSave: function () {}
};
return this;
};
return CustomWidget;
});
```