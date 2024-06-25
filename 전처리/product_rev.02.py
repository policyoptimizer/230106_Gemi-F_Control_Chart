# 아래 3가지 칼럼명을 아래와 같이 영어로 수정
# 제품 > Product 
# 배치 > Batch 
# 불순물(Triester) > Impurity(Triester) 

# Site 라는 칼럼에 온산, 익산 2가지 값이 있는데
# Onsan, Iksan 이렇게 값을 변경함

# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
data = dataiku.Dataset("data_Rev02")
df = data.get_dataframe()

# 칼럼명 영어로 수정
df.rename(columns={'제품': 'Product', '배치': 'Batch', '불순물(Triester)': 'Impurity(Triester)'}, inplace=True)

# Site 값 영어로 수정
df['Site'] = df['Site'].replace({'온산': 'Onsan', '익산': 'Iksan'})

# 제품별 데이터프레임 분리
DP26_df = df[df['Product'] == 'DP26']
DP37_df = df[df['Product'] == 'DP37']
DP57_df = df[df['Product'] == 'DP57']
DP58_df = df[df['Product'] == 'DP58']
DP67_df = df[df['Product'] == 'DP67']
DP72_df = df[df['Product'] == 'DP72']

# Write recipe outputs
DP26 = dataiku.Dataset("DP26")
DP26.write_with_schema(DP26_df)
DP37 = dataiku.Dataset("DP37")
DP37.write_with_schema(DP37_df)
DP57 = dataiku.Dataset("DP57")
DP57.write_with_schema(DP57_df)
DP58 = dataiku.Dataset("DP58")
DP58.write_with_schema(DP58_df)
DP67 = dataiku.Dataset("DP67")
DP67.write_with_schema(DP67_df)
DP72 = dataiku.Dataset("DP72")
DP72.write_with_schema(DP72_df)

