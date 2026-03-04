@echo off
chcp 65001 >nul 2>&1
setlocal
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"

echo ============================================
echo  Sistema de Informes Delictuales
echo  Policia de Tucuman
echo ============================================
echo.
echo [INFO] Directorio: %ROOT%
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
timeout /t 2 /nobreak >nul 2>&1
echo [OK] Puertos liberados.
echo.

:: -------------------------------------------
:: 2. Verificar Docker CLI
:: -------------------------------------------
where docker >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker no esta instalado.
    echo Descargue Docker Desktop desde https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo [OK] Docker encontrado.

:: -------------------------------------------
:: 3. Verificar que el daemon Docker este corriendo
:: -------------------------------------------
docker info >nul 2>&1
if errorlevel 1 (
    echo [INFO] Docker Desktop no esta corriendo. Iniciando...
    if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
        start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    ) else (
        echo [ERROR] No se encontro Docker Desktop. Inicielo manualmente.
        pause
        exit /b 1
    )
    echo [INFO] Esperando que Docker Desktop arranque...
    set DOCKER_TRIES=0
    call :WAIT_DOCKER
    echo [OK] Docker Desktop listo.
    echo.
) else (
    echo [OK] Docker Desktop activo.
)

:: -------------------------------------------
:: 4. Iniciar contenedor PostgreSQL+PostGIS
:: -------------------------------------------
docker ps --filter "name=delitos_db" --format "{{.Names}}" 2>nul | findstr "delitos_db" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Iniciando base de datos PostgreSQL + PostGIS...
    call :START_DB
    echo [INFO] Esperando que la base de datos este lista...
    set DB_TRIES=0
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
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    pause
    exit /b 1
)
echo [OK] Python encontrado.
where node >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js no esta instalado o no esta en el PATH.
    pause
    exit /b 1
)
echo [OK] Node.js encontrado.
echo.

:: -------------------------------------------
:: 6. Instalar dependencias del backend (solo si faltan)
:: -------------------------------------------
echo [INFO] Verificando dependencias del backend...
if not exist "%ROOT%\backend\.venv\Scripts\uvicorn.exe" (
    echo [INFO] Creando entorno virtual e instalando dependencias...
    cd /d "%ROOT%\backend"
    python -m venv .venv
    call ".venv\Scripts\activate.bat"
    pip install -r requirements.txt --quiet
    call deactivate
    cd /d "%ROOT%"
)
if not exist "%ROOT%\backend\.venv\Scripts\uvicorn.exe" (
    echo [ERROR] uvicorn no se instalo correctamente.
    echo Ejecute manualmente:
    echo   cd "%ROOT%\backend"
    echo   python -m venv .venv
    echo   .venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)
echo [OK] Backend dependencias listas.

:: -------------------------------------------
:: 7. Instalar dependencias del frontend (solo si faltan)
:: -------------------------------------------
echo [INFO] Verificando dependencias del frontend...
if not exist "%ROOT%\frontend\node_modules\.package-lock.json" (
    echo [INFO] Instalando dependencias npm...
    cd /d "%ROOT%\frontend"
    call npm install
    cd /d "%ROOT%"
)
echo [OK] Frontend dependencias listas.
echo.

:: -------------------------------------------
:: 8. Arrancar backend
:: -------------------------------------------
echo [INFO] Iniciando servidor backend en http://localhost:8000 ...
start "Backend - FastAPI" /D "%ROOT%\backend" cmd /k ".venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000 --reload"

echo [INFO] Esperando que el backend responda (max 60s)...
set BACKEND_TRIES=0
call :WAIT_BACKEND
echo [OK] Backend respondiendo correctamente.
echo.

:: -------------------------------------------
:: 9. Arrancar frontend
:: -------------------------------------------
echo [INFO] Iniciando servidor frontend en http://localhost:3000 ...
start "Frontend - Next.js" /D "%ROOT%\frontend" cmd /k "npm run dev"

echo [INFO] Esperando que el frontend compile (max 45s)...
set FRONT_TRIES=0
call :WAIT_FRONTEND
echo [OK] Frontend listo.
echo.

:: Abrir navegador
start "" "http://localhost:3000"

echo ============================================
echo  TODO LISTO - Servidores activos:
echo   - Frontend: http://localhost:3000
echo   - Backend:  http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo ============================================
echo.
echo Presione cualquier tecla para DETENER todo.
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

:: ===========================================================
:: SUBRUTINAS
:: ===========================================================

:START_DB
docker compose -f "%ROOT%\docker-compose.yml" up -d >nul 2>&1
if not errorlevel 1 goto :eof
docker-compose -f "%ROOT%\docker-compose.yml" up -d >nul 2>&1
if not errorlevel 1 goto :eof
echo [ERROR] No se pudo iniciar la base de datos.
pause
exit /b 1

:WAIT_DOCKER
timeout /t 5 /nobreak >nul 2>&1
docker info >nul 2>&1
if not errorlevel 1 goto :eof
set /a DOCKER_TRIES+=1
if %DOCKER_TRIES% geq 24 (
    echo [ERROR] Docker no arranco despues de 2 minutos.
    pause
    exit /b 1
)
goto :WAIT_DOCKER

:WAIT_DB
timeout /t 3 /nobreak >nul 2>&1
docker exec delitos_db pg_isready -U delitos_user -d delitos_tucuman >nul 2>&1
if not errorlevel 1 goto :eof
set /a DB_TRIES+=1
if %DB_TRIES% geq 20 (
    echo [ERROR] Base de datos no arranco.
    pause
    exit /b 1
)
goto :WAIT_DB

:WAIT_BACKEND
timeout /t 3 /nobreak >nul 2>&1
curl.exe -s --max-time 2 http://127.0.0.1:8000/ >nul 2>&1
if not errorlevel 1 goto :eof
set /a BACKEND_TRIES+=1
echo        intento %BACKEND_TRIES% de 20...
if %BACKEND_TRIES% geq 20 (
    echo [ERROR] Backend no respondio. Revise la ventana "Backend - FastAPI".
    pause
    exit /b 1
)
goto :WAIT_BACKEND

:WAIT_FRONTEND
timeout /t 3 /nobreak >nul 2>&1
curl.exe -s --max-time 2 http://127.0.0.1:3000/ >nul 2>&1
if not errorlevel 1 goto :eof
set /a FRONT_TRIES+=1
echo        intento %FRONT_TRIES% de 15...
if %FRONT_TRIES% geq 15 (
    echo [WARN] Frontend tardo mas de lo esperado. Abriendo navegador igualmente.
    goto :eof
)
goto :WAIT_FRONTEND
