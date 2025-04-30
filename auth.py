# auth.py
import hashlib
from functools import wraps
from dash import Dash, html, dcc, Input, Output, State, callback_context
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash
# 模拟用户数据库
users_db = {
    'admin': {
        'password': '5f4dcc3b5aa765d61d8327deb882cf99',  # md5('password')
        'role': 'admin'
    },
    'user1': {
        'password': '5f4dcc3b5aa765d61d8327deb882cf99',  # md5('password')
        'role': 'user'
    }
}

# 当前用户状态
current_user = {
    'is_authenticated': False,
    'username': None,
    'role': None
}

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def verify_user(username, password):
    if username in users_db:
        if users_db[username]['password'] == hash_password(password):
            return True
    return False

def login_required(roles=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user['is_authenticated']:
                return html.Div("请先登录", style={'textAlign': 'center', 'marginTop': '20%'})
            
            if roles and current_user['role'] not in roles:
                return html.Div("权限不足", style={'textAlign': 'center', 'marginTop': '20%'})
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

def create_login_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader("用户登录"),
            dbc.ModalBody([
                dbc.Input(id="login-username", placeholder="用户名", type="text"),
                dbc.Input(id="login-password", placeholder="密码", type="password", style={'marginTop': '10px'}),
                html.Div(id="login-message", style={'color': 'red', 'marginTop': '10px'})
            ]),
            dbc.ModalFooter([
                dbc.Button("登录", id="login-submit", color="primary"),
                dbc.Button("取消", id="login-cancel", color="secondary")
            ])
        ],
        id="login-modal",
        is_open=False
    )

def create_logout_button():
    return html.Div(
        dbc.Button("注销", id="logout-button", color="danger", outline=True),
        style={'position': 'absolute', 'right': '20px', 'top': '20px'}
    )

def create_auth_navbar():
    return html.Div(
        [
            # 用户信息显示区（始终存在）
            # html.Div(
            #     id="user-info",
            #     style={'position': 'absolute', 'right': '20px', 'top': '20px'}
            # ),
            
            # 登录按钮（始终存在，通过样式控制显示/隐藏）
            dbc.Button(
                "登录", 
                id="login-button", 
                color="primary", 
                outline=True,
                style={'display': 'none'} if current_user['is_authenticated'] else {}
            ),
            
            # 注销按钮（始终存在，通过样式控制显示/隐藏）
            dbc.Button(
                "注销",
                id="logout-button",
                color="danger",
                outline=True,
                style={'display': 'none'} if not current_user['is_authenticated'] else {}
            ),
            # dcc.Location(id='redirect-to-home', refresh=True)  # 新增重定向组件
        ],
        style={'position': 'absolute', 'right': '20px', 'top': '20px'}
    )
    
    
# # 在 auth.py 中添加新回调
# @app.callback(
#     Output("nav-links-container", "children"),  # 更新导航链接
#     Input("auth-state", "data")               # 监听登录状态变化
# )
# def update_nav_links(auth_state):
#     return generate_nav_links()  # 重新生成链接
# # 在auth.py中添加
def register_auth_callbacks(app):
    @app.callback(
        [Output("login-modal", "is_open"),
         Output("auth-state", "data"),
        #  Output("user-info", "children"),
         Output("login-message", "children"),
         Output("login-button", "style"),
         Output("logout-button", "style"),
         Output("redirect-to-home", "pathname")],  # 所有Output集中在这里
        [Input("login-button", "n_clicks"),
         Input("login-submit", "n_clicks"),
         Input("login-cancel", "n_clicks"),
         Input("logout-button", "n_clicks")
         ],
        [State("login-username", "value"),
         State("login-password", "value"),
         State("login-modal", "is_open"),
         State("auth-state", "data")]
    )
    def handle_auth(login_btn, submit_btn, cancel_btn, logout_btn,
                   username, password, is_open, auth_data):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == "login-button":
            # return True, dash.no_update, dash.no_update, "", dash.no_update, dash.no_update, None
            return True, dash.no_update, "", dash.no_update, dash.no_update, None
        elif button_id == "login-submit":
            if username and password and verify_user(username, password):
                current_user.update({
                    'is_authenticated': True,
                    'username': username,
                    'role': users_db[username]['role']
                })
               
                return (
                    False,  # 关闭模态框
                    current_user,  # 更新认证状态
                    # f"欢迎, {username}",  # 用户信息
                    "",  # 清空错误消息
                    {'display': 'none'},  # 隐藏登录按钮
                    {},  # 显示注销按钮
                    '/'  # 重定向到主页
                )
            return (
                True,  # 保持模态框打开
                dash.no_update, 
                # dash.no_update, 
                "用户名或密码错误", 
                dash.no_update, 
                dash.no_update, 
                None
            )
        
        elif button_id == "login-cancel":
            return (
                False, 
                dash.no_update, 
                # dash.no_update, 
                "", 
                dash.no_update, 
                dash.no_update, 
                None
            )
        
        elif button_id == "logout-button":
            current_user.update({
                'is_authenticated': False,
                'username': None,
                'role': None
            })
            return (
                False, 
                current_user, 
                # "", 
                "",
                {},  # 显示登录按钮
                {'display': 'none'},  # 隐藏注销按钮
                None
            )
        
        return (
            is_open, 
            dash.no_update, 
            # dash.no_update, 
            "", 
            dash.no_update, 
            dash.no_update, 
            None
        )