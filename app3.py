import dash
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import numpy as np

app = dash.Dash(__name__)

# 创建模拟交易数据
dates = pd.date_range('2023-01-01', periods=5, freq='M')
stocks = ['股票A', '股票B', '股票C']
df = pd.DataFrame()

for stock in stocks:
    returns = np.random.normal(0.02, 0.05, size=len(dates))
    temp_df = pd.DataFrame({
        '日期': dates.strftime('%Y-%m'),
        '股票': stock,
        '收益率': returns,
        '交易量': np.random.randint(1000, 10000, size=len(dates))
    })
    df = pd.concat([df, temp_df])

# 计算统计数据
stats_df = df.groupby('股票').agg(
    平均收益率=('收益率', 'mean'),
    波动率=('收益率', 'std'),
    最大收益=('收益率', 'max'),
    最小收益=('收益率', 'min'),
    总交易量=('交易量', 'sum')
).reset_index()

# 美化数据
stats_df['平均收益率'] = stats_df['平均收益率'].map('{:.2%}'.format)
stats_df['波动率'] = stats_df['波动率'].map('{:.2%}'.format)
stats_df['最大收益'] = stats_df['最大收益'].map('{:.2%}'.format)
stats_df['最小收益'] = stats_df['最小收益'].map('{:.2%}'.format)

app.layout = html.Div([
    html.H1('金融市场分析仪表盘'),
    html.Div([
        html.Label('选择股票:'),
        dcc.Dropdown(
            id='stock-dropdown',
            options=[{'label': stock, 'value': stock} for stock in df['股票'].unique()],
            value=stocks[:2],
            multi=True
        )
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='stock-graph')
        ], style={'width': '70%', 'display': 'inline-block'}),
        html.Div([
            html.H3('股票统计数据'),
            dash_table.DataTable(
                id='stats-table',
                columns=[{"name": i, "id": i} for i in stats_df.columns],
                data=stats_df.to_dict('records'),
                style_cell={'textAlign': 'center'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top'})
    ]),
    html.Div([
        html.H3('历史交易数据'),
        dash_table.DataTable(
            id='trade-table',
            page_size=10,
            style_cell={'textAlign': 'center'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        )
    ])
])

@callback(
    Output('stock-graph', 'figure'),
    Output('trade-table', 'data'),
    Output('trade-table', 'columns'),
    Input('stock-dropdown', 'value')
)
def update_content(selected_stocks):
    # 更新图表
    filtered_df = df[df['股票'].isin(selected_stocks)]
    fig = px.line(filtered_df, x='日期', y='收益率', color='股票',
                  title='股票收益率趋势分析')
    
    # 更新交易表格
    display_df = filtered_df.copy()
    display_df['收益率'] = display_df['收益率'].map('{:.2%}'.format)
    table_data = display_df.to_dict('records')
    columns = [{"name": i, "id": i} for i in display_df.columns]
    
    return fig, table_data, columns

if __name__ == '__main__':
    app.run(port=8052)