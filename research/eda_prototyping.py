import pandas as pd

# ---------------------------------------------------------
# STEP 0: Data Loading & Structural EDA
# Purpose: Validating raw shift data integrity before processing daily metrics.
# Ensuring no missing values or data type mismatches in the source file.
# ---------------------------------------------------------
df_metrics = pd.read_csv('data/restaurant_metrics_dashboard.csv')
df_raw = pd.read_csv('data/restaurant_shifts_raw.csv')

print("### [EDA] Dataset Overview ###")
# Checking the shape and basic info of raw shift data
print(f"Raw Shifts Shape: {df_raw.shape}")
print(f"Daily Metrics Shape: {df_metrics.shape}")

# Inspecting column types and null values (7shifts values data integrity)
print("\n--- Raw Data Info ---")
print(df_raw.info())

print("\n--- Missing Values Check ---")
print(df_raw.isnull().sum())

# Basic statistical distribution to detect outliers early
print("\n--- Numerical Distribution (Raw) ---")
print(df_raw[['hours_worked', 'labor_cost']].describe())

# ---------------------------------------------------------
# STEP 1: Feature Engineering & Pre-processing
# Based on the EDA, we transform raw data into business insights.
# ---------------------------------------------------------
df_metrics['date'] = pd.to_datetime(df_metrics['date'])

# Using a standard wage for modeling ($17.60 - Ontario min wage + buffer)
avg_wage = 17.60 
df_metrics['labor_hours'] = df_metrics['labor_cost'] / avg_wage
df_metrics['splh'] = df_metrics['daily_sales'] / df_metrics['labor_hours']
df_metrics['labor_pct'] = (df_metrics['labor_cost'] / df_metrics['daily_sales']) * 100

# ---------------------------------------------------------
# STEP 2: Deep Dive - Labor Efficiency Analysis
# ---------------------------------------------------------
df_metrics['day_name'] = df_metrics['date'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_stats = df_metrics.groupby('day_name')[['labor_pct', 'splh']].mean().reindex(day_order)

print("\n### [Analysis] Weekly Labor Efficiency Summary ###")
print(daily_stats)

# ---------------------------------------------------------
# STEP 3: Identifying Anomalies & Inconsistencies
# Finding days that deviate from the 30% industry target.
# ---------------------------------------------------------
# Extract days where Labor % exceeds 35% to identify operational inconsistencies.
inefficient_days = df_metrics[df_metrics['labor_pct'] > 35]
print(f"\nObservation: Found {len(inefficient_days)} days with high labor cost (>35%)")

# Correlation Check: Does higher sales volume lead to better efficiency?
correlation = df_metrics['daily_sales'].corr(df_metrics['labor_pct'])
print(f"Insight: Correlation between Sales and Labor % is {correlation:.2f}")

# ---------------------------------------------------------
# STEP 4: Final Ranking for Actionable Strategy
# ---------------------------------------------------------
ranking = daily_stats.sort_values(by='labor_pct', ascending=True)

print("\n" + "="*50)
print("🏆 FINAL LABOR EFFICIENCY RANKING (Strategy Priority)")
print("="*50)
for i, (day, row) in enumerate(ranking.iterrows(), 1):
    status = "✅ BEST" if i == 1 else ("⚠️ NEEDS CHECK" if i == len(ranking) else "")
    print(f"{i}. {day:<10} | Labor %: {row['labor_pct']:.2f}% | SPLH: ${row['splh']:.2f} {status}")
print("="*50)
