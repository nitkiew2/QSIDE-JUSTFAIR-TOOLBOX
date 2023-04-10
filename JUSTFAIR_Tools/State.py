#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:19:24 2023

@author: jason, alexis
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from JUSTFAIR_Tools.toolbox import subset_data_multi_level_summary, filter_years, tb_compare_section_to_larger_group
from JUSTFAIR_Tools.plotting import plot_section_vs_state, plot_section_vs_state_trends, plot_section_and_rest_data

### State class
class State:
    def __init__(self, inp_name, inp_data_url, inp_paths, 
                 order_of_outputs = ['Above Departure', 'Within Range', 'Below Range', 
                                        'Missing, Indeterminable, or Inapplicable'], 
                 colors = ['lightcoral', 'lightgrey', 'cornflowerblue', 'turquoise'],
                 using_url = True):
        self.name = inp_name
        
        if using_url:
            url=inp_data_url
            url='https://drive.google.com/uc?id=' + url.split('/')[-2]
            self.data = pd.read_csv(url, low_memory = False)  # pandas dataframe object
        else:
            file_path = inp_data_url
            self.data = pd.read_csv(file_path, low_memory = False)
        
        self.paths = inp_paths  # dictionary object.  
        # Always follows the format useful_id --> (name_in_data, dict(levels)).
        # Levels doesn't always exist, but is needed for variables like departure
        #path pairs are always (name_in_data, dict(levels)) or (name_in_data, None)
        
        self.order_of_outputs = order_of_outputs
        #this is how you want to arrange your output on graphs
        #is basically the order of the levels in paths[departure][1]
        
        self.colors = colors
        
        self.average_percents= []  #list, for all years, state averages for all people
        self.yearly_average_percents = {}  # dictionary, state averages for all people for each year
                                             # format of: year (int) --> [averages_list]
        
        self.years = np.sort(self.data[self.paths['year'].df_colname].unique())  # generate a sorted list of years for data



        ###  get average_percents
        
        counts = self.data.groupby(self.paths['departure'].df_colname).count()
        counts = counts.rename(self.paths['departure'].levels)
        counts = counts.iloc[:,0]

        for item in self.order_of_outputs:
            self.average_percents.append(round((100 * counts.loc[item]  /  self.data.shape[0]),2))
        
        ### get yearly_average_percents
        for year in self.years:
            subset_dat = self.data[ self.data[self.paths['year'].df_colname ] == year]
            counts = subset_dat.groupby(self.paths['departure'].df_colname).count()
            counts = counts.rename(self.paths['departure'].levels)
            counts = counts.iloc[:,0]
            
            percentages = []
            for item in self.order_of_outputs:
                percentages.append(round((100 * counts.loc[item]  /  subset_dat.shape[0]),2))
            self.yearly_average_percents[year] = percentages


### List Paths
    def list_paths(self):
         """
         print the paths of a state.  These are acceptable entries for inp_list_of_groups

         Returns
         -------
         None.

         """
         for key in self.paths.keys():
             print(key)
             
             
### Generalizable Multi-Level Summary

    def generalizable_multi_level_summary(self, inp_list_of_groups = ['departure'], years = None, plot = 'stacked bar'):
        '''
        Grouping by any combination (or none) of factor variables.  There is only one assumption to calling this function: the last level passed into inp_list_of_groups.  
        Basically, calling with only \['departure'\] means we are not grouping by any factor variable. This is a multi-level analysis of the path groups that are specified
        using the inp_list_of_groups parameter. Using the plot parameter you can specify if you want a bar, stacked bar or pie. 

        Parameters:
            stateobj: the state in question.  We need the state's yearly_average_percents to plot the graph
            inp_list_of_groups: Choose path description using string name
            years: the specified years.  Either a range or none
            plot: Choose type of plot based off of ('stacked bar', 'bar', 'pie')

        Returns:
            Specified type of plot and data table of the specified data
        '''
        # we should have a subplots vs stacked parameter here maybe?  either do lots of individual graphs or stacked
        subset_dat = filter_years(self, years)  #first, filter for the years we are looking for
        return subset_data_multi_level_summary(self, subset_dat, self.name, inp_list_of_groups, plot)



### Average from Filter Years

    def calc_state_avg_for_yearspan(self, years):
        '''
        Calculates the state's averages for a select span of years.  It uses the state's yearly_average_percents 
        and calculates the mean for the selected years by using the second parameter 'years'.

        Parameters:
            stateobj: a state object
            years: the specified years.  Either a range or none

        Returns:
            average value based on years
        '''
        avg_for_yearspan = []
        for year in years:
            avg_for_yearspan.append(self.yearly_average_percents[year])
        avg_for_yearspan = np.array(avg_for_yearspan)
        means = np.mean(avg_for_yearspan, axis = 0)  # take the average of each column
        rounded = means.round(2)
        return rounded





### State Trends

    def state_trends(self, compressed = False):
        '''
        This function plots the state trends over time.

        Parameters:
            stateobj: the state in question.  We need the state's yearly_average_percents to plot the graph
            compressed: if true, plot all lines on one graph.  If false, plot all lines on separate graphs.

        Returns:
            Line graph plot over the span of years for each category of departure times
        '''
        state_data_y = np.zeros((len(self.years), len(self.order_of_outputs)))
        for year in range(len(self.years)):
            state_data_y[year] = self.yearly_average_percents[self.years[year]]

        colors = ['lightcoral', 'lightgrey', 'cornflowerblue', 'turquoise']
        if compressed:
            fig, ax = plt.subplots(figsize=(10, 7))
            for col in range(len(self.order_of_outputs)):
                ax.plot(self.years, state_data_y[:,col], '-o', label=self.order_of_outputs[col], color = colors[col])
            ttl = self.name + ' Trends'
            ax.legend()
            ax.set_title(ttl)
            ax.set_xlabel('year')
            ax.set_ylabel('percentage (%)')
        else:
            for col in range(len(self.order_of_outputs)):
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(self.years, state_data_y[:,col], '-o', color = colors[col])
                ttl = self.name + ' ' + self.order_of_outputs[col] + ' over time.'
                ax.set_title(ttl)
                ax.set_xlabel('year')
                ax.set_ylabel('percentage (%)')



    ### Individual Section Analysis
    def compare_section_to_larger_group(self, section_category_name, section_name,
                                        larger_group_category_name, larger_group_name,
                                        inp_list_of_groups = ['departure'], years=None, plot=True):
        """
        Compare a subsection to its larger whole.  Note, the larger group must have 
    
        Parameters
        ----------
        section_category_name : str
            state the paths name that is the category our section is in.  ex: judge, county, district.
        section_name : str
            the name of the section we are looking at.
        larger_group_category_name : str
            the paths name of the category for the larger group.  Ex: county, district, state.
        larger_group_name : str
            name of the larger group.  For this tto work, the section must be a 
            subsection of this larger group.
        inp_list_of_groups : list, optional
            list paths names you wish to group by. The default is ['departure'].
        years : list, optional
            specify a range of years to look at. The default is None, and if None 
            is specified, it will pull all eyars where data is available.
        plot : bool, optional
            flag for if the function should generate graphs. The default is True.
    
        Returns
        a pandas datraframe of the following format:
            df[year][section] = section data for that yeat, has percent and count
            df[year][rest] = data for the year ofr the larger section
    
        """
        return tb_compare_section_to_larger_group(self, section_category_name, section_name,
                                            larger_group_category_name, larger_group_name,
                                            inp_list_of_groups, years, plot)
                
    
    def compare_judge_to_county(self, judge_name, county_name,
                                        inp_list_of_groups = ['departure'], years=None, plot=True):
        """
        Compare a judge to a county they operate in. 
    
        Parameters
        ----------
        section_name : str
            the name of the judge we are looking at.
        larger_group_name : str
            name of the county.  For this tto work, the judge must be active in this county.
        inp_list_of_groups : list, optional
            list paths names you wish to group by. The default is ['departure'].
        years : list, optional
            specify a range of years to look at. The default is None, and if None 
            is specified, it will pull all eyars where data is available.
        plot : bool, optional
            flag for if the function should generate graphs. The default is True.
    
        Returns
        a pandas datraframe of the following format:
            df[year][section] = section data for that yeat, has percent and count
            df[year][rest] = data for the year ofr the larger section
    
        """
        return tb_compare_section_to_larger_group(self, 'judge', judge_name,
                                            'county', county_name,
                                            inp_list_of_groups, years, plot)
    
    def compare_judge_to_state(self, judge_name, inp_list_of_groups = ['departure'], years=None, plot=True):
        """
        Compare a judge to a state they operate in. 
    
        Parameters
        ----------
        section_name : str
            the name of the judge we are looking at.
        inp_list_of_groups : list, optional
            list paths names you wish to group by. The default is ['departure'].
        years : list, optional
            specify a range of years to look at. The default is None, and if None 
            is specified, it will pull all eyars where data is available.
        plot : bool, optional
            flag for if the function should generate graphs. The default is True.
    
        Returns
        a pandas datraframe of the following format:
            df[year][section] = section data for that yeat, has percent and count
            df[year][rest] = data for the year ofr the larger section
    
        """
        return tb_compare_section_to_larger_group(self, 'judge', judge_name,
                                            'state', self.name,
                                            inp_list_of_groups, years, plot)

        