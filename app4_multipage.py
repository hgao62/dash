# app.py
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from auth import create_auth_navbar, create_login_modal, current_user
import dash
from dash import Dash, html, dcc, Input, Output
app = Dash(__name__, 
           use_pages=True, 
           suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])


def generate_nav_links():
    links = []
    for page in dash.page_registry.values():
        # 检查页面是否可见（新增 visible_to 检查）
        visible = True
        if page.get('require_auth', False) and not current_user['is_authenticated']:
            visible = False
        if 'roles' in page and current_user.get('role') not in page['roles']:
            visible = False
            
        if visible:
            links.append(
                dcc.Link(
                    page['name'],
                    href=page["path"],
                    className='nav-link',
                    style={'display': 'none'} if page.get('require_auth') and not current_user.get('is_authenticated') else {}
                )
            )
    return links

app.layout = html.Div([
    # 认证控制组件（放在所有内容之前）
    dcc.Location(id='redirect-to-home', refresh=True),
    html.Div(id='auth-redirect-message', style={'display': 'none'}),
    # 认证导航栏
    create_auth_navbar(),
    
    # 登录模态框
    create_login_modal(),
    
    # 主标题和导航
    html.Div([
        html.H1('金融市场多页面分析仪表盘', className='app-title'),
        html.Div(id="nav-links-container", children=generate_nav_links(), className='nav-bar'),
        html.Hr()
    ], className='header',),
    
    # 页面内容
    dash.page_container,
    
    # 存储登录状态
    dcc.Store(id='auth-state', storage_type='session'),
    dcc.Store(id='requested-path', storage_type='session')  # 记录原始请求路径
])

# 在 auth.py 中添加新回调
@app.callback(
    Output("nav-links-container", "children"),  # 更新导航链接
    Input("auth-state", "data")               # 监听登录状态变化
)
def update_nav_links(auth_state):
    return generate_nav_links()  # 重新生成链接

# 添加认证相关回调
from auth import register_auth_callbacks
register_auth_callbacks(app)

if __name__ == '__main__':
    app.run(port=8053)