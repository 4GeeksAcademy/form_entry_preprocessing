import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

import build_features as features

from constants import TO_DROP

#Loading the data
data = pd.read_csv('../data/raw/All_Form_Entries.csv', dtype={'utm_content': 'object', 
                                                              'current_download': 'object', 
                                                              'state': 'object', 'lead_type': 'object',
                                                              'lead_generation_app':'object'})



#Changing type of columns 
features.change_to_datetime(data,'created_at')
features.change_to_datetime(data,'updated_at')
features.change_to_datetime(data,'won_at')

#Changing format
features.change_format(data,'created_at')
features.change_format(data,'updated_at')
features.change_format(data,'won_at')

#Format change also changed the column type to object, so we need to convert it to datetime again 
features.change_to_datetime(data,'created_at')
features.change_to_datetime(data,'updated_at')
features.change_to_datetime(data,'won_at')

#creating new columns
data['year-month'] = data['created_at'].dt.strftime('%Y-%m')
data['created_time'] = data['created_at'].dt.strftime('%H:%M:%S')
data['has_gclid'] = np.where(data['gclid'].isnull(), '0', '1')
data['days_to_convert'] = (data['won_at'] - data['created_at']).dt.days.abs()


#Combine first and last name ignoring nulls
features.combine_columns(data, 'first_name', 'last_name', 'fullname')

# shift column 'Fullname' to third position
fourth_column = data.pop('fullname')
data.insert(3, 'fullname', fourth_column)

#drop null columns
features.drop_null_columns(data)


#drop irrelevant columns
data.drop(TO_DROP, axis=1, inplace=True)

#drop testing rows
features.drop_test_rows(data)

#dropping two other test rows identified
data.drop(data[data['utm_source'] == 'test_s'].index, inplace = True)
data.drop(data[data['utm_source'] == 'fintech'].index, inplace = True)

print('Number of columns after dropping columns: ', data.shape)

#remove duplicated rows by combining them considering the first creation date
data = features.remove_duplicates(data)

#Clean course column
data = features.clean_course(data,'course')

#Clean location column
data = features.clean_location(data,'location')

#clean language column
data = features.clean_language(data,'language')

#clean utm_source

data = features.assign_with_conditions(data)

data = features.clean_utm_source(data,'utm_source')

#clean utm_medium
data = features.clean_utm_medium(data,'utm_medium')

# Assign values
data = features.assign_lead_type(data, 'tags','lead_type')

print(data.shape)
