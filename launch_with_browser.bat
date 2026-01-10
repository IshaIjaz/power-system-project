@echo off
title ⚡ Power System Project - Auto Browser
color 0A

echo.
echo ========================================
echo    POWER SYSTEM PROJECT - ONE CLICK    
echo ========================================
echo.

echo 📊 Starting Dashboard...
start "Dashboard" cmd /k "cd /d "D:\power-system-project" && streamlit run dashboard\power_dashboard.py"

echo ⏳ Waiting 3 seconds for dashboard to start...
timeout /t 3 /nobreak > nul

echo 🌐 Opening browser...
start "" "http://localhost:8501"

echo.
echo 🔄 Starting Live Simulator...
start "Simulator" cmd /k "cd /d "D:\power-system-project" && python scripts\live_simulator.py"

echo.
echo 🧮 Running Calculations...
start "Calculations" cmd /k "cd /d "D:\power-system-project" && python scripts\calculate_losses.py"

echo.
echo ✅ ALL SYSTEMS STARTED!
echo.
echo 📊 Dashboard: http://localhost:8501
echo 🔄 Simulator: Running in background
echo 🧮 Calculations: Completed
echo.
echo Press any key to close this window (others will keep running)...
pause > nul