# trend_Rev.04.py 
# 코드가 기존꺼보다 좀 더 간결함 
# 이거 참고해서 좀 더 develop 하든동

import dataiku
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# Dash 앱 인스턴스 생성
# app = Dash(__name__)

# 데이터셋 이름 목록
datasets_names = [
   "DP26_Assay", "DP26_Triester", "DP37_Assay", "DP57_Assay", "DP57_Chiral",
   "DP57_Total_Impurity", "DP58_Assay", "DP58_Chiral", "DP67_AUI", "DP67_Total_Impurity",
   "DP72_Assay", "DP72_Chiral", "DP72_AUI", "DP72_Total_Impurity", "DP72_ROI", "DP72_Impurity-1"
]

# 데이터셋 로드 및 그래프 생성
graphs = []
for dataset_name in datasets_names:
   dataset = dataiku.Dataset(dataset_name)
   df = dataset.get_dataframe()
   # 배치와 주요 측정치(예시: Assay, Chiral 등)를 기준으로 막대 그래프 생성
   # 여기서는 '배치'와 'Assay'를 예시로 사용하며, 실제 데이터에 따라 적절한 필드명을 사용해야 합니다.
   if '배치' in df.columns and df.columns[-1] in df.columns:  # 마지막 컬럼을 측정치로 가정
       graph = px.bar(df, x='배치', y=df.columns[-1], title=f"{dataset_name} by Batch")
       graphs.append(dcc.Graph(figure=graph))

# 앱 레이아웃 설정
app.layout = html.Div([
   html.H1("Dataiku Datasets Visualization"),
   html.Div(graphs)
])

# # 서버 실행
# if __name__ == '__main__':
#    app.run_server(debug=True)

