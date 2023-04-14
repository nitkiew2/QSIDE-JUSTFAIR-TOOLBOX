#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 22:57:19 2023

@author: jason
"""

import pandas as pd

class Demographic:
    """
    A class for initializing and storing the state database.

    Attributes:
    -----------
    state_name: str
        The name of the state for which data is being collected.
    year: str
        The year for which data is being collected.

    Methods:
    --------
    __init__(self, state, year):
        Initializes the Demographic object with the state name and year of data collection.
    get_url(self, year):
        Retrieves the data URL from a dictionary based on the year parameter.
    pull_data(self, url):
        Reads the data from a CSV file and returns it as a pandas dataframe.
    get_columns(self):
        Returns the column names for the appropriate year of data collection.
    make_columns_dict(self):
        Generates a dictionary of column names for each year of data collection.
    make_state_database(self):
        Creates a new dataframe with columns corresponding to the appropriate year of data collection.

    """
    def __init__(self, state, year):
        """
        Initializes the Demographic object with the state name and year of data collection.

        Parameters:
        -----------
        state : str
            The name of the state for which data is being collected.
        year : str
            The year for which data is being collected.

        """
        self.state_name = state
        self.year = year
        
        self.get_url(year)
        
        self.column_dictionary = self.get_columns()
        
        self.raw_data = self.pull_data(self.data_url)
        self.state_data = self.make_state_database()
        
    def get_url(self, year):
        """
        Retrieves the data URL from a dictionary based on the year parameter.

        Parameters:
        -----------
        year : str
            The year for which data is being collected.

        """
        url_dictionary = {
            '2010': ("https://drive.google.com/file/d/1aE0MYMimeWIbYL8HmqpHoaJs2vhTE3zs/view?usp=sharing"),
            '2011': ("https://drive.google.com/file/d/1KKVHaxGLAqOeWYYT0VzsUi1dDQ-eHeHb/view?usp=sharing"),
            '2012': ("https://drive.google.com/file/d/1J7BRmv1GxA3nG3NPCCVNhKsTqq7WDvpw/view?usp=sharing"),
            '2013': ("https://drive.google.com/file/d/1M_TH6rWzNygx31dwYwUoz8ZsU9v8uE1z/view?usp=sharing"),
            '2014': ("https://drive.google.com/file/d/1zV2SBArknO9md1vyslzIUHncNxQ_cDTr/view?usp=sharing"),
            '2015': ("https://drive.google.com/file/d/1q_wc0fHwhThKC9XcORyqtYc9SkFzbqUN/view?usp=sharing"),
            '2016': ("https://drive.google.com/file/d/12Q_WX3a9kpJEQfibNyydwEWYJD5CLW6k/view?usp=sharing"),
            '2017': ("https://drive.google.com/file/d/1QjmK6LPo-u96Hl24zPSA0zeXQY7QkQt7/view?usp=sharing"),
            '2018': ("https://drive.google.com/file/d/13man95TZzsOPlCI-hg7AoEYGo-pFApR9/view?usp=sharing"),
            '2019': ("https://drive.google.com/file/d/11yrEfti1sbZ5aH25XbBZUSvD5eGZMrWl/view?usp=sharing"),
            '2021': ("https://drive.google.com/file/d/1pqzQ-jJSumkJ82vAGWkm0uV2Ts5b5ISG/view?usp=sharing")
        }
        
        if year not in url_dictionary:
            self.url = None
            print('ERROR! ' + self.year + ' dataset for ' + self.state_name + " is not available.")
        else:
            data_id = url_dictionary[year].split('/')[-2]
            self.data_url = f"https://drive.google.com/uc?export=download&id={data_id}"
            
    def pull_data(self, url):
        """
        Downloads a CSV file from the specified URL and returns its contents as a pandas DataFrame.

        Args:
            url (str): The URL of the CSV file to download.

        Returns:
            pandas.DataFrame: A DataFrame containing the data from the CSV file.
        """
        df = pd.read_csv(url, encoding = 'utf-8', header=0)
        return df
    
    def get_columns(self):
        """
        Return the appropriate column names based on the year of the dataset.

        If the year is 2016 or earlier, return the column names for 'Format A'.
        Otherwise, return the column names for 'Format B'.

        Returns:
            list: A list of strings representing the column names.
        """
        column_dict = self.make_columns_dict()
        if int(self.year) <= 2016:
            return column_dict['Format A']
        else:
            return column_dict['Format B']
        
    def make_columns_dict(self):
        """
        Create and return a dictionary with the columns of the Census dataset, organized by race, age, and sex. 
        The columns in the dictionary are divided into two formats (Format A and Format B) based on the year of the Census data. 
    
        Returns:
            dict: A dictionary containing the column names organized by race, age, and sex for Format A and Format B.
        """
        column_dict = {'Format A': {}, 'Format B': {}}
        
        column_dict["Format A"]['Race'] = ['NAME',
                      'DP05_0032E',
                      'DP05_0033E',
                      'DP05_0034E',
                      'DP05_0039E',
                      'DP05_0047E',
                      'DP05_0052E',
                      'DP05_0053E']
        age_list_code = []
        for i in range(4, 17):
            str_i = str(i)
            if len(str_i) == 1:
                age_list_code.append("DP05_000" + str_i + "E")
            else:
                age_list_code.append("DP05_00" + str_i + "E")           
        age_list_code.reverse()
        column_dict['Format A']['Age'] = ['NAME',
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop()]
        column_dict['Format A']['Sex'] = ['NAME','DP05_0002E','DP05_0003E']
    
        column_dict['Format B']['Race'] = ['NAME',
                      'DP05_0037E',
                      'DP05_0038E',
                      'DP05_0039E',
                      'DP05_0044E',
                      'DP05_0052E',
                      'DP05_0057E',
                      'DP05_0058E']
        age_list_code = []
        for i in range(5, 18):
            str_i = str(i)
            if len(str_i) == 1:
                age_list_code.append("DP05_000" + str_i + "E")
            else:
                age_list_code.append("DP05_00" + str_i + "E")           
        age_list_code.reverse()
        column_dict['Format B']['Age'] = ['NAME',
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop(),
                      age_list_code.pop()]
        column_dict['Format B']['Sex'] = ['NAME','DP05_0002E','DP05_0003E']
        
        return column_dict
    
    def make_state_database(self):
        """
        Returns a dictionary representing the state's demographic database.
    
        The dictionary has three keys: 'Race', 'Age', and 'Sex', each pointing to a pandas DataFrame object 
        containing the corresponding demographic data for the state. The data is extracted from the Census API 
        based on the state name provided at initialization.
    
        Returns:
            dict: A dictionary containing the demographic data for the state.
        """
        data_base = {'Race': None, 'Age': None, 'Sex': None}
        data_base['Race'] = self.race_data(self.state_name)
        data_base['Age'] = self.age_data(self.state_name)
        data_base['Sex'] = self.sex_data(self.state_name)
        return data_base
        
    def race_data(self, state):
        """
        Returns a Pandas DataFrame containing the race data for a given state.
    
        Args:
            state (str): The name of the state for which to retrieve race data.
        
        Returns:
            pd.DataFrame: A Pandas DataFrame containing the race data for the specified state.
                The DataFrame includes the following columns:
                    - Counties in [state]
                    - White
                    - Black or African American
                    - American Indian and Alaska Native
                    - Asian
                    - Native Hawaiian and Other Pacific Islander
                    - Others
                    - Two or more races
        """
        labels = ['Counties in ' + state, 'White', 'Black or African American', 'American Indian and Alaska Native', 'Asian', 'Native Hawaiian and Other Pacific Islander', 'Others', 'Two or more races']
        df = self.raw_data.filter(self.column_dictionary['Race'])
        select_df = self.state_select(df, state)
        select_df.columns = labels
        pd_df = select_df.iloc[1:]
        return pd_df.reset_index(drop=True)
    
    def sex_data(self, state):
        """
        Retrieves sex demographic data for a given state from the raw_data DataFrame.

        Args:
            state (str): The name of the state for which to retrieve the data.

        Returns:
            pd_df (pandas.DataFrame): A DataFrame containing the sex demographic data for the specified state, with columns
            representing the number of males and females.

        """
        labels = ['Counties in ' + state, 'Male', 'Female']
        df = self.raw_data.filter(self.column_dictionary['Sex'])
        select_df = self.state_select(df, state)
        select_df.columns = labels
        pd_df = select_df.iloc[1:]
        return pd_df.reset_index(drop=True)
    
    def age_data(self, state):
        """
        Extracts age data for a specified state from the raw data and returns it as a Pandas DataFrame.

        Args:
        - state (str): The name of the state for which to extract age data.

        Returns:
        - pd_df (pandas.DataFrame): A DataFrame containing age data for the specified state, with county names
          as the index and age ranges as columns. The age ranges are as follows:
            * Age 0 to 4 years (5-year range)
            * Age 5 to 9 years (5-year range)
            * Age 10 to 14 years (5-year range)
            * Age 15 to 19 years (5-year range)
            * Age 20 to 24 years (5-year range)
            * Age 25 to 34 years (10-year range)
            * Age 35 to 44 years (10-year range)
            * Age 45 to 54 years (10-year range)
            * Age 55 to 59 years (5-year range)
            * Age 60 to 64 years (5-year range)
            * Age 65 to 74 years (10-year range)
            * Age 75 to 84 years (10-year range)
            * Age 85 years or older
        """
        labels = ['Counties in ' + state, 
                                        'Age 0 to 4 years', #5 Year Range 
                                        'Age 5 to 9 years', #5 Year Range
                                        'Age 10 to 14 years', #5 Year Range
                                        'Age 15 to 19 years', #5 Year Range
                                        'Age 20 to 24 years', #5 Year Range
                                        'Age 25 to 34 years', #10 Year Range
                                        'Age 35 to 44 years', #10 Year Range
                                        'Age 45 to 54 years', #10 Year Range
                                        'Age 55 to 59 years', #5 Year Range
                                        'Age 60 to 64 years', #5 Year Range
                                        'Age 65 to 74 years', #10 Year Range
                                        'Age 75 to 84 years', #10 Year Range
                                        'Age 85 years or older'] 
            
        
        df = self.raw_data.filter(self.column_dictionary['Age'])
        select_df = self.state_select(df, state)
        select_df.columns = labels
        pd_df = select_df.iloc[1:]
        return pd_df.reset_index(drop=True)
    
    def state_select(self, df, state):
        """
        Selects rows from a dataframe where the 'NAME' column contains the provided state name,
        and removes the county and state names from the 'NAME' column.
    
        Args:
            df: pandas.DataFrame object, input dataframe
            state: str, state name to select
    
        Returns:
            pandas.DataFrame object, filtered dataframe with selected state rows and modified 'NAME' column

        """
        filtered_df = df.loc[df['NAME'].str.contains(state), :]
        filtered_df.loc[:, 'NAME'] = filtered_df['NAME'].str.replace('County, ' + state, '')
        return filtered_df

    def get(self, table):
        """
        Returns the data for a given table.

        Args:
        - table (str): The name of the table to retrieve data for.

        Returns:
        - pandas.DataFrame: The data for the specified table.
        """
        data = self.state_data[table]
        return data



