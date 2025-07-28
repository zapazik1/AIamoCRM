---
title: "Синхронизация задач"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/web/sdk/todo/sync
section: developers
---

Если виджет предоставляет возможность синхронизации задач amoCRM с другими сервисами управления задачами, то он может встроиться в модальное окно синхронизации.

![](/uploads/2020/06/image1-3-1024x615.png)

Для этого необходимо указать локейшны задач в **manifest.json**:

```
{

  ...

  "locations": [

    "tlist",

    "tline",

    "tcalendar"

  ],

  ...

}
```

В колбэках виджета также есть специальный колбэк “**calendarSync**”, который выполнится при открытии данного модального окна, он обязательно должен возвращать объект с определенного вида, что описан в примере ниже.

```
this.callbacks: {

  calendarSync: function() {

    var load_promise = new Promise(function(resolve, reject) {

      // Запрос на бэк-энд для получения статуса виджета

      setTimeout(resolve, 2000);

    }

  

    return {

      // {String} Заголовок виджета в модалке синхронизации

      name: this.langs.widget.name,

      // {String} Описание виджета в модалке синхронизации

      description: this.langs.widget.description,

      // {Boolean|Promise} Состояние синхронизации.

      // Если Boolean, то виджет сразу примет это состояние,

      // но обычно нужно сделать запрос на back-end, 

      // поэтому можно вернуть promise, где resolve(true|false)

      // задаст состояние синхронизации виджета после получения ответа,

      // А reject([error_msg]) выведет сообщение об ошибке.

      enabled: load_promise || false,

      // {Function} Callback на нажатие кнопки "Включить".

      // Должен вернуть Promise

      onEnable: function() {

        return new Promise(function(resolve, reject) {

          if (confirm('Вы действительно хотите установить виджет')) {

            resolve();

          } else {

            reject('Вы отказались от установки виджета')

          }

      },

      // {Function} Callback на нажатие кнопки "Отключить".

      // Должен вернуть Promise

      onDisable: function() {

        return new Promise(function(resolve, reject) {

          var answer = prompt('Введите секретный ключ для подтверждения отключения:');

          

          if (answer === 'Super manager!') {

            resolve();

          } else {

            reject('Неверный секретный ключ.')

          }

      },

      // {Function} - Необязательный Callback на нажатие кнопки настроек.

      // Когда есть, в правом углу виджета появляется шестеренка с настройками.

      // На нажатие по ней можно написать свою логику.

      // Функция может ничего не возвращать.

      onSetup: function() {

        // Ваш код

      },

    };

  }

}

```