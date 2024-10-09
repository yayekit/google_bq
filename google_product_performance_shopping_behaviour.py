import plotly.express as px
import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.io as pio

# Load the data
df = pd.read_csv('bquxjob_51c0d03b_19272317b0a.csv')

# Function to identify outliers
def is_outlier(s):
    lower_bound = s.mean() - (s.std() * 2)
    upper_bound = s.mean() + (s.std() * 2)
    return ~s.between(lower_bound, upper_bound)

# Identify outliers
df['is_view_outlier'] = is_outlier(df['total_product_views'])
df['is_purchase_outlier'] = is_outlier(df['total_purchases'])
df['is_outlier'] = df['is_view_outlier'] | df['is_purchase_outlier']

# Create the scatter plot
fig = px.scatter(df, 
                 x='total_product_views', 
                 y='total_purchases',
                 size='total_add_to_cart',
                 hover_name='product_name',
                 hover_data=['sessions', 'users'],
                 color='total_add_to_cart',
                 color_continuous_scale='Viridis',
                 title='Product Performance: Views vs Purchases',
                 labels={
                     'total_product_views': 'Total Product Views',
                     'total_purchases': 'Total Purchases',
                     'total_add_to_cart': 'Total Add to Cart'
                 })

# Update layout for better readability
fig.update_layout(
    xaxis_title='Total Product Views',
    yaxis_title='Total Purchases',
    coloraxis_colorbar_title='Add to Cart'
)

# Add annotations for outliers
for idx, row in df[df['is_outlier']].iterrows():
    fig.add_annotation(
        x=row['total_product_views'],
        y=row['total_purchases'],
        text=row['product_name'],
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=20,
        ay=-30,
        bgcolor="white",
        opacity=0.8
    )

# Show the plot
fig.show()

# Save as a high-resolution PNG image
fig.write_image("google_product_performance_shopping_behaviour.png", scale=5, width=1920, height=1080)