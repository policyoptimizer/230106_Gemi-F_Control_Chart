# 넬슨 법칙 초안

import dataiku
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# Dash 앱 인스턴스 생성
# app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# 데이터셋 이름 목록
dataset_names = [
   "DP26_Assay", "DP26_Triester", "DP37_Assay", "DP57_Assay", "DP57_Chiral",
   "DP57_Total_Impurity", "DP58_Assay", "DP58_Chiral", "DP67_AUI", "DP67_Total_Impurity",
   "DP72_Assay", "DP72_Chiral", "DP72_AUI", "DP72_Total_Impurity", "DP72_ROI", "DP72_Impurity-1"
]

# 데이터와 그래프를 로드하는 함수
def load_data_and_create_graphs(dataset_name):
   # 데이터셋 로드
   dataset = dataiku.Dataset(dataset_name)
   df = dataset.get_dataframe()
   
   # 이동 평균 및 넬슨 법칙의 이상치 계산
   column_name = df.columns[-1]  # 데이터셋의 마지막 컬럼을 측정치로 가정
   window_size = 5
   df['MA'] = df[column_name].rolling(window=window_size).mean()
   df['MR'] = df[column_name].diff().abs().rolling(window=window_size).mean()
   mean = df[column_name].mean()
   std = df[column_name].std()
   df['Anomaly'] = (df[column_name] > mean + 3 * std) | (df[column_name] < mean - 3 * std)
   
   # ARIMA 모델을 사용하여 예측 추가
   model = ARIMA(df[column_name], order=(1, 1, 1))
   model_fit = model.fit()
   df['Forecast'] = model_fit.predict(start=0, end=len(df) - 1, typ='levels')
   
   # 그래프 생성
   time_series_fig = px.line(df, x=df.index, y=[column_name, "MA", "Forecast"],
                             labels={"value": "Measurement", "variable": "Type"},
                             title=f"{dataset_name} - Time Series Analysis")
   anomaly_fig = px.scatter(df, x=df.index, y=column_name, color="Anomaly",
                            title=f"{dataset_name} - Anomaly Detection")
   
   return time_series_fig, anomaly_fig

# 모든 데이터셋에 대한 탭 생성
tabs_children = []
for name in dataset_names:
   time_series_graph, anomaly_graph = load_data_and_create_graphs(name)
   tab = dcc.Tab(label=name, children=[
       html.Div([
           dcc.Graph(figure=time_series_graph),
           dcc.Graph(figure=anomaly_graph)
       ])
   ])
   tabs_children.append(tab)

# 앱 레이아웃 설정
app.layout = html.Div([
   html.H1('Data Analysis with Statistical Methods Across Multiple Datasets'),
   dcc.Tabs(id="tabs", children=tabs_children)
])

# 서버 실행
# if __name__ == '__main__':
#    app.run_server(debug=True)
