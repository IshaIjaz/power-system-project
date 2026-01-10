import pandas as pd
import math

def calculate_losses_for_line(line):
    """Calculate losses for a single transmission line"""
    SYSTEM_VOLTAGE = 11  # kV
    
    # 1. Calculate current (I = P / (√3 * V * pf))
    current_amps = (line['load_kw'] * 1000) / (math.sqrt(3) * SYSTEM_VOLTAGE * 1000 * line['power_factor'])
    
    # 2. Calculate line resistance
    total_resistance = line['resistance_ohm_km'] * line['line_length_km']
    
    # 3. Calculate I²R losses (3-phase)
    line_losses_kw = 3 * (current_amps ** 2) * total_resistance / 1000
    
    # 4. Calculate transformer losses
    transformer_losses_kw = line['load_kw'] * (1 - line['transformer_efficiency'])
    
    # 5. Total losses
    total_losses_kw = line_losses_kw + transformer_losses_kw
    
    # 6. Loss percentage
    loss_percentage = (total_losses_kw / line['load_kw']) * 100
    
    # 7. Voltage drop
    total_reactance = line['reactance_ohm_km'] * line['line_length_km']
    voltage_drop_v = current_amps * (total_resistance * line['power_factor'] + 
                                   total_reactance * math.sqrt(1 - line['power_factor']**2))
    
    return {
        'line_id': line['line_id'],
        'area_name': line['area_name'],
        'current_amps': round(current_amps, 2),
        'line_losses_kw': round(line_losses_kw, 2),
        'transformer_losses_kw': round(transformer_losses_kw, 2),
        'total_losses_kw': round(total_losses_kw, 2),
        'loss_percentage': round(loss_percentage, 2),
        'voltage_drop_v': round(voltage_drop_v, 2),
        'efficiency': round(100 - loss_percentage, 2)
    }

def calculate_and_save(input_file='data/power_system.csv', 
                      output_file='data/loss_calculations.csv'):
    """Calculate losses from input file and save to output file"""
    try:
        df = pd.read_csv(input_file)
        print(f"📖 Reading data from: {input_file}")
        print(f"   Found {len(df)} transmission lines")
        
        # Calculate for each line
        results = []
        for index, line in df.iterrows():
            result = calculate_losses_for_line(line)
            results.append(result)
        
        # Create results DataFrame
        results_df = pd.DataFrame(results)
        
        # Save to file
        results_df.to_csv(output_file, index=False)
        print(f"💾 Results saved to: {output_file}")
        
        return results_df
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find {input_file}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def print_summary(results_df):
    """Print summary statistics"""
    if results_df is None or len(results_df) == 0:
        print("No data to summarize")
        return
    
    print("\n" + "=" * 60)
    print("📊 SYSTEM SUMMARY:")
    print("=" * 60)
    
    # Calculate from original data
    df = pd.read_csv('data/power_system.csv')
    total_load = df['load_kw'].sum()
    total_loss = results_df['total_losses_kw'].sum()
    
    print(f"Total Load: {total_load:,.2f} kW")
    print(f"Total System Losses: {total_loss:,.2f} kW")
    print(f"Overall Loss Percentage: {(total_loss/total_load*100):.2f}%")
    print(f"Overall Efficiency: {100 - (total_loss/total_load*100):.2f}%")
    
    # Find best and worst lines
    worst_line = results_df.loc[results_df['loss_percentage'].idxmax()]
    best_line = results_df.loc[results_df['efficiency'].idxmax()]
    
    print(f"\n🔴 Worst Performing Line: {worst_line['line_id']} ({worst_line['loss_percentage']:.2f}% loss)")
    print(f"🟢 Best Performing Line: {best_line['line_id']} ({best_line['efficiency']:.2f}% efficiency)")

if __name__ == "__main__":
    print("=" * 60)
    print("⚡ POWER SYSTEM LINE LOSS CALCULATOR")
    print("=" * 60)
    
    # Calculate with original data
    results = calculate_and_save('data/power_system.csv', 'data/loss_calculations.csv')
    
    if results is not None:
        # Print line-by-line results
        print("\n📈 LINE-BY-LINE RESULTS:")
        print("-" * 60)
        for _, row in results.iterrows():
            print(f"{row['line_id']} - {row['area_name']}:")
            print(f"  Current: {row['current_amps']} A | Loss: {row['total_losses_kw']} kW | Efficiency: {row['efficiency']}%")
        
        # Print summary
        print_summary(results)