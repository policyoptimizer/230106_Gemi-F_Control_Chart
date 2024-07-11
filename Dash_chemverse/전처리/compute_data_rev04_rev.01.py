# 이미 제품별로는 나눴고,
# 이제 중요 시험 항목만 추출함
# 이 때 시험명은 영어로 변경함


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
data_rev03 = dataiku.Dataset("data_rev03")
data_rev03_df = data_rev03.get_dataframe()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

data_rev04_df = data_rev03_df # For this sample code, simply copy input to output


# Write recipe outputs
data_rev04 = dataiku.Dataset("data_rev04")
data_rev04.write_with_schema(data_rev04_df)

