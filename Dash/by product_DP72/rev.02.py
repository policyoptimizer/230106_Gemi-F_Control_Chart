# 수정사항
# x 축에 배치번호 추가
# 상한, 하한선 추가
# moving average 5, 10, 15 선택

import dataiku
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Dash 앱 인스턴스 생성
# app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# 데이터셋 로드 및 그래프 생성 함수
def load_data_and_create_graphs(dataset_name, window_size):
   dataset = dataiku.Dataset(dataset_name)
   df = dataset.get_dataframe()
   
   # 데이터 분석 및 그래프 생성
   batch_column = df.columns[2]  # 2 번째 컬럼 배치 번호
   column_name = df.columns[-1]  # 마지막 컬럼 측정치
   df['MA'] = df[column_name].rolling(window=window_size).mean()
   mean = df[column_name].mean()
   std = df[column_name].std()
   df['Upper_Bound'] = mean + std
   df['Lower_Bound'] = mean - std
   df['Anomaly'] = (df[column_name] > df['MA'] + 3 * df[column_name].rolling(window=window_size).std()) | \
                   (df[column_name] < df['MA'] - 3 * df[column_name].rolling(window=window_size).std())
   
   # 추세선 그래프
   trend_fig = px.line(df, x=batch_column, y=[column_name, 'MA', 'Upper_Bound', 'Lower_Bound'],
                       title=f"{dataset_name} - Trend and Moving Average")
   
   # 이상치 탐지 그래프
   anomaly_fig = px.scatter(df, x=batch_column, y=column_name, color='Anomaly',
                            title=f"{dataset_name} - Anomaly Detection")
   
   return trend_fig, anomaly_fig

# DP72 제품에 대한 탭 생성
dp72_tabs = []
for dataset in ["DP72_Assay", "DP72_Chiral", "DP72_AUI", "DP72_Total_Impurity", "DP72_ROI", "DP72_Impurity-1"]:
   trend_fig, anomaly_fig = load_data_and_create_graphs(dataset, 5)
   tab = dcc.Tab(label=dataset, children=[
       html.Div([
           dcc.Graph(figure=trend_fig),
           dcc.Graph(figure=anomaly_fig)
       ])
   ])
   dp72_tabs.append(tab)

# 앱 레이아웃 설정
app.layout = html.Div([
   html.H1('DP72 Analysis Dashboard'),
   dcc.Dropdown(
       id='window-size-dropdown',
       options=[
           {'label': '5', 'value': 5},
           {'label': '10', 'value': 10},
           {'label': '15', 'value': 15}
       ],
       value=5,
       clearable=False,
       style={'width': '50%'}
   ),
   dcc.Tabs(id="dp72-tabs", children=dp72_tabs)
])

@app.callback(
   Output('dp72-tabs', 'children'),
   Input('window-size-dropdown', 'value')
)
def update_tabs(window_size):
   dp72_tabs = []
   for dataset in ["DP72_Assay", "DP72_Chiral", "DP72_AUI", "DP72_Total_Impurity", "DP72_ROI", "DP72_Impurity-1"]:
       trend_fig, anomaly_fig = load_data_and_create_graphs(dataset, window_size)
       tab = dcc.Tab(label=dataset, children=[
           html.Div([
               dcc.Graph(figure=trend_fig),
               dcc.Graph(figure=anomaly_fig)
           ])
       ])
       dp72_tabs.append(tab)
   return dp72_tabs

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#    app.run_server(debug=True)
