# 년도를 선택할 수 있게 해달라
# 최근 30, 50, 100배치

import dataiku
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import numpy as np

# Dash 앱 인스턴스 생성
# app = Dash(__name__)

# 데이터셋 로드 함수
def load_data(dataset_name):
   dataset = dataiku.Dataset(dataset_name)
   df = dataset.get_dataframe()
   return df

# 최근 배치 데이터 및 통계 계산 함수
def get_recent_batches_and_stats(df, num_batches):
   recent_batches = df.sort_values(by='배치').tail(num_batches)
   stats = {
       'mean': recent_batches.mean().round(2),
       'std': recent_batches.std().round(2)
   }
   return recent_batches, stats

# 연도별 데이터 필터링 함수
def filter_by_year(df, start_year, end_year): 
    df['연도'] = df['배치'].apply(lambda x: int(x[1:3]) if x[0] == 'M' else int(x[3:5])) 
    filtered_df = df[(df['연도'] >= start_year) & (df['연도'] <= end_year)] 
    return filtered_df


# 테이블 생성 함수
def create_table(df, stats):
   header = [html.Tr([html.Th(col, style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'}) for col in df.columns])]
   rows = [html.Tr([html.Td(df.iloc[i][col], style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'}) for col in df.columns]) for i in range(len(df))]
   summary = [html.Tr([html.Td("Mean"), html.Td(stats['mean'])]),
              html.Tr([html.Td("Std"), html.Td(stats['std'])])]
   return html.Table(header + rows + summary, style={'border': '1px solid black', 'border-collapse': 'collapse', 'width': '90%', 'margin': 'auto', 'margin-top': '20px'})

# DP26 부터 DP72 까지 탭 생성 함수
def create_tabs():
   tabs = []
   for dataset in ["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"]:
       tabs.append(dcc.Tab(label=dataset, children=[
           html.Div([
               html.H3(f'{dataset} 최근 배치 결과', style={'text-align': 'center'}),
               dcc.Dropdown(
                   id=f'batch-dropdown-{dataset}',
                   options=[
                       {'label': '30 배치', 'value': 30},
                       {'label': '50 배치', 'value': 50},
                       {'label': '모든 결과', 'value': 'all'}
                   ],
                   value=30,
                   clearable=False,
                   style={'width': '50%', 'margin': 'auto'}
               ),
               html.Div(id=f'table-container-{dataset}')
           ]),
           html.Div([
               html.H3(f'{dataset} 연도별 결과', style={'text-align': 'center'}),
               dcc.Input(id=f'start-year-{dataset}', type='number', placeholder='시작 년도', style={'margin-right': '10px'}),
               dcc.Input(id=f'end-year-{dataset}', type='number', placeholder='종료 년도', style={'margin-right': '10px'}),
               html.Button('필터링', id=f'filter-button-{dataset}', n_clicks=0),
               html.Div(id=f'yearly-table-container-{dataset}')
           ])
       ]))
   return tabs

# 앱 레이아웃 설정
app.layout = html.Div([
   html.H1('최근 배치 분석', style={'text-align': 'center'}),
   dcc.Tabs(id="tabs", children=create_tabs())
])

# 콜백 함수 설정
@app.callback(
   [Output(f'table-container-{dataset}', 'children') for dataset in ["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"]],
   [Input(f'batch-dropdown-{dataset}', 'value') for dataset in ["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"]]
)
def update_tables(*batch_sizes):
   tables = []
   for dataset, batch_size in zip(["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"], batch_sizes):
       df = load_data(dataset)
       df = df.dropna(axis=1, how='all')  # 모든 값이 NaN인 칼럼 제거
       if batch_size == 'all':
           recent_batches, stats = get_recent_batches_and_stats(df, len(df))
       else:
           recent_batches, stats = get_recent_batches_and_stats(df, batch_size)
       table = create_table(recent_batches, stats)
       tables.append(table)
   return tables

@app.callback(
   [Output(f'yearly-table-container-{dataset}', 'children') for dataset in ["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"]],
   [Input(f'filter-button-{dataset}', 'n_clicks') for dataset in ["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"]],
   [Input(f'start-year-{dataset}', 'value') for dataset in ["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"]],
   [Input(f'end-year-{dataset}', 'value') for dataset in ["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"]]
)
def update_yearly_tables(*inputs):
   tables = []
   n_clicks_list = inputs[:6]
   start_year_list = inputs[6:12]
   end_year_list = inputs[12:]
   
   for dataset, n_clicks, start_year, end_year in zip(["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"], n_clicks_list, start_year_list, end_year_list):
       if n_clicks > 0 and start_year is not None and end_year is not None:
           df = load_data(dataset)
           df = df.dropna(axis=1, how='all')  # 모든 값이 NaN인 칼럼 제거
           filtered_df = filter_by_year(df, start_year, end_year)
           stats = {
               'mean': filtered_df.mean().round(2),
               'std': filtered_df.std().round(2)
           }
           table = create_table(filtered_df, stats)
           tables.append(table)
       else:
           tables.append(html.Div())
   return tables

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#     app.run_server(debug=True)
