__author__ = 'nabeelh-dev'

import numpy as np
import datetime
import json
from collections import OrderedDict
from operator import itemgetter

def getMinMaxDates(date_list):
    datetime_array = [np.datetime64(x) for x in date_list]
    '''
    datetime_array = []
    for date in date_list:
        temp_date = np.datetime64(date)
        datetime_array.append(temp_date)
    '''

    sorted_dates = np.sort(datetime_array, axis=0)
    return sorted_dates[0].astype(datetime.datetime).strftime('%Y-%m-%d'), \
           sorted_dates[-1].astype(datetime.datetime).strftime('%Y-%m-%d')

def getUniqueCounts(value_list):
    unique_counts = {}
    for value in value_list:
        unique_counts[value] = unique_counts.get(value, 0) + 1

    sorted_dict = OrderedDict(sorted(unique_counts.items(), key=itemgetter(1), reverse=True))
    sorted_dict['Lines Sum'] = sum([v for k, v in sorted_dict.items()])
    return json.dumps(sorted_dict, indent=4)