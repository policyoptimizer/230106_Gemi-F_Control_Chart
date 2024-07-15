# 데이터이쿠에서 데이터를 분배하는 새로운 방법
# 제품별로 나눴음

# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
data_rev04 = dataiku.Dataset("data_rev04")
data_rev04_df = data_rev04.get_dataframe()

# Function to filter dataframe by product
def filter_dataframe_by_product(df, product):
    return df[df['product'] == product]

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

# Create dataframes for each product and write to corresponding datasets
for product, dataset_name in product_dataset_mapping.items():
    product_df = filter_dataframe_by_product(data_rev04_df, product)
    dataset = dataiku.Dataset(dataset_name)
    dataset.write_with_schema(product_df)
