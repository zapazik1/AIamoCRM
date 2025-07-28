---
title: "Левое меню и подразделы"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/web/sdk/left/menu
section: developers
---

amoCRM позволяет виджетам добавлять собственные пункты в главное меню. Разработка этого функционала осуществляется только в публичных интеграциях при наличии технического аккаунта. При установке виджета с такой возможностью в аккаунте пользователя в левом меню появится новый пункт виджета.

Визуально такой пункт будет отличаться от системных, чтобы пользователь понимал, что данная функциональность не является штатной, пример показан на скриншоте ниже.

![](https://i.postimg.cc/13wrYvKH/image1.jpg)

Итак, чтобы добавить собственный пункт меню необходимо добавить следующие строки в **manifest.json**

```json
{
...
"locations": [
"widget\_page"
],
"left\_menu": {
"realty\_widget\_code": {
"title": "lang.code",
"icon": "images/home\_page.svg",
"submenu": {
"sub\_item\_code\_1": {
"title": "lang.code", // код лэнга подпункта
"sort": 2
},
"sub\_item\_code\_2": {
"title": "lang.code",
"sort": 1
}
}
}
},
...
}
```

Как видим обязательно нужно добавить **widget\_page** в список локейшнов виджета, далее появляется свойство **left\_menu**, ключ **realty\_widget\_code** это код пункта меню, также у пункта меню могут быть подпункты, в таком случае страница пункта виджета будет иметь дочернее меню как на скриншоте ниже. Сортировкой подпунктов можно управлять с помощью свойства **sort**.

![](https://i.postimg.cc/T3MrmrXW/image2.jpg)

По умолчанию пункт меню добавляется после раздела настройки в конец главного меню, однако, у виджета есть возможность управлять своим положением, например, можно поставить пункт виджета после раздела "Сделки":

```json
{
...
"left\_menu": {
"realty\_widget\_code": {
"title": "lang.code",
"icon": "images/home\_page.svg",
"sort": {
"after": "leads"
},
"submenu": {
"sub\_item\_code\_1": {
"title": "lang.code"
},
"sub\_item\_code\_2": {
"title": "lang.code"
}
}
}
}
...
}
```

Список кодов системных меню, которые можно указать в качестве значения **after**:

- dashboard
- leads
- customers
- tasks
- catalogs
- mail
- stats
- settings

Помимо собственного пункта меню виджет может добавить подпункты в системные меню "Аналитики" (**stats**) и "Настроек" (**settings**), вот пример кода в **manifest.json** для добавления нового пункта в меню раздела "Аналитика":

```json
{
...
"left\_menu": {
"stats": {
"submenu": {
"custom\_sub\_item\_1": {
"title": "lang.code"
},
"custom\_sub\_item\_2": {
"title": "lang.code"
}
}
}
},
...
}
```

Также виджет может скрывать системные пункты меню, кроме пункта "Настройки", в данном случае manifest.json должен выглядеть так:

```json
{
...
"left\_menu": {
"stats": {
"is\_hidden": true
},
"mail": {
"is\_hidden": true
}
}
...
}
```

Список кодов системных меню, которые поддерживают скрытие:

- dashboard
- leads
- customers
- tasks
- catalogs
- mail
- stats

Для обработки клика по пунктам меню в виджете предусмотрен специальный колбэк **initMenuPage**, данный колбэк на вход принимает объект следующего вида:

```json
{
"location": "widget\_page", // "stats" or "settings"
"item\_code": "custom\_item\_1", // только в созданных пунктах левого меню
"subitem\_code": "sub\_item\_1" // код подпункта
}
```

В location приходит обозначение сущности, в которой находится пункт меню, как мы уже знаем пункт меню может быть добавлен как дочерний в системные разделы.

В item\_code – код пункта меню, в subitem\_code код подпункта, если пользователь перешел в дочерний пункт меню.

Пример реализации колбэка **initMenuPage**:

```js
this.callbacks = {
/\*\*
\* Метод срабатывает, когда пользователь переходит на кастомную страницу виджета.
\* Мы должны отрендерить страницу в зависимости от состоянии страницы.
\*
\* @param params - Передается текущее состояние страницы. Формат такой:
\* {
\* location: 'widget-page', // текущая локация
\* item\_code: 'custom\_item\_1', // ключ, который был указан в manifest.json
\* subitem\_code: 'custom\_sub\_item\_3' // ключ подпункта, который был указан в manifest.json
\* }
\*/
initMenuPage: \_.bind(function (params) {
switch (params.location) {
case 'stats': // в этом случае item\_code, мы не получим
switch (params.subitem\_code) {
case 'sub\_item\_1':
self.getTemplate(
'stats\_\_sub\_item\_1',
{},
function (template) {
$('#work-area-' + self.get\_settings().widget\_code).html('Пункт Аналитика, подпункт 1');
});
break;
case 'sub\_item\_2':
self.getTemplate(
'stats\_\_sub\_item\_2',
{},
function (template) {
$('#work-area-' + self.get\_settings().widget\_code).html('Пункт Аналитика, подпункт 2');
});
break;
}
break;
case 'settings': // в этом случае item\_code, мы не получим
// noop
break;
case 'widget\_page':
switch (params.item\_code) {
case 'custom\_item\_3':
switch (params.subitem\_code) {
case 'sub\_item\_1':
self.getTemplate(
'custom\_item\_3\_\_sub\_item\_1',
{},
function (template) {
$('#work-area-' + self.get\_settings().widget\_code).html('Пункт 3, подпункт 1');
});
break;
// etc.
}
break;
// etc.
}
break;
}
}, self),
}
```