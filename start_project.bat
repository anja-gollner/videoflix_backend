@echo off
:: 1. Starte Redis im Hintergrund
start "" "C:\Program Files\Redis\redis-server.exe"

:: 2. Warte 10 Sekunden, damit Redis genügend Zeit hat, zu starten
timeout /t 10 /nobreak >nul

:: 3. Starte redis-cli und führe AUTH aus
start "" cmd /k "C:\Program Files\Redis\redis-cli.exe" auth foobared

:: 4. Warte 5 Sekunden, um sicherzustellen, dass redis-cli erfolgreich verbunden ist
timeout /t 5 /nobreak >nul

:: 5. Starte den RQ Worker in PowerShell (VS Code)
start "" powershell -NoExit -Command "cd 'C:\2_dev\1_DeveloperAkademie\2 Projekte Backend\10_videoflix_backend'; python manage.py rqworker --worker-class patch_rq_worker.PatchedWindowsWorker default"

:: 6. Starte den Django-Server in PowerShell (VS Code)
start "" powershell -NoExit -Command "cd 'C:\2_dev\1_DeveloperAkademie\2 Projekte Backend\10_videoflix_backend'; python manage.py runserver"
