@echo off
echo ========================================
echo   Iniciando Celery Worker
echo ========================================
echo.

cd backend

echo Iniciando Celery worker...
echo.

celery -A tasks worker --loglevel=info --pool=solo
