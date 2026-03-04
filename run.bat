@echo off
setlocal
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"

echo ============================================
echo  Sistema de Informes Delictuales
echo  Policia de Tucuman
echo ============================================
echo.

:: -------------------------------------------
:: 1. Liberar puertos 8000 y 3000 si ya estan ocupados
:: -------------------------------------------
echo [INFO] Liberando puertos anteriores...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":8000 " ^| findstr "LISTENING"') do (
    taskkill /PID %%a /F >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":3000 " ^| findstr "LISTENING"') do (
    taskkill /PID %%a /F >nul 2>&1
)
timeout /t 2 /nobreak >nul

:: -------------------------------------------
:: 2. Verificar Docker CLI
:: -------------------------------------------
where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker no esta instalado.
    echo Descargue Docker Desktop desde https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

:: -------------------------------------------
:: 3. Verificar que el daemon Docker este corriendo
:: -------------------------------------------
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [INFO] Docker Desktop no esta corriendo. Iniciando...
    if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
        start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    ) else (
        echo [ERROR] No se encontro Docker Desktop. Inicielo manualmente y vuelva a ejecutar.
        pause
        exit /b 1
    )
    echo Esperando que Docker Desktop arranque (puede tardar 60 segundos)...
    call :WAIT_DOCKER
    echo [OK] Docker Desktop listo.
    echo.
)

:: -------------------------------------------
:: 4. Iniciar contenedor PostgreSQL+PostGIS
:: -------------------------------------------
docker ps --filter "name=delitos_db" --format "{{.Names}}" 2>nul | findstr "delitos_db" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [INFO] Iniciando base de datos PostgreSQL + PostGIS...
    docker-compose -f "%ROOT%\docker-compose.yml" up -d
    echo Esperando que la base de datos este lista...
    call :WAIT_DB
    echo [OK] Base de datos lista.
) else (
    echo [OK] Base de datos ya esta activa.
)
echo.

:: -------------------------------------------
:: 5. Verificar Python y Node
:: -------------------------------------------
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    pause
    exit /b 1
)
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js no esta instalado o no esta en el PATH.
    pause
    exit /b 1
)

:: -------------------------------------------
:: 6. Instalar dependencias del backend (solo si faltan)
:: -------------------------------------------
echo [INFO] Verificando dependencias del backend...
if not exist "%ROOT%\backend\.venv\Scripts\uvicorn.exe" (
    echo [INFO] Creando entorno virtual e instalando dependencias...
    cd /d "%ROOT%\backend"
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt --quiet
    call deactivate
    cd /d "%ROOT%"
)
echo [OK] Backend listo.

:: -------------------------------------------
:: 7. Instalar dependencias del frontend (solo si faltan)
:: -------------------------------------------
echo [INFO] Verificando dependencias del frontend...
if not exist "%ROOT%\frontend\node_modules\next" (
    echo [INFO] Instalando dependencias npm...
    cd /d "%ROOT%\frontend"
    call npm install --silent
    cd /d "%ROOT%"
)
echo [OK] Frontend listo.
echo.

:: -------------------------------------------
:: 8. Arrancar backend
:: -------------------------------------------
echo [INFO] Iniciando servidor backend en http://localhost:8000 ...
start "Backend - FastAPI" cmd /k "cd /d %ROOT%\backend && .venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000 --reload"

echo [INFO] Esperando que el backend este listo...
call :WAIT_BACKEND
echo [OK] Backend respondiendo.
echo.

:: -------------------------------------------
:: 9. Arrancar frontend
:: -------------------------------------------
echo [INFO] Iniciando servidor frontend en http://localhost:3000 ...
start "Frontend - Next.js" cmd /k "cd /d %ROOT%\frontend && npm run dev"

echo [INFO] Esperando que el frontend compile (puede tardar ~15 segundos)...
timeout /t 12 /nobreak >nul
start "" "http://localhost:3000"

echo.
echo ============================================
echo  Servidores iniciados correctamente:
echo   - Frontend: http://localhost:3000
echo   - Backend:  http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo ============================================
echo.
echo Cierre esta ventana o presione cualquier tecla para DETENER todo.
pause >nul

:: -------------------------------------------
:: 10. Cleanup al salir
:: -------------------------------------------
echo.
echo [INFO] Deteniendo servidores...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":8000 " ^| findstr "LISTENING"') do (
    taskkill /PID %%a /F >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":3000 " ^| findstr "LISTENING"') do (
    taskkill /PID %%a /F >nul 2>&1
)
taskkill /FI "WINDOWTITLE eq Backend - FastAPI" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Frontend - Next.js" /T /F >nul 2>&1
echo [OK] Servidores detenidos.
endlocal
exit /b 0

:: -------------------------------------------
:: Subrutina: esperar a que Docker daemon este listo
:: -------------------------------------------
:WAIT_DOCKER
timeout /t 5 /nobreak >nul
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 goto :WAIT_DOCKER
exit /b 0

:: -------------------------------------------
:: Subrutina: esperar a que PostgreSQL acepte conexiones
:: -------------------------------------------
:WAIT_DB
timeout /t 3 /nobreak >nul
docker exec delitos_db pg_isready -U delitos_user -d delitos_tucuman >nul 2>&1
if %ERRORLEVEL% neq 0 goto :WAIT_DB
exit /b 0

:: -------------------------------------------
:: Subrutina: esperar a que el backend HTTP responda
:: -------------------------------------------
:WAIT_BACKEND
timeout /t 3 /nobreak >nul
curl -s --max-time 2 http://127.0.0.1:8000/ >nul 2>&1
if %ERRORLEVEL% neq 0 goto :WAIT_BACKEND
exit /b 0
