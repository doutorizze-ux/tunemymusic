@echo off
echo ========================================
echo   Enviando código para o GitHub
echo ========================================
echo.
echo IMPORTANTE: Substitua a URL abaixo pela URL do seu repositório!
echo.
set /p REPO_URL="Cole a URL do seu repositório GitHub aqui: "

git remote add origin %REPO_URL%
git branch -M main
git push -u origin main

echo.
echo ========================================
echo   Código enviado com sucesso!
echo ========================================
pause
