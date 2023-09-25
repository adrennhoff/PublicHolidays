"""
This file Nager.Date's REST API to obtain a list of public holidays
around the world for 2023 and 2024
"""

import requests
import json
import pandas as pd

# Obtain the list of the available countries
response = requests.get('https://date.nager.at/api/v3/AvailableCountries')
countries = json.loads(response.content)

# Obtain the list of public holidays for each of the available countries
holiday_list = pd.DataFrame(columns = ['name','countryCode','country','date', 'type', 'global'])

# Loop over countries
for i in range(len(countries)):
    # Loop over 2023 and 2024
    for yr in ['2023','2024']:
        # Call API
        URL = 'https://date.nager.at/api/v3/publicholidays/' + yr + '/' + countries[i]['countryCode']
        response = requests.get(URL)
        public_holidays = json.loads(response.content)
        # Stack results in data frame
        for h in range(len(public_holidays)):
            # Check to see that holiday is Public
            if 'Public' in public_holidays[h]['types']:
                holiday_list = pd.concat([holiday_list, pd.DataFrame.from_records([{'name' : public_holidays[h]['name'],
                                                                               'countryCode' : public_holidays[h]['countryCode'],
                                                                               'country' : countries[i]['name'],
                                                                               'date' : public_holidays[h]['date'],
                                                                               'type' : 'Public',
                                                                               'global' : public_holidays[h]['global']}])])

# Write the data frame to a CSV file
holiday_list.to_csv('holidays.csv', index = False)
