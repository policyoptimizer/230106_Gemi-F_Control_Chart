# 일부 구현됨

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# from statsmodels.tsa.arima.model import ARIMA
import dataiku

data_Rev02 = dataiku.Dataset("data_Rev02")
data_Rev02_df = data_Rev02.get_dataframe()

# 각 제품별 데이터 프레임을 딕셔너리로 저장
dataframes = {
   'DP26': data_Rev02_df[data_Rev02_df['제품'] == 'DP26'],
   'DP37': data_Rev02_df[data_Rev02_df['제품'] == 'DP37'],
   'DP57': data_Rev02_df[data_Rev02_df['제품'] == 'DP57'],
   'DP58': data_Rev02_df[data_Rev02_df['제품'] == 'DP58'],
   'DP67': data_Rev02_df[data_Rev02_df['제품'] == 'DP67'],
   'DP72': data_Rev02_df[data_Rev02_df['제품'] == 'DP72']
}

# 스트림릿 앱 제목 설정
st.title('제품 품질 관리 대시보드')

# 서브플롯 설정 (24행 3열, 여기서는 샘플로 줄여 표시)
fig, axes = plt.subplots(nrows=len(dataframes), ncols=3, figsize=(45, 15))
axes = axes.flatten()

# 시각화 로직 구현 (데이터프레임을 참조하여 차트 생성)
for i, (name, df) in enumerate(dataframes.items()):
   # 간단한 데이터 표시
   st.write(f"데이터 미리보기 - {name}", df.head())
   
   # 차트 그리기
   fig, ax = plt.subplots()
   ax.plot(df['배치'], df['Assay'], marker='o', linestyle='-')
   ax.set_title(f"{name} - Assay")
   ax.set_xlabel('Batch')
   ax.set_ylabel('Assay')
   st.pyplot(fig)

plt.tight_layout()
st.pyplot()
