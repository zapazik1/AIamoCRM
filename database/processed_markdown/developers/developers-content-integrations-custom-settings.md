---
title: "Расширенные настройки"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/integrations/custom/settings
section: developers
---

### Расширенные настройки виджета

Виджеты amoCRM поддерживают добавление на страничку настроек виджета собственной программной логики – поля произвольной структуры и внешнего вида.

Поле произвольной структуры состоит из hidden input (поле, через которое осуществляется чтение и сохранение ), div -элемента, в который можно выводить DOM-элементы для взаимодействия с пользователем и некотого javascript-кода, который обеспечивает необходимую логику.

Для использования поля произвольной структуры необходимо сделать два простых шага:

1. Добавить поле в manifest.json и разрешить виджету исполняться на страничке настроек
2. Реализовать чтение и запись данных

#### Описание поля произвольной структуры в manifest.json

Это самое обычное поле со специальным типом custom, возможно не более одного такого поля в одном виджете. Не забудьте добавить местоположение “settings” в массив locations в mainfest.json!

**Важно:** поле с типом “custom” может содержать json-строку либо число. Строчный тип данных на сервере сохраняться не будет.

```
"settings": {
"apikey": {
...
},
...,
"myfield": {
"name": "settings.apikey",
"type": "custom",
"required": false
}
}
}
```

Соберите виджет и загрузите его в аккаунт. Вам станет доступен div с ID \_custom\_content и hidden input с ID \_custom.

Чтобы изменения вашего поля отражались в форме и ее кнопках, нужно создавать событие change на спрятанном системном инпуте. Вот пример того, как можно это сделать:

```
$( 'input[name="имя вашего поля"]' ).trigger ( 'change' ) ;
```

### Страница виджета в разделе “Настройки”

Виджеты amoCRM могут создавать свою собственную страницу в разделе “Настройки”

Для этого необходимо в списке [областей подключения](/developers/content/integrations/areas) виджета указать область advanced\_settings. На данной странице у виджета будет срабатывать callback advancedSettings.

Данная странице полностью контролируется виджетом. DOM-страницы и её структуру виджеты должны формировать сами.

Также, виджету необходимо в задать новый блок advanced в manifest.json, в котором будет храниться ключ title – наименование данной страницы.

Пример файла manifest.json

```
{
"widget": {
"name": "widget.name",
"description": "widget.description",
"short\_description": "widget.short\_description",
"code": "example\_widget",
"secret\_key": "e2888047a01bc97aa250118c2fa518dba57a4034ccf16dca784dca292d89324f",
"version": "1.9",
"interface\_version": 2,
"init\_once": false,
"locale": [
"ru"
],
"installation": true
},
"locations": [
"everywhere",
"settings",
"advanced\_settings"
],
"settings": {
"login": {
"name": "settings.login",
"type": "text",
"required": false
}
},
"advanced": {
"title": "advanced.title"
}
}
```

[JS SDK](/developers/content/integrations/js_sdk)