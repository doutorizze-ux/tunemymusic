@echo off
echo ========================================
echo   Iniciando Frontend - TuneMyMusic
echo ========================================
echo.

cd frontend

echo [1/2] Verificando dependencias...
call npm install

echo.
echo [2/2] Iniciando servidor de desenvolvimento...
echo Frontend rodando em: http://localhost:5173
echo.

call npm run dev
