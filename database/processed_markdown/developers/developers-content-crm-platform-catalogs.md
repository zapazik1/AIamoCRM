---
title: "Списки"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/crm/platform/catalogs
section: developers
---

### Добавление, обновление и удаление списков

Эти методы доступны только пользователям, у которые есть права на доступ к спискам. Методы позволяют добавлять списки по одному или пакетно, а также обновлять данные по уже существующим спискам и удалять их.

##### URL метода

*POST /api/v2/catalogs*

#### Параметры

| Параметр | Тип | Описание |
| --- | --- | --- |
| add | array | Перечень добавляемых списков |
| update | array | Обновление существующих списков   Все параметры, которые описанны в add действуют также и в update |
| delete | array | Перечень удаляемых списков |
| add/name  *require* | string | Название списка |
| add/type | string | Тип списка   “regular” – список, “invoices” – счета |
| add/can\_add\_elements | bool | Добавление счета из интерфейса |
| add/can\_show\_in\_cards | bool | Возможность добавить вкладку со списком в карточку сделки/покупателя |
| add/can\_link\_multiple | bool | Возможность привязывать один элемент данного списка к нескольким сделкам/покупателям |
| add/request\_id | int | Уникальный идентификатор записи в клиентской программе, необязательный параметр (информация о request\_id нигде не сохраняется) |
| update/id  *require* | int | Уникальный идентификатор списка, который указывается с целью его обновления |
| delete  *require* | array | Массив с уникальными идентификаторами списков, которые указываются с целью удаления |

Пример запроса на добавление списка

#### Пример запроса

```
{
add: [
{
name: "Товары"
}
]
}
```

Пример запроса на обновление списка

#### Пример запроса

```
{
update: [
{
id: "2456" ,
name: "Товары"
}
]
}
```

Пример запроса на удаление списков

#### Пример запроса:

```
{
delete : [
{
2456 ,
2472 ,
2483
}
]
}
```

#### Параметры ответа

| Параметр | Описание |
| --- | --- |
| id | Уникальный идентификатор новой сущности |
| request\_id | Уникальный идентификатор сущности в клиентской программе, если request\_id не передан в запросе, то он генерируется автоматически |
| \_links | Массив содержащий информацию о запросе |
| \_links/self | Массив содержащий информацию о текущем запросе |
| \_links/self/href | Относительный URL текущего запроса |
| \_links/self/method | Метод текущего запроса |
| \_embedded | Массив содержащий информацию прилегающую к запросу |
| \_embedded/items | Массив содержащий информацию по каждому отдельному элементу |

#### Пример ответа

```
{
\_link: {
self: {
href: "/api/v2/catalogs" ,
method: "post"
}
} ,
\_embedded: {
items: [
{
id: 4223 ,
\_link: {
self: {
href: "/api/v2/catalogs?id=4223" ,
method: "get"
}
}
}
]
}
}
```

#### Добавление списков

Для создания нового спискаа необходимо описать массив, содержащий информацию о нём и поместить его в массив следующего вида: **$catalogs[‘add’]**

Наше API также поддерживает одновременное добавление сразу нескольких списков. Для этого мы помещаем в массив **$catalogs[‘add’]** несколько массивов, каждый из которых описывает необходимые данные для создания соответствующего списка.

#### Пример интеграции

```
$catalogs['add'] = array(
array(
'name' => 'Tariffs',
),
array(
'name' => 'Products',
),
);
/\* Теперь подготовим данные, необходимые для запроса к серверу \*/
$subdomain = 'test'; #Наш аккаунт - поддомен
#Формируем ссылку для запроса
$link = 'https://' . $subdomain . '.amocrm.ru/api/v2/catalogs';
/\* Нам необходимо инициировать запрос к серверу. Воспользуемся библиотекой cURL (поставляется в составе PHP). Подробнее о работе с этой
библиотекой Вы можете прочитать в мануале. \*/
$curl = curl\_init(); #Сохраняем дескриптор сеанса cURL
#Устанавливаем необходимые опции для сеанса cURL
curl\_setopt($curl, CURLOPT\_RETURNTRANSFER, true);
curl\_setopt($curl, CURLOPT\_USERAGENT, 'amoCRM-API-client/1.0');
curl\_setopt($curl, CURLOPT\_URL, $link);
curl\_setopt($curl, CURLOPT\_CUSTOMREQUEST, 'POST');
curl\_setopt($curl, CURLOPT\_POSTFIELDS, json\_encode($catalogs));
curl\_setopt($curl, CURLOPT\_HTTPHEADER, array('Content-Type: application/json'));
curl\_setopt($curl, CURLOPT\_HEADER, false);
curl\_setopt($curl, CURLOPT\_COOKIEFILE, dirname(\_\_FILE\_\_) . '/cookie.txt'); #PHP>5.3.6 dirname(\_\_FILE\_\_) -> \_\_DIR\_\_
curl\_setopt($curl, CURLOPT\_COOKIEJAR, dirname(\_\_FILE\_\_) . '/cookie.txt'); #PHP>5.3.6 dirname(\_\_FILE\_\_) -> \_\_DIR\_\_
curl\_setopt($curl, CURLOPT\_SSL\_VERIFYPEER, 0);
curl\_setopt($curl, CURLOPT\_SSL\_VERIFYHOST, 0);
$out = curl\_exec($curl); #Инициируем запрос к API и сохраняем ответ в переменную
$code = curl\_getinfo($curl, CURLINFO\_HTTP\_CODE);
/\* Теперь мы можем обработать ответ, полученный от сервера. Это пример. Вы можете обработать данные своим способом. \*/
$code = (int)$code;
$errors = array(
301 => 'Moved permanently',
400 => 'Bad request',
401 => 'Unauthorized',
403 => 'Forbidden',
404 => 'Not found',
500 => 'Internal server error',
502 => 'Bad gateway',
503 => 'Service unavailable',
);
try {
#Если код ответа не равен 200 или 204 - возвращаем сообщение об ошибке
if ($code != 200 && $code != 204) {
throw new Exception(isset($errors[$code]) ? $errors[$code] : 'Undescribed error', $code);
}
} catch (Exception $E) {
die('Ошибка: ' . $E->getMessage() . PHP\_EOL . 'Код ошибки: ' . $E->getCode());
}
/\*
Данные получаем в формате JSON, поэтому, для получения читаемых данных,
нам придётся перевести ответ в формат, понятный PHP
\*/
$Response = json\_decode($out, true);
$Response = $Response['\_embedded']['items'];
$output = 'ID добавленных каталогов:' . PHP\_EOL;
foreach ($Response as $v) {
if (is\_array($v)) {
$output .= $v['id'] . PHP\_EOL;
}
}
return $output;
```

#### Обновление списков

Для обновления списка необходимо описать массив, содержащий информацию о нём и поместить его в массив следующего вида: **$catalogs[‘update’]**

Наше API также поддерживает одновременное обновление сразу нескольких списков. Для этого мы помещаем в массив **$catalogs[‘update’]** несколько массивов, каждый из которых описывает необходимые данные для обновления соответствующего списка.

#### Пример интеграции

```
$catalogs['update'] = array(
array(
'id' => 2561,
'name' => 'Products',
),
array(
'id' => 2562,
'name' => 'Cars',
),
);
/\* Теперь подготовим данные, необходимые для запроса к серверу \*/
$subdomain = 'test'; #Наш аккаунт - поддомен
#Формируем ссылку для запроса
$link = 'https://' . $subdomain . '.amocrm.ru/api/v2/catalogs';
/\* Нам необходимо инициировать запрос к серверу. Воспользуемся библиотекой cURL (поставляется в составе PHP). Подробнее о работе с этой
библиотекой Вы можете прочитать в мануале. \*/
$curl = curl\_init(); #Сохраняем дескриптор сеанса cURL
#Устанавливаем необходимые опции для сеанса cURL
curl\_setopt($curl, CURLOPT\_RETURNTRANSFER, true);
curl\_setopt($curl, CURLOPT\_USERAGENT, 'amoCRM-API-client/1.0');
curl\_setopt($curl, CURLOPT\_URL, $link);
curl\_setopt($curl, CURLOPT\_CUSTOMREQUEST, 'POST');
curl\_setopt($curl, CURLOPT\_POSTFIELDS, json\_encode($catalogs));
curl\_setopt($curl, CURLOPT\_HTTPHEADER, array('Content-Type: application/json'));
curl\_setopt($curl, CURLOPT\_HEADER, false);
curl\_setopt($curl, CURLOPT\_COOKIEFILE, dirname(\_\_FILE\_\_) . '/cookie.txt'); #PHP>5.3.6 dirname(\_\_FILE\_\_) -> \_\_DIR\_\_
curl\_setopt($curl, CURLOPT\_COOKIEJAR, dirname(\_\_FILE\_\_) . '/cookie.txt'); #PHP>5.3.6 dirname(\_\_FILE\_\_) -> \_\_DIR\_\_
curl\_setopt($curl, CURLOPT\_SSL\_VERIFYPEER, 0);
curl\_setopt($curl, CURLOPT\_SSL\_VERIFYHOST, 0);
$out = curl\_exec($curl); #Инициируем запрос к API и сохраняем ответ в переменную
$code = curl\_getinfo($curl, CURLINFO\_HTTP\_CODE);
/\* Теперь мы можем обработать ответ, полученный от сервера. Это пример. Вы можете обработать данные своим способом. \*/
$code = (int)$code;
$errors = array(
301 => 'Moved permanently',
400 => 'Bad request',
401 => 'Unauthorized',
403 => 'Forbidden',
404 => 'Not found',
500 => 'Internal server error',
502 => 'Bad gateway',
503 => 'Service unavailable',
);
try {
#Если код ответа не равен 200 или 204 - возвращаем сообщение об ошибке
if ($code != 200 && $code != 204) {
throw new Exception(isset($errors[$code]) ? $errors[$code] : 'Undescribed error', $code);
}
} catch (Exception $E) {
die('Ошибка: ' . $E->getMessage() . PHP\_EOL . 'Код ошибки: ' . $E->getCode());
}
```

#### Удаление списков

Для удаления списка необходимо описать массив, содержащий информацию о нём и поместить его в массив следующего вида: **$catalogs[‘delete’]**

Наше API также поддерживает одновременное удаление сразу нескольких списков. Для этого мы помещаем в массив **$catalogs[‘delete’]** несколько элементов, каждый из которых описывает необходимые данные для удаления соответствующего списка.

#### Пример интеграции

```
$catalogs['delete'] = array(
2561,
2562,
);
/\* Теперь подготовим данные, необходимые для запроса к серверу \*/
$subdomain = 'test'; #Наш аккаунт - поддомен
#Формируем ссылку для запроса
$link = 'https://' . $subdomain . '.amocrm.ru/api/v2/catalogs';
/\* Нам необходимо инициировать запрос к серверу. Воспользуемся библиотекой cURL (поставляется в составе PHP). Подробнее о работе с этой
библиотекой Вы можете прочитать в мануале. \*/
$curl = curl\_init(); #Сохраняем дескриптор сеанса cURL
#Устанавливаем необходимые опции для сеанса cURL
curl\_setopt($curl, CURLOPT\_RETURNTRANSFER, true);
curl\_setopt($curl, CURLOPT\_USERAGENT, 'amoCRM-API-client/1.0');
curl\_setopt($curl, CURLOPT\_URL, $link);
curl\_setopt($curl, CURLOPT\_CUSTOMREQUEST, 'POST');
curl\_setopt($curl, CURLOPT\_POSTFIELDS, json\_encode($catalogs));
curl\_setopt($curl, CURLOPT\_HTTPHEADER, array('Content-Type: application/json'));
curl\_setopt($curl, CURLOPT\_HEADER, false);
curl\_setopt($curl, CURLOPT\_COOKIEFILE, dirname(\_\_FILE\_\_) . '/cookie.txt'); #PHP>5.3.6 dirname(\_\_FILE\_\_) -> \_\_DIR\_\_
curl\_setopt($curl, CURLOPT\_COOKIEJAR, dirname(\_\_FILE\_\_) . '/cookie.txt'); #PHP>5.3.6 dirname(\_\_FILE\_\_) -> \_\_DIR\_\_
curl\_setopt($curl, CURLOPT\_SSL\_VERIFYPEER, 0);
curl\_setopt($curl, CURLOPT\_SSL\_VERIFYHOST, 0);
$out = curl\_exec($curl); #Инициируем запрос к API и сохраняем ответ в переменную
$code = curl\_getinfo($curl, CURLINFO\_HTTP\_CODE);
/\* Теперь мы можем обработать ответ, полученный от сервера. Это пример. Вы можете обработать данные своим способом. \*/
$code = (int)$code;
$errors = array(
301 => 'Moved permanently',
400 => 'Bad request',
401 => 'Unauthorized',
403 => 'Forbidden',
404 => 'Not found',
500 => 'Internal server error',
502 => 'Bad gateway',
503 => 'Service unavailable',
);
try {
#Если код ответа не равен 200 или 204 - возвращаем сообщение об ошибке
if ($code != 200 && $code != 204) {
throw new Exception(isset($errors[$code]) ? $errors[$code] : 'Undescribed error', $code);
}
} catch (Exception $E) {
die('Ошибка: ' . $E->getMessage() . PHP\_EOL . 'Код ошибки: ' . $E->getCode());
}
```

### Перечень списков

Метод для получения перечня списков аккаунта.

##### URL метода

*GET /api/v2/catalogs*

#### Параметры GET

| Параметр | Описание |
| --- | --- |
| id | Выбрать элемент с заданным ID |

#### Параметры ответа

| Параметр | Тип | Описание |
| --- | --- | --- |
| id | int | Уникальный идентификатор списка |
| name | string | Название списка |
| created\_by | int | ID пользователя, создавшего список |
| created\_at | timestamp | Дата создания |
| sort | int | Параметр указывает на каком месте будет находиться список |
| \_links | array | Массив содержащий информацию о запросе |
| \_links/self | array | Массив содержащий информацию о текущем запросе |
| \_links/self/href | string | Относительный URL текущего запроса |
| \_links/self/method | string | Метод текущего запроса |
| \_embedded | array | Массив содержащий информацию прилегающую к запросу |
| \_embedded/items | array | Массив содержащий информацию по каждому отдельному элементу |

#### Пример ответа

```
{
\_links: {
self: {
href: "/api/v2/catalogs" ,
method: "get"
}
} ,
\_embedded: {
items: [
{
id: 4223 ,
name: "Товары" ,
created\_by: 504141 ,
created\_at: 1508930391 ,
sort: 10 ,
\_links: {
self: {
href: "/api/v2/catalogs?id=4223" ,
method: "get"
}
}
} ,
{
id: 4222 ,
name: "Услуги" ,
created\_by: 504141 ,
created\_at: 1508930288 ,
sort: 20 ,
\_links: {
self: {
href: "/api/v2/catalogs?id=4222" ,
method: "get"
}
}
}
]
}
}
```

#### Пример запроса:

```
/\* Для начала нам необходимо инициализировать данные, необходимые для составления запроса. \*/
$subdomain = 'test'; #Наш аккаунт - поддомен
#Формируем ссылку для запроса
$link = 'https://' . $subdomain . '.amocrm.ru/api/v2/catalogs';
/\* Заметим, что в ссылке можно передавать и другие параметры, которые влияют на выходной результат (смотрите документацию).
Следовательно, мы можем заменить ссылку, приведённую выше на одну из следующих, либо скомбинировать параметры так, как Вам необходимо. \*/
$link = 'https://' . $subdomain . '.amocrm.ru/api/v2/catalogs';
$link = 'https://' . $subdomain . '.amocrm.ru/api/v2/catalogs?id=2634';
/\* Нам необходимо инициировать запрос к серверу. Воспользуемся библиотекой cURL (поставляется в составе PHP). Подробнее о работе с этой
библиотекой Вы можете прочитать в мануале. \*/
$curl = curl\_init(); #Сохраняем дескриптор сеанса cURL
#Устанавливаем необходимые опции для сеанса cURL
curl\_setopt($curl, CURLOPT\_RETURNTRANSFER, true);
curl\_setopt($curl, CURLOPT\_USERAGENT, 'amoCRM-API-client/1.0');
curl\_setopt($curl, CURLOPT\_URL, $link);
curl\_setopt($curl, CURLOPT\_HEADER, false);
curl\_setopt($curl, CURLOPT\_COOKIEFILE, dirname(\_\_FILE\_\_) . '/cookie.txt'); #PHP>5.3.6 dirname(\_\_FILE\_\_) -> \_\_DIR\_\_
curl\_setopt($curl, CURLOPT\_COOKIEJAR, dirname(\_\_FILE\_\_) . '/cookie.txt'); #PHP>5.3.6 dirname(\_\_FILE\_\_) -> \_\_DIR\_\_
curl\_setopt($curl, CURLOPT\_SSL\_VERIFYPEER, 0);
curl\_setopt($curl, CURLOPT\_SSL\_VERIFYHOST, 0);
// Выполняем запрос к серверу.
$out = curl\_exec($curl); #Инициируем запрос к API и сохраняем ответ в переменную
$code = curl\_getinfo($curl, CURLINFO\_HTTP\_CODE);
curl\_close($curl);
/\* Теперь мы можем обработать ответ, полученный от сервера. Это пример. Вы можете обработать данные своим способом. \*/
$code = (int)$code;
$errors = array(
301 => 'Moved permanently',
400 => 'Bad request',
401 => 'Unauthorized',
403 => 'Forbidden',
404 => 'Not found',
500 => 'Internal server error',
502 => 'Bad gateway',
503 => 'Service unavailable',
);
try {
#Если код ответа не равен 200 или 204 - возвращаем сообщение об ошибке
if ($code != 200 && $code != 204) {
throw new Exception(isset($errors[$code]) ? $errors[$code] : 'Undescribed error', $code);
}
} catch (Exception $E) {
die('Ошибка: ' . $E->getMessage() . PHP\_EOL . 'Код ошибки: ' . $E->getCode());
}
/\*
Данные получаем в формате JSON, поэтому, для получения читаемых данных,
нам придётся перевести ответ в формат, понятный PHP
\*/
$Response = json\_decode($out, true);
$Response = $Response['\_embedded']['items'];
```