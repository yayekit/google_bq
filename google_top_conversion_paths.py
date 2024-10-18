import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    csv_file = 'bquxjob_6d7220c_19271ce2c4e.csv'
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file '{csv_file}' not found.")
    df = pd.read_csv(csv_file)
    required_columns = ['total_transactions', 'total_sessions', 'conversion_path', 'user_count']
    if not all(col in df.columns for col in required_columns):
        missing_cols = [col for col in required_columns if col not in df.columns]
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
    df['conversion_rate'] = df['total_transactions'] / df['total_sessions']
    df['path_length'] = df['conversion_path'].str.count('>') + 1
    df['first_touch'] = df['conversion_path'].str.split('>').str[0].str.strip()
    color_map = {
        'Organic Search': '#1f77b4',
        'Referral': '#ff7f0e',
        'Direct': '#2ca02c',
        'Paid Search': '#d62728',
        'Social': '#9467bd',
        'Display': '#8c564b'
    }
    fig = create_figure(df, color_map)
    fig.show()
    fig.write_image("google_top_conversion_paths.png", scale=5, width=1920, height=1080)

def create_figure(df, color_map):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Top 10 Conversion Paths",
            "Conversion Rate vs Path Length",
            "Sessions vs Transactions",
            "Channel Distribution"
        ),
        specs=[
            [{"type": "bar"}, {"type": "scatter"}],
            [{"type": "scatter"}, {"type": "pie"}]
        ]
    )
    add_conversion_path_bar(fig, df, color_map)
    add_conversion_rate_scatter(fig, df, color_map)
    add_sessions_vs_transactions_scatter(fig, df, color_map)
    add_channel_distribution_pie(fig, df, color_map)
    fig.update_layout(height=1000, width=1200)
    fig.update_xaxes(title_text="Conversion Path", row=1, col=1)
    fig.update_xaxes(title_text="Total Sessions", row=2, col=1)
    fig.update_yaxes(title_text="Total Transactions", row=1, col=1)
    fig.update_yaxes(title_text="Total Transactions", row=2, col=1)
    fig.add_annotation(
        text="Marker size represents user count",
        xref="x domain", yref="paper",
        x=0.5, y=-0.25,
        showarrow=False,
        row=2, col=1
    )
    return fig

def add_conversion_path_bar(fig, df, color_map):
    top_10 = df.nlargest(10, 'total_transactions')
    marker_colors = [
        color_map.get(path.split('>')[0].strip(), '#636EFA') for path in top_10['conversion_path']
    ]
    fig.add_trace(
        go.Bar(
            x=top_10['conversion_path'],
            y=top_10['total_transactions'],
            name='Transactions',
            marker_color=marker_colors
        ),
        row=1, col=1
    )

def add_conversion_rate_scatter(fig, df, color_map):
    marker_colors = [color_map.get(touch, '#636EFA') for touch in df['first_touch']]
    marker_sizes = df['total_transactions'] / 10
    fig.add_trace(
        go.Scatter(
            x=df['path_length'],
            y=df['conversion_rate'],
            mode='markers',
            marker=dict(size=marker_sizes, color=marker_colors),
            text=df['conversion_path'],
            name='Conversion Rate'
        ),
        row=1, col=2
    )
    fig.update_xaxes(title_text="Path Length", range=[-1, 12], dtick=2, row=1, col=2)
    fig.update_yaxes(title_text="Conversion Rate", range=[-0.02, 0.14], dtick=0.02, row=1, col=2)

def add_sessions_vs_transactions_scatter(fig, df, color_map):
    marker_colors = [color_map.get(touch, '#636EFA') for touch in df['first_touch']]
    marker_sizes = df['user_count'] / 1000
    fig.add_trace(
        go.Scatter(
            x=df['total_sessions'],
            y=df['total_transactions'],
            mode='markers',
            marker=dict(size=marker_sizes, color=marker_colors),
            text=df['conversion_path'],
            name='Sessions vs Transactions'
        ),
        row=2, col=1
    )

def add_channel_distribution_pie(fig, df, color_map):
    channel_distribution = df.groupby('first_touch')['total_transactions'].sum()
    labels = channel_distribution.index
    values = channel_distribution.values
    colors = [color_map.get(channel, '#636EFA') for channel in labels]
    fig.add_trace(
        go.Pie(
            labels=labels,
            values=values,
            name='Channel Distribution',
            marker=dict(colors=colors)
        ),
        row=2, col=2
    )

if __name__ == "__main__":
    main()
