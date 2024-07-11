# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
data_rev03 = dataiku.Dataset("data_rev03")
data_rev03_df = data_rev03.get_dataframe()




# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

DP14Chunbo_df = ... # Compute a Pandas dataframe to write into DP14Chunbo
DP14Langhua_df = ... # Compute a Pandas dataframe to write into DP14Langhua
DP18_c_df = ... # Compute a Pandas dataframe to write into DP18_c
DP26_c_df = ... # Compute a Pandas dataframe to write into DP26_c
DP26onsan_df = ... # Compute a Pandas dataframe to write into DP26onsan
DP37_c_df = ... # Compute a Pandas dataframe to write into DP37_c
DP57_c_df = 
DP58_c_df = 
DP58onsan_df = 
DP60_df = 
DP67_c_df = 
DP72_c_df = 
Zemiglo_df = 
Zemidapa_df = 
Zemimet_50_500mg_df = 
Zemimet_50_1000mg_df = 
Zemimet_25_500mg_df = 
Zemimet_25_1000mg_df = 
Zemilow_50_5mg_df = 
Zemilow_50_10mg_df = 
Zemilow_50_20mg_df = 
Zemimet_25_750mg_df = 



# Write recipe outputs
DP14Chunbo = dataiku.Dataset("DP14Chunbo")
DP14Chunbo.write_with_schema(DP14Chunbo_df)
DP14Langhua = dataiku.Dataset("DP14Langhua")
DP14Langhua.write_with_schema(DP14Langhua_df)
DP18_c = dataiku.Dataset("DP18_c")
DP18_c.write_with_schema(DP18_c_df)
DP26_c = dataiku.Dataset("DP26_c")
DP26_c.write_with_schema(DP26_c_df)
DP26onsan = dataiku.Dataset("DP26onsan")
DP26onsan.write_with_schema(DP26onsan_df)
DP37_c = dataiku.Dataset("DP37_c")
DP37_c.write_with_schema(DP37_c_df)
DP57_c = dataiku.Dataset("DP57_c")
DP57_c.write_with_schema(DP57_c_df)
DP58_c = dataiku.Dataset("DP58_c")
DP58_c.write_with_schema(DP58_c_df)
DP58onsan = dataiku.Dataset("DP58onsan")
DP58onsan.write_with_schema(DP58onsan_df)
DP60 = dataiku.Dataset("DP60")
DP60.write_with_schema(DP60_df)
DP67_c = dataiku.Dataset("DP67_c")
DP67_c.write_with_schema(DP67_c_df)
DP72_c = dataiku.Dataset("DP72_c")
DP72_c.write_with_schema(DP72_c_df)
Zemiglo = dataiku.Dataset("Zemiglo")
Zemiglo.write_with_schema(Zemiglo_df)
Zemidapa = dataiku.Dataset("Zemidapa")
Zemidapa.write_with_schema(Zemidapa_df)
Zemimet_50_500mg = dataiku.Dataset("Zemimet_50_500mg")
Zemimet_50_500mg.write_with_schema(Zemimet_50_500mg_df)
Zemimet_50_1000mg = dataiku.Dataset("Zemimet_50_1000mg")
Zemimet_50_1000mg.write_with_schema(Zemimet_50_1000mg_df)
Zemimet_25_500mg = dataiku.Dataset("Zemimet_25_500mg")
Zemimet_25_500mg.write_with_schema(Zemimet_25_500mg_df)
Zemimet_25_1000mg = dataiku.Dataset("Zemimet_25_1000mg")
Zemimet_25_1000mg.write_with_schema(Zemimet_25_1000mg_df)
Zemilow_50_5mg = dataiku.Dataset("Zemilow_50_5mg")
Zemilow_50_5mg.write_with_schema(Zemilow_50_5mg_df)
Zemilow_50_10mg = dataiku.Dataset("Zemilow_50_10mg")
Zemilow_50_10mg.write_with_schema(Zemilow_50_10mg_df)
Zemilow_50_20mg = dataiku.Dataset("Zemilow_50_20mg")
Zemilow_50_20mg.write_with_schema(Zemilow_50_20mg_df)
Zemimet_25_750mg = dataiku.Dataset("Zemimet_25_750mg")
Zemimet_25_750mg.write_with_schema(Zemimet_25_750mg_df)

