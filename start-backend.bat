@echo off
echo ========================================
echo   Iniciando Backend - TuneMyMusic
echo ========================================
echo.

cd backend

echo [1/2] Verificando dependencias...
pip install -r requirements.txt

echo.
echo [2/2] Iniciando servidor Flask...
echo Backend rodando em: http://localhost:8889
echo.

python app.py
