@echo off
setlocal
cd /d "%~dp0"
where docker >nul 2>nul
if errorlevel 1 (
  echo Docker nao encontrado. Instale e abra o Docker Desktop.
  exit /b 1
)
docker compose run --build --rm tests
exit /b %errorlevel%
