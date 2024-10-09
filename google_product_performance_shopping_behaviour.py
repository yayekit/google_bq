import plotly.express as px
import pandas as pd

# Assuming you've saved the CSV file as 'shopping_behavior.csv'
df = pd.read_csv('bquxjob_51c0d03b_19272317b0a.csv')

# Create the scatter plot
fig = px.scatter(df, 
                 x='total_product_views', 
                 y='total_purchases',
                 size='total_add_to_cart',  # Size of points represents add to cart actions
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

# Show the plot
fig.show()