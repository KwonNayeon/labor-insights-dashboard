# Labor Performance Insights Dashboard

This project is a decision-making tool designed for restaurant managers to optimize labor costs and monitor scheduling efficiency. It provides actionable insights into labor-to-sales ratios and payroll error patterns.

## Project Overview
- **Objective**: To visualize labor cost efficiency and identify operational bottlenecks (e.g., payroll errors, labor variance).
- **Target Audience**: Store Managers and Operations Directors.
- **Tools**: Python, Streamlit, Plotly, Pandas.

## Directory Structure
- `data/`: Contains generated mock datasets for analysis.
- `data_generator.py`: Script to programmatically generate restaurant operations data.
- `app.py`: Main Streamlit application for the interactive dashboard.
- `requirements.txt`: List of required Python packages.

## Note on Data Privacy
To ensure data privacy and demonstrate business logic understanding, all datasets used in this project are programmatically generated **mock data** that reflect real-world restaurant operations, including weekend peak trends and role-based wage variances.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Generate data: `python data_generator.py`
3. Run dashboard: `streamlit run app.py`
