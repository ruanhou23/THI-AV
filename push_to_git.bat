@echo off
title Push TOEIC Master to GitHub
cd /d "%~dp0"

echo ========================================================
echo    DANG DONG BO VA DAY CODE LEN GITHUB: ruanhou23/THI-AV
echo ========================================================
echo.
echo Neu trinh duyet bat len cua so dang nhap GitHub, vui long nhan "Sign in with your browser" (hoac nhap Personal Access Token).
echo.

git branch -M main
git push -u origin main

echo.
if %ERRORLEVEL% equ 0 (
    echo ========================================================
    echo   [THANH CONG] Da day toan bo code len GitHub!
    echo   Trang web se tu dong chay tai:
    echo   https://ruanhou23.github.io/THI-AV/
    echo ========================================================
) else (
    echo ========================================================
    echo   [LUU Y] Neu gap loi Authentication failed:
    echo   1. Hay vao https://github.com/settings/tokens tao 1 Token (tich chon 'repo').
    echo   2. Chay lenh:
    echo      git remote set-url origin https://<TOKEN>@github.com/ruanhou23/THI-AV.git
    echo      git push -u origin main
    echo ========================================================
)

echo.
pause
