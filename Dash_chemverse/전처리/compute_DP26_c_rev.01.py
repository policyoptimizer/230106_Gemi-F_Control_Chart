# 데이터이쿠에서 데이터를 분배하는 새로운 방법
# 제품별로 df 별도로 구성함

```
product : DP72
site : Iksan

DPB-정량01 > Assay
DPB-키랄순도01 > Chiral
DPB-순도(총불순물)01 > Total Impurity
DPB-순도(DP-IMP-1)01 > Impurity-1
DPB-순도(미특정불순물)01 > AUI
DPB-강열잔분01 > ROI

product : DP67
site : Iksan

DPT-순도(총불순물)01 > Total Impurity
DPT-순도(DP-IMP-1)01 > Impurity-1
DPT-순도(미특정불순물)01 > AUI

DP


DPS-함량01 > Assay

DPS-Chiral순도01 > Chiral

DPS-총불순물합01 > Total Impurity

DPS-DP-IMP-101 > Impurity

DPS-DPIMP101 > DP Impurity

DPS-개별불순물01 > Individual Impurity

DPS-강열잔분01 > Residue

DPY-유기부성분총합01 > Total Organic Impurity

DPY-부성분(DP-IMP-1)01 > Impurity

DPY-신규부성분01 > New Impurity

DPF-함량01 > Assay

DPF-Chiral01 > Chiral

DPF-유기부성분총합01 > Total Organic Impurity

NFP0000D-Assay(NMR01 > Assay

NFP0000D-함량01 > Assay

106114-함량01 > Assay

106114-Chiral순도01 > Chiral

BAN-함량01 > Assay

BAN-Chiral순도01 > Chiral

106113-함량01 > Assay

106113-Assay(NMR)01 > Assay

106113-Triester01 > Triester

HFP-NMR01 > NMR

GEM-함량01 > Assay

GEM-총유연물질01 > Related Substances

GEM-DPIMP1유연물질01 > DP IMP Related Substances

GEM-미지개개유연물질01 > Unknown Individual Related Substances

GLA-제미글립틴함량01 > Gemigliptin Assay

GLA-제미총유연물질01 > Gemigliptin Related Substances

GLA-제미DPIMP1유연물질01 > Gemigliptin DPIMP1 Related Substances

GLA-제미미지유연물질01 > Unknown Gemigliptin Related Substances

GMT-제미글립틴함량01 > Gemigliptin Assay

GMT-제미총유연물질01 > Total Gemigliptin Related Substances

GMT-DPIMP1제미유연물질01 > Gemigliptin DPIMP1 Related Substances

GMT-제미미지유연물질01 > Unknown Gemigliptin Related Substances

ZMG-제미글립틴함량01 > Gemigliptin Assay

ZMG-총제미유연물질01 > Total Gemigliptin Related Substances

ZMG-DPIMP1제미유연물질01 > Gemigliptin DPIMP1 Related Substances

ZMJ-제미글립틴함량01 > Gemigliptin Assay01

ZMJ-제미글립틴함량02 > Gemigliptin Assay02

ZMJ-제미총유연물질01 > Total Gemigliptin Related Substances01

ZMJ-DP-IMP-1제미유연물질01 > Gemigliptin DP-IMP-1 Related Substances01

ZMJ-제미미지유연물질01 > Unknown Gemigliptin Related Substances01
```


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


