# 좀 더 이쁘게 보고서 다듬음
# 현재까지 Best

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
def load_data_and_create_graphs(dataset_name, window_size, sigma_level):
   dataset = dataiku.Dataset(dataset_name)
   df = dataset.get_dataframe()
   
   # 데이터 분석 및 그래프 생성
   batch_column = df.columns[2]  # 2 번째 컬럼 배치 번호
   column_name = df.columns[-1]  # 마지막 컬럼 측정치
   df['MA'] = df[column_name].rolling(window=window_size).mean()
   mean = df[column_name].mean()
   std = df[column_name].std()
   upper_bound = mean + sigma_level * std
   lower_bound = mean - sigma_level * std
   df['Upper_Bound'] = upper_bound
   df['Lower_Bound'] = lower_bound
   
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
   std_value = df[column_name].std()
   recent_avg = df[column_name].tail(5).mean()
   trend_text = "안정" if abs(recent_avg - mean_value) / mean_value < 0.02 else ("상승" if recent_avg > mean_value else "하락")
   
   summary_table = html.Table([
       html.Thead(html.Tr([html.Th("항목"), html.Th("결과")], style={'text-align': 'center'})),
       html.Tbody([
           html.Tr([html.Td("최대", style={'text-align': 'center'}), html.Td(f"{max_value:.2f}", style={'text-align': 'center'})]),
           html.Tr([html.Td("최소", style={'text-align': 'center'}), html.Td(f"{min_value:.2f}", style={'text-align': 'center'})]),          
           html.Tr([html.Td("평균", style={'text-align': 'center'}), html.Td(f"{mean_value:.2f}", style={'text-align': 'center'})]),
           html.Tr([html.Td("표준편차", style={'text-align': 'center'}), html.Td(f"{std_value:.2f}", style={'text-align': 'center'})]),
           html.Tr([html.Td("상한", style={'text-align': 'center'}), html.Td(f"{upper_bound:.2f}", style={'text-align': 'center'})]),
           html.Tr([html.Td("하한", style={'text-align': 'center'}), html.Td(f"{lower_bound:.2f}", style={'text-align': 'center'})]),
           html.Tr([html.Td("최근 5배치 평균", style={'text-align': 'center'}), html.Td(f"{recent_avg:.2f}", style={'text-align': 'center'})]),
           html.Tr([html.Td("경향", style={'text-align': 'center'}), html.Td(trend_text, style={'text-align': 'center'})])
       ], style={'border': '1px solid black'})
   ], style={'width': '50%', 'margin': 'auto', 'border-collapse': 'collapse', 'border': '1px solid black'})
   
   return trend_fig, anomaly_fig, summary_table

# DP72 제품에 대한 탭 생성 함수
def create_dp72_tabs(window_size, sigma_level):
   dp72_tabs = []
   for dataset in ["DP72_Assay", "DP72_Chiral", "DP72_AUI", "DP72_Total_Impurity", "DP72_ROI", "DP72_Impurity-1"]:
       trend_fig, anomaly_fig, summary_table = load_data_and_create_graphs(dataset, window_size, sigma_level)
       tab = dcc.Tab(label=dataset, children=[
           html.Div([
               html.H3('요약 보고서'),
               summary_table,
               dcc.Graph(figure=trend_fig),
               dcc.Graph(figure=anomaly_fig)
           ])
       ])
       dp72_tabs.append(tab)
   return dp72_tabs

# 앱 레이아웃 설정
app.layout = html.Div([
   html.H1('DP72 Analysis Dashboard'),
   html.Div([
       html.Label('윈도우 사이즈', style={'margin-right': '10px'}),
       dcc.Dropdown(
           id='window-size-dropdown',
           options=[
               {'label': '5', 'value': 5},
               {'label': '10', 'value': 10},
               {'label': '15', 'value': 15}
           ],
           value=5,
           clearable=False,
           style={'width': '30%', 'display': 'inline-block', 'margin-right': '10px'}
       ),
       html.Label('시그마 레벨', style={'margin-right': '10px'}),
       dcc.Dropdown(
           id='sigma-level-dropdown',
           options=[
               {'label': '1시그마', 'value': 1},
               {'label': '2시그마', 'value': 2},
               {'label': '3시그마', 'value': 3}
           ],
           value=1,
           clearable=False,
           style={'width': '30%', 'display': 'inline-block'}
       )
   ], style={'text-align': 'center', 'margin-bottom': '20px'}),
   dcc.Tabs(id="dp72-tabs", children=create_dp72_tabs(5, 1)),
   html.Div([
       html.H3('넬슨 법칙 설명'),
       html.P('Rule 1: 데이터 포인트가 평균으로부터 3 표준편차 이상 벗어날 때.'),
       html.P('Rule 2: 연속 9개의 데이터 포인트가 모두 평균보다 클 때 또는 작을 때.'),
       html.P('Rule 3: 연속 6개의 데이터 포인트가 계속 증가하거나 감소할 때.'),
       html.P('Rule 4: 연속 14개의 데이터 포인트 중 두 개 이상이 평균으로부터 2 표준편차 이상 벗어날 때.')
   ], style={'margin-top': '20px', 'text-align': 'left'})
])

@app.callback(
   Output('dp72-tabs', 'children'),
   Input('window-size-dropdown', 'value'),
   Input('sigma-level-dropdown', 'value')
)
def update_tabs(window_size, sigma_level):
   return create_dp72_tabs(window_size, sigma_level)

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#    app.run_server(debug=True)
