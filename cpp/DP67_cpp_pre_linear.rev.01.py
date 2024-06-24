# -*- coding: utf-8 -*-
import dataiku
from dataiku import pandasutils as pdu
import pandas as pd

# Read input dataset
dp67_cpp_df = dataiku.Dataset("DP67_cpp_df")
dp67_cpp_df_df = dp67_cpp_df.get_dataframe()

# Drop unnecessary columns
columns_to_drop = ['Sample', 'CollectionDate', 'DS', 'Appearance', 'IR Identification']
dp67_cpp_df_df = dp67_cpp_df_df.drop(columns=columns_to_drop)

# Check for missing values
print("Missing values:")
print(dp67_cpp_df_df.isnull().sum())

# Fill missing values with the mean of each column
dp67_cpp_df_df = dp67_cpp_df_df.fillna(dp67_cpp_df_df.mean())

# Normalize/Standardize the data if necessary
# from sklearn.preprocessing import StandardScaler
# scaler = StandardScaler()
# dp67_cpp_df_df_scaled = pd.DataFrame(scaler.fit_transform(dp67_cpp_df_df), columns=dp67_cpp_df_df.columns)

# For this example, we will use the raw data without normalization/standardization

# Write preprocessed dataset for further analysis
dp67_cpp_linear = dataiku.Dataset("DP67_cpp_linear")
dp67_cpp_linear.write_with_schema(dp67_cpp_df_df)

