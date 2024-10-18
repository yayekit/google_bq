import os
import pandas as pd
import plotly.express as px
import plotly.io as pio

def main():
    csv_file = 'bquxjob_51c0d03b_19272317b0a.csv'
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"File '{csv_file}' not found.")
    df = pd.read_csv(csv_file)
    required_columns = [
        'total_product_views', 'total_purchases', 'total_add_to_cart',
        'product_name', 'sessions', 'users'
    ]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in data: {', '.join(missing_cols)}")
    df = identify_outliers(df)
    fig = create_scatter_plot(df)
    fig.show()
    fig.write_image(
        "google_product_performance_shopping_behaviour.png",
        scale=5,
        width=1920,
        height=1080
    )

def identify_outliers(df):
    def is_outlier(s):
        return ~s.between(s.mean() - 2 * s.std(), s.mean() + 2 * s.std())
    df['is_view_outlier'] = is_outlier(df['total_product_views'])
    df['is_purchase_outlier'] = is_outlier(df['total_purchases'])
    df['is_outlier'] = df['is_view_outlier'] | df['is_purchase_outlier']
    return df

def create_scatter_plot(df):
    colors = {
        'text': 'black',
        'background': 'white',
        'grid': 'lightgrey',
        'zero_line': 'grey',
        'arrow': '#636363'
    }
    fonts = {
        'title': {'size': 24, 'color': colors['text'], 'family': 'Arial Black'},
        'axis_title': {'size': 18, 'color': colors['text'], 'family': 'Arial Black'},
        'colorbar_title': {'size': 16, 'color': colors['text'], 'family': 'Arial Black'},
        'annotation': {'size': 16, 'color': colors['text'], 'family': 'Arial Black'},
        'tick': {'size': 14, 'color': colors['text'], 'family': 'Arial'}
    }
    fig = px.scatter(
        df,
        x='total_product_views',
        y='total_purchases',
        size='total_add_to_cart',
        hover_name='product_name',
        hover_data=['sessions', 'users'],
        color='total_add_to_cart',
        color_continuous_scale='Viridis',
        labels={
            'total_product_views': 'Total Product Views',
            'total_purchases': 'Total Purchases',
            'total_add_to_cart': 'Total Add to Cart'
        }
    )
    fig.update_layout(
        title={'text': 'Product Performance: Views vs Purchases', 'font': fonts['title']},
        xaxis_title={'text': 'Total Product Views', 'font': fonts['axis_title']},
        yaxis_title={'text': 'Total Purchases', 'font': fonts['axis_title']},
        coloraxis_colorbar_title={'text': 'Add to Cart', 'font': fonts['colorbar_title']},
        font=fonts['tick'],
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background']
    )
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=colors['grid'],
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor=colors['zero_line']
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=colors['grid'],
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor=colors['zero_line']
    )
    for _, row in df[df['is_outlier']].iterrows():
        fig.add_annotation(
            x=row['total_product_views'],
            y=row['total_purchases'],
            text=row['product_name'],
            showarrow=True,
            arrowhead=2,
            arrowsize=0.5,
            arrowwidth=0.5,
            arrowcolor=colors['arrow'],
            ax=20,
            ay=-30,
            bgcolor=colors['background'],
            opacity=0.9,
            font=fonts['annotation']
        )
    return fig

if __name__ == '__main__':
    main()
