---
title: "Системные модули"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/web/sdk/system/modules
section: developers
---

### Оглавление

- [Вендорные модули](#Вендорные-модули)
- [Модули amoCRM](#Модули-amoCRM)
- [Объект Modal для работы с модальным окном](#Объект-Modal-для-работы-с-модальным-окном)

### Вендорные модули

Для того, чтобы сократить количество загружаемых ресурсов из сети и ускорить работу amoCRM в браузере клиента, виджеты могут использовать вендорные библиотеки, предоставляемые системой.

| Модуль | Версия | Ссылка на NPM |
| --- | --- | --- |
| underscore | 1.9.1 |  |
| backbone | 1.1.2 |  |
| jquery | 2.1.3 |  |
| twigjs | 0.8.9 |  |
| browser-detect | 0.2.28 |  |
| chartjs | 2.9.2 |  |
| colorpicker | 3.0.0 |  |
| rangeslider | 2.3.2 |  |
| clipboard | 1.5.10 |  |
| cocktail | 0.5.15 |  |
| accounting | 0.3.2 |  |
| device | 0.8.0 |  |
| enquire | 2.1.1 |  |
| FileAPI | 2.0.5 |  |
| google-libphonenumber | 3.0.0 |  |
| jplayer | 2.9.2 |  |
| js-uuid | 0.0.6 |  |
| fullcalendar | 2.3.1 |  |
| moment | 2.24.0 |  |
| pubsub | 1.5.3 |  |
| steady | 2.0.0 |  |
| store | 1.3.20 |  |
| cropperjs | 1.2.2 |  |
| virtualized-list | 2.2.0 |  |
| quill | 1.3.6 |  |
| intl\_tel\_input | 3.7.1 |  |

Можно использовать любую из этих библиотек в соответствии с API указанной версии, ознакомиться с API можно по ссылкам на NPM. Для использования в своем виджете укажите код модуля из таблицы в зависимостях виджета в **script.js**:

```javascript
define(['jquery', 'moment'], function ($, moment) {
$('#my\_widget\_selector').css('color', 'red');
console.log(moment().format('DD-MM-YYYY'));
});
```

### Модули amoCRM

Помимо внешних модулей виджеты могут использовать некоторые части amoCRM для более нативной интеграции в систему.

Наверное, самый часто используемый модуль это модальное окно (**lib/components/base/modal**). Вот пример его использования в **script.js**:

```javascript
define(['jquery', 'underscore', 'lib/components/base/modal'], function ($, \_, Modal) {
return function () {
var self = this;
this.callbacks = {
init: function () { return true; },
bind\_actions: function () {
$(document).on(
'click.' + self.get\_settings().widget\_code,
'.my\_widget\_button',
function () {
new Modal({
// собственный класс для модального окна,
// если нужно в нем поменять какие-то стили
class\_name: '',
// метод, отрабатывающий при
// готовности модального окна
// получает в параметр jQuery-объект $modal\_body
// тела модального окна, все внутренности
// окна будут в нем
init: \_.noop,
// кастомный `destroy`, может вернуть `false`,
// тогда закрытия окна не произойдет
destroy: \_.noop,
// контейнер, куда попадет
// модальное окно и относительно
// какого элемента будет центрироваться
container: document.body,
// если нужно запретить закрытие модального окна
// по клику на оверлэе, просто передаем в options
// `disable\_overlay\_click`
disable\_overlay\_click: false,
// если нужно запретить закрытие модального окна
// по нажатию на escape
disable\_escape\_keydown: false,
// если нужно запретить дефолтную обработку enter
disable\_enter\_keydown: false,
// параметр отвечает за анимацию всплывания
// модального окна, если передать `true`,
// то оно запустится с анимацией увеличения и появления
init\_animation: false,
// по умолчанию оверлей у модалок белый,
// изменить если нужен темный оверлей
default\_overlay: false,
// элемент, который получает фокус,
// по умолчанию это кнопка акцепта. нужен для того,
// чтобы снимать фокус с кнопки вызвавшей событие
focus\_element: '.js-modal-accept',
});
}
)
},
render: function () { return true; },
destroy: function () {
$(document).off('.' + self.get\_settings().widget\_code);
return true;
},
settings: function () { return true; },
onSave: function () { return true; }
}
};
});
```

### Объект Modal для работы с модальным окном

Для работы с ним необходимо:

1. Подключить в файле script.js
2. Вызвать модальное окно в момент когда оно должно появиться
3. Передать необходимые параметры при вызове

В данном примере показано использование объекта модального окна Modal

Отдельный пример приведен ниже.

```javascript
define(['jquery', 'lib/components/base/modal'], function ($, Modal) {
var CustomWidget = function () {
this.callbacks = {
// ...
bind\_actions: function () {
// ...
var data = 'TestSome text';
modal = new Modal({
class\_name: 'modal-window',
init: function ($modal\_body) {
var $this = $(this);
$modal\_body
.trigger('modal:loaded') // запускает отображение модального окна
.html(data)
.trigger('modal:centrify') // настраивает модальное окно
.append('');
},
destroy: function () {
}
});
// ...
return true;
}
}
}
return CustomWidget;
});
```

Для работы с объектом модальное окно необходимо подключить его через require (define в начале script.js) и передать параметры : class\_name, init() , destroy(). В init передаются данные для отображения в модальном окне и события trigger для того, чтобы запустить методы объекта Modal и вывести модальное окно в DOM.

#### Параметры

| Параметр | Описание |
| --- | --- |
| class\_name | Дополнительные классы для модального окна |
| can\_centrify | костыльный параметр центровки для мобильных устройств некоторые модальные окна нужно специаль перецентрировать после закрытия клавиатуры на мобильном планшете |
| init | метод, отрабатывающий при готовности модального окна получает в параметр jQuery-объект $modal\_body тела модального окна, все внутренности окна будут в нем |
| destroy | кастомный `destroy`, может вернуть `false`, тогда закрытия окна не произойдет |
| container | контейнер, куда попадет модальное окно и относительно какого элемента будет центрироваться |
| disable\_overlay\_click | если нужно запретить закрытие модального окна по клику на оверлэе, просто передаем в options `disable\_overlay\_click` |
| disable\_escape\_keydown | если нужно запретить закрытие модального окна по нажатию на escape |
| disable\_enter\_keydown | если нужно запретить дефолтную обработку enter |
| init\_animation | параметр отвечает за анимацию всплывания модального окна, если передать `true`, то оно запустится с анимацией увеличения и появления |
| default\_overlay | по умолчанию оверлей у модалок белый, изменить если нужен темный оверлей |
| preload\_templates | шаблоны для прелоада, можно передать массив необходимых шаблонов twig для подгрузки |
| focus\_element | элемент, который получает фокус, по умолчанию это кнопка акцепта. нужен для того, чтобы снимать фокус с кнопки вызвавшей событие |
| centrify\_animation | нужна ли анимация при центрировании модального окна |
| disable\_cancel\_click | отключает закрытие модального окна по крестику и оверлею |
| disable\_resize | отключить ресайз модального окна при инициализации |