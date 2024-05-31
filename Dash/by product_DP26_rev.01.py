import dataiku
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
​
# Dash 앱 인스턴스 생성
app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
​
# 데이터셋 이름과 해당 제품 매핑
product_datasets = {
   "DP26": ["DP26_Assay", "DP26_Triester"],
   "DP37": ["DP37_Assay"],
   "DP57": ["DP57_Assay", "DP57_Chiral", "DP57_Total_Impurity"],
   "DP58": ["DP58_Assay", "DP58_Chiral"],
   "DP67": ["DP67_AUI", "DP67_Total_Impurity"],
   "DP72": ["DP72_Assay", "DP72_Chiral", "DP72_AUI", "DP72_Total_Impurity", "DP72_ROI", "DP72_Impurity-1"]
}
​
# 데이터셋 로드 및 그래프 생성 함수
def create_figure(dataset_name):
   dataset = dataiku.Dataset(dataset_name)
   df = dataset.get_dataframe()
   figure = px.bar(df, x='batch', y=df.columns[-1], title=f"{dataset_name} by Batch")
   return figure
​
# 대시보드 탭 구성
tabs_children = []
for product, datasets in product_datasets.items():
   product_tabs = []
   for dataset in datasets:
       figure = create_figure(dataset)
       tab = dcc.Tab(label=dataset, children=[
           html.Div([
               dcc.Graph(figure=figure)
           ])
       ])
       product_tabs.append(tab)
​
   product_tab = dcc.Tab(label=product, children=[
       html.Div([
           dcc.Tabs(id=f"{product}-tabs", children=product_tabs)
       ])
   ])
   tabs_children.append(product_tab)
​
# 앱 레이아웃 설정
app.layout = html.Div([
   html.H1('Data Analysis Dashboard by Product and Test'),
   dcc.Tabs(id="main-tabs", children=tabs_children)
])
​
# 서버 실행 (Dataiku 웹앱에서 이 부분은 제외)
if __name__ == '__main__':
   app.run_server(debug=True)
​​
