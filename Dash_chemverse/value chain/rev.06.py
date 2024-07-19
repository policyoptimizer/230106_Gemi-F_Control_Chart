# 우선 비슷하게 밸류 체인 그렸음
# 신호등 제대로 작동 안하고,
# 하단에 raw data 확인 잘 안됨

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
    {'id': 'DP14', 'label': 'DP14', 'pos': (1.5, 8), 'group': '온산, CMO'},
    {'id': 'DP58', 'label': 'DP58', 'pos': (1.5, 6), 'group': '온산, CMO'},
    {'id': 'DP26', 'label': 'DP26', 'pos': (1.5, 4), 'group': '온산, CMO'},
    {'id': 'DP37', 'label': 'DP37', 'pos': (4, 4), 'group': '온산'},
    {'id': 'DP18', 'label': 'DP18', 'pos': (5, 8), 'group': '온산'},
    {'id': 'DP57', 'label': 'DP57', 'pos': (5, 6), 'group': '온산'},
    {'id': 'DP60', 'label': 'DP60', 'pos': (6.5, 6), 'group': '온산, 익산'},
    {'id': 'DP67', 'label': 'DP67', 'pos': (7.5, 6), 'group': '온산, 익산'},
    {'id': 'DP72', 'label': 'DP72', 'pos': (8.5, 6), 'group': '온산, 익산'},
    {'id': 'Gemiglo', 'label': 'Gemiglo', 'pos': (10.5, 8), 'group': '오송'},
    {'id': 'Gemimet', 'label': 'Gemimet', 'pos': (10.5, 7), 'group': '오송'},
    {'id': 'Gemilow', 'label': 'Gemilow', 'pos': (10.5, 6), 'group': '오송'},
    {'id': 'Gemidapa', 'label': 'Gemidapa', 'pos': (10.5, 5), 'group': '오송'},
]

edges = [
    {'from': 'DP14', 'to': 'DP18'},
    {'from': 'DP26', 'to': 'DP37'},
    {'from': 'DP18', 'to': 'DP60'},
    {'from': 'DP37', 'to': 'DP57'},
    {'from': 'DP58', 'to': 'DP57'},
    {'from': 'DP57', 'to': 'DP60'},
    {'from': 'DP60', 'to': 'DP67'},
    {'from': 'DP67', 'to': 'DP72'},
    {'from': 'DP72', 'to': 'Gemiglo'},
    {'from': 'DP72', 'to': 'Gemimet'},
    {'from': 'DP72', 'to': 'Gemilow'},
    {'from': 'DP72', 'to': 'Gemidapa'}
]

# 그룹별 배경색 정의
group_colors = {
    '온산, CMO': 'rgba(173, 216, 230, 0.2)',  # lightblue
    '온산': 'rgba(144, 238, 144, 0.2)',  # lightgreen
    '온산, 익산': 'rgba(240, 128, 128, 0.2)',  # lightcoral
    '오송': 'rgba(250, 250, 210, 0.2)'   # lightgoldenrodyellow
}

# Dash 앱 인스턴스 생성
# app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('제품 품질 신호등: 우리 Gemi 푸르게 푸르게'),
    html.Div(id='group-labels', style={'text-align': 'center', 'margin-bottom': '20px', 'display': 'flex', 'justify-content': 'space-between'}),
    dcc.Graph(id='value-chain-graph', figure={}),
    html.Button('Show/Hide Raw Data', id='toggle-button', n_clicks=0),
    html.Div(id='raw-data', style={'display': 'none', 'margin-top': '20px'}),
    html.Div(id='criteria-output', style={'margin-top': '20px', 'white-space': 'pre-wrap'})
], style={'text-align': 'center'})

@app.callback(
    [Output('value-chain-graph', 'figure'),
     Output('raw-data', 'children'),
     Output('criteria-output', 'children'),
     Output('group-labels', 'children')],
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

    # 그룹별 배경색 추가
    for group, color in group_colors.items():
        group_nodes = [node for node in nodes if node['group'] == group]
        if group_nodes:
            x0 = min(node['pos'][0] for node in group_nodes) - 0.5
            x1 = max(node['pos'][0] for node in group_nodes) + 0.5
            y0 = min(node['pos'][1] for node in group_nodes) - 0.5
            y1 = max(node['pos'][1] for node in group_nodes) + 0.5
            fig.add_shape(
                type="rect",
                x0=x0,
                x1=x1,
                y0=y0,
                y1=y1,
                line=dict(width=0),
                fillcolor=color,
            )

    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='black'),
        hoverinfo='none',
        mode='lines'
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
        paper_bgcolor='white',  # 전체 배경색 제거
        plot_bgcolor='white',  # 전체 배경색 제거
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    group_labels = []
    for group, color in group_colors.items():
        group_labels.append(html.Span(group, style={'background-color': color, 'padding': '5px', 'margin': '5px', 'border-radius': '5px', 'flex': '1'}))

    return fig, raw_data_tables, criteria_message, group_labels

@app.callback(
    Output('raw-data', 'style'),
    [Input('toggle-button', 'n_clicks')]
)
def toggle_raw_data(n_clicks):
    return {'display': 'block' if n_clicks % 2 == 1 else 'none'}

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#     app.run_server(debug=True)

