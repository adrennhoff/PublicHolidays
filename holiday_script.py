"""
This file contains several different functions that return information related to the Nager.Date
holiday data. Each function is given a unique name so that it can be examined on its own
"""

import pandas as pd
from datetime import datetime, timedelta

# Load the CSV file of data from local directory
holiday_data = pd.read_csv('./holidays.csv')
holiday_list = holiday_data.to_dict('records')

# Define the basic function
def holidays1():
    # Define today's date
    today = datetime.today()
    # Select list of future US holidays
    US = [x for x in holiday_list if x['countryCode'] == 'US' and datetime.strptime(x['date'], '%Y-%m-%d') >= today]
    return US[:10]

# Incorporate global holiday variable with default set to None
def holidays2(globe = None):
    # Define today's date
    today = datetime.today()
    # Select list of future US holidays
    US = [x for x in holiday_list if x['countryCode'] == 'US' and datetime.strptime(x['date'], '%Y-%m-%d') >= today]
    US_holidays = []
    for r in range(len(US)):
        if globe is None or US[r]['global'] == globe:
            US_holidays.append(US[r])
    return US_holidays[:10]

# Incorporate comparison country
def holidays3(globe=None, comparison_country=None):
    # Define today's date
    today = datetime.today()
    
    US_holidays = []
    comparison_holidays = []
    
    for r in range(len(holiday_list)):
        hdate = datetime.strptime(holiday_list[r]['date'], '%Y-%m-%d')
        if hdate >= today:
            if holiday_list[r]['countryCode'] == 'US':
                if globe is None or holiday_list[r]['global'] == globe:
                    US_holidays.append(holiday_list[r])
            elif holiday_list[r]['country'] == comparison_country:
                comparison_holidays.append(holiday_list[r])
    
    if comparison_country is not None:
        shared_dates = set(h['date'] for h in comparison_holidays)        
        matched = [h for h in US_holidays if h['date'] in shared_dates]
    else:
        matched = US_holidays
    
    return matched[:10]

# New function that finds which countries have the most
# overlap with the supplied comparison_country
def most_common_countries(comparison_country="United States"):
    countries = pd.unique(holiday_data['country'])
    country_count = pd.DataFrame(0, columns = ['common_dates'], index = countries)
    
    comp_country = [x for x in holiday_list if x['country'] == comparison_country]
    
    today = datetime.today()
    end_date = today + timedelta(days = 364)
    
    # Find the holidays dates for comparison_country
    comparison_dates = []
    for h in range(len(comp_country)):
        hdate = datetime.strptime(comp_country[h]['date'], '%Y-%m-%d')
        if hdate >= today and hdate < end_date:
            comparison_dates.append(comp_country[h]['date'])

    # Now loop over all rows
    for r in range(len(holiday_list)):
        if holiday_list[r]['country'] != comparison_country and holiday_list[r]['date'] in comparison_dates:
            country_count.loc[holiday_list[r]['country']] += 1
    
    # Format output to return
    sorted_countries = country_count.sort_values(by=['common_dates'], ascending = False)
    sorted_countries['country'] = sorted_countries.index
    return sorted_countries[:10].to_dict('records')