# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 14:29:08 2016

@author: Mike
"""

import pandas as pd
import sys
import transform_lib as tf
import numpy as np
import compare as cp
import validation_tool as vt


load_file = sys.argv[1]

obs_file = pd.read_csv(load_file, dtype=object)

# Sort out the times =============================----------------------------------------------#
obs_file['dim_item_id_7'] = obs_file['dim_item_id_7'].astype(str)
obs_file['dim_item_id_7'][obs_file['dim_item_id_7'] == 'nan'] = ''

# Quarters
obs_file['time_dim_item_id'][obs_file['dim_item_id_7'] != ''] = obs_file['dim_item_id_6'].str[0:4] + ' ' + obs_file['dim_item_id_7'].str[0:2]
obs_file['time_type'][obs_file['dim_item_id_7'] != ''] = 'Quarter'

# Years
obs_file['time_dim_item_id'][obs_file['dim_item_id_7'] == ''] = obs_file['dim_item_id_6'].str[0:4]
obs_file['time_type'][obs_file['dim_item_id_7'] == ''] = 'Year'

# Tidy up both
obs_file['time_type'][-1:] = ''
obs_file['time_dim_item_id'][-1:] = ''
obs_file['time_dim_item_label_eng'] = obs_file['time_dim_item_id']


# Build dimension item 1 =============================----------------------------------------------#

# Make them all string then get rid of nan's:
for col in ['dim_item_id_2', 'dim_item_id_3', 'dim_item_id_4', 'dim_item_id_5']:
    obs_file[col] = obs_file[col].astype(str)
    obs_file[col] = obs_file[col].str.replace('nan', '')
    obs_file[col] = obs_file[col].str.strip()


for i, row in obs_file.iterrows():
        # If 2 is not blank - concat it onto 1. Rinse and repeat.
        if row['dim_item_id_3'] != '':
                obs_file.ix[i, 'dim_item_id_2'] = obs_file.ix[i, 'dim_item_id_2'] + ' ' + obs_file.ix[i, 'dim_item_id_3']
        if row['dim_item_id_4'] != '':
                obs_file.ix[i, 'dim_item_id_2'] = obs_file.ix[i, 'dim_item_id_2'] + ' ' + obs_file.ix[i, 'dim_item_id_4']
        if row['dim_item_id_5'] != '':
                obs_file.ix[i, 'dim_item_id_2'] = obs_file.ix[i, 'dim_item_id_2'] + ' ' + obs_file.ix[i, 'dim_item_id_5']
                
obs_file['dimension_item_label_eng_2'] = obs_file['dim_item_id_2']


# round observations to 1 decimal point =============================----------------------------------------------#
obs_file['observation'][1:-1] = obs_file['observation'][1:-1].map(float).map(lambda x: np.round(x, 0))

# Now get rid of .0, whole numbers are fine
obs_file['observation'] = obs_file['observation'].astype(str)
obs_file['observation'] = obs_file['observation'].map(lambda x: x.replace('.0', ''))


# finalise and output =============================----------------------------------------------#

obs_file = tf.dismiss(obs_file, ['dim_id_3', 'dim_id_4', 'dim_id_5', 'dim_id_6', 'dim_id_7'])

out_filename = 'transform'+load_file[4:]
vt.frame_checks(obs_file, out_filename)
obs_file.to_csv(out_filename, index=False)

# Now run the coparissons against past datasets
cp.compare(sys.argv[2], out_filename)


