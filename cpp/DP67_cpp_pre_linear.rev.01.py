# 쥬피터 노트북
# 데이터 형태 파악할 때

# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
DP67_cpp_df = dataiku.Dataset("DP67_cpp_df")
DP67_cpp_df_df = DP67_cpp_df.get_dataframe()

print(DP67_cpp_df_df.dtypes)

