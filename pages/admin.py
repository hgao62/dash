# pages/admin.py
from dash import html, dash_table, register_page
from auth import login_required
from data import df

register_page(
    __name__,
    path='/admin',
    name='管理员面板',
    require_auth=True,
    roles=['admin']  # 需要管理员权限
)

@login_required(roles=['admin'])
def layout():
    return html.Div([
        html.H2('管理员面板', className='page-title'),
        html.H3('所有用户交易记录'),
        dash_table.DataTable(
            id='admin-table',
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict('records'),
            page_size=10,
            style_table={'overflowX': 'auto'}
        )
    ], className='page-layout')