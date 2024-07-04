import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# app = dash.Dash(__name__)

# 예시 제품 데이터
products = [
    {'name': 'DP67', 'status': 'green', 'spec': 'AUI: 0.1% 이하, Total Impurity: 2.0% 이하'},
    {'name': 'DP72', 'status': 'red', 'spec': 'Assay: 98.0~102.0%, Chiral: 99.0%ee 이상, AUI: 0.1% 이하, Total Impurity: 2.0% 이하, ROI: 0.20% 이하, Impurity-1: 1.0% 이하'},
    # 추가 제품 예시
    {'name': 'Product3', 'status': 'yellow', 'spec': 'Spec details...'},
    {'name': 'Product4', 'status': 'green', 'spec': 'Spec details...'},
    {'name': 'Product5', 'status': 'red', 'spec': 'Spec details...'},
    {'name': 'Product6', 'status': 'green', 'spec': 'Spec details...'},
    {'name': 'Product7', 'status': 'yellow', 'spec': 'Spec details...'},
    {'name': 'Product8', 'status': 'green', 'spec': 'Spec details...'},
    {'name': 'Product9', 'status': 'red', 'spec': 'Spec details...'},
    {'name': 'Product10', 'status': 'green', 'spec': 'Spec details...'}
]

def create_product_section(product):
    return html.Div([
        html.H3(product['name']),
        html.Div(style={'background-color': product['status'], 'width': '20px', 'height': '20px', 'border-radius': '50%', 'display': 'inline-block', 'margin-right': '10px'}),
        html.Span(product['spec']),
        html.Br(),
        dcc.Link('상세보기', href=f'/{product["name"]}')
    ], style={'margin-bottom': '20px', 'padding': '10px', 'border': '1px solid #ddd', 'border-radius': '5px'})

app.layout = html.Div([
    html.H1('제품 상태 개요'),
    html.P('각 제품의 현재 상태를 나타냅니다.'),
    html.Div([create_product_section(product) for product in products]),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# 각 제품의 상세 페이지 콜백
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/DP67':
        # DP67 상세 페이지 내용
        return html.Div([
            html.H2('DP67 상세 정보'),
            dcc.Graph(
                figure=go.Figure(
                    data=[go.Scatter(x=np.arange(10), y=np.random.random(10))]
                )
            ),
            dcc.Link('뒤로가기', href='/')
        ])
    elif pathname == '/DP72':
        # DP72 상세 페이지 내용
        return html.Div([
            html.H2('DP72 상세 정보'),
            dcc.Graph(
                figure=go.Figure(
                    data=[go.Scatter(x=np.arange(10), y=np.random.random(10))]
                )
            ),
            dcc.Link('뒤로가기', href='/')
        ])
    else:
        return html.Div([
            html.H2('제품을 선택해주세요.')
        ])

if __name__ == '__main__':
    app.run_server(debug=True)

