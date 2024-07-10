# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
tb_insp_result_sample = dataiku.Dataset("tb_insp_result_sample")
tb_insp_result_sample_df = tb_insp_result_sample.get_dataframe()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

data_rev03_df = tb_insp_result_sample_df # For this sample code, simply copy input to output


# Write recipe outputs
data_rev03 = dataiku.Dataset("data_rev03")
data_rev03.write_with_schema(data_rev03_df)
