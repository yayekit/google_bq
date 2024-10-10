import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the data
df  =  pd.read_csv('bquxjob_6d7220c_19271ce2c4e.csv')

# Calculate conversion rate and path length
df['conversion_rate'] = df['total_transactions'] / df['total_sessions']
df['path_length'] = df['conversion_path'].str.count('>') + 1

# Create the subplot structure
fig = make_subplots(
    rows = 2, cols = 2,
    subplot_titles = ("Top 10 Conversion Paths", "Conversion Rate vs Path Length", 
                    "Sessions vs Transactions", "Channel Distribution"),
    specs = [[{"type": "bar"}, {"type": "scatter"}],
           [{"type": "scatter"}, {"type": "pie"}]]
)

# 1. Bar Chart: Top 10 Conversion Paths
top_10 = df.nlargest(10, 'total_transactions')
fig.add_trace(
    go.Bar(x = top_10['conversion_path'], y = top_10['total_transactions'], name = 'Transactions'),
    row = 1, col = 1
)

# 2. Scatter Plot: Conversion Rate vs Path Length
fig.add_trace(
    go.Scatter(x = df['path_length'], y = df['conversion_rate'], mode = 'markers', 
               marker = dict(size = df['total_transactions']/10, color = df['total_sessions'], colorscale = 'Viridis'),
               text = df['conversion_path'], name = 'Conversion Rate'),
    row = 1, col = 2
)

# 3. Scatter Plot: Sessions vs Transactions
fig.add_trace(
    go.Scatter(x = df['total_sessions'], y = df['total_transactions'], mode = 'markers',
               marker = dict(size = df['user_count']/1000, color = df['path_length'], colorscale = 'Viridis'),
               text = df['conversion_path'], name = 'Sessions vs Transactions'),
    row = 2, col = 1
)

# 4. Pie Chart: Channel Distribution (First Touch)
channel_distribution = df.groupby(df['conversion_path'].str.split('>').str[0])['total_transactions'].sum()
fig.add_trace(
    go.Pie(labels = channel_distribution.index, values = channel_distribution.values, name = 'Channel Distribution'),
    row = 2, col = 2
)

# Update layout
fig.update_layout(height = 1000, width = 1200, title_text = "Conversion Path Analysis Dashboard")
fig.update_xaxes(title_text = "Conversion Path", row = 1, col = 1)
fig.update_xaxes(title_text = "Path Length", row = 1, col = 2)
fig.update_xaxes(title_text = "Total Sessions", row = 2, col = 1)
fig.update_yaxes(title_text = "Total Transactions", row = 1, col = 1)
fig.update_yaxes(title_text = "Conversion Rate", row = 1, col = 2)
fig.update_yaxes(title_text = "Total Transactions", row = 2, col = 1)

# Show the plot
fig.show()

# Save the plot as a high-rez image
fig.write_image("google_top_conversion_paths.png", scale = 5, width = 1920, height = 1080)