import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Labor Optimization Dashboard", layout="wide")

st.title("Labor Performance Analytics Dashboard")
st.markdown("Strategic tool for analyzing labor cost efficiency and operational scheduling.")

# 2. Data Loading
@st.cache_data
def load_data():
    # Loading the processed daily metrics generated from the research script
    df = pd.read_csv('data/restaurant_metrics_dashboard.csv', parse_dates=['date'])
    return df

df = load_data()

# 3. Sidebar Configuration
with st.sidebar:
    st.header("Control Panel")
    
    st.subheader("Dataset Summary")
    total_days = len(df)
    start_date = df['date'].min().strftime('%Y-%m-%d')
    end_date = df['date'].max().strftime('%Y-%m-%d')
    
    # 불필요한 수식어를 빼고 팩트 위주로 정리
    st.info(f"**Analyzing {total_days} days** of data.\n\n"
            f"**Period:** {start_date} to {end_date}")
    
    st.divider()
    
    # Analysis Filters
    st.subheader("Analysis Filters")
    date_range = st.date_input("Select Date Range", [df['date'].min(), df['date'].max()])

# 4. Executive Summary: Key Performance Indicators (KPIs)
st.subheader("Executive KPI Overview")
avg_labor_pct = df['labor_pct'].mean()
total_sales_sum = df['daily_sales'].sum()
total_errors = df['payroll_error'].sum()

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
kpi_col1.metric("Avg Labor Cost %", f"{avg_labor_pct:.1f}%", help="Target Benchmark: 25-30%")
kpi_col2.metric("Total Revenue", f"${total_sales_sum:,.0f}")
kpi_col3.metric("Payroll Anomalies", int(total_errors))

# 5. Financial Impact: Cost Saving Opportunity
st.divider()
st.subheader("Labor Cost Optimization Opportunity")

# Calculation logic for potential savings based on a 30% efficiency target
target_pct = 30
excess_labor_df = df[df['labor_pct'] > target_pct].copy()
excess_labor_df['potential_savings'] = excess_labor_df['labor_cost'] - (excess_labor_df['daily_sales'] * (target_pct / 100))

total_potential_savings = excess_labor_df['potential_savings'].sum()

save_col1, save_col2 = st.columns([1, 2])

with save_col1:
    st.metric("Total Potential Savings", f"${total_potential_savings:,.2f}")
    st.caption(f"Estimated savings by optimizing {len(excess_labor_df)} days exceeding the {target_pct}% target.")

with save_col2:
    if total_potential_savings > 0:
        st.info(f"By refining scheduling for specific inefficient days, the operation could reclaim **${total_potential_savings:,.2f}** in net profit.")
    else:
        st.success("Labor efficiency is currently within the optimal performance range.")

# 6. Trend Analysis: Financial Tracking
st.subheader("Daily Revenue vs. Labor Expenditure Trend")
fig_line = px.line(df, x='date', y=['daily_sales', 'labor_cost'],
              labels={'value': 'Amount (CAD)', 'date': 'Date'},
              color_discrete_map={'daily_sales': '#1f77b4', 'labor_cost': '#ff7f0e'})
st.plotly_chart(fig_line, use_container_width=True)

# Statistical Correlation Analysis
correlation = df['daily_sales'].corr(df['labor_pct'])
st.write(f"Statistical Insight: The correlation between Sales and Labor % is **{correlation:.2f}**.")
if correlation < 0:
    st.caption("Note: A negative correlation indicates that fixed labor costs are better utilized as sales volume increases.")

# 7. Operational Analysis: Day-of-Week Efficiency
st.divider()
st.subheader("Weekly Efficiency Performance Ranking")

df['day_of_week'] = df['date'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_stats = df.groupby('day_of_week')[['labor_pct', 'daily_sales']].mean().reindex(day_order).reset_index()

fig_bar = px.bar(daily_stats, x='day_of_week', y='labor_pct',
                 color='labor_pct',
                 color_continuous_scale='RdYlGn_r', 
                 labels={'labor_pct': 'Labor Cost %', 'day_of_week': 'Day'})
fig_bar.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Industry Benchmark (30%)")
st.plotly_chart(fig_bar, use_container_width=True)

# 8. Operational Anomalies
st.subheader("Operational Efficiency Alerts")
inefficient_days = df[df['labor_pct'] > 35].sort_values(by='labor_pct', ascending=False)

if not inefficient_days.empty:
    st.warning(f"Identified {len(inefficient_days)} instances where labor cost exceeded the 35% threshold.")
    st.dataframe(inefficient_days[['date', 'daily_sales', 'labor_cost', 'labor_pct']], 
                 use_container_width=True, hide_index=True)
else:
    st.success("No critical labor cost spikes detected in the current period.")

# 9. Strategic Recommendation
st.divider()
best_day = daily_stats.sort_values('labor_pct').iloc[0]['day_of_week']
worst_day = daily_stats.sort_values('labor_pct').iloc[-1]['day_of_week']

st.info(f"""
### Strategic Insights
* **High Performance Analysis:** **{best_day}** exhibits the highest labor efficiency. This performance level serves as the benchmark for scheduling optimization.
* **Optimization Focus:** **{worst_day}** shows the highest labor cost ratio. A detailed shift review is recommended to identify potential labor leakage.
* **Profitability Goal:** Aligning labor costs with the **30% industry benchmark** across all operating days will maximize net profitability.
""")
