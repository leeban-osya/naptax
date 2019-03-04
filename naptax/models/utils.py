__author__ = 'nabeelh-dev'

import numpy as np
import datetime
import json
from collections import OrderedDict
from operator import itemgetter

def sortDates(date_list):
    date_array = []
    for date in date_list:
        temp_date = np.datetime64(date)
        date_array.append(temp_date)

    sorted_dates = np.sort(date_array, axis=0)
    return sorted_dates[0].astype(datetime.datetime).strftime('%Y-%m-%d'), \
           sorted_dates[-1].astype(datetime.datetime).strftime('%Y-%m-%d')

def getUniqueCounts(value_list):
    unique_counts = {}
    for value in value_list:
        unique_counts[value] = unique_counts.get(value, 0) + 1

    line_sum = 0
    for k,v in unique_counts.items():
        line_sum += int(v)

    sorted_dict = OrderedDict(sorted(unique_counts.items(), key=itemgetter(1), reverse=True))
    sorted_dict['Lines Sum'] = line_sum
    return json.dumps(sorted_dict, indent=4)