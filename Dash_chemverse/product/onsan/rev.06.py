# 여전히 콜백 함수가 제대로 반영되지 않고 있음

import dataiku
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import re

# app = Dash(__name__)

# 넬슨 법칙 탐지 함수들
def check_rule_1(series, mean, std):
    return (series > mean + 3 * std) | (series < mean - 3 * std)

def check_rule_2(series, mean):
    violations = (series > mean).rolling(window=9).sum().ge(9) | (series < mean).rolling(window=9).sum().ge(9)
    return violations.shift(-8).fillna(False)

def check_rule_3(series):
    increasing = series.diff().gt(0).rolling(window=6).sum().ge(6)
    decreasing = series.diff().lt(0).rolling(window=6).sum().ge(6)
    return increasing.shift(-5).fillna(False) | decreasing.shift(-5).fillna(False)

def check_rule_4(series, mean, std):
    two_std = (series > mean + 2 * std) | (series < mean - 2 * std)
    rule_4_violations = two_std.rolling(window=14).sum().ge(2).astype(bool)
    return rule_4_violations, two_std

def parse_batch_no(batch_no):
    match = re.match(r'([A-Z]+)(\d{2})(\d{2})(\d{2})(\d+)', batch_no)
    if match:
        product_code, year, month, day, seq = match.groups()
        return f"{product_code}{year}{month}{day}{seq.zfill(5)}"
    return batch_no

# 데이터셋 로드 및 그래프 생성 함수
def load_data_and_create_graphs(df, product, insp_code, window_size, sigma_level, recent_batches, trend_threshold, excluded_batches):
    df = df[df['product'] == product]
    df = df[df['insp_code'] == insp_code]

    if excluded_batches:
        df = df[~df['batch_no'].isin(excluded_batches)]

    # 배치 번호 정렬
    df['parsed_batch_no'] = df['batch_no'].apply(parse_batch_no)
    df = df.sort_values(by='parsed_batch_no')

    df['MA'] = df['insp_result_value'].rolling(window=window_size).mean()
    mean = df['insp_result_value'].mean()
    std = df['insp_result_value'].std()
    upper_bound = mean + sigma_level * std
    lower_bound = mean - sigma_level * std
    df['Upper_Bound'] = upper_bound
    df['Lower_Bound'] = lower_bound

    df['Anomaly_Rule1'] = check_rule_1(df['insp_result_value'], mean, std)
    df['Anomaly_Rule2'] = check_rule_2(df['insp_result_value'], mean)
    df['Anomaly_Rule3'] = check_rule_3(df['insp_result_value'])
    rule_4_violations, two_std = check_rule_4(df['insp_result_value'], mean, std)
    df['Anomaly_Rule4'] = rule_4_violations
    df['Two_Std'] = two_std
    df['Normal'] = ~(df['Anomaly_Rule1'] | df['Anomaly_Rule2'] | df['Anomaly_Rule3'] | df['Anomaly_Rule4'])

    trend_fig = px.line(df, x='batch_no', y=['insp_result_value', 'MA'], title=f"{product} - {insp_code} Trend and Moving Average")
    trend_fig.add_trace(go.Scatter(x=df['batch_no'], y=df['Upper_Bound'], mode='lines', name='Upper Bound', line=dict(dash='dash')))
    trend_fig.add_trace(go.Scatter(x=df['batch_no'], y=df['Lower_Bound'], mode='lines', name='Lower Bound', line=dict(dash='dash')))
    trend_fig.add_trace(go.Scatter(x=df['batch_no'], y=[df['insp_min_value'].iloc[0]]*len(df), mode='lines', name='Spec Lower', line=dict(color='blue', dash='dot')))
    trend_fig.add_trace(go.Scatter(x=df['batch_no'], y=[df['insp_max_value'].iloc[0]]*len(df), mode='lines', name='Spec Upper', line=dict(color='red', dash='dot')))

    anomaly_fig = go.Figure()
    anomaly_fig.add_trace(go.Scatter(x=df['batch_no'], y=df['insp_result_value'], mode='markers', name='Normal', marker=dict(color='lightgrey')))
    anomaly_fig.add_trace(go.Scatter(x=df['batch_no'][df['Anomaly_Rule1']], y=df['insp_result_value'][df['Anomaly_Rule1']],
                                     mode='markers', name='Rule 1 Violation', marker=dict(color='red')))
    anomaly_fig.add_trace(go.Scatter(x=df['batch_no'][df['Anomaly_Rule2']], y=df['insp_result_value'][df['Anomaly_Rule2']],
                                     mode='markers', name='Rule 2 Violation', marker=dict(color='purple')))
    anomaly_fig.add_trace(go.Scatter(x=df['batch_no'][df['Anomaly_Rule3']], y=df['insp_result_value'][df['Anomaly_Rule3']],
                                     mode='markers', name='Rule 3 Violation', marker=dict(color='green')))
    anomaly_fig.add_trace(go.Scatter(x=df['batch_no'][df['Two_Std']], y=df['insp_result_value'][df['Two_Std']],
                                     mode='markers', name='Rule 4 Violation (2σ)', marker=dict(color='orange')))
    anomaly_fig.add_trace(go.Scatter(x=df['batch_no'], y=[df['insp_min_value'].iloc[0]]*len(df), mode='lines', name='Spec Lower', line=dict(color='blue', dash='dot')))
    anomaly_fig.add_trace(go.Scatter(x=df['batch_no'], y=[df['insp_max_value'].iloc[0]]*len(df), mode='lines', name='Spec Upper', line=dict(color='red', dash='dot')))

    min_value = df['insp_result_value'].min()
    max_value = df['insp_result_value'].max()
    mean_value = df['insp_result_value'].mean()
    std_value = df['insp_result_value'].std()
    recent_avg = df['insp_result_value'].tail(recent_batches).mean()
    trend_text = "안정" if abs(recent_avg - mean_value) / mean_value < trend_threshold else ("상승" if recent_avg > mean_value else "하락")

    summary_table = html.Table([
        html.Thead(html.Tr([html.Th("항목"), html.Th("결과")], style={'text-align': 'center'})),
        html.Tbody([
            html.Tr([html.Td("경향성 판단", style={'text-align': 'center'}), html.Td(trend_text, style={'text-align': 'center'})]),
            html.Tr([html.Td("최근 n 배치 평균", style={'text-align': 'center'}), html.Td(f"{recent_avg:.2f}", style={'text-align': 'center'})]),
            html.Tr([html.Td("Historical 평균", style={'text-align': 'center'}), html.Td(f"{mean_value:.2f}", style={'text-align': 'center'})]),
            html.Tr([html.Td("Historical 표준편차", style={'text-align': 'center'}), html.Td(f"{std_value:.2f}", style={'text-align': 'center'})]),
            html.Tr([html.Td("Historical 최대", style={'text-align': 'center'}), html.Td(f"{max_value:.2f}", style={'text-align': 'center'})]),
            html.Tr([html.Td("Historical 최소", style={'text-align': 'center'}), html.Td(f"{min_value:.2f}", style={'text-align': 'center'})]),
            html.Tr([html.Td("UCL (조정가능)", style={'text-align': 'center'}), html.Td(f"{upper_bound:.2f}", style={'text-align': 'center'})]),
            html.Tr([html.Td("LCL (조정가능)", style={'text-align': 'center'}), html.Td(f"{lower_bound:.2f}", style={'text-align': 'center'})]),
            html.Tr([html.Td("허용 기준", style={'text-align': 'center'}), html.Td(f"{df['insp_min_value'].iloc[0]} - {df['insp_max_value'].iloc[0]}", style={'text-align': 'center'})])
        ], style={'border': '1px solid black'})
    ], style={'width': '50%', 'margin': 'auto', 'border-collapse': 'collapse', 'border': '1px solid black'})

    return trend_fig, anomaly_fig, summary_table

# 제품별 탭 생성 함수
def create_product_tab(df, product, window_size, sigma_level, recent_batches, trend_threshold):
    insp_codes = df[df['product'] == product]['insp_code'].unique()
    tabs = []
    for insp_code in insp_codes:
        trend_fig, anomaly_fig, summary_table = load_data_and_create_graphs(df, product, insp_code, window_size, sigma_level, recent_batches, trend_threshold, [])
        tabs.append(dcc.Tab(label=insp_code, children=[
            html.Div([
                html.H3(f'{product} - {insp_code} 요약 보고서', id=f'{product}-{insp_code}-summary-title'),
                summary_table,
                html.Div([
                    html.Div([
                        html.Label('최근 배치 수:', style={'margin-right': '15px'}),
                        dcc.Dropdown(
                            id=f'{product}-{insp_code}-recent-batches-dropdown',
                            options=[{'label': f'{i} 배치', 'value': i} for i in [5, 7, 10]],
                            value=recent_batches,
                            clearable=False,
                            style={'margin-right': '60px'}
                        ),
                        html.Label('경향성 판단 Threshold:', style={'margin-right': '15px'}),
                        dcc.Dropdown(
                            id=f'{product}-{insp_code}-trend-threshold-dropdown',
                            options=[{'label': f'{i}%', 'value': i/100} for i in [2, 5, 10]],
                            value=trend_threshold,
                            clearable=False,
                            style={'margin-right': '40px'}
                        ),
                        html.Label('시그마 레벨:', style={'margin-right': '15px'}),
                        dcc.Dropdown(
                            id=f'{product}-{insp_code}-sigma-level-dropdown',
                            options=[{'label': f'{i} 시그마', 'value': i} for i in [1, 2, 3]],
                            value=sigma_level,
                            clearable=False,
                            style={'margin-right': '60px'}
                        )
                    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'flex-wrap': 'wrap', 'margin-bottom': '10px'}),
                    html.Div([
                        html.Label('윈도우 사이즈:', style={'margin-right': '15px'}),
                        dcc.Dropdown(
                            id=f'{product}-{insp_code}-window-size-dropdown',
                            options=[{'label': f'{i} 배치', 'value': i} for i in [5, 10, 15]],
                            value=window_size,
                            clearable=False,
                            style={'margin-right': '40px'}
                        ),
                        html.Label('제외할 배치 번호:', style={'margin-right': '15px'}),
                        dcc.Input(id=f'{product}-{insp_code}-exclude-batches-input', type='text', value='', style={'margin-right': '80px'}),
                        html.Button('적용', id=f'{product}-{insp_code}-apply-button', n_clicks=0)
                    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'flex-wrap': 'wrap'})
                ]),
                dcc.Graph(id=f'{product}-{insp_code}-trend-graph', figure=trend_fig, config={'clickmode': 'event+select'}),
                dcc.Graph(id=f'{product}-{insp_code}-anomaly-graph', figure=anomaly_fig)
            ])
        ]))
    return tabs

# 제품 탭 생성 함수
def create_product_tabs(df, window_size, sigma_level, recent_batches, trend_threshold):
    # 제품명을 지정된 순서대로 정렬
    product_order = ["DP26", "DP26 onsan", "DP37", "DP57", "DP58", "DP58 onsan", "DP67", "DP72"]
    df['product'] = pd.Categorical(df['product'], categories=product_order, ordered=True)
    df = df.sort_values(by='product')  # 제품명으로 정렬
    products = df['product'].unique()

    product_tabs = []
    for product in products:
        product_tabs.append(dcc.Tab(label=product, children=[
            dcc.Tabs(id=f"{product}-tabs", children=create_product_tab(df, product, window_size, sigma_level, recent_batches, trend_threshold))
        ]))
    return product_tabs

# 데이터 로드 및 앱 레이아웃 설정
dataset = dataiku.Dataset("onsan")
df = dataset.get_dataframe()

app.layout = html.Div([
    html.H1('Onsan Site Product Quality Analysis'),
    dcc.Tabs(id="product-tabs", children=create_product_tabs(df, 5, 1, 5, 0.02)),
    html.Div([
        html.H3('넬슨 법칙'),
        html.P('Rule 1: 데이터 포인트가 평균으로부터 3 표준편차 이상 벗어날 때.'),
        html.P('Rule 2: 연속 9개의 데이터 포인트가 모두 평균보다 클 때 또는 작을 때.'),
        html.P('Rule 3: 연속 6개의 데이터 포인트가 계속 증가하거나 감소할 때.'),
        html.P('Rule 4: 연속 14개의 데이터 포인트 중 두 개 이상이 평균으로부터 2 표준편차 이상 벗어날 때.')
    ], style={'margin-top': '20px', 'text-align': 'left'})
])

# 콜백 함수 생성기
def generate_callback(product, insp_code):
    @app.callback(
        [Output(f'{product}-{insp_code}-trend-graph', 'figure'),
         Output(f'{product}-{insp_code}-anomaly-graph', 'figure'),
         Output(f'{product}-{insp_code}-summary-title', 'children')],
        [Input(f'{product}-{insp_code}-apply-button', 'n_clicks')],
        [State(f'{product}-{insp_code}-recent-batches-dropdown', 'value'),
         State(f'{product}-{insp_code}-trend-threshold-dropdown', 'value'),
         State(f'{product}-{insp_code}-sigma-level-dropdown', 'value'),
         State(f'{product}-{insp_code}-window-size-dropdown', 'value'),
         State(f'{product}-{insp_code}-exclude-batches-input', 'value')]
    )
    def update_graphs(n_clicks, recent_batches, trend_threshold, sigma_level, window_size, exclude_batches):
        exclude_batches_list = [batch.strip() for batch in exclude_batches.split(',')] if exclude_batches else []
        trend_fig, anomaly_fig, summary_table = load_data_and_create_graphs(df, product, insp_code, window_size, sigma_level, recent_batches, trend_threshold, exclude_batches_list)
        return trend_fig, anomaly_fig, summary_table

    return update_graphs

# 모든 제품과 검사 코드에 대해 콜백 등록
products = df['product'].unique()
for product in products:
    insp_codes = df[df['product'] == product]['insp_code'].unique()
    for insp_code in insp_codes:
        app.callback(
            [Output(f'{product}-{insp_code}-trend-graph', 'figure'),
             Output(f'{product}-{insp_code}-anomaly-graph', 'figure'),
             Output(f'{product}-{insp_code}-summary-title', 'children')],
            [Input(f'{product}-{insp_code}-apply-button', 'n_clicks')],
            [State(f'{product}-{insp_code}-recent-batches-dropdown', 'value'),
             State(f'{product}-{insp_code}-trend-threshold-dropdown', 'value'),
             State(f'{product}-{insp_code}-sigma-level-dropdown', 'value'),
             State(f'{product}-{insp_code}-window-size-dropdown', 'value'),
             State(f'{product}-{insp_code}-exclude-batches-input', 'value')]
        )(generate_callback(product, insp_code))

# 서버 실행 (Dataiku 웹앱에서는 이 부분을 제외합니다)
# if __name__ == '__main__':
#     app.run_server(debug=True)

