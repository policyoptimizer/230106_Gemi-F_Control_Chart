# 각 제품을
# batch_no 를 기준으로 오름차순으로 정렬

# DP26_c
# 예) Y200106004, M220621012 등
# Y or M 이후 두 자리는 년도임
# Y 로 시작하는 배치를 먼저 배치해주고, 그 다음 M 으로 시작하는 배치를 정렬
# Y or M 으로 시작하지 않는 다른 형식의 배치는 테스트 배치이므로 삭제

# DP26onsan
# 예) HFP24001
# HFP로 배치가 시작하고,
# HFP 이후 2자리는 년도임

# DP37_c
# 예) NFP20002

# DP57_c
# 예) DPF18001

# DP58_c
# 예) Y190614008, M220622003
# Y 로 시작하는 배치를 먼저 배치해주고, 그 다음 M 으로 시작하는 배치를 정렬
# Y or M 으로 시작하지 않는 다른 형식의 배치는 테스트 배치이므로 삭제

# DP58onsan
# 예) BAN24001 형식

# DP67_c
# 예) DPT15001, DPY23024
# DPTxxxxx 를 먼저 배치해주고, 그 다음 DPYxxxxx 배치를 정렬

# DP72_c
# 예) DPB15001

# Zemiglo
# 예) GEM15740A, GEM17536 등
# 오름차순으로 정렬

# Zemidapa
# 예) GLA22501

# Zemimet_50_500mg
# 예) GMT17544

# Zemimet_50_1000mg
# 예) ZMG19564A

# Zemimet_25_500mg
# 예) ZMJ18546

# Zemimet_25_1000mg
# 예) ZMK19501

# Zemilow_50_5mg
# 예) ZRA19501

# Zemilow_50_10mg
# 예) ZRB19501

# Zemilow_50_20mg
# 예) ZRC20501

# Zemimet_25_750mg
# 예) ZML23501


# -*- coding: utf-8 -*-
import dataiku
import pandas as pd
import numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
data_rev04 = dataiku.Dataset("data_rev04")
data_rev04_df = data_rev04.get_dataframe()

# Function to filter dataframe by product
def filter_dataframe_by_product(df, product):
    return df[df['product'] == product]

# Function to sort dataframe by batch number
def sort_dataframe_by_batch(df):
    def batch_sort_key(batch_no):
        if batch_no.startswith('Y'):
            return (0, batch_no)
        elif batch_no.startswith('M'):
            return (1, batch_no)
        else:
            return (2, batch_no)
    df_sorted = df.copy()
    df_sorted['sort_key'] = df_sorted['batch_no'].apply(batch_sort_key)
    df_sorted = df_sorted.sort_values('sort_key').drop('sort_key', axis=1)
    return df_sorted

# List of products and corresponding dataset names
product_dataset_mapping = {
    'DP26': 'DP26_c',
    'DP26 onsan': 'DP26onsan',
    'DP37': 'DP37_c',
    'DP57': 'DP57_c',
    'DP58': 'DP58_c',
    'DP58 onsan': 'DP58onsan',
    'DP67': 'DP67_c',
    'DP72': 'DP72_c',
    'Zemiglo': 'Zemiglo',
    'Zemidapa': 'Zemidapa',
    'Zemimet 50/500mg': 'Zemimet_50_500mg',
    'Zemimet 50/1000mg': 'Zemimet_50_1000mg',
    'Zemimet 25/500mg': 'Zemimet_25_500mg',
    'Zemimet 25/1000mg': 'Zemimet_25_1000mg',
    'Zemilow 50/5mg': 'Zemilow_50_5mg',
    'Zemilow 50/10mg': 'Zemilow_50_10mg',
    'Zemilow 50/20mg': 'Zemilow_50_20mg',
    'Zemimet 25/750mg': 'Zemimet_25_750mg'
}

# Create dataframes for each product, sort them, and write to corresponding datasets
for product, dataset_name in product_dataset_mapping.items():
    product_df = filter_dataframe_by_product(data_rev04_df, product)
    product_df_sorted = sort_dataframe_by_batch(product_df)
    dataset = dataiku.Dataset(dataset_name)
    dataset.write_with_schema(product_df_sorted)

