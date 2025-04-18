from dash import html, dcc, dash_table
import plotly.express as px
import pandas as pd
from dash import register_page
from dash import Dash
import dash
from data import df


register_page(
    __name__,
    path='/risk-analysis',
    name='风险分析',
    require_auth=True  # 需要登录
)

# Calculate risk metrics
risk_df = df.copy()
pivot_df = risk_df.pivot(index='日期', columns='股票', values='收益率')

# Rolling volatility
rolling_vol = pivot_df.rolling(window=3).std()

# Maximum drawdown calculation
def calculate_drawdown(returns):
    cumulative_returns = (1 + returns).cumprod()
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns / running_max) - 1
    return drawdown.min()

max_drawdowns = {stock: calculate_drawdown(pivot_df[stock].dropna()) 
                for stock in pivot_df.columns}

# Correlation matrix
correlation = pivot_df.corr()

layout = html.Div([
    html.H2('风险分析', className='page-title'),
    html.Div([
        html.Div([
            html.H3('波动率趋势'),
            dcc.Graph(
                figure=px.line(rolling_vol.reset_index().melt(id_vars='日期'), 
                         x='日期', y='value', color='股票',
                         title='3个月滚动波动率')
            )
        ], className='graph-container'),
        html.Div([
            html.H3('相关性分析'),
            dcc.Graph(
                figure=px.imshow(correlation, 
                            text_auto=True,
                            color_continuous_scale='RdBu_r',
                            title='股票收益率相关性矩阵')
            )
        ], className='graph-container'),
        html.Div([
            html.H3('最大回撤'),
            dash_table.DataTable(
                data=[{'股票': k, '最大回撤': f'{v:.2%}'} for k, v in max_drawdowns.items()],
                columns=[
                    {'name': '股票', 'id': '股票'},
                    {'name': '最大回撤', 'id': '最大回撤'}
                ],
                style_cell={'textAlign': 'center'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                page_size=10
            )
        ], className='table-container')
    ], className='page-content')
], className='page-layout')