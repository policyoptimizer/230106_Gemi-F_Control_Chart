# 아래에 요약 테이블 추가

import dataiku
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Dash 앱 인스턴스 생성
# app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# 넬슨 법칙 탐지 함수들
def check_rule_1(series, mean, std):
   return (series > mean + 3 * std) | (series < mean - 3 * std)

def check_rule_2(series, mean):
   return (series > mean).rolling(window=9).sum().ge(9) | \
          (series < mean).rolling(window=9).sum().ge(9)

def check_rule_3(series):
   return series.diff().gt(0).rolling(window=6).sum().ge(6) | \
          series.diff().lt(0).rolling(window=6).sum().ge(6)

def check_rule_4(series, mean, std):
   two_std = (series > mean + 2 * std) | (series < mean - 2 * std)
   return two_std.rolling(window=14).apply(lambda x: np.sum(x) >= 2, raw=True).fillna(0).astype(bool)

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
   
   # 넬슨 법칙 적용
   df['Anomaly_Rule1'] = check_rule_1(df[column_name], mean, std)
   df['Anomaly_Rule2'] = check_rule_2(df[column_name], mean)
   df['Anomaly_Rule3'] = check_rule_3(df[column_name])
   df['Anomaly_Rule4'] = check_rule_4(df[column_name], mean, std)
   
   # 추세선 그래프
   trend_fig = px.line(df, x=batch_column, y=[column_name, 'MA', 'Upper_Bound', 'Lower_Bound'],
                       title=f"{dataset_name} - Trend and Moving Average")
   
   # 이상치 탐지 그래프
   anomaly_fig = px.scatter(df, x=batch_column, y=column_name, title=f"{dataset_name} - Anomaly Detection")
   anomaly_fig.add_scatter(x=df[batch_column][df['Anomaly_Rule1']], y=df[column_name][df['Anomaly_Rule1']],
                           mode='markers', name='Rule 1 Violation', marker=dict(color='red'))
   anomaly_fig.add_scatter(x=df[batch_column][df['Anomaly_Rule2']], y=df[column_name][df['Anomaly_Rule2']],
                           mode='markers', name='Rule 2 Violation', marker=dict(color='purple'))
   anomaly_fig.add_scatter(x=df[batch_column][df['Anomaly_Rule3']], y=df[column_name][df['Anomaly_Rule3']],
                           mode='markers', name='Rule 3 Violation', marker=dict(color='green'))
   anomaly_fig.add_scatter(x=df[batch_column][df['Anomaly_Rule4']], y=df[column_name][df['Anomaly_Rule4']],
                           mode='markers', name='Rule 4 Violation', marker=dict(color='orange'))
   
   # 요약 통계 계산
   min_value = df[column_name].min()
   max_value = df[column_name].max()
   mean_value = df[column_name].mean()
   recent_trend = df[column_name].tail(5).mean()
   trend_text = "Increasing" if recent_trend > mean_value else "Decreasing" if recent_trend < mean_value else "Stable"
   
   summary_table = html.Table([
       html.Thead(html.Tr([html.Th("Metric"), html.Th("Value")])),
       html.Tbody([
           html.Tr([html.Td("Minimum"), html.Td(f"{min_value:.2f}")]),
           html.Tr([html.Td("Maximum"), html.Td(f"{max_value:.2f}")]),
           html.Tr([html.Td("Mean"), html.Td(f"{mean_value:.2f}")]),
           html.Tr([html.Td("Recent Trend (last 5 batches)"), html.Td(trend_text)])
       ])
   ])
   
   return trend_fig, anomaly_fig, summary_table

# DP72 제품에 대한 탭 생성 함수
def create_dp72_tabs(window_size):
   dp72_tabs = []
   for dataset in ["DP72_Assay", "DP72_Chiral", "DP72_AUI", "DP72_Total_Impurity", "DP72_ROI", "DP72_Impurity-1"]:
       trend_fig, anomaly_fig, summary_table = load_data_and_create_graphs(dataset, window_size)
       tab = dcc.Tab(label=dataset, children=[
           html.Div([
               dcc.Graph(figure=trend_fig),
               dcc.Graph(figure=anomaly_fig),
               summary_table
           ])
       ])
       dp72_tabs.append(tab)
   return dp72_tabs

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
   dcc.Tabs(id="dp72-tabs", children=create_dp72_tabs(5))
])

@app.callback(
   Output('dp72-tabs', 'children'),
   Input('window-size-dropdown', 'value')
)
def update_tabs(window_size):
   return create_dp72_tabs(window_size)

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#    app.run_server(debug=True)
