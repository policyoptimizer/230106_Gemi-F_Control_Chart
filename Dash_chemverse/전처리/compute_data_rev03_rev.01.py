# -*- coding: utf-8 -*-
import dataiku
import pandas as pd
import numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
tb_insp_result_sample = dataiku.Dataset("tb_insp_result_sample")
tb_insp_result_sample_df = tb_insp_result_sample.get_dataframe()

# 필요한 칼럼만 선택
columns_to_keep = ['batch_no', 'insp_code', 'insp_min_value', 'insp_max_value', 'insp_result_value']
filtered_df = tb_insp_result_sample_df[columns_to_keep]

# product 및 site 컬럼 추가 함수 정의
def add_product_and_site(row):
    batch_no = row['batch_no']
    insp_code = row['insp_code']
   
    if isinstance(batch_no, str):
        if batch_no.startswith('TAP'):
            return 'DP14 Chunbo', 'Onsan'
        elif batch_no.startswith('DPI'):
            return 'DP18', 'Onsan'
        elif batch_no.startswith('AFP'):
            return 'DP26 onsan', 'Onsan'
        elif batch_no.startswith('NFP'):
            return 'DP37', 'Onsan'
        elif batch_no.startswith('DPF'):
            return 'DP57', 'Onsan'
        elif batch_no.startswith('BAN'):
            return 'DP58 onsan', 'Onsan'
        elif batch_no.startswith('DPX'):
            return 'DP60', 'Onsan'
        elif batch_no.startswith('DPC'):
            return 'DP60', 'Iksan'
        elif batch_no.startswith('DPY'):
            return 'DP67', 'Onsan'
        elif batch_no.startswith('DPT'):
            return 'DP67', 'Iksan'
        elif batch_no.startswith('DPS'):
            return 'DP72', 'Onsan'
        elif batch_no.startswith('DPB'):
            return 'DP72', 'Iksan'
        elif batch_no.startswith('GEM'):
            return 'Zemiglo', 'Osong'
        elif batch_no.startswith('GLA'):
            return 'Zemidapa', 'Osong'
        elif batch_no.startswith('GMT'):
            return 'Zemimet 50/500mg', 'Osong'
        elif batch_no.startswith('ZMG'):
            return 'Zemimet 50/1000mg', 'Osong'
        elif batch_no.startswith('ZMJ'):
            return 'Zemimet 25/500mg', 'Osong'
        elif batch_no.startswith('ZMK'):
            return 'Zemimet 25/1000mg', 'Osong'
        elif batch_no.startswith('ZRA'):
            return 'Zemilow 50/5mg', 'Osong'
        elif batch_no.startswith('ZRB'):
            return 'Zemilow 50/10mg', 'Osong'
        elif batch_no.startswith('ZRC'):
            return 'Zemilow 50/20mg', 'Osong'
        elif batch_no.startswith('ZML'):
            return 'Zemimet 25/750mg', 'Osong'
   
    if isinstance(insp_code, str):
        if insp_code.startswith('107310'):
            return 'DP14 Langhua', 'Onsan'
        elif insp_code.startswith('106113'):
            return 'DP26', 'Onsan'
        elif insp_code.startswith('106114'):
            return 'DP58', 'Onsan'
   
    return np.nan, np.nan

# DataFrame에 product 및 site 컬럼 추가
filtered_df[['product', 'site']] = filtered_df.apply(add_product_and_site, axis=1, result_type="expand")

# product가 비어 있는 행 삭제
filtered_df = filtered_df.dropna(subset=['product'])

# Compute recipe outputs from inputs
data_rev03_df = filtered_df

# Write recipe outputs
data_rev03 = dataiku.Dataset("data_rev03")
data_rev03.write_with_schema(data_rev03_df)

