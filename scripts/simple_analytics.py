"""
SIMPLE ANALYTICS FOR POWER SYSTEM
Shows trends and insights
"""
import pandas as pd
import numpy as np
from datetime import datetime

def analyze_system():
    print("=" * 60)
    print("📊 POWER SYSTEM ANALYTICS")
    print("=" * 60)
    
    # Load data
    try:
        df = pd.read_csv('data/power_system.csv')
        loss_df = pd.read_csv('data/loss_calculations.csv')
        
        # Merge data
        merged = pd.merge(df, loss_df, on=['line_id', 'area_name'])
        
        print(f"System has {len(merged)} transmission lines")
        print()
        
        # 1. Basic statistics
        print("1️⃣ BASIC STATISTICS:")
        print("-" * 40)
        print(f"Total Load: {merged['load_kw'].sum():,.0f} kW")
        print(f"Total Losses: {merged['total_losses_kw'].sum():,.1f} kW")
        print(f"Average Efficiency: {merged['efficiency'].mean():.1f}%")
        print(f"Average Loss %: {merged['loss_percentage'].mean():.2f}%")
        print()
        
        # 2. Performance ranking
        print("2️⃣ LINE PERFORMANCE RANKING:")
        print("-" * 40)
        ranked = merged.sort_values('efficiency', ascending=False)
        for i, (_, row) in enumerate(ranked.iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            print(f"{medal} {row['line_id']} - {row['area_name']}: {row['efficiency']:.1f}% efficiency")
        print()
        
        # 3. Problem identification
        print("3️⃣ PROBLEM IDENTIFICATION:")
        print("-" * 40)
        
        # High losses
        high_loss = merged[merged['loss_percentage'] > 3.5]
        if not high_loss.empty:
            print("⚠️  High Loss Lines (>3.5%):")
            for _, row in high_loss.iterrows():
                print(f"   {row['line_id']}: {row['loss_percentage']:.2f}% loss")
        
        # High voltage drop
        high_vdrop = merged[merged['voltage_drop_v'] > 150]
        if not high_vdrop.empty:
            print("\n⚠️  High Voltage Drop (>150V):")
            for _, row in high_vdrop.iterrows():
                print(f"   {row['line_id']}: {row['voltage_drop_v']:.1f} V drop")
        
        # 4. Recommendations
        print("\n4️⃣ RECOMMENDATIONS:")
        print("-" * 40)
        
        # Find line with highest losses
        worst = merged.loc[merged['loss_percentage'].idxmax()]
        print(f"🔴 Priority Action: {worst['line_id']} ({worst['area_name']})")
        print(f"   Current loss: {worst['loss_percentage']:.2f}%")
        print(f"   Suggested: Check {worst['conductor_type']} conductor condition")
        
        # Cost analysis
        electricity_rate = 0.10  # $ per kWh
        daily_loss_cost = merged['total_losses_kw'].sum() * 24 * electricity_rate
        print(f"\n💰 Daily Cost of Losses: ${daily_loss_cost:.2f}")
        print(f"💰 Annual Cost of Losses: ${daily_loss_cost * 365:,.2f}")
        
        # Potential savings (10% reduction)
        potential_savings = daily_loss_cost * 0.10 * 365
        print(f"💰 Potential Annual Savings (10% improvement): ${potential_savings:,.2f}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Please run calculate_losses.py first")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    analyze_system()