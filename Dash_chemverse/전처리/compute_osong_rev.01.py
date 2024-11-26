# data_rev04 의 복잡한 데이터 셋을 오송, 익산, 온산 3가지로 나누기

# -*- coding: utf-8 -*-
import dataiku
import pandas as pd
from dataiku import pandasutils as pdu

# Read recipe inputs
data_rev04 = dataiku.Dataset("data_rev04")
data_rev04_df = data_rev04.get_dataframe()

# Compute recipe outputs
# Osong, Iksan, Onsan 데이터셋으로 나누기
osong_df = data_rev04_df[data_rev04_df['site'] == 'Osong']
iksan_df = data_rev04_df[data_rev04_df['site'] == 'Iksan']
onsan_df = data_rev04_df[data_rev04_df['site'] == 'Onsan']

# Write recipe outputs
osong = dataiku.Dataset("osong")
osong.write_with_schema(osong_df)
iksan = dataiku.Dataset("iksan")
iksan.write_with_schema(iksan_df)
onsan = dataiku.Dataset("onsan")
onsan.write_with_schema(onsan_df)

