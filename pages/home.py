from dash import html, dcc, dash_table
import plotly.express as px
from dash import register_page
from dash import Dash
import dash
from auth import login_required
# Access the shared app instance
from data import df, stats_df

# Register this page
register_page(
    __name__,
    path='/',
    name='市场概览',
    
    require_auth=True  # 需要登录
)



@login_required()
def layout():
    return html.Div([
    html.H2('市场概览', className='page-title'),
    html.Div([
        html.Div([
            dcc.Graph(
                figure=px.line(df, x='日期', y='价格', color='股票',
                         title='股票价格趋势')
            )
        ], className='graph-container'),
        html.Div([
            html.H3('市场统计数据'),
            dash_table.DataTable(
                id='market-stats-table',
                columns=[{"name": i, "id": i} for i in stats_df.columns],
                data=stats_df.to_dict('records'),
                style_cell={'textAlign': 'center'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                page_size=10
            )
        ], className='stats-container')
    ], className='page-content')
], className='page-layout')
# Page layout
