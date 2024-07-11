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






import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
data_rev03 = dataiku.Dataset("data_rev03")
data_rev03_df = data_rev03.get_dataframe()




# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

DP26_c_df = ... # Compute a Pandas dataframe to write into DP26_c
DP26onsan_df = ... # Compute a Pandas dataframe to write into DP26onsan
DP37_c_df = ... # Compute a Pandas dataframe to write into DP37_c
DP57_c_df = 
DP58_c_df = 
DP58onsan_df = 
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

