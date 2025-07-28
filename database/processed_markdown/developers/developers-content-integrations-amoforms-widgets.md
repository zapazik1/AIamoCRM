---
title: "Виджеты в веб-формах"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/integrations/amoforms-widgets
section: developers
---

### Возможности и принципы работы виджетов в веб-формах

Начиная с релиза “Весна 2021”, мы добавили возможность добавлять виджеты в веб-формы

**Начало работы**

Чтобы существующий или новый виджет начал поддерживать функционал работы в веб-формах, вам необходимо добавить новый объект amoforms\_settings и указать дополнительный location amoforms в [файле manifest.json](/developers/content/integrations/structure#manifest).

Location **amoforms**, говорит о том, что виджет готов к работе в веб-формах

#### Параметры объекта amoforms\_settings

| Параметр | Тип данных | Описание |
| --- | --- | --- |
| title | string | Ключ в ланг файле для отображения названия пункта виджета в веб-формах. **Обязательный параметр** |
| required | boolean | Обязательность в веб-формах, прежде чем клиент нажмет обычную кнопку “Отправить”, ему необходимо нажать на кнопку виджета. **Необязательный параметр** |
| error\_text | string | Ключ в ланг файле для отображения ошибки виджета в веб-формах. **Необязательный параметр** |

**Обработка данных клиента**

После того, как клиент нажмет на кнопку виджета, вы можете обработать данные. Для этого необходимо реализовать файл amoforms.js на одном уровне с script.js

#### Пример amoforms.js

```
amoFormsWidget(function (params) {
var result = {};
console.log(params); // данные о веб-форме
alert('Модалка');
setTimeout(() => {
result.safasf = 123;
}, 1000);
// эту функцию мы выполним,
// когда пользователь нажмет на кнопку отправить
return function (FORM\_REQUEST\_ID) {
// FORM\_REQUEST\_ID - идентификатор заявки формы
// его же мы пришлем в хуке при создании/обновлении сделки
// для этого, вам необходимо подписаться на хуки в Настройки -> Интеграции -> Webhooks
return new Promise(function (resolve, reject) {
setTimeout(function () {
// отправляем
console.log('send data to server', result, FORM\_REQUEST\_ID);
resolve({ status: "ok", request\_id: FORM\_REQUEST\_ID });
}, 2000);
});
};
});
```

#### Пример входных данных amoFormsWidget, если это обычная веб-форма

```
{
"payload": {
"accountHash": "7BVxbn2TyWyZuWqTOPBNqlzlxIH7s9RnizIR0oNpFk/BVeUgXyA3bj9lNzXDqT2k",
"entity": {}
}
}
```

#### Пример входных данных amoFormsWidget, если это индивидуальная или реферальная анкета

```
{
"payload": {
"accountHash": "7BVxbn2TyWyZuWqTOPBNqlzlxIH7s9RnizIR0oNpFk8OTupMxh4pUpSNzgIBl6dx",
"entity": {
"entity\_type": 2,
"entity\_id": 10423467
}
}
}
```

#### Пример расшифровки accountHash с помощью PHP

```
$accountHash = '7BVxbn2TyWyZuWqTOPBNqlzlxIH7s9RnizIR0oNpFk8OTupMxh4pUpSNzgIBl6dx'; //Зашифрованный идентификатор аккаунта и формы
$clientSecret = 'PhYB7AUmMYr8InTALNYfvePZY33B6Vqs7UeFyM3sUIMHQMuedGlfX6r8vaSSASDsd'; //client\_secret вашей интеграции
$decrypt = openssl\_decrypt($accountHash, 'aes-256-cbc', $clientSecret);
var\_dump($decrypt);
// Output:
string(40) "{"account\_id":12345678,"form\_id":12345}"
```