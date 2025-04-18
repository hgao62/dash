import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

# 扩展数据集
df = pd.DataFrame({
    '日期': ['2023-01', '2023-02', '2023-03', '2023-04', '2023-05'] * 3,
    '股票': ['股票A'] * 5 + ['股票B'] * 5 + ['股票C'] * 5,
    '收益率': [3.5, 1.2, 5.7, -2.3, 4.1,  # 股票A
            2.1, 3.5, 1.9, 3.2, -1.5,   # 股票B
            1.5, -0.5, 3.2, 4.5, 2.1]   # 股票C
})

app.layout = html.Div([
    html.H1('交互式金融数据分析'),
    html.Div([
        html.Label('选择股票:'),
        dcc.Dropdown(
            id='stock-dropdown',
            options=[{'label': stock, 'value': stock} for stock in df['股票'].unique()],
            value=['股票A', '股票B'],  # 默认选择
            multi=True
        )
    ]),
    dcc.Graph(id='stock-graph')
])

@callback(
    Output('stock-graph', 'figure'),
    Input('stock-dropdown', 'value')
)
def update_graph(selected_stocks):
    filtered_df = df[df['股票'].isin(selected_stocks)]
    fig = px.line(filtered_df, x='日期', y='收益率', color='股票',
                  title='股票收益率分析')
    return fig

if __name__ == '__main__':
    app.run(port=8051)