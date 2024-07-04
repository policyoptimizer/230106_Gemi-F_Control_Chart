# DP67만 우선 적용

# 마지막 배치 결과를 기준으로 함
# 신호등의 기준은 초록(정상), 노랑(위험), 빨강(규격을 벗어남)으로 설정합니다. 

# 초록 (정상): 값이 기준 이하인 경우
# 노랑 (위험): 값이 기준에 근접한 경우 (기준의 90% 이상)
# 빨강 (규격을 벗어남): 값이 기준을 초과한 경우

# 시험 항목의 예시 기준:
# AUI: 0.1% 이하가 정상
# Total Impurity: 2.0% 이하가 정상

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
def determine_status(value, spec):
    if value <= spec:
        return 'green'
    elif value <= spec * 1.1:
        return 'yellow'
    else:
        return 'red'

# Dash 앱 인스턴스 생성
# app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('CQA DP67 AUI, Total Impurity 신호등'),
    html.Div([
        html.H2('DP67 AUI'),
        html.Div(id='dp67-aui-signal', style={'width': '100px', 'height': '100px', 'background-color': 'grey'}),
        html.H2('DP67 Total Impurity'),
        html.Div(id='dp67-total-impurity-signal', style={'width': '100px', 'height': '100px', 'background-color': 'grey'}),
        html.Button('데이터 로드 및 신호등 업데이트', id='update-button', n_clicks=0),
        html.Div(id='debug-output', style={'margin-top': '20px', 'white-space': 'pre-wrap'})
    ], style={'text-align': 'center'})
])

@app.callback(
    [Output('dp67-aui-signal', 'style'),
     Output('dp67-total-impurity-signal', 'style'),
     Output('debug-output', 'children')],
    [Input('update-button', 'n_clicks')]
)
def update_signals(n_clicks):
    if n_clicks > 0:
        df_aui = load_data("DP67_AUI")
        df_total_impurity = load_data("DP67_Total_Impurity")

        # 데이터셋 로드 성공 여부 확인
        if isinstance(df_aui, str) or isinstance(df_total_impurity, str):
            return [{'width': '100px', 'height': '100px', 'background-color': 'grey'},
                    {'width': '100px', 'height': '100px', 'background-color': 'grey'},
                    f"Error loading datasets:\nDP67_AUI: {df_aui}\nDP67_Total_Impurity: {df_total_impurity}"]

        # 데이터셋의 컬럼 이름과 첫 몇 행을 확인
        debug_message = f"DP67_AUI Columns: {df_aui.columns.tolist()}\n" \
                        f"DP67_AUI Head:\n{df_aui.head()}\n\n" \
                        f"DP67_Total_Impurity Columns: {df_total_impurity.columns.tolist()}\n" \
                        f"DP67_Total_Impurity Head:\n{df_total_impurity.head()}\n"

        # 마지막 값을 가져와 신호등 상태 결정
        latest_aui_value = df_aui.iloc[-1]['AUI'] if 'AUI' in df_aui.columns else None
        latest_total_impurity_value = df_total_impurity.iloc[-1]['Total Impurity'] if 'Total Impurity' in df_total_impurity.columns else None

        aui_spec = 0.1
        total_impurity_spec = 2.0

        aui_status = determine_status(latest_aui_value, aui_spec) if latest_aui_value is not None else 'grey'
        total_impurity_status = determine_status(latest_total_impurity_value, total_impurity_spec) if latest_total_impurity_value is not None else 'grey'

        debug_message += f"Latest AUI Value: {latest_aui_value}\nAUI Status: {aui_status}\n" \
                         f"Latest Total Impurity Value: {latest_total_impurity_value}\nTotal Impurity Status: {total_impurity_status}"

        return [{'width': '100px', 'height': '100px', 'background-color': aui_status},
                {'width': '100px', 'height': '100px', 'background-color': total_impurity_status},
                debug_message]
   
    return [{'width': '100px', 'height': '100px', 'background-color': 'grey'},
            {'width': '100px', 'height': '100px', 'background-color': 'grey'},
            'No data loaded']

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#     app.run_server(debug=True)

