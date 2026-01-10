@echo off
echo ⚡ POWER SYSTEM PROJECT - ONE CLICK LAUNCH
echo ==========================================
echo.

echo 📊 Starting Dashboard...
start "Dashboard" cmd /k "cd /d "D:\power-system-project" && streamlit run dashboard/power_dashboard.py"

timeout /t 2 /nobreak > nul

echo 🔄 Starting Live Simulator...
start "Simulator" cmd /k "cd /d "D:\power-system-project" && python scripts/live_simulator.py"

timeout /t 2 /nobreak > nul

echo 🧮 Running Calculations...
start "Calculations" cmd /k "cd /d "D:\power-system-project" && python scripts/calculate_losses.py && pause"

echo.
echo ✅ ALL SYSTEMS STARTED!
echo.
echo 📊 Dashboard: http://localhost:8501
echo 🔄 Simulator: Running in background
echo 🧮 Calculations: Completed
echo.
echo Press any key to close this window (others will keep running)...
pause > nul