# 좀 더 상세하게 Rule 1,2,3,4 구성됨

import dataiku
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

# 데이터셋 이름 목록
dataset_names = [
 "DP26_Assay", "DP26_Triester", "DP37_Assay", "DP57_Assay", "DP57_Chiral",
 "DP57_Total_Impurity", "DP58_Assay", "DP58_Chiral", "DP67_AUI", "DP67_Total_Impurity",
 "DP72_Assay", "DP72_Chiral", "DP72_AUI", "DP72_Total_Impurity", "DP72_ROI", "DP72_Impurity-1"
]

# 넬슨 법칙 탐지 함수
def check_nelson_rules(series):
   mean = series.mean()
   std = series.std()
   rule1 = (series > mean + 3 * std) | (series < mean - 3 * std)
   rule2 = (series > mean).rolling(window=9).sum().ge(9) | (series < mean).rolling(window=9).sum().ge(9)
   rule3 = series.diff().gt(0).rolling(window=6).sum().ge(6) | series.diff().lt(0).rolling(window=6).sum().ge(6)
   two_std = (series > mean + 2 * std) | (series < mean - 2 * std)
   rule4 = two_std.rolling(window=14).apply(lambda x: np.sum(x) >= 2, raw=True).fillna(0).astype(bool)
   return rule1, rule2, rule3, rule4

# 데이터와 그래프를 로드하는 함수
def load_data_and_create_graphs(dataset_name):
   # 데이터셋 로드
   dataset = dataiku.Dataset(dataset_name)
   df = dataset.get_dataframe()

   column_name = df.columns[-1]  # 데이터셋의 마지막 컬럼을 측정치로 가정
   series = df[column_name]
   
   # ARIMA 모델을 사용하여 예측 추가
   model = ARIMA(series, order=(1, 1, 1))
   model_fit = model.fit()
   df['Forecast'] = model_fit.predict(start=0, end=len(df) - 1, typ='levels')
   
   # 넬슨 규칙 적용
   rule1, rule2, rule3, rule4 = check_nelson_rules(series)
   df['Rule1'] = rule1
   df['Rule2'] = rule2
   df['Rule3'] = rule3
   df['Rule4'] = rule4
   
   # 이상치 탐지를 위한 그래프 생성
   fig = px.scatter(df, x=df.index, y=column_name, color=np.select([rule1, rule2, rule3, rule4],
                               ['Rule1', 'Rule2', 'Rule3', 'Rule4'], default='No Anomaly'),
                    title=f"{dataset_name} - Nelson Rules Anomaly Detection")
   fig.update_traces(marker_size=10)
   return fig

# 앱 레이아웃 설정
# app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
tabs_children = [dcc.Tab(label=name, children=[dcc.Graph(figure=load_data_and_create_graphs(name))]) for name in dataset_names]
app.layout = html.Div([
   html.H1('Data Analysis with Statistical Methods Across Multiple Datasets'),
   dcc.Tabs(id="tabs", children=tabs_children)
])

# 서버 실행
# if __name__ == '__main__':
#    app.run_server(debug=True)
