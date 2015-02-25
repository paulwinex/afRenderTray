Simple PyQt tray icon to cycle restart afRender.exe and hide afRender console to tray.

INSTALL
Windows only!

1. Copy afRenderTray.cmd and afRenderTray.pyw to CGRU root folder
2. Put afRenderTray.cmd to windows startup folder

RUS
Скрипт сделан для случаев когда рендерноды часто перезагружаются. По умолчанию при невозможности подключения к серверу afRender просто закрывается. 
Данный скрипт будет повторять попытки каждые 20 секунд пока не подключится. Даже если выключить рендер командой с сервера.
