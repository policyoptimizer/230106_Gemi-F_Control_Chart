# value chain 추가

import dataiku
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
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

# Dash 앱 인스턴스 생성
# app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('품질 신호등: 우리 Gemi 푸르게 푸르게'),
    html.Div(id='value-chain', style={'display': 'flex', 'justify-content': 'center'}),
    html.Button('데이터 로드 및 신호등 업데이트', id='update-button', n_clicks=0),
    html.Div(id='criteria-output', style={'position': 'absolute', 'bottom': '20px', 'right': '20px', 'text-align': 'left', 'white-space': 'pre-wrap'}),
    html.Div(id='debug-output', style={'margin-top': '20px', 'white-space': 'pre-wrap'})
], style={'text-align': 'center', 'position': 'relative'})

@app.callback(
    [Output('value-chain', 'children'),
     Output('debug-output', 'children'),
     Output('criteria-output', 'children')],
    [Input('update-button', 'n_clicks')]
)
def update_signals(n_clicks):
    if n_clicks > 0:
        datasets = {
            "DP26_Assay": (None, None, True),  # Assay는 Information Only
            "DP26_Triester": (None, 0.5, False),
            "DP37_Assay": (None, None, True),  # Assay는 Information Only
            "DP57_Assay": (93.0, 102.0, False),
            "DP57_Chiral": (97.0, None, False),
            "DP57_Total_Impurity": (None, 5.0, False),
            "DP58_Assay": (95.0, 102.0, False),
            "DP58_Chiral": (96.0, None, False),
            "DP67_AUI": (None, 0.1, False),
            "DP67_Total_Impurity": (None, 2.0, False),
            "DP72_Assay": (98.0, 102.0, False),
            "DP72_Chiral": (99.0, None, False),
            "DP72_AUI": (None, 0.1, False),
            "DP72_Total_Impurity": (None, 2.0, False),
            "DP72_ROI": (None, 0.20, False),
            "DP72_Impurity-1": (None, 1.0, False)
        }

        signals = {}
        debug_message = ""
        criteria_message = (
            "신호등 기준:\n"
            "빨강: 시험 규격을 벗어남 (규격의 90% 이하 또는 110% 이상)\n"
            "초록: 정상\n"
            "노랑: 규격의 90% 이상 110% 미만\n"
            "파랑: 정보만 표시\n"
        )

        for dataset_name, (spec_min, spec_max, info_only) in datasets.items():
            df = load_data(dataset_name)
            if isinstance(df, str):
                debug_message += f"Error loading {dataset_name}: {df}\n"
                signals[dataset_name] = 'grey'
            else:
                column_name = df.columns[-1]  # 마지막 컬럼 측정치
                latest_value = df.iloc[-1][column_name] if column_name in df.columns else None
                status = determine_status(latest_value, spec_min, spec_max, info_only) if latest_value is not None else 'grey'

                debug_message += f"{dataset_name} Columns: {df.columns.tolist()}\n{dataset_name} Head:\n{df.head()}\n"
                debug_message += f"Latest {dataset_name} Value: {latest_value}\n{dataset_name} Status: {status}\n\n"

                signals[dataset_name] = status
       
        # Create value chain figure
        fig = create_value_chain(signals)

        return dcc.Graph(figure=fig), debug_message, criteria_message
   
    return [], 'No data loaded', '신호등 기준:\n빨강: 시험 규격을 벗어남 (규격의 90% 이하 또는 110% 이상)\n초록: 정상\n노랑: 규격의 90% 이상 110% 미만\n파랑: Information Only\n'

def create_value_chain(signals):
    fig = go.Figure()

    nodes = [
        {'id': 'DP14', 'label': 'DP14', 'pos': (1, 8)},
        {'id': 'DP26', 'label': 'DP26', 'pos': (1, 6)},
        {'id': 'DP37', 'label': 'DP37', 'pos': (2, 6)},
        {'id': 'DP58', 'label': 'DP58', 'pos': (1, 7)},
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

    nodes_dict = {node['id']: node for node in nodes}

    for node in nodes:
        color = signals.get(node['id'], 'lightgrey')
        fig.add_trace(go.Scatter(
            x=[node['pos'][0]],
            y=[node['pos'][1]],
            mode='markers+text',
            marker=dict(size=50, color=color, symbol='square'),
            text=node['label'],
            textposition="bottom center",
            name=node['label']
        ))

    edges = [
        ('DP14', 'DP18'),
        ('DP18', 'DP60'),
        ('DP26', 'DP37'),
        ('DP37', 'DP57'),
        ('DP58', 'DP57'),
        ('DP57', 'DP60'),
        ('DP60', 'DP67'),
        ('DP67', 'DP72'),
        ('DP72', 'Gemiglo'),
        ('DP72', 'Gemimet'),
        ('DP72', 'Gemiro'),
        ('DP72', 'Gemidapa')
    ]

    for edge in edges:
        fig.add_trace(go.Scatter(
            x=[nodes_dict[edge[0]]['pos'][0], nodes_dict[edge[1]]['pos'][0]],
            y=[nodes_dict[edge[0]]['pos'][1], nodes_dict[edge[1]]['pos'][1]],
            mode='lines',
            line=dict(color='black', width=2),
            name=f'{edge[0]}-{edge[1]}'
        ))

    fig.update_layout(
        title='제미F Value Chain',
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, range=[0, 12]),
        yaxis=dict(showgrid=False, zeroline=False, range=[0, 9]),
        width=1600,
        height=800
    )

    return fig

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#     app.run_server(debug=True)

