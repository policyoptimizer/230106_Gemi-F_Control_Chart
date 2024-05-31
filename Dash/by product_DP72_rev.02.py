# 수정사항
# x 축에 배치번호 추가
# 상한, 하한선 추가
# moving average 5, 10, 15 선택

import dataiku
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Dash 앱 인스턴스 생성
# app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# 데이터셋 로드 및 그래프 생성 함수
def load_data_and_create_graphs(dataset_name, window_size=5):
   dataset = dataiku.Dataset(dataset_name)
   df = dataset.get_dataframe()
   
   # 데이터 분석 및 그래프 생성
   column_name = df.columns[-1]  # 가정: 데이터셋의 마지막 컬럼을 측정치로 사용
   df['MA'] = df[column_name].rolling(window=int(window_size)).mean()
   df['Upper'] = df['MA'] + df[column_name].rolling(window=int(window_size)).std()
   df['Lower'] = df['MA'] - df[column_name].rolling(window=int(window_size)).std()
   df['Anomaly'] = (df[column_name] > df['Upper']) | (df[column_name] < df['Lower'])
   
   # 추세선 그래프
   fig = px.line(df, x='batch', y=[column_name, 'MA', 'Upper', 'Lower'],
                 labels={'value': 'Measurement', 'variable': 'Type'},
                 title=f"{dataset_name} - Trend, Moving Average, and Control Limits")
   
   # 이상치 탐지 그래프
   anomaly_fig = px.scatter(df, x='batch', y=column_name, color='Anomaly',
                            title=f"{dataset_name} - Anomaly Detection")
   
   return fig, anomaly_fig

# DP72 제품에 대한 탭 생성
dp72_tabs = []
for dataset in ["DP72_Assay", "DP72_Chiral", "DP72_AUI", "DP72_Total_Impurity", "DP72_ROI", "DP72_Impurity-1"]:
   fig, anomaly_fig = load_data_and_create_graphs(dataset)
   tab = dcc.Tab(label=dataset, children=[
       html.Div([
           dcc.Graph(figure=fig),
           dcc.Graph(figure=anomaly_fig)
       ])
   ])
   dp72_tabs.append(tab)

# 드롭다운 및 상호작용 설정
@app.callback(
   [Output(f"{dataset}-graph", "figure") for dataset in ["DP72_Assay", "DP72_Chiral", "DP72_AUI", "DP72_Total_Impurity", "DP72_ROI", "DP72_Impurity-1"]],
   [Input("window-size", "value")]
)
def update_graphs(window_size):
   figures = []
   for dataset in ["DP72_Assay", "DP72_Chiral", "DP72_AUI", "DP72_Total_Impurity", "DP72_ROI", "DP72_Impurity-1"]:
       fig, _ = load_data_and_create_graphs(dataset, window_size)
       figures.append(fig)
   return figures

# 앱 레이아웃 설정
app.layout = html.Div([
   html.H1('DP72 Analysis Dashboard'),
   dcc.Dropdown(
       id='window-size',
       options=[
           {'label': '5 Days', 'value': '5'},
           {'label': '10 Days', 'value': '10'},
           {'label': '15 Days', 'value': '15'}
       ],
       value='5',
       style={'width': '200px'}
   ),
   dcc.Tabs(id="dp72-tabs", children=dp72_tabs)
])

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#    app.run_server(debug=True)
