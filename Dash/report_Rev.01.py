# 우선 보고서 넣기

import plotly.express as px
import dataiku
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Dash 앱 인스턴스 생성 
# 이쿠에서는 하면 안됨
# app = dash.Dash(__name__)

# 여러 데이터셋 로드
datasets = {
 "DP26_Assay": dataiku.Dataset("DP26_Assay").get_dataframe(),
 "DP26_Triester": dataiku.Dataset("DP26_Triester").get_dataframe(),
 "DP37_Assay": dataiku.Dataset("DP37_Assay").get_dataframe(),
 "DP57_Assay": dataiku.Dataset("DP57_Assay").get_dataframe(),
 "DP57_Chiral": dataiku.Dataset("DP57_Chiral").get_dataframe(),
 "DP57_Total_Impurity": dataiku.Dataset("DP57_Total_Impurity").get_dataframe(),    
 "DP58_Assay": dataiku.Dataset("DP58_Assay").get_dataframe(),    
 "DP58_Chiral": dataiku.Dataset("DP58_Chiral").get_dataframe(),
 "DP67_AUI": dataiku.Dataset("DP67_AUI").get_dataframe(),
 "DP67_Total_Impurity": dataiku.Dataset("DP67_Total_Impurity").get_dataframe(),    
 "DP72_Assay": dataiku.Dataset("DP72_Assay").get_dataframe(),
 "DP72_Chiral": dataiku.Dataset("DP72_Chiral").get_dataframe(),
 "DP72_AUI": dataiku.Dataset("DP72_AUI").get_dataframe(),
 "DP72_Total_Impurity": dataiku.Dataset("DP72_Total_Impurity").get_dataframe(),    
 "DP72_ROI": dataiku.Dataset("DP72_ROI").get_dataframe(),
 "DP72_Impurity-1": dataiku.Dataset("DP72_Impurity-1").get_dataframe()
}

# 각 데이터셋에 대한 그래프 생성 함수
def create_figure(dataframe, x, y, title, color):
 return px.bar(dataframe, x=x, y=y, title=title, color=color)

# 각 데이터셋에 대한 그래프 생성
figures = {
 "DP26_Assay": create_figure(datasets["DP26_Assay"], '배치', 'Assay', 'DP26 Assay by Batch', 'Site'),
 "DP26_Triester": create_figure(datasets["DP26_Triester"], '배치', '불순물(Triester)', 'DP26 Triester by Batch', 'Site'),
 "DP37_Assay": create_figure(datasets["DP37_Assay"], '배치', 'Assay', 'DP37 Assay by Batch', 'Site'),
 "DP57_Assay": create_figure(datasets["DP57_Assay"], '배치', 'Assay', 'DP57 Assay by Batch', 'Site'),
 "DP57_Chiral": create_figure(datasets["DP57_Chiral"], '배치', 'Chiral', 'DP57 Chiral by Batch', 'Site'),
 "DP57_Total_Impurity": create_figure(datasets["DP57_Total_Impurity"], '배치', 'Total Impurity', 'DP57 Total Impurity by Batch', 'Site'),
 "DP58_Assay": create_figure(datasets["DP58_Assay"], '배치', 'Assay', 'DP58 Assay by Batch', 'Site'),    
 "DP58_Chiral": create_figure(datasets["DP58_Chiral"], '배치', 'Chiral', 'DP58 Chiral by Batch', 'Site'),
 "DP67_AUI": create_figure(datasets["DP67_AUI"], '배치', 'AUI', 'DP67 AUI by Batch', 'Site'),
 "DP67_Total_Impurity": create_figure(datasets["DP67_Total_Impurity"], '배치', 'Total Impurity', 'DP67 Total Impurity by Batch', 'Site'),
 "DP72_Assay": create_figure(datasets["DP72_Assay"], '배치', 'Assay', 'DP72 Assay by Batch', 'Site'),
 "DP72_Chiral": create_figure(datasets["DP72_Chiral"], '배치', 'Chiral', 'DP72 Chiral by Batch', 'Site'),
 "DP72_AUI": create_figure(datasets["DP72_AUI"], '배치', 'AUI', 'DP72 AUI by Batch', 'Site'),
 "DP72_Total_Impurity": create_figure(datasets["DP72_Total_Impurity"], '배치', 'Total Impurity', 'DP72 Total Impurity by Batch', 'Site'),
 "DP72_ROI": create_figure(datasets["DP72_ROI"], '배치', 'ROI', 'DP72 ROI by Batch', 'Site'),
 "DP72_Impurity-1": create_figure(datasets["DP72_Impurity-1"], '배치', 'Impurity-1', 'DP72 Impurity-1 by Batch', 'Site')
}

# 앱 레이아웃 설정
app.layout = html.Div([
 html.H1('Data Analysis Dashboard'),
 dcc.Tabs(id="tabs", children=[
     dcc.Tab(label='DP26', children=[
         html.Div([
             html.H3('Assay Analysis'),
             dcc.Graph(id='dp26-assay-graph', figure=figures["DP26_Assay"])
         ]),
         html.Div([
             html.H3('Triester Analysis'),
             dcc.Graph(id='dp26-triester-graph', figure=figures["DP26_Triester"])
         ])
     ]),
     dcc.Tab(label='DP37', children=[
         html.Div([
             html.H3('Assay Analysis'),
             dcc.Graph(id='dp37-assay-graph', figure=figures["DP37_Assay"])
         ])
     ]),
     dcc.Tab(label='DP57', children=[
         html.Div([
             html.H3('Assay Analysis'),
             dcc.Graph(id='dp57-assay-graph', figure=figures["DP57_Assay"])
         ]),
         html.Div([
             html.H3('Chiral Analysis'),
             dcc.Graph(id='dp57-chiral-graph', figure=figures["DP57_Chiral"])
         ]),
         html.Div([
             html.H3('Total Impurity Analysis'),
             dcc.Graph(id='dp57-total-impurity-graph', figure=figures["DP57_Total_Impurity"])
         ])
     ]),
     dcc.Tab(label='DP58', children=[
         html.Div([
             html.H3('Assay Analysis'),
             dcc.Graph(id='dp58-assay-graph', figure=figures["DP58_Assay"])
         ]),
         html.Div([
             html.H3('Chiral Analysis'),
             dcc.Graph(id='dp58-chiral-graph', figure=figures["DP58_Chiral"])
         ])
     ]),
     dcc.Tab(label='DP67', children=[
         html.Div([
             html.H3('AUI Analysis'),
             dcc.Graph(id='dp67-aui-graph', figure=figures["DP67_AUI"])
         ]),
         html.Div([
             html.H3('Total Impurity Analysis'),
             dcc.Graph(id='dp67-total-impurity-graph', figure=figures["DP67_Total_Impurity"])
         ])
     ]),
     dcc.Tab(label='DP72', children=[
         html.Div([
             html.H3('Assay Analysis'),
             dcc.Graph(id='dp72-assay-graph', figure=figures["DP72_Assay"])
         ]),
         html.Div([
             html.H3('Chiral Analysis'),
             dcc.Graph(id='dp72-chiral-graph', figure=figures["DP72_Chiral"])
         ]),
         html.Div([
             html.H3('AUI Analysis'),
             dcc.Graph(id='dp72-aui-graph', figure=figures["DP72_AUI"])
         ]),
         html.Div([
             html.H3('Total Impurity Analysis'),
             dcc.Graph(id='dp72-total-impurity-graph', figure=figures["DP72_Total_Impurity"])
         ]),
         html.Div([
             html.H3('ROI Analysis'),
             dcc.Graph(id='dp72-roi-graph', figure=figures["DP72_ROI"])
         ]),
         html.Div([
             html.H3('Impurity-1 Analysis'),
             dcc.Graph(id='dp72-impurity-1-graph', figure=figures["DP72_Impurity-1"])
         ])
     ])
 ])
])

# 서버 설정 (이쿠에서는 불필요함)
# if __name__ == '__main__':
# app.run_server(debug=True)
