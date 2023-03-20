#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:19:24 2023

@author: jason, alexis
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from JUSTFAIR_Tools.toolbox import subset_data_multi_level_summary, filter_years
from JUSTFAIR_Tools.plotting import plot_section_vs_state, plot_section_vs_state_trends

### State class
class State:
    def __init__(self, inp_name, inp_data_url, inp_paths, 
                 order_of_outputs = ['Above Departure', 'Within Range', 'Below Range', 
                                        'Missing, Indeterminable, or Inapplicable'], using_url = True):
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

    def individual_section_analysis(self, category_name, section_name, inp_list_of_groups = ['departure'], years = None, plot = True):
        '''
        Outputs bar graph, stacked bar graph, and line graph of a Judges sentencing length over specified years

        Parameters:
            stateobj: a state object
            section_name: name of the judge, for formatting the title
            inp_list_of_groups: default is the sentencing departure ranges, can add other columns values to compare
            years: the specified years.  Either a range or none
            plot: Choose type of plot based off of ('stacked bar', 'bar', 'pie')

        Returns:
            Plots of subset of specified data for judges sentencing length
        '''
        section_filtered_data = self.data[self.data[self.paths[category_name].df_colname]== section_name]
        # get the years where the judge was active
        overlapping_years = years
        if years is None:
            overlapping_years = np.sort(section_filtered_data[self.paths['year'].df_colname].unique())
        print(section_name, 'was active in the years:', overlapping_years)

        groups_to_filter_by = []  # this list keeps track of the column names in our stateobj.data we are grouping by
        # get the column names in our stateobj.data we are grouping by
        for group in inp_list_of_groups:
            groups_to_filter_by.append(self.paths[group].df_colname)
        #groups_to_filter_by.append(stateobj.paths['departure'][0])  # add departure as a group by on the end, as that is our 
                                                                    # the variable we are looking at

        #time to get the aggregate


        #grouping by 
        #divide by count(all_items_but_daparture) for departure percentages for each subgroup
        counts = section_filtered_data.groupby(self.paths['departure'].df_colname).count()
        perc = round( (100 * counts/ section_filtered_data.shape[0]),2)  #if we are just grouping by departure, 
                                                                       #we divide by data frame length
        # renames the values that have levels
        perc = perc.rename(self.paths['departure'].levels, level = 0)
        counts = counts.rename(self.paths['departure'].levels, level = 0)

        # pull the data we need from our dataframes    
        perc = perc.iloc[:,0]  # all columns are the same, so we pull the first one
        counts = counts.iloc[:,0]  # all columns are the same, so we pull the first one

        #create an output dataframe to return
        agg_comb_df = pd.concat([counts,perc],axis=1)  # combine our two columns into a dataframe
        agg_comb_df.columns = ['count', 'percent']  # rename columns 

        state_avg_for_years = self.calc_state_avg_for_yearspan(overlapping_years)
        section_averages = []
        for departure_type in self.order_of_outputs:
            section_averages.append(perc.loc[departure_type,])

        if plot:
            plot_section_vs_state(self.order_of_outputs, section_averages, 
                                state_avg_for_years, section_name, self.name)

        #now we plot the changes over time vs the state
        section_data_y = np.zeros((len(overlapping_years), len(self.order_of_outputs)))
        state_data_y = np.zeros((len(overlapping_years), len(self.order_of_outputs)))
        for year in range(len(overlapping_years)):
            section_year_data = section_filtered_data[section_filtered_data[self.paths['year'][0]]== overlapping_years[year]]
            perc = round( (100 * section_year_data.groupby(self.paths['departure'][0]).count()/ section_year_data.shape[0]),2)
            perc = perc.rename(self.paths['departure'][1], level = 0)
            perc = perc.iloc[:,0]

            for departure_type in range(len(self.order_of_outputs)):
                if self.order_of_outputs[departure_type] in perc.index:
                    section_data_y[year, departure_type] = perc.loc[self.order_of_outputs[departure_type]]

            state_data_y[year] = self.yearly_average_percents[overlapping_years[year]]

        for departure_type in range(len(self.order_of_outputs)):
            if section_data_y[-1, departure_type] >= state_data_y[-1, departure_type]:
                print(section_name, 'currently has a(n)', self.order_of_outputs[departure_type], 'rate at or above state average in years queried')
            else:
                print(section_name, 'currently has a(n)', self.order_of_outputs[departure_type], 'rate below state average in years queried')

        if plot:
            plot_section_vs_state_trends(overlapping_years, section_data_y, state_data_y, section_name) 
            subset_data_multi_level_summary(section_filtered_data, inp_list_of_groups, plot = 'stacked bar')


### Individual Section Analysis

    def individual_section_analysis_v2(self, category_name, section_name, inp_list_of_groups = ['departure'], years = None, plot = True):
        '''
        Outputs bar graph, stacked bar graph, and line graph of a Judges sentencing length over specified years

        Parameters:
            stateobj: a state object
            section_name: name of the judge, for formatting the title
            inp_list_of_groups: default is the sentencing departure ranges, can add other columns values to compare
            years: the specified years.  Either a range or none
            plot: Choose type of plot based off of ('stacked bar', 'bar', 'pie')

        Returns:
            Plots of subset of specified data for judges sentencing length
        '''
        section_filtered_data = self.data[self.data[self.paths[category_name].df_colname]== section_name]
        # get the years where the judge was active
        overlapping_years = years
        if years is None:
            overlapping_years = np.sort(section_filtered_data[self.paths['year'].df_colname].unique())
        print(section_name, 'was active in the years:', overlapping_years)

        groups_to_filter_by = []  # this list keeps track of the column names in our stateobj.data we are grouping by
        # get the column names in our stateobj.data we are grouping by
        total_number_of_subgroups = 1
        for group in inp_list_of_groups:
            groups_to_filter_by.append(self.paths[group].df_colname)
            total_number_of_subgroups = total_number_of_subgroups * len(self.paths[group].levels)
        
        section_data = np.zeros((len(overlapping_years), total_number_of_subgroups , len(self.order_of_outputs)))
        # section_data[year][]



        