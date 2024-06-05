# 첫 10배치

import dataiku
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Dash 앱 인스턴스 생성
# app = Dash(__name__)

# 데이터셋 로드 함수
def load_data(dataset_name):
   dataset = dataiku.Dataset(dataset_name)
   df = dataset.get_dataframe()
   return df

# 최근 10배치 데이터 및 통계 계산 함수
def get_recent_batches_and_stats(df):
   recent_batches = df.sort_values(by='배치').tail(10)
   stats = {
       'mean': recent_batches.mean(),
       'std': recent_batches.std()
   }
   return recent_batches, stats

# 테이블 생성 함수
def create_table(df, stats):
   header = [html.Tr([html.Th(col) for col in df.columns])]
   rows = [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(len(df))]
   summary = [html.Tr([html.Td("Mean"), html.Td(stats['mean'])]),
              html.Tr([html.Td("Std"), html.Td(stats['std'])])]
   return html.Table(header + rows + summary)

# DP26 부터 DP72 까지 탭 생성 함수
def create_tabs():
   tabs = []
   for dataset in ["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"]:
       df = load_data(dataset)
       recent_batches, stats = get_recent_batches_and_stats(df)
       table = create_table(recent_batches, stats)
       tabs.append(dcc.Tab(label=dataset, children=[
           html.Div([
               html.H3(f'{dataset} 최근 10배치 결과'),
               table
           ])
       ]))
   return tabs

# 앱 레이아웃 설정
app.layout = html.Div([
   html.H1('제품 배치 분석 대시보드'),
   dcc.Tabs(id="tabs", children=create_tabs())
])

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#     app.run_server(debug=True)
