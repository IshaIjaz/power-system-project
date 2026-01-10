"""
LIVE DATA SIMULATOR
Simulates real-time changes in power system
"""
import pandas as pd
import numpy as np
import time
from datetime import datetime

print("=" * 60)
print("🔄 LIVE DATA SIMULATOR FOR POWER SYSTEM")
print("=" * 60)

def simulate_live_data():
    # Load original data
    df = pd.read_csv('data/power_system.csv')
    
    print("Original data loaded:")
    print(df[['line_id', 'area_name', 'load_kw', 'power_factor']])
    print()
    
    # Create variations
    variation_count = 0
    
    try:
        while True:
            # Get current time
            current_time = datetime.now().strftime("%H:%M:%S")
            
            # Create small random variations (±5%)
            load_variation = 1 + np.random.uniform(-0.05, 0.05, len(df))
            pf_variation = np.random.uniform(-0.02, 0.02, len(df))
            
            # Apply variations
            df['load_kw'] = df['load_kw'] * load_variation
            df['power_factor'] = df['power_factor'] + pf_variation
            
            # Keep power factor between 0.75 and 0.95
            df['power_factor'] = df['power_factor'].clip(0.75, 0.95)
            
            # Round values for readability
            df['load_kw'] = df['load_kw'].round(1)
            df['power_factor'] = df['power_factor'].round(3)
            
            # Save to new file
            df.to_csv('data/power_system_live.csv', index=False)
            
            # Run calculations
            import sys
            import os
            sys.path.append('.')
            
            # Import and run calculation function
            from scripts.calculate_losses import calculate_and_save
            
            # Call calculation (we'll modify calculate_losses.py)
            calculate_and_save('data/power_system_live.csv', 'data/loss_calculations_live.csv')
            
            print(f"[{current_time}] Variation {variation_count+1}:")
            print(f"   Line 1 Load: {df.iloc[0]['load_kw']:.1f} kW (was 850 kW)")
            print(f"   Line 1 PF: {df.iloc[0]['power_factor']:.3f} (was 0.850)")
            print()
            
            variation_count += 1
            time.sleep(5)  # Update every 5 seconds
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Simulation stopped by user")
        print(f"Total variations simulated: {variation_count}")
        return df

if __name__ == "__main__":
    print("Starting simulation... Press Ctrl+C to stop")
    print()
    final_data = simulate_live_data()
    
    print("\n" + "=" * 60)
    print("📊 FINAL SIMULATED DATA:")
    print("=" * 60)
    print(final_data[['line_id', 'area_name', 'load_kw', 'power_factor']])