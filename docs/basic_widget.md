# Детализированный план создания виджета-чата для amoCRM

## 1. Подготовка рабочего окружения
1. Создать пустую папку для виджета (например, `chat_widget`)
2. Создать базовую структуру директорий:
   - `/images` для логотипов
   - `/i18n` для файлов локализации
   - `/templates` для шаблонов (при необходимости)
   - `/css` для стилей

## 2. Подготовка логотипов
1. Создать логотипы и разместить их в папке `/images`:
   - logo_main.png (400x272px)
   - logo_small.png (108x108px)
   - logo.png (130x100px)
   - logo_medium.png (240x84px)
   - logo_min.png (84x84px)
   - logo_dp.png (174x109px) (для Digital Pipeline)

## 3. Создание файлов локализации
1. Создать файл `/i18n/ru.json`:
   ```json
   {
     "widget": {
       "name": "Чат-виджет",
       "short_description": "Простой чат для amoCRM",
       "description": "Виджет добавляет кнопку чата в интерфейс amoCRM"
     },
     "settings": {},
     "tour": {
       "description": "Виджет добавляет кнопку для открытия чата"
     },
     "userLang": {
       "chatButton": "Чат",
       "placeholder": "Введите сообщение...",
       "send": "Отправить",
       "close": "Закрыть"
     }
   }
   ```
2. Создать аналогичный файл `/i18n/en.json`

## 4. Создание CSS файла
1. Создать файл `/css/style.css`:
   ```css
   .chat-button {
     position: fixed;
     bottom: 20px;
     right: 20px;
     width: 50px;
     height: 50px;
     border-radius: 50%;
     background-color: #4285f4;
     color: white;
     font-size: 24px;
     border: none;
     cursor: pointer;
     box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
     z-index: 999;
   }

   .chat-window {
     position: fixed;
     bottom: 20px;
     right: 20px;
     width: 300px;
     height: 400px;
     border-radius: 10px;
     background-color: white;
     box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
     display: flex;
     flex-direction: column;
     overflow: hidden;
     z-index: 1000;
   }

   .chat-header {
     background-color: #4285f4;
     color: white;
     padding: 10px;
     display: flex;
     justify-content: space-between;
   }

   .chat-messages {
     flex: 1;
     padding: 10px;
     overflow-y: auto;
   }

   .message {
     margin-bottom: 10px;
     padding: 8px 12px;
     border-radius: 18px;
     max-width: 70%;
     word-wrap: break-word;
   }

   .message.user {
     background-color: #e3f2fd;
     margin-left: auto;
   }

   .chat-input {
     display: flex;
     padding: 10px;
     border-top: 1px solid #eee;
   }

   .chat-input input {
     flex: 1;
     padding: 8px;
     border: 1px solid #ddd;
     border-radius: 18px;
     margin-right: 8px;
   }

   .chat-input button {
     background-color: #4285f4;
     color: white;
     border: none;
     border-radius: 50%;
     width: 32px;
     height: 32px;
     cursor: pointer;
   }
   ```

## 5. Создание manifest.json
1. Создать файл `manifest.json`:
   ```json
   {
     "widget": {
       "name": "widget.name",
       "description": "widget.description",
       "short_description": "widget.short_description",
       "version": "1.0.0",
       "interface_version": 2,
       "init_once": false,
       "locale": ["ru", "en"],
       "installation": true,
       "support": {
         "link": "https://example.com/support",
         "email": "support@example.com"
       }
     },
     "locations": ["lcard-1", "ccard-1"],
     "tour": {
       "is_tour": true,
       "tour_images": {
         "ru": ["/images/logo.png"],
         "en": ["/images/logo.png"]
       },
       "tour_description": "tour.description"
     }
   }
   ```

## 6. Создание script.js
1. Создать файл `script.js`:
   ```javascript
   define(['jquery'], function ($) {
     var CustomWidget = function () {
       var self = this,
           system = self.system(),
           langs = self.langs,
           chatButton = null,
           chatWindow = null,
           chatMessages = null,
           chatInput = null,
           messages = [],
           isChatOpen = false;
           
       // Приватный метод для создания кнопки чата
       this.createChatButton = function() {
         if (chatButton) return chatButton;
         
         chatButton = $('<button>')
           .addClass('chat-button')
           .text('💬')
           .attr('title', self.i18n('userLang').chatButton)
           .on('click', function() {
             self.toggleChat();
           });
           
         return chatButton;
       };
       
       // Приватный метод для создания окна чата
       this.createChatWindow = function() {
         if (chatWindow) return chatWindow;
         
         var userLang = self.i18n('userLang');
         
         chatWindow = $('<div>').addClass('chat-window').hide();
         
         // Создаем заголовок чата
         var header = $('<div>').addClass('chat-header');
         $('<span>').text(userLang.chatButton).appendTo(header);
         $('<button>')
           .text('✖')
           .attr('title', userLang.close)
           .on('click', function() {
             self.toggleChat();
           })
           .appendTo(header);
         
         // Создаем контейнер для сообщений
         chatMessages = $('<div>').addClass('chat-messages');
         
         // Создаем форму ввода
         var inputContainer = $('<div>').addClass('chat-input');
         chatInput = $('<input>')
           .attr('type', 'text')
           .attr('placeholder', userLang.placeholder)
           .on('keydown', function(e) {
             if (e.key === 'Enter') {
               self.sendMessage();
             }
           })
           .appendTo(inputContainer);
         
         $('<button>')
           .text('➤')
           .attr('title', userLang.send)
           .on('click', function() {
             self.sendMessage();
           })
           .appendTo(inputContainer);
         
         // Собираем всё в окно чата
         chatWindow.append(header, chatMessages, inputContainer);
         
         return chatWindow;
       };
       
       // Метод для отображения/скрытия чата
       this.toggleChat = function() {
         isChatOpen = !isChatOpen;
         
         if (isChatOpen) {
           chatButton.hide();
           chatWindow.show();
         } else {
           chatWindow.hide();
           chatButton.show();
         }
       };
       
       // Метод для добавления сообщения в чат
       this.addMessage = function(text, sender) {
         var message = {
           text: text,
           sender: sender
         };
         
         messages.push(message);
         
         var messageEl = $('<div>')
           .addClass('message')
           .addClass(sender)
           .text(message.text);
         
         chatMessages.append(messageEl);
         chatMessages.scrollTop(chatMessages[0].scrollHeight);
       };
       
       // Метод для отправки сообщения
       this.sendMessage = function() {
         var text = chatInput.val().trim();
         
         if (!text) return;
         
         // Добавляем сообщение пользователя
         self.addMessage(text, 'user');
         
         // Очищаем поле ввода
         chatInput.val('');
         
         // Здесь можно добавить отправку сообщения на сервер, например:
         /*
         self.crm_post(
           'https://example.com/api/message',
           {
             message: text,
             user_id: self.system().amouser_id
           },
           function(response) {
             // Добавляем ответ от сервера
             if (response && response.message) {
               self.addMessage(response.message, 'bot');
             }
           },
           'json'
         );
         */
       };
       
       // Загрузка стилей виджета
       this.loadStyles = function() {
         var settings = self.get_settings();
         var version = settings.version || '1.0.0';
         
         if ($('link[href="' + settings.path + '/css/style.css?v=' + version + '"]').length < 1) {
           $('head').append('<link href="' + settings.path + '/css/style.css?v=' + version + '" type="text/css" rel="stylesheet">');
         }
       };

       this.callbacks = {
         // Функция init вызывается один раз при инициализации виджета
         init: function() {
           console.log('Initialization of chat widget');
           return true;
         },
         
         // Функция render вызывается каждый раз при отрисовке виджета
         render: function() {
           console.log('Render of chat widget');
           
           // Загружаем стили
           self.loadStyles();
           
           // Создаем элементы чата
           var button = self.createChatButton();
           var window = self.createChatWindow();
           
           // Добавляем элементы на страницу
           $('body').append(button, window);
           
           return true;
         },
         
         // Функция bind_actions вызывается сразу после render
         bind_actions: function() {
           console.log('Binding actions for chat widget');
           return true;
         },
         
         // Функция settings вызывается при открытии настроек виджета
         settings: function() {
           return true;
         },
         
         // Функция onSave вызывается при сохранении настроек
         onSave: function() {
           return true;
         },
         
         // Функция destroy вызывается при удалении виджета
         destroy: function() {
           // Удаляем созданные элементы
           if (chatButton) chatButton.remove();
           if (chatWindow) chatWindow.remove();
           
           // Очищаем переменные
           chatButton = null;
           chatWindow = null;
           chatMessages = null;
           chatInput = null;
           messages = [];
           isChatOpen = false;
         },
         
         // Обработчик выбора сделок
         leads: {
           selected: function() {
             return true;
           }
         },
         
         // Обработчик выбора контактов
         contacts: {
           selected: function() {
             return true;
           }
         }
       };
       
       return this;
     };
     
     return CustomWidget;
   });
   ```

## 7. Подготовка архива с виджетом
1. Создать архив виджета, включающий:
   - `manifest.json`
   - `script.js`
   - `/images` (с логотипами)
   - `/i18n` (с файлами локализации)
   - `/css` (со стилями)

## 8. Установка виджета в amoCRM
1. Войти в amoCRM с правами администратора
2. Перейти в раздел "Настройки" -> "Интеграции" -> "Разработчикам"
3. Выбрать "Загрузить виджет" и загрузить созданный архив
4. Выполнить настройку виджета (при необходимости)
5. Активировать виджет

## 9. Тестирование виджета
1. Перейти в карточку сделки или контакта
2. Убедиться, что кнопка чата отображается
3. Проверить открытие и закрытие окна чата
4. Проверить отправку сообщений

## 10. Отладка (при необходимости)
1. Использовать консоль браузера для просмотра ошибок
2. Проверить корректность работы всех колбэков виджета
3. Убедиться, что стили загружаются правильно
