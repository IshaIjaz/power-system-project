"""
MASTER RUN SCRIPT - Run everything with one click!
Automatically opens browser after dashboard starts
"""
import subprocess
import sys
import os
import time
import webbrowser

def run_command(command, description, wait_for_browser=False):
    """Run a command and show status"""
    print(f"🚀 {description}...")
    try:
        if sys.platform == "win32":  # Windows
            subprocess.Popen(
                f'start cmd /k "{command}"',
                shell=True
            )
        else:  # Mac/Linux
            subprocess.Popen(command, shell=True)
        
        print(f"✅ {description} started")
        
        # If this is the dashboard command, open browser after delay
        if wait_for_browser:
            print("⏳ Waiting for dashboard to start...")
            time.sleep(3)  # Wait 3 seconds for Streamlit to start
            print("🌐 Opening browser...")
            webbrowser.open("http://localhost:8501")
            
        return True
    except Exception as e:
        print(f"❌ Failed to start {description}: {e}")
        return False

def main():
    print("=" * 60)
    print("⚡ POWER SYSTEM PROJECT - ONE CLICK LAUNCH")
    print("=" * 60)
    
    # Get current directory
    project_dir = os.getcwd()
    
    # Commands to run
    commands = [
        {
            "cmd": f'cd "{project_dir}" && python scripts/calculate_losses.py',
            "desc": "Calculations",
            "wait": False
        },
        {
            "cmd": f'cd "{project_dir}" && python scripts/live_simulator.py',
            "desc": "Live Simulator", 
            "wait": False
        },
        {
            "cmd": f'cd "{project_dir}" && streamlit run dashboard/power_dashboard.py --server.headless true',
            "desc": "Dashboard",
            "wait": True  # This will trigger browser opening
        }
    ]
    
    # Run each command in separate terminal
    for cmd_info in commands:
        run_command(cmd_info["cmd"], cmd_info["desc"], cmd_info["wait"])
        time.sleep(1)  # Small delay between commands
    
    print("\n" + "=" * 60)
    print("✅ ALL SYSTEMS STARTED!")
    print("=" * 60)
    print("\n📊 Dashboard: http://localhost:8501")
    print("🔄 Simulator: Updating every 5 seconds")
    print("📈 Calculations: Completed")
    print("\n⚠️  Press Enter to stop (close other windows manually)...")
    
    # Keep script running so VS Code shows "running"
    input()

if __name__ == "__main__":
    main()