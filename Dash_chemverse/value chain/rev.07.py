# 신호등 로직 수정

# 각 제품의 마지막 배치에 해당되는 제품의 품질 특성을 기준으로
# 허용기준 내에 있으면 초록색,
# 허용기준의 2% 를 벗어나면 노란색,
# 허용기준을 벗어나면 빨간색

# 그리고, 노란색이나 빨간색일 경우
# 왜 그렇게 되는지 간단하게 설명

# 사용자가 최근 배치의 어떤 시험 항목 결과가 이러니까
# 빨간색이다 등

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
def determine_status(value, spec_min=None, spec_max=None):
    light_green = '#90EE90'  # 연한 초록색
    yellow = '#FFFF00'  # 노란색
    red = '#FF0000'  # 빨간색
   
    if spec_min is not None and spec_max is not None:
        if spec_min <= value <= spec_max:
            return light_green, ""
        elif spec_min * 0.98 <= value <= spec_max * 1.02:
            return yellow, f"{value} is within 2% of limits {spec_min} and {spec_max}."
        else:
            return red, f"{value} is out of limits {spec_min} and {spec_max}."
    elif spec_max is not None:
        if value <= spec_max:
            return light_green, ""
        elif value <= spec_max * 1.02:
            return yellow, f"{value} is within 2% of limit {spec_max}."
        else:
            return red, f"{value} is out of limit {spec_max}."
    elif spec_min is not None:
        if value >= spec_min:
            return light_green, ""
        elif value >= spec_min * 0.98:
            return yellow, f"{value} is within 2% of limit {spec_min}."
        else:
            return red, f"{value} is out of limit {spec_min}."
    return 'grey', "No data"

# 제품별 품질 특성 정의
product_specs = {
    "DP72": {"Assay": (98.0, 102.0), "Chiral": (None, None), "Total Impurity": (None, 2.0), "IMP-1": (None, 1.0), "AUI": (None, 0.1), "ROI": (None, 0.20)},
    "DP67": {"Total Impurity": (None, 2.0), "IMP-1": (None, 1.0), "AUI": (None, 0.1)},
    "DP57": {"Assay": (93.0, 102.0), "Chiral": (97.0, None), "Total Impurity": (None, 5.0)},
    "DP37": {"Assay": (None, None)},
    "DP58": {"Assay": (95.0, 102.0), "Chiral": (96.0, None)},
    "DP58onsan": {"Assay": (95.0, 102.0), "Chiral": (96.0, None)},
    "DP26": {"Assay": (None, None), "Impurity(Triester)": (None, 0.5)},
    "DP26onsan": {"Assay": (None, None), "Impurity(Triester)": (None, 0.5)},
    "Zemiglo": {"Assay": (None, None), "Total Impurity": (None, 2.0), "IMP-1": (None, 1.0), "AUI": (None, 0.1)},
    "Zemidapa": {"Assay": (None, None), "Total Impurity": (None, 2.0), "IMP-1": (None, 1.0), "AUI": (None, 0.1)},
    "Zemimet_50_500mg": {"Assay": (None, None), "Total Impurity": (None, 2.0), "IMP-1": (None, 1.0), "AUI": (None, 0.1)},
    "Zemimet_50_1000mg": {"Assay": (None, None), "Total Impurity": (None, 2.0), "IMP-1": (None, 1.0), "AUI": (None, 0.1)},
    "Zemimet_25_500mg": {"Assay": (None, None), "Total Impurity": (None, 2.0), "IMP-1": (None, 1.0), "AUI": (None, 0.1)},
    "Zemimet_25_1000mg": {"Assay": (None, None), "Total Impurity": (None, 2.0), "IMP-1": (None, 1.0), "AUI": (None, 0.1)},
    "Zemilow_50_5mg": {"Assay": (None, None), "Total Impurity": (None, 2.0), "IMP-1": (None, 1.0), "AUI": (None, 0.1)},
    "Zemilow_50_10mg": {"Assay": (None, None), "Total Impurity": (None, 2.0), "IMP-1": (None, 1.0), "AUI": (None, 0.1)},
    "Zemilow_50_20mg": {"Assay": (None, None), "Total Impurity": (None, 2.0), "IMP-1": (None, 1.0), "AUI": (None, 0.1)},
    "Zemimet_25_750mg": {"Assay": (None, None), "Total Impurity": (None, 2.0), "IMP-1": (None, 1.0), "AUI": (None, 0.1)}
}

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
    html.Div(id='criteria-output', style={'margin-top': '20px', 'white-space': 'pre-wrap'}),
    html.Div(id='status-output', style={'margin-top': '20px', 'white-space': 'pre-wrap'})
], style={'text-align': 'center'})

@app.callback(
    [Output('value-chain-graph', 'figure'),
     Output('raw-data', 'children'),
     Output('criteria-output', 'children'),
     Output('group-labels', 'children'),
     Output('status-output', 'children')],
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
        "빨강: 시험 규격을 벗어남 (허용기준의 2%를 벗어남)\n"
        "초록: 허용기준 내에 있음\n"
        "노랑: 허용기준의 2% 이내에서 벗어남\n"
    )

    node_x = []
    node_y = []
    node_text = []
    node_color = []
    raw_data_tables = []
    status_messages = []

    for node in nodes:
        dataset_name = f"{node['id']}_c"
        df = load_data(dataset_name)
        product_name = node['label']
        status_message = f"Product: {product_name}\n"

        if isinstance(df, str):
            node_color.append('grey')
            status_message += f"Error: {df}\n"
        else:
            product_spec = product_specs.get(product_name)
            if not product_spec:
                node_color.append('grey')
                status_message += "No specifications found.\n"
            else:
                latest_batch = df.iloc[-1]
                status_message += f"Batch: {latest_batch['batch_no']}\n"
                batch_statuses = []

                for spec_name, (spec_min, spec_max) in product_spec.items():
                    if spec_name in latest_batch:
                        value = latest_batch[spec_name]
                        color, reason = determine_status(value, spec_min, spec_max)
                        batch_statuses.append((spec_name, color, reason))

                if all(color == '#90EE90' for _, color, _ in batch_statuses):
                    node_color.append('#90EE90')
                elif any(color == '#FF0000' for _, color, _ in batch_statuses):
                    node_color.append('#FF0000')
                else:
                    node_color.append('#FFFF00')

                for spec_name, color, reason in batch_statuses:
                    if color != '#90EE90':
                        status_message += f"{spec_name}: {reason}\n"

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

        node_x.append(node['pos'][0])
        node_y.append(node['pos'][1])
        node_text.append(node['label'])
        status_messages.append(status_message)

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

    return fig, raw_data_tables, criteria_message, group_labels, "\n\n".join(status_messages)

@app.callback(
    Output('raw-data', 'style'),
    [Input('toggle-button', 'n_clicks')]
)
def toggle_raw_data(n_clicks):
    return {'display': 'block' if n_clicks % 2 == 1 else 'none'}

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#     app.run_server(debug=True)

