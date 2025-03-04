#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Voltaire Vergara
# Created Date: 7/6/2019
# =============================================================================
'''
The aim of this file is to reproduce the population data that is indicated in the document, Buffalo Turning the corner,
for the neighborhood, Ellicott Neighborhood.
Once reproduced, all the data will be turned into csv files for visualization
'''
import csv
import json
import requests
from itertools import zip_longest
from functools import partial
# =============================================================================
api_key = '3fad1f7c603dfb341edd045495a58a7c0e77f15c'  # API key
# The parameters are set to have my API key and the geography level down to the block level of Ellicott neighborhood
parameters = {"key": api_key, "for": "block group:1,2,4", "in": "state:36+county:029+tract:001402"}
num_blocks = 3
api_base_url = lambda acs_year: 'https://api.census.gov/data/' + acs_year + '/acs/acs5?'  # API call link
# ==============================================================================

def update_response_parameters(dict_param ,base_url): # returns response
    parameters.update(dict_param)
    response = requests.get(url=base_url, params=parameters)
    return response.json()

def main():

    # these are the variables needed for the gentrification early warning system
    variables = {"Total population": "B01003_001E",
                 # race
                 "Total number of person(only Black or African American)": "B02001_003E",
                 "Total number of person(only White)": "B02001_002E",
                 "Total number of person(only Hisapnic)": "B03002_012E",
                 # household type
                 "Total Number of Housing Units": "B25001_001E",
                 "Total Number of Renter per housing unit": "B25003_003E",
                 "Total Number of Vacant Housing Units": "B25002_003E",
                 # poverty
                 "Total Population for whom poverty status is determined" : "C17002_001E",
                 "Total below povery line (population whose poverty level is determined)": ["C17002_002E", "C17002_003E"],
                 # gross rent as income
                 "Total Median Gross Rent As A Percentage Of Household Income In The Past 12 Months (Dollars)":
                                                                                                        "B25071_001E",
                 # educational attainment
                 "Total Population that is 25 years and older ": "B15003_001E",
                 "Total Population 25 years and older that have less than a college education":
                        ["B15003_0" + str(i).zfill(2) + "E" for i in range(2, 19)]}




    # This calculates the percentages on a block level , then puts them into a csv file
    with open('UBgentrification_data.csv', mode='w') as data:
        data_writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        # headers
        block_list = ["Block"]
        tract_list = ["tract"]
        var_list = []
        for var_title, var_code in variables.items():
            data_list = [] # this is for variables that needed accumulation of data
            year = 2016
            # calculates whether there are multiple variables that needed to be added to get the whole percentage
            if isinstance(var_code, list):  # checks if the pair is a list
                data_list = [0] * num_blocks  # initializes the array to zero so that it can accumulate totals
                for codes in var_code:
                    json_data = update_response_parameters(dict_param={"get": codes}, base_url=api_base_url(str(year)))
                    for block_count in range(1, len(json_data)):  # it starts at 1 because that's after the header
                        data_list[block_count-1] += int(json_data[block_count][0])
            else:
                json_data = update_response_parameters(dict_param={"get": var_code}, base_url=api_base_url(str(year)))

            var_data = [var_title]  # the is inside the for loop since it needs to keep adding variables onto the header

            for block in range(1, len(json_data)):
                var_data.append(json_data[block][0] if len(data_list) == 0 else data_list[block-1])
                tract_list.append(json_data[block][3]) if len(tract_list) <= num_blocks else None
                block_list.append(json_data[block][4]) if len(block_list) <= num_blocks else None # !! THESE ARE ONLY ADDED CUZ THERES NO YEARS

            var_list.append(var_data)

        result = zip_longest(tract_list, block_list, *var_list, fillvalue='None')
        data_writer.writerows(result)
        data.close()
    '''parameters.update( {"get": "B02001_003E"} ) # till 18
    
    
    
    response = requests.get(api_base_url('2016'), params = parameters)
    json = response.content.decode("utf-8")'''
  #  print(list(result), sep = '\n')

if __name__ == '__main__' :
    main()
'''
THIS IS TO CALCULATE ON A NEIGHBORHOOD LEVEL 

def ACScalculate_percent(variable_sample, variable_total,year, num_block = 3):

    assumes that 
    :param variable_sample: 
    :param variable_total: 
    :param year 
    :param num_block
    :return:

    parameters.update( {"get": variable_sample + "," + variable_total})
    response = requests.get(api_base_url(str(year)), params=parameters)
    json = response.json()
    for i in range(1, num_block):
        var_count =+ json[i][1] 
        total_var_count =+ json[i][1] 
    if isinstance(variable_sample, list): 
        var_count = 0
        for var in variable_sample: 
            parameters.update( {"get": var })
            response = requests.get(api_base_url(str(year)), params = parameters) 
            json = response.json()
            for i in range(1,num_block):
                var_count =+ json[i][0]

    else:

    return (var_count / total_var_count) * 100
'''
