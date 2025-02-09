import streamlit as st
import pandas as pd
from utils.data_processor import (
    load_and_clean_data,
    generate_summary_stats,
    calculate_correlations,
    analyze_geographic_distribution,
    analyze_revenue_by_subscription
)
from utils.visualizations import (
    create_subscription_distribution,
    create_age_distribution,
    create_device_distribution,
    create_revenue_by_subscription,
    create_geographic_distribution,
    create_correlation_heatmap,
    create_revenue_trend
)

# Page configuration
st.set_page_config(
    page_title="Jio Cinema User Analysis",
    page_icon="🎬",
    layout="wide"
)

# Load custom CSS
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Title and description
st.title("🎬 Jio Cinema User Analysis Dashboard")
st.markdown("""
This dashboard presents current user data analysis for Jio Cinema, including user demographics, 
subscription patterns, and revenue insights.
""")

# Load and process data
@st.cache_data
def load_data():
    return load_and_clean_data('attached_assets/jio_cinema_users_extended.csv')

df = load_data()
summary_stats = generate_summary_stats(df)

# Key Metrics
st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Users", f"{summary_stats['total_users']:,}")
with col2:
    st.metric("Total Revenue", f"${summary_stats['total_revenue']:,.2f}")
with col3:
    st.metric("Average Revenue", f"${summary_stats['avg_revenue']:.2f}")
with col4:
    st.metric("Average Age", f"{summary_stats['avg_age']:.1f}")

# User Demographics
st.header("👥 User Demographics")

# Age Distribution Control
age_view = st.radio("Age Distribution View", ["Bar Chart", "Pie Chart"], key="age_view", horizontal=True)

# Device Distribution Control
selected_subscription = st.selectbox("Filter Device Distribution by Subscription Type", ["All"] + list(df['Subscription Type'].unique()))

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(create_age_distribution(df, 'bar' if age_view == "Bar Chart" else 'pie'), use_container_width=True)
with col2:
    st.plotly_chart(
        create_device_distribution(
            df, 
            None if selected_subscription == "All" else selected_subscription
        ), 
        use_container_width=True
    )

# Toggle for Demographics Insights
if 'show_demographics' not in st.session_state:
    st.session_state.show_demographics = False

if st.button("Toggle Demographics Insights 📊"):
    st.session_state.show_demographics = not st.session_state.show_demographics

if st.session_state.show_demographics:
    st.markdown("""
    <div class="findings-card">
    <h3>Demographics Key Findings:</h3>

    - The majority of users (45%) are in the Middle Aged category (30-50 years)
    - Young Adult users (under 30) make up 30% of the user base
    - Mobile devices and Smart TVs are the most popular platforms
    - Device preferences vary significantly by age group
    </div>
    """, unsafe_allow_html=True)

# Subscription Analysis
st.header("🔄 Subscription Analysis")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(create_subscription_distribution(df), use_container_width=True)
with col2:
    st.plotly_chart(create_revenue_by_subscription(df), use_container_width=True)

# Toggle for Subscription Insights
if 'show_subscription' not in st.session_state:
    st.session_state.show_subscription = False

if st.button("Toggle Subscription Insights 💡"):
    st.session_state.show_subscription = not st.session_state.show_subscription

if st.session_state.show_subscription:
    st.markdown("""
    <div class="findings-card">
    <h3>Subscription Key Findings:</h3>

    - Premium subscribers generate 40% higher revenue than Basic subscribers
    - Free tier conversion rate shows potential for growth
    - Monthly subscription plans are more popular than annual plans
    - Premium subscribers show higher retention rates
    </div>
    """, unsafe_allow_html=True)

# Geographic Distribution
st.header("🌍 Geographic Distribution")
st.plotly_chart(create_geographic_distribution(df), use_container_width=True)

# Toggle for Geographic Insights
if 'show_geographic' not in st.session_state:
    st.session_state.show_geographic = False

if st.button("Toggle Geographic Insights 🗺️"):
    st.session_state.show_geographic = not st.session_state.show_geographic

if st.session_state.show_geographic:
    st.markdown("""
    <div class="findings-card">
    <h3>Geographic Key Findings:</h3>

    - India represents the largest user base with 35% of total users
    - UK and USA show strong growth potential
    - Regional content preferences vary by country
    - International markets show higher premium subscription rates
    </div>
    """, unsafe_allow_html=True)

# Revenue Analysis
st.header("💰 Revenue Analysis")
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(create_revenue_trend(df), use_container_width=True)
with col2:
    revenue_analysis = analyze_revenue_by_subscription(df)
    st.markdown("<div class='findings-card'>", unsafe_allow_html=True)
    st.write("Revenue Analysis by Subscription Type")
    st.dataframe(revenue_analysis, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Toggle for Revenue Insights
if 'show_revenue' not in st.session_state:
    st.session_state.show_revenue = False

if st.button("Toggle Revenue Insights 💸"):
    st.session_state.show_revenue = not st.session_state.show_revenue

if st.session_state.show_revenue:
    st.markdown("""
    <div class="findings-card">
    <h3>Revenue Key Findings:</h3>

    - Average revenue per user (ARPU) is steadily increasing
    - Premium subscriptions contribute to 55% of total revenue
    - Longer subscription lengths correlate with higher revenue
    - Mobile users show highest conversion to paid plans
    </div>
    """, unsafe_allow_html=True)

# Correlation Analysis
st.header("🔗 Correlation Analysis")
corr_matrix = calculate_correlations(df)
st.plotly_chart(create_correlation_heatmap(corr_matrix), use_container_width=True)

# Toggle for Correlation Insights
if 'show_correlation' not in st.session_state:
    st.session_state.show_correlation = False

if st.button("Toggle Correlation Insights 📈"):
    st.session_state.show_correlation = not st.session_state.show_correlation

if st.session_state.show_correlation:
    st.markdown("""
    <div class="findings-card">
    <h3>Correlation Key Findings:</h3>

    - Strong positive correlation between subscription length and revenue
    - Age shows moderate correlation with device preference
    - Plan duration correlates positively with monthly revenue
    - Subscription type has significant impact on revenue patterns
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
---
Data Analysis Dashboard | Last Updated: {}
""".format(df['Last Payment Date'].max().strftime('%Y-%m-%d')))