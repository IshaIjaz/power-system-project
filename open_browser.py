"""
Simple browser launcher - Opens dashboard in browser
"""
import webbrowser
import time

print("🌐 Opening Power System Dashboard...")
time.sleep(2)  # Wait 2 seconds for Streamlit to start
webbrowser.open("http://localhost:8501")
print("✅ Browser opened! If not, manually go to: http://localhost:8501")
input("Press Enter to close...")