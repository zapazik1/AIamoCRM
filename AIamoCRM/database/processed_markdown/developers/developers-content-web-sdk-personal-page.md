---
title: "Кабинет клиента"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/web/sdk/personal/page
section: developers
---

в amoCRM существует личный кабинет клиента. Активировать его можно на странице “Общие настройки” под настройками левого меню. Там есть отдельная секция.

Данный пункт доступен только для тарифов выше "базового".

![](https://i.postimg.cc/nctN1ndQ/2022-11-14-17-06-49.png)

Для входа необходимо в селекте выбрать виджет для отправки смс. Если есть виджеты конкретного типа, то показывается селект, иначе текст красного цвета со ссылкой, которая ведет на страницу интеграции -> каталог с виджетами для отправки смс.

Авторизация происходит по номеру телефона который клиент указывает в сделке.

В сайдбаре слева находятся данные по сделке, контакты и аккордион с виджетами. Кнопка с виджетами будет доступа только если интеграция настроена для отображения в кабинете клиента.

### Настройка виджета для кабинета клиента

Чтобы виджет маунтился в кабинет клиента необходимо добавить location в **manifest.json**

```javascript
{
...
"locations": [
"personal\_page" // указываем personal\_page
],
...
}
```

В корневой папке проекта виджета создаем одноименный js файл **personal\_page.js**

**Общий вид personal\_page.js**

```javascript
// Мы используем requirejs для импорта модулей в рантайме
// См. секцию "Объявленные зависимости", чтобы узнать, какие модули предоставлены для импорта.
define(['amocrm-sdk', 'jquery', 'dateformat'], function (initAmocrmWidgetSdk, $, dateFormat) {
// Этот код выполняется один раз при импорте модуля
const WidgetSdk = initAmocrmWidgetSdk({
version: '1.0.0',
})
// Чтобы виджет заработал, нужно вернуть объект с колбэками
return {
initLead(params) {
console.warn('WIDGET: initLead with token: ', params.token)
return () => {
console.warn('WIDGET: initLead destroyed')
}
},
registerWidgetsBarSlot(el) {
const $el = $(el)
const sysData = WidgetSdk.methods.getState(WidgetSdk.constants.PUBLIC\_STATE\_ENTITIES.sys)
const formattedTime = dateFormat(Date.now(), sysData.timeFormat)
$el.text('Hello world!')
console.warn(`WIDGET registerWidgetsBarSlot inited at ${formattedTime}`)
return () => {
console.warn('WIDGET: registerWidgetsBarSlot destroyed')
}
},
}
})
```

### Callbacks:

***initLead***

Вызывается сразу после подключения модуля и каждый раз, когда меняется активная сделка.

**Обязательный колбэк**  
**Аргументы**

- *params (object):* Параметры сделки.
- *params.token (string):* Токен в формате JWT, подписанный client\_secret’ом от интеграции.

**Должен возвращать**

- *(() => void):* Колбэк может вернуть функцию, она будет вызвана, когда пользователь покинет активную сделку. Будет гарантировано вызвана до повторного исполнения `initLead`.
- *(void):* Можно ничего не возвращать, если нет необходимости подчищать данные при смене аккаунта.

***registerWidgetsBarSlot***

Необходим для добавления виджета в боковую панель с виджетами. Будет вызван во время рендера, после того, как завершится `initLead`.

**Обязательный колбэк**  
**Аргументы**

- *el (HtmlElement):* Получает html element с классом `WidgetSdk.constants.GLOBAL_CLASS_NAMES.widgetBarItemContainer` для рендера содержимого виджета.

**Должен возвращать**

- *(() => void):* Колбэк может вернуть функцию, она будет вызвана, когда приложение задестроет компонент с виджетом.
- *(void):* Можно ничего не возвращать, если нет необходимости подчищать данные при дестрое.

### Объявленные зависимости

Модули, которые используются в самом приложении и предоставлены разработчикам виджетов, чтобы не загружать их повторно.

- amocrm-sdk – См. `initAmocrmWidgetSdk` из следующей секции.
- import-modules – requirejs обернытый в промис.
- [jquery](https://github.com/jquery/jquery)
- [react](https://github.com/facebook/react)
- [react-dom](https://github.com/facebook/react)
- [@reduxjs/toolkit](https://github.com/reduxjs/redux-toolkit)
- [react-redux](https://github.com/reduxjs/react-redux)
- [immer.produce](https://github.com/immerjs/immer)
- [immer.current](https://github.com/immerjs/immer)
- [nanoid](https://github.com/ai/nanoid) – non-secure версия
- [classnames](https://github.com/JedWatson/classnames)
- [dateformat](https://github.com/felixge/node-dateformat) – Используется для форматирования дат в проекте.
- [lodash](https://github.com/lodash/lodash)

### amocrm-sdk

***initAmocrmWidgetSdk***

Функция, получаемая с помощью requirejs.

**Аргументы**

- *options (object)*
- *options.version (string):* Обязательно нужно указать версию SDK, которой вы пользуетесь, чтобы избежать проблем с изменением возвращаемого формата.

**Возвращает**

Создает инстанс WidgetSdk следующего вида:

```javascript
type Constants = {
DATE\_FORMATS: {
americanNormal: 'dd/mm/yyyy',
americanInversed: 'mm/dd/yyyy',
russianNormal: 'dd.mm.yyyy',
chineseNormal: 'yyyy/mm/dd',
},
TIME\_FORMATS: {
twelve: 'h:MM TT',
twentyFour: 'HH:MM',
},
SUPPORTED\_LANGS: {
ru: 'ru',
en: 'en',
es: 'es',
pt: 'pt',
},
LEAD\_FIELD\_SOURCES: {
lead: 'lead',
contacts: 'contacts',
company: 'company',
},
FIELD\_TYPES: {
text: 'text',
numeric: 'numeric',
checkbox: 'checkbox',
date: 'date',
select: 'select',
multiselect: 'multiselect',
url: 'url',
textarea: 'textarea',
radiobutton: 'radiobutton',
streetaddress: 'streetaddress',
smartAddress: 'smartAddress',
legalEntity: 'legalEntity',
birthday: 'birthday',
dateTime: 'dateTime',
multitext: 'multitext',
budget: 'budget',
},
PUBLIC\_STATE\_ENTITIES: {
sys: 'sys',
lead: 'lead',
leadFields: 'leadFields',
authors: 'authors',
},
// Содержит все имена классов, начинающиеся на `js-`
GLOBAL\_CLASS\_NAMES: {
widgetBarItemContainer: string,
},
}
type SysModel = {
currencySymbol: string,
dateFormat: ValueOf,
timeFormat: ValueOf,
lang: ValueOf,
isRemovalAvailable: boolean,
logoUrl: string,
pageTitle: string,
}
type LeadModel = {
id: string,
pid: string,
isLeadLoaded: boolean,
fieldIds: string[],
statuses: Array,
managerId: string,
contacts: Record,
company: {
id: string,
name: string,
fieldIds: string[],
} | null,
}
type LeadFieldsModel = Record,
name: string,
type: ValueOf,
value: any,
}
>
type AuthorsModel = Record
type RouterQuery = {
leadId?: string,
accountId?: string,
}
type WidgetSdk = {
methods: {
// Запрашивает данные сущности по её имени
getState: (entityName: ValueOf) => SysModel | LeadModel | LeadFieldsModel | AuthorsModel | null,
// Подписывается на изменение данных сущности. Возвращает функцию для подчистки слушателя изменений.
// Третьим аргументом можно передать дополнительные параметры.
subscribe: (
entityName: FirstArgument,
callback: (ReturnType) => void,
options?: {
// Если withInitialResult true, то при создании подписки callback будет сразу же вызван с текущим значением.
withInitialResult?: boolean,
}
) => () => void,
// Получает динамические id по урлу
getRouterQuery: () => RouterQuery,
},
constants: Constants,
}
```

### Developer utils

Для удобства разработки виджетов мы предоставляем набор вспомогательных функций, что находятся в `window.AMOCRM.developer`. Они созданы для облегчения разработки и не должны находиться в коде финального продукта.

Сейчас доступные методы:

***addWidget***

Добавляет виджет в стор приложения кабинет клиента, как это было бы при получении виджета с бэкенда amoCRM. Удобно для проверки js виджета без необходимости открывать интерфейс amoCRM и загружать каждый раз новый архив с правками.

Для подключения виджета с локального компьютера в консоли браузера необходимо выполнить следующий метод (значения аргументов см. ниже):

```js
window.AMOCRM.developer.addWidget({
script: 'http://localhost:3000',
token: 'foo',
})
//параметр токен может принимать пустую строку, если тестируется фронт
```

*При переключении сделок, виджет будет сбрасываться и понадобится повторный вызов метода в консоли.*  
*При вызове метода будет отображаться только подключаемый виджет. Для отката необходимо обновить страницу.*

**Аргументы**

- *widgetParams (object):* Параметры виджета в формате, в котором они хранятся на фронте.
- *widgetParams.script (string):* Ссылка на js файл вашего виджета.
- *widgetParams.token (string):* Имитация токена в формате JWT, что будет передан в колбэк `initLead`.

**Возвращает**

- *(void)*