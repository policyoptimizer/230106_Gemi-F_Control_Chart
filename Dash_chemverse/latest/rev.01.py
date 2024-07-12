# -*- coding: utf-8 -*-
import dataiku
from dash import Dash, dcc, html, Input, Output, State
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
    recent_batches = df.sort_values(by='batch_no').tail(num_batches)
    stats = {
        'mean': recent_batches.mean(numeric_only=True).round(2),
        'std': recent_batches.std(numeric_only=True).round(2)
    }
    return recent_batches, stats

# 연도별 데이터 필터링 함수
def filter_by_year(df, start_year, end_year):
    df['Year'] = df['batch_no'].apply(lambda x: int(x[1:3]) if x[0] == 'M' else int(x[3:5]))
    if start_year is None and end_year is None:
        return df
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    return filtered_df

# 요약 테이블 생성 함수
def create_summary_table(stats):
    summary_header = html.Tr([html.Th("Statistic", style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'})] +
                             [html.Th(col, style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'}) for col in stats['mean'].index])
    summary_mean_row = html.Tr([html.Td("Mean", style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'})] +
                               [html.Td(stats['mean'][col], style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'}) for col in stats['mean'].index])
    summary_std_row = html.Tr([html.Td("Std Dev", style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'})] +
                              [html.Td(stats['std'][col], style={'border': '1px solid black', 'padding': '5px', 'text-align': 'center'}) for col in stats['std'].index])
    summary_table = html.Table([summary_header, summary_mean_row, summary_std_row],
                               style={'border': '1px solid black', 'border-collapse': 'collapse', 'width': '90%', 'margin': 'auto', 'margin-top': '20px', 'background-color': '#f9f9f9'})
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
    for dataset in ["DP26_c", "DP26onsan", "DP37_c", "DP57_c", "DP58_c", "DP58onsan", "DP67_c", "DP72_c",
                    "Zemiglo", "Zemidapa", "Zemimet_50_500mg", "Zemimet_50_1000mg", "Zemimet_25_500mg",
                    "Zemimet_25_1000mg", "Zemilow_50_5mg", "Zemilow_50_10mg", "Zemilow_50_20mg", "Zemimet_25_750mg"]:
        tabs.append(dcc.Tab(label=dataset, children=[
            html.Div([
                html.H3(f'{dataset} ', style={'text-align': 'center'}),
                html.Div([
                    dcc.Dropdown(
                        id=f'batch-dropdown-{dataset}',
                        options=[
                            {'label': '30 Batches', 'value': 30},
                            {'label': '50 Batches', 'value': 50},
                            {'label': 'All Batches', 'value': 'all'}
                        ],
                        value=30,
                        clearable=False,
                        style={'width': '50%', 'margin': 'auto'}
                    ),
                    html.Div([
                        dcc.Dropdown(
                            id=f'start-year-{dataset}',
                            options=[{'label': 'All', 'value': None}] + [{'label': str(year), 'value': year} for year in range(20, 25)],
                            placeholder='Start Year',
                            style={'width': '45%', 'display': 'inline-block', 'margin-right': '10px'}
                        ),
                        dcc.Dropdown(
                            id=f'end-year-{dataset}',
                            options=[{'label': 'All', 'value': None}] + [{'label': str(year), 'value': year} for year in range(20, 25)],
                            placeholder='End Year',
                            style={'width': '45%', 'display': 'inline-block'}
                        ),
                        html.Button('Filter', id=f'filter-button-{dataset}', n_clicks=0),
                        html.Button('Download CSV', id=f'download-button-{dataset}', n_clicks=0),
                        dcc.Download(id=f'download-{dataset}')
                    ], style={'text-align': 'center', 'margin': '10px 0'}),
                ], style={'text-align': 'center', 'margin': '20px 0'}),
                html.Div(id=f'table-container-{dataset}')
            ])
        ]))
    return tabs

# 앱 레이아웃 설정
app.layout = html.Div([
    html.H1('Recent Batches', style={'text-align': 'center'}),
    dcc.Tabs(id="tabs", children=create_tabs())
])

# 콜백 함수 설정
@app.callback(
    [Output(f'table-container-{dataset}', 'children') for dataset in ["DP26_c", "DP26onsan", "DP37_c", "DP57_c", "DP58_c", "DP58onsan", "DP67_c", "DP72_c",
                    "Zemiglo", "Zemidapa", "Zemimet_50_500mg", "Zemimet_50_1000mg", "Zemimet_25_500mg",
                    "Zemimet_25_1000mg", "Zemilow_50_5mg", "Zemilow_50_10mg", "Zemilow_50_20mg", "Zemimet_25_750mg"]],
    [Input(f'filter-button-{dataset}', 'n_clicks') for dataset in ["DP26_c", "DP26onsan", "DP37_c", "DP57_c", "DP58_c", "DP58onsan", "DP67_c", "DP72_c",
                    "Zemiglo", "Zemidapa", "Zemimet_50_500mg", "Zemimet_50_1000mg", "Zemimet_25_500mg",
                    "Zemimet_25_1000mg", "Zemilow_50_5mg", "Zemilow_50_10mg", "Zemilow_50_20mg", "Zemimet_25_750mg"]],
    [State(f'batch-dropdown-{dataset}', 'value') for dataset in ["DP26_c", "DP26onsan", "DP37_c", "DP57_c", "DP58_c", "DP58onsan", "DP67_c", "DP72_c",
                    "Zemiglo", "Zemidapa", "Zemimet_50_500mg", "Zemimet_50_1000mg", "Zemimet_25_500mg",
                    "Zemimet_25_1000mg", "Zemilow_50_5mg", "Zemilow_50_10mg", "Zemilow_50_20mg", "Zemimet_25_750mg"]],
    [State(f'start-year-{dataset}', 'value') for dataset in ["DP26_c", "DP26onsan", "DP37_c", "DP57_c", "DP58_c", "DP58onsan", "DP67_c", "DP72_c",
                    "Zemiglo", "Zemidapa", "Zemimet_50_500mg", "Zemimet_50_1000mg", "Zemimet_25_500mg",
                    "Zemimet_25_1000mg", "Zemilow_50_5mg", "Zemilow_50_10mg", "Zemilow_50_20mg", "Zemimet_25_750mg"]],
    [State(f'end-year-{dataset}', 'value') for dataset in ["DP26_c", "DP26onsan", "DP37_c", "DP57_c", "DP58_c", "DP58onsan", "DP67_c", "DP72_c",
                    "Zemiglo", "Zemidapa", "Zemimet_50_500mg", "Zemimet_50_1000mg", "Zemimet_25_500mg",
                    "Zemimet_25_1000mg", "Zemilow_50_5mg", "Zemilow_50_10mg", "Zemilow_50_20mg", "Zemimet_25_750mg"]]
)
def update_tables(*inputs):
    n_clicks_list = inputs[:18]
    batch_sizes = inputs[18:36]
    start_year_list = inputs[36:54]
    end_year_list = inputs[54:]
    tables = []

    for dataset, n_clicks, batch_size, start_year, end_year in zip(
            ["DP26_c", "DP26onsan", "DP37_c", "DP57_c", "DP58_c", "DP58onsan", "DP67_c", "DP72_c",
                    "Zemiglo", "Zemidapa", "Zemimet_50_500mg", "Zemimet_50_1000mg", "Zemimet_25_500mg",
                    "Zemimet_25_1000mg", "Zemilow_50_5mg", "Zemilow_50_10mg", "Zemilow_50_20mg", "Zemimet_25_750mg"],
            n_clicks_list,
            batch_sizes,
            start_year_list,
            end_year_list):

        df = load_data(dataset)
        df = df.dropna(axis=1, how='all')  # 모든 값이 NaN인 칼럼 제거

        if start_year is None and end_year is None:
            recent_batches, stats = get_recent_batches_and_stats(df, batch_size if batch_size != 'all' else len(df))
        else:
            filtered_df = filter_by_year(df, start_year, end_year)
            if batch_size != 'all':
                filtered_df = filtered_df.tail(batch_size)
            stats = {
                'mean': filtered_df.mean(numeric_only=True).round(2),
                'std': filtered_df.std(numeric_only=True).round(2)
            }
            summary_table = create_summary_table(stats)
            data_table = create_data_table(filtered_df)
            tables.append(html.Div([summary_table, data_table]))
            continue

        summary_table = create_summary_table(stats)
        data_table = create_data_table(recent_batches)
        tables.append(html.Div([summary_table, data_table]))
    return tables

# CSV 다운로드 콜백 함수 설정
def create_download_callback(dataset):
    @app.callback(
        Output(f'download-{dataset}', 'data'),
        Input(f'download-button-{dataset}', 'n_clicks'),
        State(f'batch-dropdown-{dataset}', 'value'),
        State(f'start-year-{dataset}', 'value'),
        State(f'end-year-{dataset}', 'value'),
        prevent_initial_call=True
    )
    def download_data(n_clicks, batch_size, start_year, end_year):
        df = load_data(dataset)
        df = df.dropna(axis=1, how='all')  # 모든 값이 NaN인 칼럼 제거

        if start_year is not None or end_year is not None:
            df = filter_by_year(df, start_year, end_year)
        if batch_size != 'all':
            df = df.tail(batch_size)

        return dcc.send_data_frame(df.to_csv, f"{dataset}_filtered.csv")

for dataset in ["DP26_c", "DP26onsan", "DP37_c", "DP57_c", "DP58_c", "DP58onsan", "DP67_c", "DP72_c",
                    "Zemiglo", "Zemidapa", "Zemimet_50_500mg", "Zemimet_50_1000mg", "Zemimet_25_500mg",
                    "Zemimet_25_1000mg", "Zemilow_50_5mg", "Zemilow_50_10mg", "Zemilow_50_20mg", "Zemimet_25_750mg"]:
    create_download_callback(dataset)

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#     app.run_server(debug=True)

