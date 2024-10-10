import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio


df = pd.read_csv('bquxjob_51c0d03b_19272317b0a.csv')

# function to identify outliers
def is_outlier(s):
    lower_bound = s.mean() - (s.std() * 2)
    upper_bound = s.mean() + (s.std() * 2)
    return ~s.between(lower_bound, upper_bound)

# marking the outliers in the df
df['is_view_outlier'] = is_outlier(df['total_product_views'])
df['is_purchase_outlier'] = is_outlier(df['total_purchases'])
df['is_outlier'] = df['is_view_outlier'] | df['is_purchase_outlier']

# scatterplot's main figure (with outliers labeled)
fig = px.scatter(df, 
                 x = 'total_product_views', 
                 y = 'total_purchases',
                 size = 'total_add_to_cart',
                 hover_name = 'product_name',
                 hover_data = ['sessions', 'users'],
                 color = 'total_add_to_cart',
                 color_continuous_scale = 'Viridis',
                 labels = {
                     'total_product_views': 'Total Product Views',
                     'total_purchases': 'Total Purchases',
                     'total_add_to_cart': 'Total Add to Cart'
                 })

fig.update_layout(
    title = {
        'text': 'Product Performance: Views vs Purchases',
        'font': {'size': 24, 'color': 'black', 'family': 'Arial Black'}
    },
    xaxis_title = {
        'text': 'Total Product Views',
        'font': {'size': 18, 'color': 'black', 'family': 'Arial Black'}
    },
    yaxis_title = {
        'text': 'Total Purchases',
        'font': {'size': 18, 'color': 'black', 'family': 'Arial Black'}
    },
    coloraxis_colorbar_title = {
        'text': 'Add to Cart',
        'font': {'size': 16, 'color': 'black', 'family': 'Arial Black'}
    },
    font = dict(size = 14),
    plot_bgcolor = 'white',
    paper_bgcolor = 'white'
)

fig.update_xaxes(showgrid = True, gridwidth = 1, gridcolor = 'lightgrey', zeroline = True, zerolinewidth = 2, zerolinecolor = 'grey')
fig.update_yaxes(showgrid = True, gridwidth = 1, gridcolor = 'lightgrey', zeroline = True, zerolinewidth = 2, zerolinecolor = 'grey')

# annotations for outliers
for idx, row in df[df['is_outlier']].iterrows():
    fig.add_annotation(
        x = row['total_product_views'],
        y = row['total_purchases'],
        text = row['product_name'],
        showarrow = True,
        arrowhead = 2,
        arrowsize = 0.5,
        arrowwidth = 0.5,
        arrowcolor = "#636363",
        ax = 20,
        ay = -30,
        bgcolor = "white",
        opacity = 0.9,
        font = dict(size = 16, color = 'black', family = 'Arial Black')
    )

# plot the plot (hehe)
fig.show()

# save as an upscale for future review
fig.write_image("google_product_performance_shopping_behaviour.png", scale = 5, width = 1920, height = 1080)