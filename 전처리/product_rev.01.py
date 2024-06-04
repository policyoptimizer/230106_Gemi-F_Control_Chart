# 데이터 셋을 각각의 제품으로 분리

# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
data = dataiku.Dataset("data_Rev02")
df = data.get_dataframe()

# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

DP26_df = df[df['제품'] == 'DP26']
DP37_df = df[df['제품'] == 'DP37']
DP57_df = df[df['제품'] == 'DP57']
DP58_df = df[df['제품'] == 'DP58']
DP67_df = df[df['제품'] == 'DP67']
DP72_df = df[df['제품'] == 'DP72']

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
