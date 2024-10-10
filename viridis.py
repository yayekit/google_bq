import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Read the CSV file
df = pd.read_csv('bquxjob_777a5640_19272ca89e0.csv')

# Create subplot with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add bar chart for conversions
fig.add_trace(
    go.Bar(
        x=df['time_lag_bucket'],
        y=df['conversions'],
        name="Conversions",
        marker_color='rgba(99,110,250,0.7)',
    ),
    secondary_y=False,
)

# Add line chart for percentage of total
fig.add_trace(
    go.Scatter(
        x=df['time_lag_bucket'],
        y=df['percentage_of_total'],
        name="Percentage of Total",
        line=dict(color='rgba(239,85,59,0.8)', width=3),
        mode='lines+markers',
    ),
    secondary_y=True,
)

# Customize layout
fig.update_layout(
    title=dict(
        text='Time Lag vs Conversions',
        font=dict(size=24, color='#000000', family="Arial Black")
    ),
    xaxis=dict(
        title=dict(
            text='Time Lag (Days)',
            font=dict(size=18, color='#000000', family="Arial Black")
        ),
        tickfont=dict(size=14, color='#000000', family="Arial")
    ),
    yaxis=dict(
        title=dict(
            text='Number of Conversions',
            font=dict(size=18, color='#000000', family="Arial Black")
        ),
        tickfont=dict(size=14, color='#000000', family="Arial")
    ),
    yaxis2=dict(
        title=dict(
            text='Percentage of Total Conversions',
            font=dict(size=18, color='#000000', family="Arial Black")
        ),
        tickfont=dict(size=14, color='#000000', family="Arial"),
        range=[0, max(df['percentage_of_total']) * 1.1]  # Adjust range for better visibility
    ),
    legend=dict(
        font=dict(size=16, color='#000000', family="Arial"),
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    ),
    plot_bgcolor='white',
    height=800,
    width=1200,
)

# Update axes
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

# Show the plot
fig.show()

# Saving the plot as am HTML to visualize later
fig.write_html("time_lag_vs_conversions.html")