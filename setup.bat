@echo off
echo ============================================
echo  Setup Inicial - Sistema de Informes
echo ============================================
echo.

:: 1. PostgreSQL via Docker
echo [1/4] Iniciando PostgreSQL + PostGIS...

where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker no esta instalado. Descargue desde https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [INFO] Docker Desktop no esta corriendo. Iniciando...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo Esperando que Docker Desktop arranque (puede tardar hasta 60 segundos)...
    call :WAIT_DOCKER
    echo [OK] Docker Desktop listo.
)

docker-compose up -d
echo Esperando que la base de datos este lista...
call :WAIT_DB
echo [OK] Base de datos lista.

:: 2. Backend Python
echo [2/4] Configurando backend Python...
cd backend
if not exist ".venv" (
    python -m venv .venv
)
call .venv\Scripts\activate.bat
pip install -r requirements.txt
echo [OK] Backend configurado.
call deactivate
cd ..

:: 3. Frontend Node.js
echo [3/4] Configurando frontend Next.js...
cd frontend
call npm install
cd ..

:: 4. Create .env from example
echo [4/4] Configurando variables de entorno...
if not exist ".env" (
    copy .env.example .env
    echo [OK] Archivo .env creado. Edite si necesita cambiar la configuracion.
) else (
    echo [OK] Archivo .env ya existe.
)

echo.
echo ============================================
echo  Setup completado!
echo  Ejecute run.bat para iniciar el sistema.
echo ============================================
pause
exit /b 0

:WAIT_DOCKER
timeout /t 5 /nobreak >nul
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 goto WAIT_DOCKER
exit /b 0

:WAIT_DB
timeout /t 3 /nobreak >nul
docker exec delitos_db pg_isready -U delitos_user -d delitos_tucuman >nul 2>&1
if %ERRORLEVEL% neq 0 goto WAIT_DB
exit /b 0
