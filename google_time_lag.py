import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.io as pio

# Read the CSV data
df = pd.read_csv('bquxjob_777a5640_19272ca89e0.csv')

# Create figure with secondary y-axis
fig = make_subplots(specs = [[{"secondary_y": True}]])

# Add bar chart for conversions
fig.add_trace(
    go.Bar(x = df['time_lag_bucket'], y = df['conversions'], name = "Conversions"),
    secondary_y = False,
)

# Add line chart for percentage of total
fig.add_trace(
    go.Scatter(x = df['time_lag_bucket'], y = df['percentage_of_total'], name = "Percentage of Total"),
    secondary_y = True,
)

# Set x-axis title
fig.update_xaxes(title_text = "Time Lag (Days)")

# Set y-axes titles
fig.update_yaxes(title_text = "Number of Conversions", secondary_y = False)
fig.update_yaxes(title_text = "Percentage of Total Conversions", secondary_y = True)

# Set title
fig.update_layout(
    title_text = "Time Lag vs Conversions",
    legend = dict(orientation = "h", yanchor = "bottom", y = 1.02, xanchor = "right", x = 1)
)

# Show the plot
fig.show()

# Save the plot as a high-rez image
fig.write_image("google_time_lag.png", scale = 5, width = 1920, height = 1080)