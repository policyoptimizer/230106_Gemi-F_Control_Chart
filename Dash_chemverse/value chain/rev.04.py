# value chain 을 좀 수정해주세요

# 우선 아래와 같이 4개로 그룹화를 해주세요

# 온산, CMO
# DP14
# DP58
# DP26 

# 온산
# DP37
# DP18
# DP57

# 온산, 익산
# DP60
# DP67
# DP72

# 오송
# Gemiglo
# Gemimet
# Gemilow
# Gemidapa

# 위 4개의 그룹을 하나의 밸류로 엮어주세요

# 그리고 품질 신호등에서
# DP14, DP18, DP60 은 별도로 없어요
# 외부에서 원료가 들어오는 거라서
# 품질 신호등으로 평가할 수가 없는데요
# 그냥 초록색으로 표기해주세요

# 마지막으로 선을 좀 수정 및 추가 해주세요

# 왼쪽에서 오른쪽으로 선으로 연결하는 것이 아니라
# 화살표로 연결해주시구요

# 현재 DP14, DP58, DP26 가 선으로 연결되어 있는데요
# 선을 해제해주세요
# DP14, DP58, DP26 는 독립된 제품이라서 연결될 필요 없습니다.

# DP14 에서 DP18 로 가는 화살표 추가
# DP18 에서 DP60 으로 가는 화살표 추가
# DP72 에서 Gemiglo, Gemimet, Gemilow, Gemidapa 로 가는 화살표 추가

# DP58 에서 DP57 로 연결될 때
# 그 중간에 DP37 이 가운데에 연결되기

import dataiku
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

# 데이터셋 로드 함수
def load_data(dataset_name):
    try:
        dataset = dataiku.Dataset(dataset_name)
        df = dataset.get_dataframe()
        return df
    except Exception as e:
        return str(e)

# 신호등 상태 결정 함수
def determine_status(value, spec_min=None, spec_max=None, info_only=False):
    light_green = '#90EE90'  # 연한 초록색
    if info_only:
        return '#ADD8E6'  # 연한 파란색 (Light Blue)
    if spec_min is not None and spec_max is not None:
        if spec_min <= value <= spec_max:
            return light_green
        elif value < spec_min * 0.9 or value > spec_max * 1.1:
            return 'red'
        else:
            return 'yellow'
    elif spec_max is not None:
        if value <= spec_max:
            return light_green
        elif value > spec_max * 1.1:
            return 'red'
        else:
            return 'yellow'
    elif spec_min is not None:
        if value >= spec_min:
            return light_green
        elif value < spec_min * 0.9:
            return 'red'
        else:
            return 'yellow'
    return 'grey'

# 노드와 엣지 정의
nodes = [
    {'id': 'DP14', 'label': 'DP14', 'pos': (1, 8)},
    {'id': 'DP58', 'label': 'DP58', 'pos': (1, 6)},
    {'id': 'DP26', 'label': 'DP26', 'pos': (1, 4)},
    {'id': 'DP37', 'label': 'DP37', 'pos': (2, 6)},
    {'id': 'DP18', 'label': 'DP18', 'pos': (3, 8)},
    {'id': 'DP57', 'label': 'DP57', 'pos': (3, 6)},
    {'id': 'DP60', 'label': 'DP60', 'pos': (5, 6)},
    {'id': 'DP67', 'label': 'DP67', 'pos': (7, 6)},
    {'id': 'DP72', 'label': 'DP72', 'pos': (9, 6)},
    {'id': 'Gemiglo', 'label': 'Gemiglo', 'pos': (11, 8)},
    {'id': 'Gemimet', 'label': 'Gemimet', 'pos': (11, 7)},
    {'id': 'Gemiro', 'label': 'Gemiro', 'pos': (11, 6)},
    {'id': 'Gemidapa', 'label': 'Gemidapa', 'pos': (11, 5)},
]

edges = [
    {'from': 'DP14', 'to': 'DP18'},
    {'from': 'DP18', 'to': 'DP60'},
    {'from': 'DP58', 'to': 'DP37'},
    {'from': 'DP37', 'to': 'DP57'},
    {'from': 'DP72', 'to': 'Gemiglo'},
    {'from': 'DP72', 'to': 'Gemimet'},
    {'from': 'DP72', 'to': 'Gemiro'},
    {'from': 'DP72', 'to': 'Gemidapa'}
]

# Dash 앱 인스턴스 생성
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('제품 품질 신호등: 우리 Gemi 푸르게 푸르게'),
    dcc.Graph(id='value-chain-graph'),
    html.Button('Show/Hide Raw Data', id='toggle-button', n_clicks=0),
    html.Div(id='raw-data', style={'display': 'none', 'margin-top': '20px'}),
    html.Div(id='criteria-output', style={'margin-top': '20px', 'white-space': 'pre-wrap'})
], style={'text-align': 'center'})

@app.callback(
    [Output('value-chain-graph', 'figure'),
     Output('raw-data', 'children'),
     Output('criteria-output', 'children')],
    [Input('toggle-button', 'n_clicks')]
)
def update_content(n_clicks):
    datasets = [
        "DP26_c", "DP26onsan", "DP37_c", "DP57_c", "DP58_c", "DP58onsan",
        "DP67_c", "DP72_c", "Zemiglo", "Zemidapa", "Zemimet_50_500mg",
        "Zemimet_50_1000mg", "Zemimet_25_500mg", "Zemimet_25_1000mg",
        "Zemilow_50_5mg", "Zemilow_50_10mg", "Zemilow_50_20mg", "Zemimet_25_750mg"
    ]

    criteria_message = (
        "신호등 기준:\n"
        "빨강: 시험 규격을 벗어남 (규격의 90% 이하 또는 110% 이상)\n"
        "초록: 정상\n"
        "노랑: 규격의 90% 이상 110% 미만\n"
        "파랑: 정보만 표시\n"
    )

    node_x = []
    node_y = []
    node_text = []
    node_color = []
    raw_data_tables = []

    for node in nodes:
        dataset_name = f"{node['id']}_c"
        df = load_data(dataset_name)
        product_name = node['label']

        if product_name in ['DP14', 'DP18', 'DP60']:
            node_color.append('#90EE90')  # 항상 초록색
        elif isinstance(df, str):
            node_color.append('grey')
        else:
            latest_batch = df.iloc[-1]
            insp_result_value = latest_batch['insp_result_value']
            insp_min_value = latest_batch['insp_min_value']
            insp_max_value = latest_batch['insp_max_value']
            status = determine_status(insp_result_value, insp_min_value, insp_max_value, False) if insp_result_value is not None else 'grey'
            node_color.append(status)

            raw_data_tables.append(html.Div([
                html.H3(product_name),
                dcc.Graph(
                    id=f'raw-data-{dataset_name}',
                    figure={
                        'data': [
                            {'x': df['batch_no'], 'y': df['insp_result_value'], 'type': 'bar', 'name': product_name}
                        ],
                        'layout': {
                            'title': product_name,
                            'xaxis': {'title': 'Batch No'},
                            'yaxis': {'title': 'Insp Result Value'}
                        }
                    }
                )
            ], style={'display': 'inline-block', 'width': '32%', 'padding': '10px'}))

    for node in nodes:
        node_x.append(node['pos'][0])
        node_y.append(node['pos'][1])
        node_text.append(node['label'])

    edge_x = []
    edge_y = []

    for edge in edges:
        from_node = next(node for node in nodes if node['id'] == edge['from'])
        to_node = next(node for node in nodes if node['id'] == edge['to'])
        edge_x.extend([from_node['pos'][0], to_node['pos'][0], None])
        edge_y.extend([from_node['pos'][1], to_node['pos'][1], None])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='black', dash='solid'),
        hoverinfo='none',
        mode='lines+markers',
        marker=dict(symbol='arrow-bar-up', size=12, angleref='previous', anglerefs='previous')
    ))

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(size=40, color=node_color, line=dict(width=2, color='black')),
        text=node_text,
        textposition='bottom center',
        hoverinfo='text'
    ))

    fig.update_layout(
        showlegend=False,
        margin=dict(l=40, r=40, b=40, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    return fig, raw_data_tables, criteria_message

@app.callback(
    Output('raw-data', 'style'),
    [Input('toggle-button', 'n_clicks')]
)
def toggle_raw_data(n_clicks):
    return {'display': 'block' if n_clicks % 2 == 1 else 'none'}

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#     app.run_server(debug=True)



