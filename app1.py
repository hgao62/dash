import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

# 初始化应用
app = dash.Dash(__name__)

# 创建简单数据
df = pd.DataFrame({
    '日期': ['2023-01', '2023-02', '2023-03', '2023-04', '2023-05'],
    '股票A收益率': [3.5, 1.2, 5.7, -2.3, 4.1],
    '股票B收益率': [2.1, 3.5, 1.9, 3.2, -1.5]
})

# 创建图表
fig = px.line(df, x='日期', y=['股票A收益率', '股票B收益率'],
               title='股票收益率比较')

# 定义应用布局
app.layout = html.Div([
    html.H1('金融数据分析仪表盘'),
    html.Div('使用Dash构建的简单金融数据可视化'),
    dcc.Graph(figure=fig)
])

# 运行应用
if __name__ == '__main__':
    app.run()