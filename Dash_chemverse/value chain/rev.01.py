import dataiku
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
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
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('제품 품질 신호등: 우리 Gemi 푸르게 푸르게'),
    html.Div(id='signals', style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'}),
    html.Button('데이터 로드 및 신호등 업데이트', id='update-button', n_clicks=0),
    html.Div(id='criteria-output', style={'margin-top': '20px', 'white-space': 'pre-wrap'}),
    html.Div(id='debug-output', style={'margin-top': '20px', 'white-space': 'pre-wrap'})
], style={'text-align': 'center'})

@app.callback(
    [Output('signals', 'children'),
     Output('debug-output', 'children'),
     Output('criteria-output', 'children')],
    [Input('update-button', 'n_clicks')]
)
def update_signals(n_clicks):
    if n_clicks > 0:
        datasets = [
            "DP26_c", "DP26onsan", "DP37_c", "DP57_c", "DP58_c", "DP58onsan",
            "DP67_c", "DP72_c", "Zemiglo", "Zemidapa", "Zemimet_50_500mg",
            "Zemimet_50_1000mg", "Zemimet_25_500mg", "Zemimet_25_1000mg",
            "Zemilow_50_5mg", "Zemilow_50_10mg", "Zemilow_50_20mg", "Zemimet_25_750mg"
        ]

        signals = []
        debug_message = ""
        criteria_message = (
            "신호등 기준:\n"
            "빨강: 시험 규격을 벗어남 (규격의 90% 이하 또는 110% 이상)\n"
            "초록: 정상\n"
            "노랑: 규격의 90% 이상 110% 미만\n"
            "파랑: 정보만 표시\n"
        )

        for dataset_name in datasets:
            df = load_data(dataset_name)
            if isinstance(df, str):
                debug_message += f"Error loading {dataset_name}: {df}\n"
                signals.append(html.Div(id=f'signal-{dataset_name}', style={
                    'width': '100px', 'height': '100px', 'background-color': 'grey',
                    'border-radius': '15px', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin': '10px'
                }, children=dataset_name))
            else:
                # 데이터셋의 최신 배치 데이터를 사용
                latest_batch = df.iloc[-1]
                insp_result_value = latest_batch['insp_result_value']
                insp_min_value = latest_batch['insp_min_value']
                insp_max_value = latest_batch['insp_max_value']
               
                status = determine_status(insp_result_value, insp_min_value, insp_max_value, False) if insp_result_value is not None else 'grey'

                debug_message += f"{dataset_name} Columns: {df.columns.tolist()}\n{dataset_name} Head:\n{df.head()}\n"
                debug_message += f"Latest {dataset_name} Value: {insp_result_value}\n{dataset_name} Status: {status}\n\n"

                signals.append(html.Div(id=f'signal-{dataset_name}', style={
                    'width': '100px', 'height': '100px', 'background-color': status,
                    'border-radius': '15px', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin': '10px'
                }, children=dataset_name))
       
        return signals, debug_message, criteria_message
   
    return [], 'No data loaded', criteria_message

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#     app.run_server(debug=True)

