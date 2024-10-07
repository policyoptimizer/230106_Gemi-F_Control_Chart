# 밸류 체인이 우측에만 절반 나옴

import dataiku
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table 

# 데이터셋 로드 함수
def load_data(dataset_name):
    try:
        dataset = dataiku.Dataset(dataset_name)
        df = dataset.get_dataframe()
        return df
    except Exception as e:
        return str(e)

# 신호등 상태 결정 함수
def determine_status(value, yellow_spec, red_spec):
    light_green = '#90EE90'  # 연한 초록색
    yellow = '#FFFF00'  # 노란색
    red = '#FF0000'  # 빨간색
   
    if red_spec[0] is not None and value < red_spec[0]:
        return red, f"{value} is below red limit {red_spec[0]}."
    if red_spec[1] is not None and value > red_spec[1]:
        return red, f"{value} is above red limit {red_spec[1]}."
   
    if yellow_spec[0] is not None and value < yellow_spec[0]:
        return yellow, f"{value} is below yellow limit {yellow_spec[0]}."
    if yellow_spec[1] is not None and value > yellow_spec[1]:
        return yellow, f"{value} is above yellow limit {yellow_spec[1]}."

    return light_green, ""

# 제품별 품질 특성 정의
red_specs = {
    "DP72": {"Assay": (98.0, 102.0), "Chiral": (99.0, None), "Total Impurity": (None, 2.0), "IMP-1": (None, 1.0), "AUI": (None, 0.1), "ROI": (None, 0.20)},
    "DP67": {"Total Impurity": (None, 2.0), "IMP-1": (None, 1.0), "AUI": (None, 0.1)},
    "DP57": {"Assay": (93.0, 102.0), "Chiral": (97.0, None), "Total Impurity": (None, 5.0)},
    "DP37": {"Assay": (None, None)},
    "DP58": {"Assay": (95.0, 102.0), "Chiral": (96.0, None)},
    "DP58onsan": {"Assay": (95.0, 102.0), "Chiral": (96.0, None)},
    "DP26": {"Assay": (None, None), "Impurity(Triester)": (None, 0.5)},
    "DP26onsan": {"Assay": (None, None), "Impurity(Triester)": (None, 0.5)},
    "Zemiglo": {"Assay": (95.0, 105.0), "Total Impurity": (None, 1.5), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemidapa": {"Assay": (95.0, 105.0), "Total Impurity": (None, 3.0), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemimet_50_500mg": {"Assay": (95.0, 105.0), "Total Impurity": (None, 3.0), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemimet_50_1000mg": {"Assay": (95.0, 105.0), "Total Impurity": (None, 3.0), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemimet_25_500mg": {"Assay": (95.0, 105.0), "Total Impurity": (None, 3.0), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemimet_25_1000mg": {"Assay": (95.0, 105.0), "Total Impurity": (None, 3.0), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemimet_25_750mg": {"Assay": (95.0, 105.0), "Total Impurity": (None, 3.0), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemilow_50_5mg": {"Assay": (95.0, 105.0), "Total Impurity": (None, 3.0), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemilow_50_10mg": {"Assay": (95.0, 105.0), "Total Impurity": (None, 3.0), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemilow_50_20mg": {"Assay": (95.0, 105.0), "Total Impurity": (None, 3.0), "IMP-1": (None, 2.0), "AUI": (None, 0.2)}
}

yellow_specs = {
    "DP72": {"Assay": (98.33, None), "Chiral": (99.09, None), "Total Impurity": (None, 0.87), "IMP-1": (None, 0.58), "AUI": (None, 0.08), "ROI": (None, 0.18)},
    "DP67": {"Total Impurity": (None, 1.18), "IMP-1": (None, 1.0), "AUI": (None, 0.11)},
    "DP57": {"Assay": (94.31, None), "Chiral": (97.58, None), "Total Impurity": (None, 3.57)},
    "DP37": {"Assay": (81.48, None)},
    "DP58": {"Assay": (95.55, None), "Chiral": (97.24, None)},
    "DP58onsan": {"Assay": (95.55, None), "Chiral": (97.24, None)},
    "DP26": {"Assay": (None, None), "Impurity(Triester)": (None, 0.5)},
    "DP26onsan": {"Assay": (None, None), "Impurity(Triester)": (None, 0.5)},
    "Zemiglo": {"Assay": (97.0, 103.0), "Total Impurity": (None, 3.0), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemidapa": {"Assay": (90.0, 110.0), "Total Impurity": (None, 3.0), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemimet_50_500mg": {"Assay": (97.0, 103.0), "Total Impurity": (None, 1.5), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemimet_50_1000mg": {"Assay": (97.0, 103.0), "Total Impurity": (None, 1.5), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemimet_25_500mg": {"Assay": (97.0, 103.0), "Total Impurity": (None, 1.5), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemimet_25_1000mg": {"Assay": (97.0, 103.0), "Total Impurity": (None, 1.5), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemimet_25_750mg": {"Assay": (97.0, 103.0), "Total Impurity": (None, 1.5), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemilow_50_5mg": {"Assay": (97.0, 103.0), "Total Impurity": (None, 1.5), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemilow_50_10mg": {"Assay": (97.0, 103.0), "Total Impurity": (None, 1.5), "IMP-1": (None, 2.0), "AUI": (None, 0.2)},
    "Zemilow_50_20mg": {"Assay": (97.0, 103.0), "Total Impurity": (None, 1.5), "IMP-1": (None, 2.0), "AUI": (None, 0.2)}
}

# 노드와 엣지 정의
nodes = [
    {'id': 'DP14', 'label': 'DP14', 'pos': (1.5, 8), 'group': '원료 (온산, CMO)', 'shape': 'square'},
    {'id': 'DP58', 'label': 'DP58', 'pos': (1.5, 6), 'group': '원료 (온산, CMO)'},
    {'id': 'DP26', 'label': 'DP26', 'pos': (1.5, 4), 'group': '원료 (온산, CMO)'},
    {'id': 'DP37', 'label': 'DP37', 'pos': (4, 4), 'group': '출발물질 (온산)'},
    {'id': 'DP18', 'label': 'DP18', 'pos': (5, 8), 'group': '출발물질 (온산)', 'shape': 'square'},
    {'id': 'DP57', 'label': 'DP57', 'pos': (5, 6), 'group': '출발물질 (온산)'},
    {'id': 'DP60', 'label': 'DP60', 'pos': (6.5, 6), 'group': '원료의약품 (온산, 익산)', 'shape': 'square'},
    {'id': 'DP67', 'label': 'DP67', 'pos': (7.5, 6), 'group': '원료의약품 (온산, 익산)'},
    {'id': 'DP72', 'label': 'DP72', 'pos': (8.5, 6), 'group': '원료의약품 (온산, 익산)'},
    {'id': 'Zemiglo', 'label': 'Zemiglo', 'pos': (10.5, 8), 'group': '완제의약품 (오송)'},
    {'id': 'Zemimet', 'label': 'Zemimet', 'pos': (10.5, 7), 'group': '완제의약품 (오송)'},
    {'id': 'Zemilow', 'label': 'Zemilow', 'pos': (10.5, 6), 'group': '완제의약품 (오송)'},
    {'id': 'Zemidapa', 'label': 'Zemidapa', 'pos': (10.5, 5), 'group': '완제의약품 (오송)'},
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
    {'from': 'DP72', 'to': 'Zemiglo'},
    {'from': 'DP72', 'to': 'Zemimet'},
    {'from': 'DP72', 'to': 'Zemilow'},
    {'from': 'DP72', 'to': 'Zemidapa'}
]

# 그룹별 배경색 정의
group_colors = {
    '원료 (온산, CMO)': 'rgba(0, 0, 255, 0.2)',  # 파랑
    '출발물질 (온산)': 'rgba(0, 255, 0, 0.2)',  # 초록
    '원료의약품 (온산, 익산)': 'rgba(255, 0, 0, 0.2)',  # 빨강
    '완제의약품 (오송)': 'rgba(255, 255, 0, 0.2)'   # 노랑
}

# 그룹별 정보 정의
group_info = {
    '원료 (온산, CMO)': {'stage_name': '원료', 'site_info': 'CMO/온산'},
    '출발물질 (온산)': {'stage_name': '출발물질', 'site_info': '온산'},
    '원료의약품 (온산, 익산)': {'stage_name': '원료의약품', 'site_info': '온산/익산'},
    '완제의약품 (오송)': {'stage_name': '완제의약품', 'site_info': '오송'}
}

# 그룹별 위치 정의
group_positions = {
    '원료 (온산, CMO)': {'x0': 0, 'x1': 2.75},
    '출발물질 (온산)': {'x0': 2.75, 'x1': 6.0},
    '원료의약품 (온산, 익산)': {'x0': 6.0, 'x1': 9.15},
    '완제의약품 (오송)': {'x0': 9.15, 'x1': 12.0}
}

# Dash 앱 인스턴스 생성
# app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('제미F 품질 현황판[CQA(Critical Quality Analysis)]'),
    html.Div(
        id='group-labels',
        style={
            'text-align': 'center',
            'margin-bottom': '20px',
            'display': 'flex',
            'justify-content': 'space-between'
        }
    ),
    html.Div([
        dcc.Graph(id='value-chain-graph', figure={}),
        html.Div(
            id='criteria-output',
            style={
                'text-align': 'left',
                'font-size': '12px',
                'white-space': 'pre-wrap',
                'margin-left': 'auto',
                'margin-top': '10px'
            }
        )
    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-end'}),
    html.Button('Show/Hide Raw Data', id='toggle-button', n_clicks=0),
    html.Div(id='raw-data', style={'display': 'none', 'margin-top': '20px'}),
    html.Div(
        id='status-output',
        style={
            'margin-top': '20px',
            'text-align': 'left',
            'padding': '10px'
        }
    )
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
        "초록: 허용기준 내에 있음\n"
        "노랑: 허용기준의 2% 이내에 근접함\n"
        "빨강: 허용기준을 벗어남\n"
    )

    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_shapes = []
    raw_data_tables = []
    status_messages = []
    table_rows = []  # 추가된 부분

    for node in nodes:
        product_name = node['label']
        batch_no = None  # 추가된 부분

        if node.get('shape') == 'square':
            node_shapes.append('square')
            node_color.append('white')
            node_x.append(node['pos'][0])
            node_y.append(node['pos'][1])
            node_text.append(node['label'])
            continue
        else:
            node_shapes.append('circle')

        dataset_name = product_name if product_name in ["Zemiglo", "Zemidapa"] else f"{node['id']}_c"
        df = load_data(dataset_name)

        status_message = f"Product: {product_name}\n"

        if product_name == 'Zemimet':
            sub_products = [
                "Zemimet_50_500mg", "Zemimet_50_1000mg", "Zemimet_25_500mg",
                "Zemimet_25_1000mg", "Zemimet_25_750mg"
            ]
            sub_colors = []
            for sub_product in sub_products:
                sub_df = load_data(sub_product)
                if isinstance(sub_df, str):
                    sub_colors.append('grey')
                else:
                    latest_batch = sub_df.iloc[-1]
                    batch_no = latest_batch.get('batch_no')  # 추가된 부분
                    for spec_name, (yellow_spec, red_spec) in zip(yellow_specs[sub_product].items(), red_specs[sub_product].items()):
                        if spec_name in latest_batch:
                            value = latest_batch[spec_name]
                            color, reason = determine_status(value, yellow_spec, red_spec)
                            if color != '#90EE90':
                                sub_colors.append(color)
            if '#FF0000' in sub_colors:
                node_color.append('#FF0000')
            elif '#FFFF00' in sub_colors:
                node_color.append('#FFFF00')
            else:
                node_color.append('#90EE90')
        elif product_name == 'Zemilow':
            sub_products = [
                "Zemilow_50_5mg", "Zemilow_50_10mg", "Zemilow_50_20mg"
            ]
            sub_colors = []
            for sub_product in sub_products:
                sub_df = load_data(sub_product)
                if isinstance(sub_df, str):
                    sub_colors.append('grey')
                else:
                    latest_batch = sub_df.iloc[-1]
                    batch_no = latest_batch.get('batch_no')  # 추가된 부분
                    for spec_name, (yellow_spec, red_spec) in zip(yellow_specs[sub_product].items(), red_specs[sub_product].items()):
                        if spec_name in latest_batch:
                            value = latest_batch[spec_name]
                            color, reason = determine_status(value, yellow_spec, red_spec)
                            if color != '#90EE90':
                                sub_colors.append(color)
            if '#FF0000' in sub_colors:
                node_color.append('#FF0000')
            elif '#FFFF00' in sub_colors:
                node_color.append('#FFFF00')
            else:
                node_color.append('#90EE90')
        elif isinstance(df, str):
            node_color.append('grey')
            status_message += f"Error: {df}\n"
        else:
            product_spec = red_specs.get(product_name)
            if not product_spec:
                node_color.append('grey')
                status_message += "No specifications found.\n"
            else:
                latest_batch = df.iloc[-1]
                batch_no = latest_batch.get('batch_no')  # 추가된 부분
                status_message += f"Batch: {batch_no}\n"
                batch_statuses = []

                for spec_name in product_spec:
                    yellow_spec = yellow_specs.get(product_name, {}).get(spec_name, (None, None))
                    red_spec = red_specs.get(product_name, {}).get(spec_name, (None, None))
                    if spec_name in latest_batch:
                        value = latest_batch[spec_name]
                        color, reason = determine_status(value, yellow_spec, red_spec)
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
            ], style={'display': 'inline-block', 'width': '24%', 'padding': '10px'}))

        node_x.append(node['pos'][0])
        node_y.append(node['pos'][1])
        node_text.append(node['label'])
        status_messages.append(status_message)

        # 테이블에 행 추가
        table_rows.append({'Product': product_name, 'Batch': batch_no if batch_no else ''})

    # 테이블 행을 사용하여 상태 아이템 생성
    status_items = []

    for row in table_rows:
        product_name = row['Product']
        batch_no = row['Batch']
        status_items.append(
            html.Div(
                [
                    html.Div(product_name, style={'font-weight': 'bold'}),
                    html.Div(batch_no)
                ],
                style={
                    'width': '25%',  # 4개의 칼럼으로 배치
                    'padding': '10px',
                    'box-sizing': 'border-box'
                }
            )
        )
    
    status_output_div = html.Div(
        children=status_items,
        style={
            'display': 'flex',
            'flex-wrap': 'wrap',
            'justify-content': 'flex-start',
            'padding': '10px'
        }
    )               
    
    edge_x = []
    edge_y = []

    for edge in edges:
        from_node = next(node for node in nodes if node['id'] == edge['from'])
        to_node = next(node for node in nodes if node['id'] == edge['to'])
        edge_x.extend([from_node['pos'][0], to_node['pos'][0], None])
        edge_y.extend([from_node['pos'][1], to_node['pos'][1], None])

    # 그룹 레이블 생성
    group_labels = []
    for group in group_colors.keys():
        info = group_info[group]
        group_labels.append(
            html.Div([
                html.Span(info['stage_name'], style={'font-size': '24px', 'font-weight': 'bold'}),
                html.Br(),
                html.Span(info['site_info']),
            ], style={'background-color': group_colors[group], 'padding': '10px', 'margin': '5px', 'border-radius': '5px', 'flex': '1', 'text-align': 'center'})
        )     
        
    fig = go.Figure()

    # 그룹별 배경색 추가
    for group in group_colors.keys():
        color = group_colors[group]
        positions = group_positions[group]
        x0 = positions['x0']
        x1 = positions['x1']
        y0 = min(node['pos'][1] for node in nodes) - 0.5
        y1 = max(node['pos'][1] for node in nodes) + 0.5
        fig.add_shape(
            type="rect",
            x0=x0,
            x1=x1,
            y0=y0,
            y1=y1,
            line=dict(width=0),
            fillcolor=color,
            layer='below'
        )

    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='black'),
        hoverinfo='none',
        mode='lines'
    ))

    for i in range(len(node_x)):
        if node_shapes[i] == 'square':
            fig.add_trace(go.Scatter(
                x=[node_x[i]], y=[node_y[i]],
                mode='markers+text',
                marker=dict(size=40, symbol='square', color=node_color[i], line=dict(width=2, color='black')),
                text=[node_text[i]],
                textposition='bottom center',
                hoverinfo='text'
            ))
        else:
            fig.add_trace(go.Scatter(
                x=[node_x[i]], y=[node_y[i]],
                mode='markers+text',
                marker=dict(size=40, color=node_color[i], line=dict(width=2, color='black')),
                text=[node_text[i]],
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

    # 상태 메시지를 표로 변환
    status_table = dash_table.DataTable(
        data=table_rows,
        columns=[{'name': 'Product', 'id': 'Product'}, {'name': 'Batch', 'id': 'Batch'}],
        style_cell={'textAlign': 'center'},
        style_header={'fontWeight': 'bold'},
        style_table={'margin': 'auto', 'width': '50%'}
    )
    
    return fig, raw_data_tables, criteria_message, group_labels, status_output_div

@app.callback(
    Output('raw-data', 'style'),
    [Input('toggle-button', 'n_clicks')]
)
def toggle_raw_data(n_clicks):
    return {'display': 'block' if n_clicks % 2 == 1 else 'none'}

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#     app.run_server(debug=True)

