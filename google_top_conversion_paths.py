import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('bquxjob_6d7220c_19271ce2c4e.csv')

# conversion rate and path length
df['conversion_rate'] = df['total_transactions'] / df['total_sessions']
df['path_length'] = df['conversion_path'].str.count('>') + 1

df['first_touch'] = df['conversion_path'].str.split('>').str[0].str.strip()

# color map for the channels
color_map = {
    'Organic Search': '#1f77b4',
    'Referral': '#ff7f0e',
    'Direct': '#2ca02c',
    'Paid Search': '#d62728',
    'Social': '#9467bd',
    'Display': '#8c564b'
}

# subplot
fig = make_subplots(
    rows = 2, cols = 2,
    subplot_titles = ("Top 10 Conversion Paths", "Conversion Rate vs Path Length", 
                    "Sessions vs Transactions", "Channel Distribution"),
    specs = [[{"type": "bar"}, {"type": "scatter"}],
           [{"type": "scatter"}, {"type": "pie"}]]
)

### plots###
#1 Conversion chart
top_10 = df.nlargest(10, 'total_transactions')
fig.add_trace(
    go.Bar(x = top_10['conversion_path'], y = top_10['total_transactions'], name = 'Transactions',
           marker_color = [color_map.get(path.split('>')[0].strip(), '#636EFA') for path in top_10['conversion_path']]),
    row = 1, col = 1
)

#2 Conversion vs path length
fig.add_trace(
    go.Scatter(x = df['path_length'], y = df['conversion_rate'], mode = 'markers', 
               marker = dict(size = df['total_transactions']/10, 
                           color = [color_map.get(touch, '#636EFA') for touch in df['first_touch']]),
               text = df['conversion_path'], name = 'Conversion Rate'),
    row = 1, col = 2
)
fig.update_xaxes(title_text = "Path Length", range = [-1, 12], dtick = 2, row = 1, col = 2)
fig.update_yaxes(title_text = "Conversion Rate", range = [-0.02, 0.14], dtick = 0.02, row = 1, col = 2)

#3 sessions vs transactions
fig.add_trace(
    go.Scatter(x = df['total_sessions'], y = df['total_transactions'], mode = 'markers',
               marker = dict(size = df['user_count']/1000, 
                           color = [color_map.get(touch, '#636EFA') for touch in df['first_touch']]),
               text = df['conversion_path'], name = 'Sessions vs Transactions'),
    row = 2, col = 1
)

#4 channel conv. distr
channel_distribution = df.groupby('first_touch')['total_transactions'].sum()
fig.add_trace(
    go.Pie(labels = channel_distribution.index, values = channel_distribution.values, name = 'Channel Distribution',
           marker = dict(colors = [color_map.get(channel, '#636EFA') for channel in channel_distribution.index])),
    row = 2, col = 2
)

fig.update_layout(height = 1000, width = 1200)
fig.update_xaxes(title_text = "Conversion Path", row = 1, col = 1)
fig.update_xaxes(title_text = "Total Sessions", row = 2, col = 1)
fig.update_yaxes(title_text = "Total Transactions", row = 1, col = 1)
fig.update_yaxes(title_text = "Total Transactions", row = 2, col = 1)

fig.add_annotation(
    text = "Marker size represents user count",
    xref = "x domain", yref = "paper",
    x = 0.5, y = -0.25,  # Adjusted y position to be below the chart
    showarrow = False,
    row = 2, col = 1
)

fig.show()

# save the plot as a high-res image
fig.write_image("google_top_conversion_paths.png", scale = 5, width = 1920, height = 1080)