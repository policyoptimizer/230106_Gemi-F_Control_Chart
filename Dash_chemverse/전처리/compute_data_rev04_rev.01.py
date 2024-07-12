# 이미 제품별로는 나눴고,
# 이제 중요 시험 항목만 추출함
# 이 때 시험명은 영어로 변경함

```
site : Iksan
product : DP72

DPB-정량01 > Assay
DPB-키랄순도01 > Chiral
DPB-순도(총불순물)01 > Total Impurity
DPB-순도(DP-IMP-1)01 > IMP-1
DPB-순도(미특정불순물)01 > AUI
DPB-강열잔분01 > ROI

site : Iksan
product : DP67

DPT-순도(총불순물)01 > Total Impurity
DPT-순도(DP-IMP-1)01 > IMP-1
DPT-순도(미특정불순물)01 > AUI

site : Onsan
product : DP72

DPS-함량01 > Assay
DPS-Chiral순도01 > Chiral
DPS-총불순물합01 > Total Impurity
DPS-DP-IMP-101 > IMP-1
DPS-DPIMP101 > IMP-1
DPS-개별불순물01 > AUI
DPS-강열잔분01 > ROI

site : Onsan
product : DP67

DPY-유기부성분총합01 > Total Impurity
DPY-부성분(DP-IMP-1)01 > IMP-1
DPY-신규부성분01 > AUI

site : Onsan
product : DP57

DPF-함량01 > Assay
DPF-Chiral01 > Chiral
DPF-유기부성분총합01 > Total Impurity

site : Onsan
product : DP37

NFP0000D-Assay(NMR01 > Assay
NFP0000D-함량01 > Assay

site : Onsan
product : DP58
               
106114-함량01 > Assay
106114-Chiral순도01 > Chiral

site : Onsan
product : DP58 onsan

BAN-함량01 > Assay
BAN-Chiral순도01 > Chiral

site : Onsan
product : DP26

106113-Assay(NMR)01 > Assay
106113-함량01 > Assay
106113-Triester01 > Impurity(Triester)

site : Onsan
product : DP26 onsan

HFP-NMR01 > Assay
HFP-Triester01 > Impurity(Triester)

site : Osong
product : Zemiglo

GEM-함량01 > Assay
GEM-총유연물질01 > Total Impurity
GEM-DPIMP1유연물질01 > IMP-1
GEM-미지개개유연물질01 > AUI

site : Osong
product : Zemidapa

GLA-제미글립틴함량01 > Assay
GLA-제미총유연물질01 > Total Impurity
GLA-제미DPIMP1유연물질01 > IMP-1
GLA-제미미지유연물질01 > AUI

site : Osong
product : Zemimet 50/500mg

GMT-제미글립틴함량01 > Assay
GMT-제미총유연물질01 > Total Impurity
GMT-DPIMP1제미유연물질01 > IMP-1
GMT-제미미지유연물질01 > AUI

site : Osong
product : Zemimet 50/1000mg

ZMG-제미글립틴함량01 > Assay
ZMG-총제미유연물질01 > Total Impurity
ZMG-DPIMP1제미유연물질01 > IMP-1
ZMG-미지제미유연물질01 > AUI

site : Osong
product : Zemimet 25/500mg

ZMJ-제미글립틴함량01 > Assay
ZMJ-제미글립틴함량02 > Assay
ZMJ-제미총유연물질01 > Total Impurity
ZMJ-DP-IMP-1제미유연물질01 > IMP-1
ZMJ-제미미지유연물질01 > AUI

site : Osong
product : Zemimet 25/1000mg

ZMK-제미글립틴함량01 > Assay
ZMK-제미총유연물질01 > Total Impurity
ZMK-제미DPIMP1유연물질01 > IMP-1
ZMK-제미미지유연물질01 > AUI

site : Osong
product : Zemilow 50/5mg

ZRA-제미글립틴함량01 > Assay
ZRA-총유연물질01 > Total Impurity
ZRA-DPIMP1제미유연물질01 > IMP-1
ZRA-미지유연물질01 > AUI

site : Osong
product : Zemilow 50/10mg

ZRB-제미글립틴함량01 > Assay
ZRB-총유연물질01 > Total Impurity
ZRB-DPIMP1제미유연물질01 > IMP-1
ZRB-미지유연물질01 > AUI

site : Osong
product : Zemilow 50/20mg

ZRC-제미글립틴함량01 > Assay
ZRC-총유연물질01 > Total Impurity
ZRC-DPIMP1제미유연물질01 > IMP-1
ZRC-미지유연물질01 > AUI

site : Osong
product : Zemimet 25/750mg

ZML-제미글립틴함량01 > Assay
ZML-제미총유연물질01 > Total Impurity
ZML-제미DPIMP1유연물질01 > IMP-1
ZML-제미미지유연물질01 > AUI
```

#################################################################

# -*- coding: utf-8 -*-
import dataiku
import pandas as pd
import numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
data_rev03 = dataiku.Dataset("data_rev03")
data_rev03_df = data_rev03.get_dataframe()

# Define mapping for insp_code based on site and product
insp_code_mapping = {
    ('Iksan', 'DP72'): {
        'DPB-정량01': 'Assay',
        'DPB-키랄순도01': 'Chiral',
        'DPB-순도(총불순물)01': 'Total Impurity',
        'DPB-순도(DP-IMP-1)01': 'IMP-1',
        'DPB-순도(미특정불순물)01': 'AUI',
        'DPB-강열잔분01': 'ROI'
    },
    ('Iksan', 'DP67'): {
        'DPT-순도(총불순물)01': 'Total Impurity',
        'DPT-순도(DP-IMP-1)01': 'IMP-1',
        'DPT-순도(미특정불순물)01': 'AUI'
    },
    ('Onsan', 'DP72'): {
        'DPS-함량01': 'Assay',
        'DPS-Chiral순도01': 'Chiral',
        'DPS-총불순물합01': 'Total Impurity',
        'DPS-DP-IMP-101': 'IMP-1',
        'DPS-DPIMP101': 'IMP-1',
        'DPS-개별불순물01': 'AUI',
        'DPS-강열잔분01': 'ROI'
    },
    ('Onsan', 'DP67'): {
        'DPY-유기부성분총합01': 'Total Impurity',
        'DPY-부성분(DP-IMP-1)01': 'IMP-1',
        'DPY-신규부성분01': 'AUI'
    },
    ('Onsan', 'DP57'): {
        'DPF-함량01': 'Assay',
        'DPF-Chiral01': 'Chiral',
        'DPF-유기부성분총합01': 'Total Impurity'
    },
    ('Onsan', 'DP37'): {
        'NFP0000D-Assay(NMR01': 'Assay',
        'NFP0000D-함량01': 'Assay'
    },
    ('Onsan', 'DP58'): {
        '106114-함량01': 'Assay',
        '106114-Chiral순도01': 'Chiral'
    },
    ('Onsan', 'DP58 onsan'): {
        'BAN-함량01': 'Assay',
        'BAN-Chiral순도01': 'Chiral'
    },
    ('Onsan', 'DP26'): {
        '106113-Assay(NMR)01': 'Assay',
        '106113-함량01': 'Assay',
        '106113-Triester01': 'Impurity(Triester)'
    },
    ('Onsan', 'DP26 onsan'): {
        'HFP-NMR01': 'Assay',
        'HFP-Triester01': 'Impurity(Triester)'
    },
    ('Osong', 'Zemiglo'): {
        'GEM-함량01': 'Assay',
        'GEM-총유연물질01': 'Total Impurity',
        'GEM-DPIMP1유연물질01': 'IMP-1',
        'GEM-미지개개유연물질01': 'AUI'
    },
    ('Osong', 'Zemidapa'): {
        'GLA-제미글립틴함량01': 'Assay',
        'GLA-제미총유연물질01': 'Total Impurity',
        'GLA-제미DPIMP1유연물질01': 'IMP-1',
        'GLA-제미미지유연물질01': 'AUI'
    },
    ('Osong', 'Zemimet 50/500mg'): {
        'GMT-제미글립틴함량01': 'Assay',
        'GMT-제미총유연물질01': 'Total Impurity',
        'GMT-DPIMP1제미유연물질01': 'IMP-1',
        'GMT-제미미지유연물질01': 'AUI'
    },
    ('Osong', 'Zemimet 50/1000mg'): {
        'ZMG-제미글립틴함량01': 'Assay',
        'ZMG-총제미유연물질01': 'Total Impurity',
        'ZMG-DPIMP1제미유연물질01': 'IMP-1',
        'ZMG-미지제미유연물질01': 'AUI'
    },
    ('Osong', 'Zemimet 25/500mg'): {
        'ZMJ-제미글립틴함량01': 'Assay',
        'ZMJ-제미글립틴함량02': 'Assay',
        'ZMJ-제미총유연물질01': 'Total Impurity',
        'ZMJ-DP-IMP-1제미유연물질01': 'IMP-1',
        'ZMJ-제미미지유연물질01': 'AUI'
    },
    ('Osong', 'Zemimet 25/1000mg'): {
        'ZMK-제미글립틴함량01': 'Assay',
        'ZMK-제미총유연물질01': 'Total Impurity',
        'ZMK-제미DPIMP1유연물질01': 'IMP-1',
        'ZMK-제미미지유연물질01': 'AUI'
    },
    ('Osong', 'Zemilow 50/5mg'): {
        'ZRA-제미글립틴함량01': 'Assay',
        'ZRA-총유연물질01': 'Total Impurity',
        'ZRA-DPIMP1제미유연물질01': 'IMP-1',
        'ZRA-미지유연물질01': 'AUI'
    },
    ('Osong', 'Zemilow 50/10mg'): {
        'ZRB-제미글립틴함량01': 'Assay',
        'ZRB-총유연물질01': 'Total Impurity',
        'ZRB-DPIMP1제미유연물질01': 'IMP-1',
        'ZRB-미지유연물질01': 'AUI'
    },
    ('Osong', 'Zemilow 50/20mg'): {
        'ZRC-제미글립틴함량01': 'Assay',
        'ZRC-총유연물질01': 'Total Impurity',
        'ZRC-DPIMP1제미유연물질01': 'IMP-1',
        'ZRC-미지유연물질01': 'AUI'
    },
    ('Osong', 'Zemimet 25/750mg'): {
        'ZML-제미글립틴함량01': 'Assay',
        'ZML-제미총유연물질01': 'Total Impurity',
        'ZML-제미DPIMP1유연물질01': 'IMP-1',
        'ZML-제미미지유연물질01': 'AUI'
    }
}

# Function to map insp_code to English
def map_insp_code(row):
    site = row['site']
    product = row['product']
    insp_code = row['insp_code']
    return insp_code_mapping.get((site, product), {}).get(insp_code, np.nan)

# Apply the mapping function
data_rev03_df['insp_code_english'] = data_rev03_df.apply(map_insp_code, axis=1)

# Filter rows where insp_code_english is not NaN
filtered_rev04_df = data_rev03_df.dropna(subset=['insp_code_english'])

# Select only the required columns
data_rev04_df = filtered_rev04_df[['batch_no', 'insp_min_value', 'insp_max_value', 'insp_result_value', 'product', 'site', 'insp_code_english']]
data_rev04_df = data_rev04_df.rename(columns={'insp_code_english': 'insp_code'})

# Write recipe outputs
data_rev04 = dataiku.Dataset("data_rev04")
data_rev04.write_with_schema(data_rev04_df)

