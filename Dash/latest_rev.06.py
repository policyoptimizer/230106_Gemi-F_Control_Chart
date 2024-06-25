# 평균, 표준편차 여전히 이상함
# 그래서 그냥 별도의 테이블로 구성하기로 함

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
    if start_year is None and end_year is None:
        return df
    filtered_df = df[(df['연도'] >= start_year) & (df['연도'] <= end_year)]
    return filtered_df

# 요약 테이블 생성 함수
def create_summary_table(stats):
    summary_header = html.Tr([html.Th("통계", style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'})] +
                             [html.Th(col, style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'}) for col in stats['mean'].index])
    summary_mean_row = html.Tr([html.Td("평균", style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'})] +
                               [html.Td(stats['mean'][col], style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'}) for col in stats['mean'].index])
    summary_std_row = html.Tr([html.Td("표준편차", style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'})] +
                              [html.Td(stats['std'][col], style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'}) for col in stats['std'].index])
    summary_table = html.Table([summary_header, summary_mean_row, summary_std_row], style={'border': '1px solid black', 'border-collapse': 'collapse', 'width': '90%', 'margin': 'auto', 'margin-top': '20px'})
    return summary_table

# 원본 데이터 테이블 생성 함수
def create_data_table(df):
    header = html.Tr([html.Th(col, style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'}) for col in df.columns])
    rows = [html.Tr([html.Td(df.iloc[i][col], style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'}) for col in df.columns]) for i in range(len(df))]
    data_table = html.Table([header] + rows, style={'border': '1px solid black', 'border-collapse': 'collapse', 'width': '90%', 'margin': 'auto', 'margin-top': '20px'})
    return data_table

# 탭 생성 함수
def create_tabs():
    tabs = []
    for dataset in ["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"]:
        tabs.append(dcc.Tab(label=dataset, children=[
            html.Div([
                html.H3(f'{dataset} 데이터 필터링', style={'text-align': 'center'}),
                dcc.Dropdown(
                    id=f'batch-dropdown-{dataset}',
                    options=[
                        {'label': '30 배치', 'value': 30},
                        {'label': '50 배치', 'value': 50},
                        {'label': '모든 배치', 'value': 'all'}
                    ],
                    value=30,
                    clearable=False,
                    style={'width': '50%', 'margin': 'auto'}
                ),
                html.Div([
                    dcc.Dropdown(
                        id=f'start-year-{dataset}',
                        options=[{'label': '전체', 'value': None}] + [{'label': str(year), 'value': year} for year in range(20, 25)],
                        placeholder='시작 년도',
                        style={'width': '45%', 'display': 'inline-block', 'margin-right': '10px'}
                    ),
                    dcc.Dropdown(
                        id=f'end-year-{dataset}',
                        options=[{'label': '전체', 'value': None}] + [{'label': str(year), 'value': year} for year in range(20, 25)],
                        placeholder='종료 년도',
                        style={'width': '45%', 'display': 'inline-block'}
                    ),
                    html.Button('필터링', id=f'filter-button-{dataset}', n_clicks=0)
                ], style={'text-align': 'center', 'margin': '10px 0'}),
                html.Div(id=f'table-container-{dataset}')
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
    [Input(f'batch-dropdown-{dataset}', 'value') for dataset in ["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"]],
    [Input(f'filter-button-{dataset}', 'n_clicks') for dataset in ["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"]],
    [Input(f'start-year-{dataset}', 'value') for dataset in ["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"]],
    [Input(f'end-year-{dataset}', 'value') for dataset in ["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"]]
)
def update_tables(*inputs):
    tables = []
    batch_sizes = inputs[:6]
    n_clicks_list = inputs[6:12]
    start_year_list = inputs[12:18]
    end_year_list = inputs[18:]
   
    for dataset, batch_size, n_clicks, start_year, end_year in zip(
            ["DP26", "DP37", "DP57", "DP58", "DP67", "DP72"],
            batch_sizes,
            n_clicks_list,
            start_year_list,
            end_year_list):
       
        df = load_data(dataset)
        df = df.dropna(axis=1, how='all')  # 모든 값이 NaN인 칼럼 제거
       
        if start_year is None and end_year is None:
            recent_batches, stats = get_recent_batches_and_stats(df, batch_size if batch_size != 'all' else len(df))
        else:
            filtered_df = filter_by_year(df, start_year, end_year)
            stats = {
                'mean': filtered_df.mean().round(2),
                'std': filtered_df.std().round(2)
            }
            summary_table = create_summary_table(stats)
            data_table = create_data_table(filtered_df)
            tables.append(html.Div([summary_table, data_table]))
            continue
           
        summary_table = create_summary_table(stats)
        data_table = create_data_table(recent_batches)
        tables.append(html.Div([summary_table, data_table]))
    return tables

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#     app.run_server(debug=True)

