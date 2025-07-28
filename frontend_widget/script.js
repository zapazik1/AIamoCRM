define(['jquery'], function ($) {
    var CustomWidget = function () {
      var self = this,
          system = self.system(),
          langs = self.langs,
          chatButton = null,
          chatWindow = null,
          chatMessages = null,
          chatInput = null,
          modelSelector = null,
          messages = [],
          availableModels = [],
          selectedModel = null,
          sessionId = null,
          isChatOpen = false,
          initialized = false;
          
      // Приватный метод для создания кнопки чата
      this.createChatButton = function() {
        if (chatButton) return chatButton;
        
        chatButton = $('<button>')
          .addClass('chat-button')
          .text('💬')
          .attr('title', self.i18n('userLang').chatButton)
          .css({
            'position': 'fixed',
            'bottom': '20px',
            'right': '20px',
            'width': '50px',
            'height': '50px',
            'border-radius': '50%',
            'background-color': '#4285f4',
            'color': 'white',
            'font-size': '24px',
            'border': 'none',
            'cursor': 'pointer',
            'box-shadow': '0 2px 10px rgba(0, 0, 0, 0.2)',
            'z-index': '9999'
          })
          .on('click', function() {
            self.toggleChat();
          });
          
        return chatButton;
      };
      
      // Метод для загрузки или создания идентификатора сессии
      this.initSessionId = function() {
        // Пытаемся загрузить sessionId из localStorage
        var savedSessionId = localStorage.getItem('amocrm_chat_session_id');
        
        if (savedSessionId) {
          console.log('Загружен существующий идентификатор сессии');
          sessionId = savedSessionId;
        } else {
          // Генерируем новый случайный идентификатор
          sessionId = 'session_' + Math.random().toString(36).substr(2, 9);
          localStorage.setItem('amocrm_chat_session_id', sessionId);
          console.log('Создан новый идентификатор сессии');
        }
        
        return sessionId;
      };
      
      // Метод для обновления идентификатора сессии
      this.updateSessionId = function(newSessionId) {
        if (newSessionId && newSessionId !== sessionId) {
          sessionId = newSessionId;
          localStorage.setItem('amocrm_chat_session_id', sessionId);
          console.log('Обновлен идентификатор сессии:', sessionId);
        }
      };
      
      // Метод для очистки истории чата и сессии
      this.clearChatHistory = function() {
        // Очищаем сообщения
        messages = [];
        
        // Очищаем контейнер сообщений
        if (chatMessages) {
          chatMessages.empty();
        }
        
        // Создаем новую сессию
        sessionId = 'session_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('amocrm_chat_session_id', sessionId);
        
        console.log('История чата очищена, создана новая сессия:', sessionId);
        
        // Добавляем сообщение об очистке истории
        self.addMessage('История диалога очищена.', 'system');
      };
      
      // Приватный метод для создания окна чата
      this.createChatWindow = function() {
        if (chatWindow) return chatWindow;
        
        var userLang = self.i18n('userLang');
        
        chatWindow = $('<div>')
          .addClass('chat-window')
          .css({
            'position': 'fixed',
            'bottom': '20px',
            'right': '20px',
            'width': '300px',
            'height': '400px',
            'border-radius': '10px',
            'background-color': 'white',
            'box-shadow': '0 2px 10px rgba(0, 0, 0, 0.2)',
            'display': 'flex',
            'flex-direction': 'column',
            'overflow': 'hidden',
            'z-index': '10000'
          })
          .hide();
        
        // Создаем заголовок чата
        var header = $('<div>')
          .addClass('chat-header')
          .css({
            'background-color': '#4285f4',
            'color': 'white',
            'padding': '10px',
            'display': 'flex',
            'justify-content': 'space-between'
          });
          
        $('<span>').text(userLang.chatButton).appendTo(header);
        
        var headerButtons = $('<div>')
          .css({
            'display': 'flex',
            'gap': '5px'
          });
        
        // Добавляем кнопку очистки истории
        $('<button>')
          .text('🗑️')
          .attr('title', userLang.clearHistory || 'Очистить историю')
          .css({
            'background': 'none',
            'border': 'none',
            'color': 'white',
            'cursor': 'pointer',
            'font-size': '14px'
          })
          .on('click', function(e) {
            e.stopPropagation(); // Предотвращаем закрытие чата
            self.clearChatHistory();
          })
          .appendTo(headerButtons);
        
        // Добавляем кнопку закрытия
        $('<button>')
          .text('✖')
          .attr('title', userLang.close)
          .css({
            'background': 'none',
            'border': 'none',
            'color': 'white',
            'cursor': 'pointer'
          })
          .on('click', function() {
            self.toggleChat();
          })
          .appendTo(headerButtons);
        
        header.append(headerButtons);
        
        // Создаем контейнер для сообщений
        chatMessages = $('<div>')
          .addClass('chat-messages')
          .css({
            'flex': '1',
            'padding': '10px',
            'overflow-y': 'auto'
          });
        
        // Создаем форму ввода
        var inputContainer = $('<div>')
          .addClass('chat-input')
          .css({
            'display': 'flex',
            'flex-direction': 'column',
            'padding': '10px',
            'border-top': '1px solid #eee'
          });
          
        var messageInputRow = $('<div>')
          .css({
            'display': 'flex',
            'margin-bottom': '8px'
          });
          
        chatInput = $('<input>')
          .attr('type', 'text')
          .attr('placeholder', userLang.placeholder)
          .css({
            'flex': '1',
            'padding': '8px',
            'border': '1px solid #ddd',
            'border-radius': '18px',
            'margin-right': '8px'
          })
          .on('keydown', function(e) {
            if (e.key === 'Enter') {
              self.sendMessage();
            }
          })
          .appendTo(messageInputRow);
        
        $('<button>')
          .text('➤')
          .attr('title', userLang.send)
          .css({
            'background-color': '#4285f4',
            'color': 'white',
            'border': 'none',
            'border-radius': '50%',
            'width': '32px',
            'height': '32px',
            'cursor': 'pointer'
          })
          .on('click', function() {
            self.sendMessage();
          })
          .appendTo(messageInputRow);
        
        // Создаем селектор модели
        var modelSelectRow = $('<div>')
          .css({
            'display': 'flex',
            'align-items': 'center',
            'font-size': '12px'
          });
          
        $('<span>')
          .text(userLang.modelLabel || 'Модель:')
          .css({
            'margin-right': '8px',
            'color': '#777'
          })
          .appendTo(modelSelectRow);
          
        modelSelector = $('<select>')
          .addClass('model-selector')
          .css({
            'flex': '1',
            'padding': '4px',
            'border': '1px solid #ddd',
            'border-radius': '4px',
            'background-color': '#f9f9f9',
            'font-size': '12px'
          })
          .on('change', function() {
            // Сохраняем выбранную модель
            selectedModel = $(this).val();
          })
          .appendTo(modelSelectRow);
        
        // Добавляем строки в контейнер ввода
        inputContainer.append(messageInputRow, modelSelectRow);
        
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
      
      // Метод для добавления чата на текущую страницу
      this.mountChatToPage = function() {
        console.log('Mounting chat to current page');
        
        // Сначала удаляем элементы из их текущего местоположения
        chatButton.detach();
        chatWindow.detach();
        
        // Затем добавляем их снова к body
        $('body').append(chatButton);
        $('body').append(chatWindow);
        
        // Убедимся, что кнопка видна (если чат не открыт)
        if (!isChatOpen) {
          chatButton.show();
        } else {
          chatWindow.show();
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
          .css({
            'margin-bottom': '10px',
            'padding': '8px 12px',
            'border-radius': '18px',
            'max-width': '70%',
            'word-wrap': 'break-word',
            'background-color': sender === 'user' ? '#e3f2fd' : (sender === 'system' ? '#f1f1f1' : '#f5f5f5'),
            'margin-left': sender === 'user' ? 'auto' : '0',
            'font-style': sender === 'system' ? 'italic' : 'normal',
            'color': sender === 'system' ? '#666' : 'inherit'
          })
          .text(message.text);
        
        chatMessages.append(messageEl);
        chatMessages.scrollTop(chatMessages[0].scrollHeight);
      };
      
      // Метод для обработки ошибок
      this.handleError = function(error) {
        console.error('Widget error:', error);
        var errorMessage = 'Произошла ошибка при отправке сообщения';
        if (error && typeof error === 'string') {
          errorMessage = error;
        }
        self.addMessage(errorMessage, 'bot');
      };

      // Метод для загрузки доступных моделей
      this.loadAvailableModels = function() {
        $.ajax({
          url: 'https://aiamocrm-production.up.railway.app/api/widget/models',
          type: 'GET',
          dataType: 'json',
          success: function(response) {
            if (response && response.status === "success" && response.models) {
              availableModels = response.models;
              self.updateModelSelector();
            } else {
              console.error('Ошибка при получении списка моделей:', response);
            }
          },
          error: function(xhr, status, error) {
            console.error('Ошибка при загрузке моделей:', error);
          }
        });
      };
      
      // Метод для обновления селектора моделей
      this.updateModelSelector = function() {
        if (!modelSelector) return;
        
        // Очищаем текущие опции
        modelSelector.empty();
        
        // Если есть доступные модели
        if (availableModels && availableModels.length > 0) {
          // Добавляем каждую модель как option
          $.each(availableModels, function(index, model) {
            $('<option>')
              .val(model.id)
              .text(model.name)
              .attr('title', model.description)
              .appendTo(modelSelector);
          });
          
          // Устанавливаем первую модель как выбранную, если ничего не выбрано
          if (!selectedModel && availableModels.length > 0) {
            selectedModel = availableModels[0].id;
            modelSelector.val(selectedModel);
          }
        } else {
          // Если моделей нет, добавляем заглушку
          $('<option>')
            .val('')
            .text(self.i18n('userLang').modelNotAvailable || 'Модели недоступны')
            .appendTo(modelSelector);
        }
      };

      // Метод для отправки сообщения на сервер
      this.sendMessage = function() {
        // Получаем текст сообщения и очищаем от лишних пробелов
        var text = chatInput.val().trim();
        
        // Проверяем, что сообщение не пустое
        if (!text) return;
        
        // Добавляем сообщение пользователя в чат
        self.addMessage(text, 'user');
        
        // Очищаем поле ввода
        chatInput.val('');
        
        // Создаем объект для отправки на сервер
        var requestData = {
          text: text,
          target: 'widget'
        };
        
        // Добавляем модель, если она выбрана
        if (selectedModel) {
          requestData.model_name = selectedModel;
        }
        
        // Добавляем идентификатор сессии, если он существует
        if (sessionId) {
          requestData.session_id = sessionId;
        }
        
        // Отправляем сообщение на сервер
        self.crm_post(
          'https://aiamocrm-production.up.railway.app/api/widget/message',
          requestData,
          function(response) {
            try {
              if (response && response.status === "success") {
                // Добавляем ответ в чат
                self.addMessage(response.message || 'Сообщение отправлено', 'bot');
                
                // Обновляем идентификатор сессии, если он вернулся с сервера
                if (response.session_id) {
                  self.updateSessionId(response.session_id);
                }
              } else {
                self.handleError(response ? response.message : 'Неизвестная ошибка');
              }
            } catch (e) {
              self.handleError('Ошибка при обработке ответа сервера');
              console.error('Error details:', e);
            }
          },
          'json'
        );
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
          
          if (!initialized) {
            // Загружаем стили
            self.loadStyles();
            
            // Инициализируем идентификатор сессии
            self.initSessionId();
            
            // Создаем элементы чата
            var button = self.createChatButton();
            var window = self.createChatWindow();
            
            // Загружаем доступные модели
            self.loadAvailableModels();
            
            // Добавляем элементы на страницу
            $('body').append(button);
            $('body').append(window);
            
            // Регистрируем обработчик события смены страницы
            $(document).off('page:changed').on('page:changed', function() {
              console.log('Page changed event detected');
              setTimeout(function() {
                self.mountChatToPage();
              }, 100); // Небольшая задержка для уверенности, что DOM новой страницы загружен
            });
            
            // Установка флага инициализации
            initialized = true;
            
            console.log('Chat widget initialized successfully');
          }
          
          return true;
        },
        
        // Функция render вызывается каждый раз при отрисовке виджета
        render: function() {
          console.log('Render of chat widget');
          
          // При рендере убедимся, что чат прикреплен к текущей странице
          if (initialized) {
            setTimeout(function() {
              self.mountChatToPage();
            }, 100);
          }
          
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
          
          // Снимаем обработчик события смены страницы
          $(document).off('page:changed');
          
          // Очищаем переменные
          chatButton = null;
          chatWindow = null;
          chatMessages = null;
          chatInput = null;
          modelSelector = null;
          messages = [];
          availableModels = [];
          selectedModel = null;
          sessionId = null;
          isChatOpen = false;
          initialized = false;
        }
      };
      
      return this;
    };
    
    return CustomWidget;
  })