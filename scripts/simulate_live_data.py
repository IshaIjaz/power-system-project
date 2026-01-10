import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

print("🔄 Starting Live Data Simulator...")
print("This will update data files every 10 seconds")
print("Press Ctrl+C to stop\n")

# Load original data
df = pd.read_csv('data/power_system.csv')

try:
    counter = 0
    while True:
        # Create timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Simulate load variations (±10%)
        df['load_kw'] = df['load_kw'] * (1 + np.random.uniform(-0.1, 0.1, len(df)))
        
        # Simulate power factor variations
        df['power_factor'] = df['power_factor'] + np.random.uniform(-0.02, 0.02, len(df))
        df['power_factor'] = df['power_factor'].clip(0.75, 0.95)
        
        # Save updated data
        df.to_csv('data/power_system_live.csv', index=False)
        
        # Update calculations
        import sys
        sys.path.append('.')
        from scripts.calculate_losses import calculate_losses
        
        print(f"[{timestamp}] Updated live data - Iteration {counter}")
        counter += 1
        
        # Wait 10 seconds
        time.sleep(10)
        
except KeyboardInterrupt:
    print("\n\n⏹️ Live simulation stopped")