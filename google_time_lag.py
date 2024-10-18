import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    # File path
    csv_file = 'bquxjob_777a5640_19272ca89e0.csv'

    # Check if file exists
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"File '{csv_file}' not found.")

    # Read data
    df = pd.read_csv(csv_file)

    # Validate data
    required_columns = ['time_lag_bucket', 'conversions', 'percentage_of_total']
    if not all(col in df.columns for col in required_columns):
        missing_cols = [col for col in required_columns if col not in df.columns]
        raise ValueError(f"Missing columns in data: {', '.join(missing_cols)}")

    # Create figure
    fig = create_time_lag_vs_conversions_figure(df)

    # Show and save figure
    fig.show()
    fig.write_image("google_time_lag.png", scale=5, width=1920, height=1080)

def create_time_lag_vs_conversions_figure(df):
    # Define colors and fonts
    colors = {
        'conversions': 'rgba(99,110,250,0.7)',
        'percentage_of_total': 'rgba(239,85,59,0.8)',
        'grid': 'lightgray',
        'text': '#000000',
        'background': 'white'
    }

    fonts = {
        'title': dict(size=24, color=colors['text'], family="Arial Black"),
        'axis_title': dict(size=18, color=colors['text'], family="Arial Black"),
        'tickfont': dict(size=14, color=colors['text'], family="Arial"),
        'legendfont': dict(size=16, color=colors['text'], family="Arial")
    }

    # Max percentage for y-axis range
    max_percentage = df['percentage_of_total'].max()

    # Create subplot with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add bar chart for conversions
    fig.add_trace(
        go.Bar(
            x=df['time_lag_bucket'],
            y=df['conversions'],
            name="Conversions",
            marker_color=colors['conversions'],
        ),
        secondary_y=False,
    )

    # Add line chart for percentage of total
    fig.add_trace(
        go.Scatter(
            x=df['time_lag_bucket'],
            y=df['percentage_of_total'],
            name="Percentage of Total",
            line=dict(color=colors['percentage_of_total'], width=3),
            mode='lines+markers',
        ),
        secondary_y=True,
    )

    # Update layout
    fig.update_layout(
        title=dict(text='Time Lag vs Conversions', font=fonts['title']),
        xaxis=dict(
            title=dict(text='Time Lag (Days)', font=fonts['axis_title']),
            tickfont=fonts['tickfont'],
            showgrid=True, gridwidth=1, gridcolor=colors['grid'],
        ),
        yaxis=dict(
            title=dict(text='Number of Conversions', font=fonts['axis_title']),
            tickfont=fonts['tickfont'],
            showgrid=True, gridwidth=1, gridcolor=colors['grid'],
        ),
        yaxis2=dict(
            title=dict(text='Percentage of Total Conversions', font=fonts['axis_title']),
            tickfont=fonts['tickfont'],
            range=[0, max_percentage * 1.1],
            showgrid=False,
        ),
        legend=dict(
            font=fonts['legendfont'],
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        plot_bgcolor=colors['background'],
        height=800,
        width=1200,
    )

    return fig

if __name__ == "__main__":
    main()
