import dataiku
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import numpy as np

# Dash 앱 인스턴스 생성
# app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# 데이터셋 로드 및 그래프 생성 함수
def load_data_and_create_graphs(dataset_name):
   dataset = dataiku.Dataset(dataset_name)
   df = dataset.get_dataframe()
   
   # 데이터 분석 및 그래프 생성
   column_name = df.columns[-1]  # 가정: 데이터셋의 마지막 컬럼을 측정치로 사용
   df['MA'] = df[column_name].rolling(window=5).mean()
   df['Anomaly'] = (df[column_name] > df['MA'] + 3 * df[column_name].rolling(window=5).std()) | \
                   (df[column_name] < df['MA'] - 3 * df[column_name].rolling(window=5).std())
   
   # 추세선 그래프
   trend_fig = px.line(df, x=df.index, y=[column_name, 'MA'], title=f"{dataset_name} - Trend and Moving Average")
   
   # 이상치 탐지 그래프
   anomaly_fig = px.scatter(df, x=df.index, y=column_name, color='Anomaly',
                            title=f"{dataset_name} - Anomaly Detection")
   
   return trend_fig, anomaly_fig

# DP67 제품에 대한 탭 생성
dp67_tabs = []
for dataset in ["DP67_AUI", "DP67_Total_Impurity"]:
   trend_fig, anomaly_fig = load_data_and_create_graphs(dataset)
   tab = dcc.Tab(label=dataset, children=[
       html.Div([
           dcc.Graph(figure=trend_fig),
           dcc.Graph(figure=anomaly_fig)
       ])
   ])
   dp67_tabs.append(tab)

# 앱 레이아웃 설정
app.layout = html.Div([
   html.H1('DP67 Analysis Dashboard'),
   dcc.Tabs(id="dp67-tabs", children=dp67_tabs)
])

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#    app.run_server(debug=True)
