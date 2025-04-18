from dash import html, dcc, dash_table, callback, Input, Output
import plotly.express as px
from dash import register_page
from dash.exceptions import PreventUpdate
from data import df,stats_df


register_page(
    __name__,
    path='/comparison',
    name='股票比较',
    require_auth=True  # 需要登录
)

layout = html.Div([
    html.H2('股票比较分析', className='page-title'),
    html.Div([
        html.Label('选择股票进行比较:', className='dropdown-label'),
        dcc.Dropdown(
            id='stocks-comparison-dropdown',
            options=[{'label': stock, 'value': stock} for stock in df['股票'].unique()],
            value=[df['股票'].iloc[0], df['股票'].iloc[1]],
            multi=True,
            className='dropdown'
        )
    ], className='control-row'),
    html.Div([
        dcc.Graph(id='returns-comparison'),
        dcc.Graph(id='price-comparison')
    ], className='graph-container'),
    html.Div([
        html.H3('性能比较表'),
        dash_table.DataTable(
            id='comparison-table',
            style_cell={'textAlign': 'center'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            page_size=10
        )
    ], className='table-container')
], className='page-layout')

@callback(
    Output('returns-comparison', 'figure'),
    Output('price-comparison', 'figure'),
    Output('comparison-table', 'data'),
    Output('comparison-table', 'columns'),
    Input('stocks-comparison-dropdown', 'value')
)
def update_comparison(selected_stocks):
    if not selected_stocks:
        raise PreventUpdate
        
    filtered_df = df[df['股票'].isin(selected_stocks)]
    
    returns_fig = px.line(filtered_df, x='日期', y='收益率', color='股票',
                   title='收益率比较')
    returns_fig.update_yaxes(tickformat='.0%')
    
    price_fig = px.line(filtered_df, x='日期', y='价格', color='股票',
                 title='价格走势比较')
    
    comparison_stats = stats_df[stats_df['股票'].isin(selected_stocks)]
    table_data = comparison_stats.to_dict('records')
    columns = [{"name": i, "id": i} for i in stats_df.columns]
    
    return returns_fig, price_fig, table_data, columns