import dash
from dash import html, dcc
import pandas as pd
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)


# App layout
app.layout = html.Div([
    html.Div([
        html.H1('金融市场多页面分析仪表盘', className='app-title'),
        html.Div([
            dcc.Link(
                f"{page['name']}", 
                href=page["path"],
                className='nav-link'
            ) for page in dash.page_registry.values()
        ], className='nav-bar'),
        html.Hr()
    ], className='header'),
    dash.page_container
])

if __name__ == '__main__':
    app.run(port=8053)