# 첫 배포 성공
# DP26_Assay, DP26_Triester 2개만 적용함

import plotly.express as px
import dataiku
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# Dataiku 데이터셋 로드
dp26_assay_dataset = dataiku.Dataset("DP26_Assay")
dp26_assay_df = dp26_assay_dataset.get_dataframe()

dp26_triester_dataset = dataiku.Dataset("DP26_Triester")
dp26_triester_df = dp26_triester_dataset.get_dataframe()

# 'DP26_Assay' 데이터에 대한 바 차트 생성
assay_fig = px.bar(dp26_assay_df, x='배치', y='Assay', title='DP26 Assay Levels by Batch', color='Site')

# 'DP26_Triester' 데이터에 대한 바 차트 생성
triester_fig = px.bar(dp26_triester_df, x='배치', y='불순물(Triester)', title='DP26 Triester Levels by Batch', color='Site')

# Dash 앱 인스턴스 생성
# app = dash.Dash(__name__)

# Dash 앱 레이아웃 설정
app.layout = html.Div([
   html.H1('DP26 Data Analysis Dashboard'),
   html.Div([
       html.H2('Assay Analysis'),
       dcc.Graph(id='assay-graph', figure=assay_fig)
   ]),
   html.Div([
       html.H2('Triester Analysis'),
       dcc.Graph(id='triester-graph', figure=triester_fig)
   ])
])
