import dash
from dash import html, dcc, dash_table, callback, Input, Output
import plotly.express as px
from dash import register_page
from dash.exceptions import PreventUpdate
from dash import Dash
from data import df, stats_df
# Access the shared app instance
app = dash.get_app()

register_page(
    __name__,
    path='/stock-analysis',
    name='个股分析'
)

layout = html.Div([
    html.H2('个股详细分析', className='page-title'),
    html.Div([
        html.Label('选择股票:', className='dropdown-label'),
        dcc.Dropdown(
            id='stock-dropdown',
            options=[{'label': stock, 'value': stock} for stock in df['股票'].unique()],
            value=df['股票'].iloc[0],
            clearable=False,
            className='dropdown'
        )
    ], className='control-row'),
    html.Div([
        html.Div([
            dcc.Graph(id='price-graph'),
            dcc.Graph(id='volume-graph')
        ], className='graph-column'),
        html.Div([
            html.H3('股票统计数据'),
            html.Div(id='stock-stats', className='stats-display'),
            html.H4('月度表现'),
            dash_table.DataTable(
                id='monthly-table',
                style_cell={'textAlign': 'center'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                page_size=10
            )
        ], className='stats-column')
    ], className='page-content')
], className='page-layout')

@callback(
    Output('price-graph', 'figure'),
    Output('volume-graph', 'figure'),
    Output('stock-stats', 'children'),
    Output('monthly-table', 'data'),
    Output('monthly-table', 'columns'),
    Input('stock-dropdown', 'value')
)
def update_stock_analysis(selected_stock):
    if not selected_stock:
        raise PreventUpdate
        
    filtered_df = df[df['股票'] == selected_stock]
    
    price_fig = px.line(filtered_df, x='日期', y='价格',
                        title=f'{selected_stock}价格走势')
    
    volume_fig = px.bar(filtered_df, x='日期', y='交易量',
                      title=f'{selected_stock}交易量')
    
    stock_stats = stats_df[stats_df['股票'] == selected_stock].iloc[0]
    stats_div = html.Div([
        html.P(f"平均收益率: {stock_stats['平均收益率']}"),
        html.P(f"波动率: {stock_stats['波动率']}"),
        html.P(f"最大收益: {stock_stats['最大收益']}"),
        html.P(f"最小收益: {stock_stats['最小收益']}"),
        html.P(f"总交易量: {stock_stats['总交易量']}"),
        html.P(f"平均价格: {stock_stats['平均价格']}")
    ])
    
    monthly_df = filtered_df.copy()
    monthly_df['收益率'] = monthly_df['收益率'].map('{:.2%}'.format)
    monthly_df['价格'] = monthly_df['价格'].map('{:.2f}'.format)
    table_data = monthly_df[['日期', '收益率', '交易量', '价格']].to_dict('records')
    columns = [{"name": i, "id": i} for i in ['日期', '收益率', '交易量', '价格']]
    
    return price_fig, volume_fig, stats_div, table_data, columns