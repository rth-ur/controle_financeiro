@echo off
setlocal
cd /d "%~dp0"
if exist "%ProgramFiles%\nodejs\node.exe" set "PATH=%ProgramFiles%\nodejs;%PATH%"
if not exist ".venv\Scripts\python.exe" (
  echo Ambiente .venv nao encontrado. Consulte APRESENTACAO.md.
  exit /b 1
)
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js nao encontrado. Reabra o VS Code apos instalar o Node.js.
  exit /b 1
)
echo === FinTrack: demonstracao dos testes ===
".venv\Scripts\python.exe" --version
node --version
echo.
".venv\Scripts\python.exe" -m pytest -v --color=yes %*
if errorlevel 1 exit /b 1
echo.
echo === Testes JavaScript existentes: API simulada ===
node tests/api.tests.js
if errorlevel 1 exit /b 1
echo.
echo Demonstracao concluida: todas as suites passaram.
exit /b 0
