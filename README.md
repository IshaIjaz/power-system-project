# ⚡ Live Power System Line Loss Monitor



## 📋 Project Overview

A real-time monitoring system for electrical transmission line losses in a 5-line power system.



## 🏗️ System Architecture

Power House (410V)

↓

Step-up Transformer (410V → 11kV)

↓

5 Outgoing Lines (11kV)

↓

5 Individual Transformers → 5 Distribution Areas



text



## 📁 Project Structure

power-system-project/

├── data/ # Data files

├── scripts/ # Calculation scripts

├── dashboard/ # Web dashboard

└── README.md # This file



text



## 🚀 Quick Start



### 1. Setup

```bash

# Clone and navigate

cd power-system-project



# Create virtual environment

python -m venv venv



# Activate (Windows)

venv\\Scripts\\activate



# Install dependencies

pip install pandas streamlit plotly

2\. Run Calculations

bash

python scripts\\calculate\_losses.py

3\. Run Dashboard

bash

streamlit run dashboard\\power\_dashboard.py

4\. For Live Simulation

bash

# In separate terminal

python scripts\\live\_simulator.py

🎯 Features

Real-time loss calculations for 5 transmission lines



Live data simulation with auto-refresh



Interactive dashboard with charts



Line performance ranking



Cost analysis and recommendations



Export functionality



📊 Dashboard Features

System Overview: Total load, losses, efficiency



Live/Static Toggle: Switch between simulated and static data



Auto-refresh: Configurable update interval



Line Details: Individual line parameters and losses



Charts: Visual representation of losses



Export: Download data as CSV



🔧 Technical Details

Voltage Levels: 410V → 11kV → Distribution



Lines: 5 independent transmission lines



Calculations: I²R losses, transformer losses, voltage drop



Framework: Streamlit for web interface



Data: Pandas for processing, Plotly for visualization



📈 Sample Output

Total System Load: 5,150 kW



Total Losses: ~160 kW



Overall Efficiency: ~97%



Line Efficiency Range: 95-98%



👥 Team



Ali Akram - Electrical Engineer

Aleeba Boota - IT Support

Isha Ijaz - IT Support

Maham Habib - IT Support







Software Developer: Implementation and dashboard

