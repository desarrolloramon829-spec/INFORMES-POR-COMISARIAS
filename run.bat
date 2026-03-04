@echo off
echo ============================================
echo  Sistema de Informes Delictuales
echo  Policia de Tucuman
echo ============================================
echo.

:: -------------------------------------------
:: 1. Verificar que Docker CLI este instalado
:: -------------------------------------------
where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker no esta instalado.
    echo Descargue Docker Desktop desde https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

:: -------------------------------------------
:: 2. Verificar que el daemon Docker este corriendo
:: -------------------------------------------
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [INFO] Docker Desktop no esta corriendo. Iniciando...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo Esperando que Docker Desktop arranque (puede tardar 30-60 segundos)...
    call :WAIT_DOCKER
    echo [OK] Docker Desktop listo.
    echo.
)

:: -------------------------------------------
:: 3. Iniciar contenedor PostgreSQL+PostGIS
:: -------------------------------------------
docker ps --filter "name=delitos_db" --format "{{.Names}}" 2>nul | findstr "delitos_db" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [INFO] Iniciando base de datos PostgreSQL + PostGIS...
    docker-compose up -d
    echo Esperando que la base de datos este lista...
    call :WAIT_DB
    echo [OK] Base de datos lista.
) else (
    echo [OK] Base de datos ya esta activa.
)

:: Check Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python no esta instalado.
    pause
    exit /b 1
)

:: Check Node.js
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js no esta instalado.
    pause
    exit /b 1
)

:: Install backend dependencies
echo.
echo [INFO] Instalando dependencias del backend...
cd backend
if not exist ".venv" (
    python -m venv .venv
)
call .venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
echo [OK] Backend listo.

:: Start backend in background
echo [INFO] Iniciando servidor backend en puerto 8000...
start "Backend - FastAPI" cmd /c "cd /d %~dp0backend && .venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

cd ..

:: Install frontend dependencies
echo.
echo [INFO] Instalando dependencias del frontend...
cd frontend
if not exist "node_modules" (
    call npm install
)
echo [OK] Frontend listo.

:: Start frontend
echo [INFO] Iniciando servidor frontend en puerto 3000...
start "Frontend - Next.js" cmd /c "cd /d %~dp0frontend && npm run dev"

cd ..

echo.
echo ============================================
echo  Servidores iniciados:
echo   - Backend:  http://localhost:8000
echo   - Frontend: http://localhost:3000
echo   - API Docs: http://localhost:8000/docs
echo ============================================
echo.
echo Presione cualquier tecla para detener...
pause >nul

:: Cleanup
echo Deteniendo servidores...
taskkill /FI "WINDOWTITLE eq Backend - FastAPI" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Frontend - Next.js" /T /F >nul 2>&1
echo Listo.
exit /b 0

:: -------------------------------------------
:: Subrutina: esperar a que Docker daemon este listo
:: -------------------------------------------
:WAIT_DOCKER
timeout /t 5 /nobreak >nul
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 goto WAIT_DOCKER
exit /b 0

:: -------------------------------------------
:: Subrutina: esperar a que PostgreSQL acepte conexiones
:: -------------------------------------------
:WAIT_DB
timeout /t 3 /nobreak >nul
docker exec delitos_db pg_isready -U delitos_user -d delitos_tucuman >nul 2>&1
if %ERRORLEVEL% neq 0 goto WAIT_DB
exit /b 0
:: Cleanup
echo Deteniendo servidores...
taskkill /FI "WINDOWTITLE eq Backend - FastAPI" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Frontend - Next.js" /T /F >nul 2>&1
echo Listo.
