import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_subscription_distribution(df):
    fig = px.pie(df, 
                 names='Subscription Type',
                 title='Subscription Type Distribution',
                 color_discrete_sequence=['#4E79A7', '#F28E2B', '#59A14F'])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        transition_duration=500,
        transition=dict(
            duration=500,
            easing='cubic-in-out'
        )
    )
    return fig

def create_age_distribution(df, view_type='bar'):
    age_dist = df['Age Bracket'].value_counts().reset_index()
    age_dist.columns = ['Age Bracket', 'Count']

    if view_type == 'bar':
        fig = px.bar(age_dist,
                    x='Age Bracket',
                    y='Count',
                    title='Age Distribution',
                    color_discrete_sequence=['#4E79A7'])
    else:  
        fig = px.pie(age_dist,
                    values='Count',
                    names='Age Bracket',
                    title='Age Distribution',
                    color_discrete_sequence=['#4E79A7', '#F28E2B', '#59A14F'])
        fig.update_traces(textposition='inside', textinfo='percent+label')

    fig.update_layout(
        xaxis_title='Age Group',
        yaxis_title='Number of Users',
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        transition_duration=500,
        transition=dict(
            duration=500,
            easing='cubic-in-out'
        )
    )
    return fig

def create_revenue_by_subscription(df, time_period='all'):
    if time_period != 'all':
        df = df[df['Join Date'] >= pd.Timestamp.now() - pd.Timedelta(time_period)]

    avg_revenue = df.groupby('Subscription Type')['Monthly Revenue'].mean().reset_index()
    fig = px.bar(avg_revenue,
                 x='Subscription Type',
                 y='Monthly Revenue',
                 title='Average Revenue by Subscription Type',
                 color_discrete_sequence=['#4E79A7'])
    fig.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        transition_duration=500,
        transition=dict(
            duration=500,
            easing='cubic-in-out'
        )
    )
    return fig

def create_device_distribution(df, subscription_type=None):
    if subscription_type:
        df = df[df['Subscription Type'] == subscription_type]

    device_dist = df['Device'].value_counts().reset_index()
    device_dist.columns = ['Device Type', 'Count']

    fig = px.bar(device_dist,
                 x='Device Type',
                 y='Count',
                 title='Device Usage Distribution',
                 color_discrete_sequence=['#F28E2B'])
    fig.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        transition_duration=500,
        transition=dict(
            duration=500,
            easing='cubic-in-out'
        )
    )
    return fig

def create_geographic_distribution(df):
    geo_dist = df['Country'].value_counts().reset_index()
    geo_dist.columns = ['Country', 'Count']

    fig = px.choropleth(geo_dist,
                       locations='Country',
                       locationmode='country names',
                       color='Count',
                       title='Geographic Distribution',
                       color_continuous_scale='Viridis')
    fig.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        transition_duration=500,
        transition=dict(
            duration=500,
            easing='cubic-in-out'
        )
    )
    return fig

def create_correlation_heatmap(corr_matrix):
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmin=-1,
        zmax=1,
        colorbar=dict(title='Correlation')
    ))
    fig.update_layout(
        title='Correlation Matrix',
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='',
        yaxis_title='',
        width=800,
        height=800,
        transition_duration=500,
        transition=dict(
            duration=500,
            easing='cubic-in-out'
        )
    )
    return fig

def create_revenue_trend(df):
    monthly_revenue = df.groupby('Join Month')['Monthly Revenue'].mean().reset_index()
    monthly_revenue['Join Month'] = monthly_revenue['Join Month'].astype(str)

    fig = px.line(monthly_revenue,
                  x='Join Month',
                  y='Monthly Revenue',
                  title='Average Monthly Revenue Trend',
                  color_discrete_sequence=['#59A14F'])
    fig.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        transition_duration=500,
        transition=dict(
            duration=500,
            easing='cubic-in-out'
        )
    )
    return fig