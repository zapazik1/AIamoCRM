---
title: "Список изменений"
description: "Система amoCRM – удобная web программа для анализа продаж, доступная в режиме online из любой точки мира! Подробности узнавайте по указанным на сайте телефонам в Москве."
url: https://www.amocrm.ru/developers/content/changelog/main
section: developers
---

Начинания с 20 декабря 2021 мы будем вести changelog (список изменений) нашей документации, API, Web SDK.  
Все последние и грядущие изменения всегда отображаются наверху страницы в порядке от новых к старым.

### 27 января 2025

- Добавлена [документация](https://www.amocrm.ru/developers/content/digital_pipeline/salesbot#%D0%9E%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA-find) по обработчику find для типа catalog\_elements.

### 17 января 2025

- Обновлена статья [Salesbot](https://www.amocrm.ru/developers/content/digital_pipeline/salesbot). Добавлен новый обработчик `send_external_message` в salesbot.

### 4 октября 2024

- Обновлена статья [Разработка интеграций](https://www.amocrm.ru/developers/content/digital_pipeline/integrations). Добавлено новое свойство `direction_of_movement` в тело хука, отправляемого в интеграцию при срабатывании триггера.

### 4 июля 2024

- Обновлена статья [Поля и группы полей](https://www.amocrm.ru/developers/content/crm_platform/custom-fields). Добавлен новый параметр sort отвечающий за сортировку результатов списка.

### 28 марта 2024

- Добавлена информация о сообщениях с [List Message](https://www.amocrm.ru/developers/content/chats/chat-capabilities#%D0%9E%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D0%B9-List-Message-WhatsApp) для WhatsApp, и их [webhooks] в API Чатов ().

### 25 марта 2024

- Добавлены ключи tags\_to\_add и tags\_to\_delete в API создания и редактировния сделок/контактов/компаний/покупателей. С помощью ключей можно передать теги, которые нужно добавить и удалить. Данные ключи могут быть полезны для избежания коллизий, когда несколько интеграций могут одновременно изменять сущность.
- Добавлен флаг invoices\_settings в метод [API параметров аккаунта](https://www.amocrm.ru/developers/content/crm_platform/account-info)

### 24 марта 2024

- Обновлена статья [API шаблонов чатов](https://www.amocrm.ru/developers/content/crm_platform/chat-templates-api). Добавлены новые поля `waba_header`, `waba_header_type` Обновление информации о создании и редактировании шаблона WhatsApp с учетом новых полей.
- Обновлена статья [API источников](https://www.amocrm.ru/developers/content/crm_platform/sources-api). Добавлен параметр `is_supports_list_message`.

### 12 февраля 2024

- Добавлено описание долгосрочных токенов для oAuth авторизации. [Подробнее](https://www.amocrm.ru/developers/content/oauth/step-by-step#%D0%94%D0%BE%D0%BB%D0%B3%D0%BE%D1%81%D1%80%D0%BE%D1%87%D0%BD%D1%8B%D0%B5-%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D1%8B)

### 29 января 2024

- Добавлены методы для работы с источником CRM Plugin. [Подробнее](https://www.amocrm.ru/developers/content/crm_platform/sources-api).

### 25 января 2024

- Изменен хук об отключении интеграции. [Подробнее](https://www.amocrm.ru/developers/content/oauth/step-by-step#Хук-об-отключении-интеграции).

### 18 декабря 2023

- Обновлена статья [Поля и группы полей](https://www.amocrm.ru/developers/content/crm_platform/custom-fields). Добавлено описание для поля emums[0][id].

### 5 декабря 2023

- Добавлен метод для прослушивания канала сокетов [self.listenSocketChannel](https://www.amocrm.ru/developers/content/web_sdk/mechanics#listenSocketChannel).

### 22 ноября 2023

- Обновлена статья [Разрешения и права](https://www.amocrm.ru/developers/content/oauth/scopes). Введен заголовок X-Context-User-ID.

### 16 ноября 2023

- Обновлена статья [API источников](https://www.amocrm.ru/developers/content/crm_platform/sources-api). Добавлен параметр waba.
- Обновлена статья [API веб хуков](https://www.amocrm.ru/developers/content/crm_platform/webhooks-api). Добавлена новая подписка на хук add\_chat\_template\_review.
- Обновлена статья [API шаблонов чатов](https://www.amocrm.ru/developers/content/crm_platform/chat-templates-api). Добавлен раздел по работе со статусами шаблонов WhatsApp. Добавлена информация о создании и редактировании шаблона WhatsApp. Добавлена информация о работе со статусами WhatsApp шаблона.

### 15 ноября 2023

- Обновлена статья о типе поля [payer](https://www.amocrm.ru/developers/content/crm_platform/custom-fields#payer)

### 13 октября 2023

- Обновлена статья [Разрешения и права](https://www.amocrm.ru/developers/content/oauth/scopes). Введено понятие полный доступ.

### 22 сентября 2023

- Обновлена статья [Поля и группы полей](https://www.amocrm.ru/developers/content/crm_platform/custom-fields). Добавлены новые параметры дополнительного поля items, отвечающие за наличие перерасчета скидки и суммы товарной позиции в счете, а также за сумму товарной позиции.
- Обновлена статься [Списки](https://www.amocrm.ru/developers/content/crm_platform/catalogs-api). Добавлен новый параметр элемента списка, предупреждающий о наличии перерасчета в счете.

### 22 сентября 2023

- Изменен хук о реакции на сообщение, добавлена информация о сообщении. Подробнее в [Форматы вебхуков чатов](https://www.amocrm.ru/developers/content/chats/chat-webhooks#%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%B0-message-%D1%80%D0%B5%D0%B0%D0%BA%D1%86%D0%B8%D0%B8)

### 20 сентября 2023

- Обновлена статья [Разрешения и права](https://www.amocrm.ru/developers/content/oauth/scopes). Вернули возможность получить код авторизации для пользователей без прав администратора.

### 26 июля 2023

- Обновлена статья [Поля и группы полей](https://www.amocrm.ru/developers/content/crm_platform/custom-fields). Добавлена фильтрация по типу поля при получении списка полей.

### 24 мая 2023

- Обновлена статья [Разрешения и права](https://www.amocrm.ru/developers/content/oauth/scopes). Новая логика выдачи доступа интеграции.

### 15 мая 2023

- Добавлены описания новых типов полей – [Поставщик](https://www.amocrm.ru/developers/content/crm_platform/custom-fields#supplier) и [Плательщик](https://www.amocrm.ru/developers/content/crm_platform/custom-fields#payer)

### 11 мая 2023

- Обновлена статья [Переменные окружения](https://www.amocrm.ru/developers/content/web_sdk/env_variables). Объект AMOCRM заменен на объект APP.

### 11 мая 2023

- Добавлен with параметр descriptions в [API методах статусов](https://www.amocrm.ru/developers/content/crm_platform/leads_pipelines#Параметры-для-GET-параметра-with)
- Добавлена возможность добавления описаний статусов в [API методах добавления статусов](https://www.amocrm.ru/developers/content/crm_platform/leads-pipelines#Добавление-статусов-в-воронку)
- Добавлена возможность добавления/редактирования/удаления описаний статусов в [API методах редактирования статусов](https://www.amocrm.ru/developers/content/crm_platform/leads-pipelines#Редактирование-статуса-воронки)

### 10 мая 2023

- Обновлена [документация](https://www.amocrm.ru/developers/content/integrations/banks-and-acquiring) по размещению интеграций для работы с эквайрингами.

### 5 мая 2023

- Добавлен with параметр user\_rank в [API методах пользователей](https://www.amocrm.ru/developers/content/crm_platform/users-api#with-3b4e201a-ba14-4f06-880e-987e2c091855-params)

### 4 мая 2023

- Добавлено описание параметров, который нужно передавать при редактировании сообщений в [API методах чатов](https://www.amocrm.ru/developers/content/chats/chat-api-reference#%D0%9E%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0-%D1%80%D0%B5%D0%B4%D0%B0%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B8%D0%BB%D0%B8-%D0%B8%D0%BC%D0%BF%D0%BE%D1%80%D1%82-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D1%8F)
- Добавлено описание метода, который нужно использовать для проставления и снятия реакций у сообщений в [API методах чатов](https://www.amocrm.ru/developers/content/chats/chat-api-reference#%D0%9E%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0-%D0%B8%D0%BB%D0%B8-%D1%81%D0%BD%D1%8F%D1%82%D0%B8%D0%B5-%D1%80%D0%B5%D0%B0%D0%BA%D1%86%D0%B8%D0%B8)
- Добавлено описание параметров, который приходят в вебхуках при использовании реакций в [API чатов](https://www.amocrm.ru/developers/content/chats/chat-webhooks#%D0%A5%D1%83%D0%BA-%D0%BE-%D1%80%D0%B5%D0%B0%D0%BA%D1%86%D0%B8%D0%B8)

### 28 апреля 2023

- Добавлено описание параметров, который нужно передавать при использовании цитат в [API методах чатов](https://www.amocrm.ru/developers/content/chats/chat-api-reference)
- Добавлено описание параметров, который приходят в вебхуках при использовании цитат в [API чатов](https://www.amocrm.ru/developers/content/chats/chat-webhooks)

### 7 февраля 2023

- Добавлен параметр call\_responsible в [API добавления звонков](https://www.amocrm.ru/developers/content/crm_platform/calls-api)
- Добавлен параметр call\_responsible в [API добавления неразобранного типа звонок](https://www.amocrm.ru/developers/content/crm_platform/unsorted-api#metadata-description)
- Добавлено описание отображения звонка в карточке в [соответствующую статью](https://www.amocrm.ru/developers/content/telephony/capabilities-2)

### 3 февраля 2023

- Добавлены методы для работы группами полей списков в [API списков](https://www.amocrm.ru/developers/content/crm_platform/custom-fields)

### 23 января 2023

- Добавлен метод объекта Widget для получения данных контактов из области карточки [this.get\_current\_card\_contacts\_data](https://www.amocrm.ru/developers/content/web_sdk/mechanics#get_current_card_contacts_data)

### 18 января 2023

- Добавлено описание возможностей [API файлов](https://www.amocrm.ru/developers/content/files/files-api).
- Добавлено описание методов [API файлов](https://www.amocrm.ru/developers/content/files/files-capabilities).
- Добавлено описание использования файлов из API файлов в [шаблонах сообщений](https://www.amocrm.ru/developers/content/crm_platform/chat-templates-api).
- Добавлено описание использования файлов из API файлов в [доп полях](https://www.amocrm.ru/developers/content/crm_platform/custom-fields).
- Добавлено описание использования файлов из API файлов в [примечаниях](https://www.amocrm.ru/developers/content/crm_platform/events-and-notes).
- Добавлено описание [scope](https://www.amocrm.ru/developers/content/oauth/scopes) для API файлов.

### 12 января 2023

- Добавлен параметр origin\_code в [API источников](https://www.amocrm.ru/developers/content/crm_platform/sources-api).

### 25 декабря 2023

- Добавлен параметр is\_need\_to\_trigger\_digital\_pipeline при добавлении примечаний в [API примечаний](https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#notes-add).

### 09 декабря 2023

- Добавлен флаг хранит ли интеграция файлы или нет, который нужно указать при [создании канала в API чатов](https://www.amocrm.ru/developers/content/chats/chat-start#%D0%A0%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%BA%D0%B0%D0%BD%D0%B0%D0%BB%D0%B0).

### 15 ноября 2022

- Добавлена документация по [виджетам в кабинете клиента](https://www.amocrm.ru/developers/content/web_sdk/personal_page).

### 27 октября 2022

- Добавлена [статья](https://www.amocrm.ru/developers/content/crm_platform/separate-platforms) про разделение amoCRM на amocrm.ru и kommo.com

### 20 июля 2022

- В раздел "Интеграции" добавлена статья "[Рекламное размещение](https://www.amocrm.ru/developers/content/integrations/advertising)".

### 14 июля 2022

- Обновлена документация по [требованиям к публичным интеграциям](https://www.amocrm.ru/developers/content/integrations/requirements).

### 24 июня 2022

- Добавлен колбек `onConversationsChange` [в crmPlugin](https://www.amocrm.ru/developers/content/web_sdk/crm_plugin).

### 21 июня 2022

- Добавлены [документация по новым типам полей](https://www.amocrm.ru/developers/content/crm_platform/custom-fields), доступых в обновлении Весна 2022: Денежное, Связанные списки, Каталоги и списки.
- Добавлена поддержка установки символьного кода для enum значений полей с множественным выбором.

### 15 июня 2022

- Добавлен метод `runDestroy` [в crmPlugin](https://www.amocrm.ru/developers/content/web_sdk/crm_plugin).

### 08 июня 2022

- Добавлен раздел с инструкцией для интеграторов по [релизу ВЕСНА 2022](https://www.amocrm.ru/developers/content/integrations/release-spring-2022).
- Обновлена документация по [требованиям к публичным интеграциям](https://www.amocrm.ru/developers/content/integrations/requirements).

### 11 мая 2022

- Добавлена поддержка [цвета тегов](https://www.amocrm.ru/developers/content/crm_platform/tags-api) для новой версии amoCRM.
- Цвет тегов теперь возвращается в [моделях сущностей](https://www.amocrm.ru/developers/content/crm_platform/leads-api) для новой версии amoCRM.

### 16 февраля 2022

- Обновлен раздел API кнопки на сайте. Добавлена информация о [кастомном user\_id](https://www.amocrm.ru/developers/content/web_sdk/crm_plugin#%D0%98%D0%B7%D0%BC%D0%B5%D0%BD%D0%B8%D1%82%D1%8C-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F-%D1%87%D0%B0%D1%82%D0%B0).

### 10 февраля 2022

- Обновлена документация по [требованиям к публичным интеграциям](https://www.amocrm.ru/developers/content/integrations/requirements).

### 03 февраля 2022

- Перенесли статью [JS SDK](https://www.amocrm.ru/developers/content/web_sdk/js_sdk) из раздела "Интеграции" в раздел "WEB SDK".

### 21 января 2022

- Добавлена поддержка `_embedded[source][external_id]` и `_embedded[source][type]` в методы [добавления сделок](https://www.amocrm.ru/developers/content/crm_platform/leads-api)
- Обновлена информация по местам использования источников, созданных через [API источников](https://www.amocrm.ru/developers/content/crm_platform/sources-api)
- Добавлена информация о галке "Множественные источники" при создании интеграции в [статье](https://www.amocrm.ru/developers/content/oauth/step-by-step)

### 20 января 2022

- Добавлена [сравнительная таблица типов интеграций](https://www.amocrm.ru/developers/content/integrations/intro), которая поможет выбрать подходящий для вас тип интеграции.

### 13 января 2022

- Обновлена документация по [требованиям к публичным интеграциям](https://www.amocrm.ru/developers/content/integrations/requirements)

### 28 декабря 2021

- Добавлена документация по [процессу модерации](https://www.amocrm.ru/developers/content/integrations/moderation).

### 24 декабря 2021

- Добавлена документация по [методам API](https://www.amocrm.ru/developers/content/crm_platform/chat-templates-api) для работы с шаблонами чатов.
- Добавлен параметр external\_id в объект шаблона в [хуках чатов](https://www.amocrm.ru/developers/content/chats/chat-webhooks).

### 20 декабря 2021

- Полностью обновлен раздел документации [API чатов](https://www.amocrm.ru/developers/content/chats/chat-capabilities) с описанием всех доступных возможностей.
- Добавлена документация по [методам API](https://www.amocrm.ru/developers/content/crm_platform/sources-api) для работы с источниками.
- Обновлен раздел [предметная область](https://www.amocrm.ru/developers/content/crm_platform/subject_area).
- В раздел [API Reference](https://www.amocrm.ru/developers/content/crm_platform/api-reference) добавлена информация об источниках.
- Обновлён раздел oAuth -> [Пример по шагам](https://www.amocrm.ru/developers/content/oauth/step-by-step).
- Добавлен [раздел с документацией](https://www.amocrm.ru/developers/content/web_sdk/forms) по методам форм, размещаемых на сайт.
- Добавлен новый параметр context в callback settings у виджетов. [Подробнее](https://www.amocrm.ru/developers/content/web_sdk/settings#settings).