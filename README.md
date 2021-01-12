# SmartHome
Управление вашими устройствами с помощью телеграм бота и приложения

## Telegram Bot
Вам не нужно создавать или регистрировать нового бота. Он уже создан и запущен на сервере.  
[Начать беседу](https://t.me/tsmarthomebot)

## Возможности
На данный момент возможностей не так много, так как данный сервис ещё на стадии тестирования внутренних функций.

1) Удаленное включение устройств
2) Выключение и перезагрузка устройств с запущенным приложением
3) Запуск .exe приложений на устройствах с ОС Windows

## Поддерживаемые платформы для приложения:
На данный момент приложение доступно для:  
1. [Windows](https://github.com/zeinlol/SmartHome/raw/main/SmartHome.exe)
2. [Raspberry Pi](https://downgit.github.io/#/home?url=https://github.com/zeinlol/SmartHome/blob/main/smarthomehub.py)

## Инструкция  
### Windows  
1) Скачайте приложение по [ссылке](https://github.com/zeinlol/SmartHome/raw/main/SmartHome.exe)
2) Введите код, указаный в телеграм боте
3) По желанию в ручную добавьте в автозагрузку  
### Raspberry
1) Скачайте приложение по [ссылке](https://downgit.github.io/#/home?url=https://github.com/zeinlol/SmartHome/blob/main/smarthomehub.py)
2) Убедитесь, что у вас установлен Python 3.7 или выше
3) Введите комманды  
> pip install wakeonlan   
> pip install pysimplegui
4) Для запуска приложения распакуйте архив и введите в терминале команду: 
> python3 ПУТЬ_К_ФАЙЛУ/smarthomehub.py
5) По желанию в ручную добавьте файл в автозагрузку

В ближайшее время появится прошивка для arduino & ESP8266
