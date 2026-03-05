# Note: This script generates synthetic restaurant operations data 
# to demonstrate business logic while ensuring data privacy.
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import os

if not os.path.exists('data'):
    os.makedirs('data')
    print("Created 'data' directory.")

# Initialize Faker and set seed for reproducibility
fake = Faker()
np.random.seed(42)

# 1. Generate Employee Master Data (15 employees)
employees = []
roles_wages = {'Barista': 18.5, 'Cook': 21.0, 'Manager': 26.0}

for _ in range(15):
    role = np.random.choice(list(roles_wages.keys()))
    employees.append({
        'employee_id': fake.uuid4()[:8],
        'name': fake.name(),
        'role': role,
        # Set hourly wage based on role with slight random variation
        'hourly_wage': roles_wages[role] + round(np.random.uniform(-2, 2), 2)
    })
employees_df = pd.DataFrame(employees)

# 2. Generate Daily Shift & Sales Data (100 days)
data = []
for day in range(100):
    # Set date starting from March 1st, 2026
    date = datetime(2026, 3, 1) + timedelta(days=day)
    is_weekend = date.weekday() >= 5
    
    # Sales Simulation: Increase sales by 60% on weekends to reflect peak demand
    base_sales = np.random.normal(5000, 1000)
    daily_sales = base_sales * (1.6 if is_weekend else 1.0)
    daily_sales = max(1500, daily_sales) # Ensure a minimum floor for sales
    
    # Shift Simulation: Number of shifts scales with daily sales volume
    num_shifts = int(daily_sales / 450) + np.random.randint(0, 3)
    
    for _ in range(num_shifts):
        emp = employees_df.sample(1).iloc[0]
        # Shift hours typically range between 4 and 9 hours
        hours = np.random.uniform(4, 9)
        cost = hours * emp['hourly_wage']
        
        # Payroll Error Simulation: 5% chance of manual entry error (key 7shifts pain point)
        payroll_error = 1 if np.random.random() < 0.05 else 0
        
        data.append({
            'date': date.date(),
            'employee_id': emp['employee_id'],
            'name': emp['name'],
            'role': emp['role'],
            'hours_worked': round(hours, 1),
            'labor_cost': round(cost, 2),
            'daily_sales': round(daily_sales, 2), # Record total daily sales for indexing
            'payroll_error': payroll_error
        })

df = pd.DataFrame(data)

# 3. Aggregate Metrics for Dashboard Processing
daily_metrics = df.groupby('date').agg({
    'labor_cost': 'sum',
    'daily_sales': 'first', # Use the first entry as daily_sales is constant per date
    'payroll_error': 'sum',
    'hours_worked': 'sum'
}).reset_index()

# Calculate Labor Cost Percentage (Target KPI for 7shifts users)
daily_metrics['labor_pct'] = (daily_metrics['labor_cost'] / daily_metrics['daily_sales']) * 100

# Export to CSV for Streamlit application
df.to_csv('data/restaurant_shifts_raw.csv', index=False)
daily_metrics.to_csv('data/restaurant_metrics_dashboard.csv', index=False)

print(f"✅ Mock data generation complete!")
print(f"Generated {len(df)} shifts across {len(daily_metrics)} days.")
print(f"Average Labor %: {round(daily_metrics['labor_pct'].mean(), 2)}%")
