# DP26_Assay, DP37_Assay 는 Information Only 라서 초록이 될 수 없음

import dataiku
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd

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
    if spec_min is not None and spec_max is not None:
        if spec_min <= value <= spec_max:
            return 'green'
        elif value < spec_min or value > spec_max:
            return 'red'
        else:
            return 'yellow'
    elif spec_max is not None:
        if value <= spec_max:
            return 'green'
        elif value > spec_max:
            return 'red'
        else:
            return 'yellow'
    elif spec_min is not None:
        if value >= spec_min:
            return 'green'
        elif value < spec_min:
            return 'red'
        else:
            return 'yellow'
    return 'grey'

# Dash 앱 인스턴스 생성
# app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('제품 품질 신호등: 우리 Gemi 푸르게 푸르게'),
    html.Div(id='signals'),
    html.Button('데이터 로드 및 신호등 업데이트', id='update-button', n_clicks=0),
    html.Div(id='debug-output', style={'margin-top': '20px', 'white-space': 'pre-wrap'})
], style={'text-align': 'center'})

@app.callback(
    [Output('signals', 'children'),
     Output('debug-output', 'children')],
    [Input('update-button', 'n_clicks')]
)
def update_signals(n_clicks):
    if n_clicks > 0:
        datasets = {
            "DP26_Assay": (None, None),  # Assay는 Information Only
            "DP26_Triester": (None, 0.5),
            "DP37_Assay": (None, None),  # Assay는 Information Only
            "DP57_Assay": (93.0, 102.0),
            "DP57_Chiral": (97.0, None),
            "DP57_Total_Impurity": (None, 5.0),
            "DP58_Assay": (95.0, 102.0),
            "DP58_Chiral": (96.0, None),
            "DP67_AUI": (None, 0.1),
            "DP67_Total_Impurity": (None, 2.0),
            "DP72_Assay": (98.0, 102.0),
            "DP72_Chiral": (99.0, None),
            "DP72_AUI": (None, 0.1),
            "DP72_Total_Impurity": (None, 2.0),
            "DP72_ROI": (None, 0.20),
            "DP72_Impurity-1": (None, 1.0)
        }

        signals = []
        debug_message = ""

        for dataset_name, (spec_min, spec_max) in datasets.items():
            df = load_data(dataset_name)
            if isinstance(df, str):
                debug_message += f"Error loading {dataset_name}: {df}\n"
                signals.append(html.Div(id=f'signal-{dataset_name}', style={'width': '100px', 'height': '100px', 'background-color': 'grey'}, children=dataset_name))
            else:
                column_name = df.columns[-1]  # 마지막 컬럼 측정치
                latest_value = df.iloc[-1][column_name] if column_name in df.columns else None
                status = determine_status(latest_value, spec_min, spec_max) if latest_value is not None else 'grey'

                debug_message += f"{dataset_name} Columns: {df.columns.tolist()}\n{dataset_name} Head:\n{df.head()}\n"
                debug_message += f"Latest {dataset_name} Value: {latest_value}\n{dataset_name} Status: {status}\n\n"

                signals.append(html.Div(id=f'signal-{dataset_name}', style={'width': '100px', 'height': '100px', 'background-color': status}, children=dataset_name))
       
        return signals, debug_message
   
    return [], 'No data loaded'

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#     app.run_server(debug=True)

