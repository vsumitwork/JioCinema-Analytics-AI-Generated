import pandas as pd
import numpy as np

def load_and_clean_data(file_path):
    # Load the data
    df = pd.read_csv(file_path)

    # Convert date columns to datetime
    date_columns = ['Join Date', 'Last Payment Date']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col])

    # Create age brackets with three categories
    df['Age Bracket'] = pd.cut(df['Age'], 
                            bins=[0, 30, 50, 100],
                            labels=['Young Adult', 'Middle Aged', 'Older Adult'])

    # Calculate subscription length
    df['Subscription Length'] = (df['Last Payment Date'] - df['Join Date']).dt.days

    # Create month-year columns for trend analysis
    df['Join Month'] = df['Join Date'].dt.to_period('M')

    return df

def generate_summary_stats(df):
    summary = {
        'total_users': len(df),
        'total_revenue': df['Monthly Revenue'].sum(),
        'avg_revenue': df['Monthly Revenue'].mean(),
        'subscription_distribution': df['Subscription Type'].value_counts().to_dict(),
        'device_distribution': df['Device'].value_counts().to_dict(),
        'avg_age': df['Age'].mean()
    }
    return summary

def calculate_correlations(df):
    numeric_cols = ['Age', 'Monthly Revenue', 'Plan Duration (Months)', 'Subscription Length']
    return df[numeric_cols].corr()

def analyze_geographic_distribution(df):
    return df['Country'].value_counts().to_dict()

def analyze_revenue_by_subscription(df):
    return df.groupby('Subscription Type')['Monthly Revenue'].agg(['mean', 'sum', 'count']).round(2)