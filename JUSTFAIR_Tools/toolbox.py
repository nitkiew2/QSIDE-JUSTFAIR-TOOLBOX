#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:20:21 2023

@author: jason
"""
import numpy as np
import pandas as pd
from JUSTFAIR_Tools.plotting import plot_departures_bar, plot_departures_stacked, plot_departures_pie, plot_section_and_rest_data



### Filter Years

def filter_years(stateobj, years):
    '''
    Every funciton has a years to filter parameter, so we are building a function here because:
    1.  if we have to edit it, we only have to edit it here
    2.  saves us time from rewriting this a bunch

    Parameters:
        stateobj: a state object
        years: the specified years.  Either a range or none

    Returns:
        a subset of the specified years of data
    '''
    subset_dat = stateobj.data
    if years is not None:  
        # if the user specifies a year range, filter the data for those years
        subset_dat = stateobj.data[stateobj.data[stateobj.paths['year'].df_colname].isin(years)]
    return subset_dat

### Plotting Data

def plot_df(stateobj, df, plot_type, groups, base_group_str):
    '''
    Main plotting function.  This is used by generalizable_multi_level_summary to take a dataframe and generate 
    graphs by calling plot_departures or plot_departures_stacked.

    we have 6 main situations here
    1. stacked bar, just departure to group by
    2. stacked bar, more than just deaprture to group by
    3. not stacked bar, just departure
    4. not stacked bar, more than just departure
    5. pie chart, just departure
    6. pie chart, more than just departure

    This is the main plotting function for generalizable_multi_level_summary and subset_multi_level_summary.  
    This function takes a state, the percentages to plot, the plot type, and any subgroups to make plots for 
    (in case we are grouping by more than just departure).

    Using this data, it creates the desired plots for the user to view

    Parameters:
        df: input dataframe.  Right now we are using percents from generalizable_multi_level_summary
        stacked: if true, produce stacked bar graphs, if false, produce nonstacked bar graphs
        groups: the parameters we are grouping by, we use these to generate titles in stacked bar graphs

    Returns:
        Plots based off the plot type, basic plotting function
    '''
    unique_identifiers = []  # list of unique tuples in df.index we will need
    unique_identifier_strings = []  # string fromat of unique_identifiers, used in graph titles.
    if  df.index.nlevels > 1:
        for ind in df.index:
            if ind[:-1] not in unique_identifiers:  # we do ind[:-1] here because the last identifier is always departure, and we want our grops to be everything but departure 
                unique_identifiers.append(ind[:-1])  # add the unique identifier tuple
                # create and add string form of the unique identifier to unique_identifier_strings
                unique_identifier_string = ''
                for string in ind[:-1]:
                    unique_identifier_string += str(string) + ' '
                unique_identifier_string = unique_identifier_string[:-1]
                unique_identifier_strings.append(unique_identifier_string)
    else:
        unique_identifier_strings = [stateobj.order_of_outputs]

    # plotting time.
    if plot_type == 'stacked bar':
        if len(groups) > 0:  #we're dealing with more then one grouping variable
            porportions = np.zeros((len(stateobj.order_of_outputs), len(unique_identifiers)))
            for dep in range(len(stateobj.order_of_outputs)):
                for unique_id in range(len(unique_identifiers)):
                    loc_id = unique_identifiers[unique_id] + (stateobj.order_of_outputs[dep],)
                    if loc_id in df.index:
                        porportions[dep, unique_id] = df.loc[loc_id,]
            #plot
            plot_departures_stacked(unique_identifier_strings, porportions, stateobj.colors, base_group_str, groups, stateobj.order_of_outputs)
        else:  # just departure
            porportions = []
            for departure_type in stateobj.order_of_outputs:
                porportions.append(df.loc[departure_type,])
            #plot
            groups.insert(0, stateobj.name)  # we need the state name for plotting purposes
            plot_departures_stacked([stateobj.name], porportions, stateobj.colors, base_group_str, groups, stateobj.order_of_outputs, s = False)

    if plot_type == 'bar' or plot_type == 'pie':  # not stacked bars
        if len(groups) > 0:  #we're dealing with more then one grouping variable
            for unique_id in unique_identifiers:
                porportions = [0,0,0,0]
                pos = 0
                for deperture_type in stateobj.order_of_outputs:
                    comb_ind = unique_id + (deperture_type,)
                    if comb_ind in df.index:
                        porportions[pos] = df.loc[comb_ind,]
                    pos += 1

                unique_id = (stateobj.name,) + unique_id
                if plot_type == 'bar':
                    plot_departures_bar(stateobj.order_of_outputs, porportions, stateobj.colors, base_group_str, unique_id)
                else:  # pie
                    plot_departures_pie(stateobj.order_of_outputs, porportions, stateobj.colors, base_group_str, unique_id)
        else:
            porportions = []
            for departure_type in stateobj.order_of_outputs:
                porportions.append(df.loc[departure_type,])
            if plot_type == 'bar':
                plot_departures_bar(stateobj.order_of_outputs, porportions, stateobj.colors, base_group_str, [], s = False) 
            else:  # pie
                plot_departures_pie(stateobj.order_of_outputs, porportions, stateobj.colors, base_group_str, [], s = False)  

### Filtered Multilevel Summary

def subset_data_multi_level_summary(stateobj, subset_dat, base_group_str, inp_list_of_groups = ['departure'], plot = 'stacked bar'):
    '''
    A slightly modified version of generalizable_multi_level_summary.  This is built to work with already filtered data.  
    It is used in individual_section_analysis.

    Parameters:
        stateobj: a state object
        subset_dat: the subset of data based on years, use filter_years to get subset of data
        base_group_str: the specified years.  Either a range or none
        inp_list_of_groups: default is the sentencing departure ranges, can add other columns values to compare
        plot: Choose type of plot based off of ('stacked bar', 'bar', 'pie')

    Returns:
        Plots of subset of specified data (race, gender) based on the type of plot given in the input parameters
    '''
    groups_to_filter_by = []  # this list keeps track of the column names in our stateobj.data we are grouping by
    # get the column names in our stateobj.data we are grouping by
    for group in inp_list_of_groups:
        groups_to_filter_by.append(stateobj.paths[group].df_colname)
    #groups_to_filter_by.append(stateobj.paths['departure'][0])  # add departure as a group by on the end, as that is our 
                                                                # the variable we are looking at

    #grouping by 

    counts = subset_dat.groupby(groups_to_filter_by).count()
    perc = None #initializing, will get value in next lines
    if len(inp_list_of_groups) > 1: # if we are grouping by more than departure
        perc = round(100 * counts / subset_dat.groupby(groups_to_filter_by[:-1]).count(), 1)
    else:
        perc = round( (100 * counts/ subset_dat.shape[0]),2)  #if we are just grouping by departure, we divide by data frame length

    # renames the values that have levels
    l=0
    for group in inp_list_of_groups:
        if stateobj.paths[group].levels is not None:
            perc = perc.rename(stateobj.paths[group].levels, level = l)
            counts = counts.rename(stateobj.paths[group].levels, level = l)
        l += 1
    # pull the data we need from our dataframes    
    perc = perc.iloc[:,0]  # all columns are the same, so we pull the first one
    counts = counts.iloc[:,0]  # all columns are the same, so we pull the first one

    #create an output dataframe to return
    comb_df = pd.concat([counts,perc],axis=1)  # combine our two columns into a dataframe
    comb_df.columns = ['count', 'percent']  # rename columns 
    if plot == 'stacked bar':
        plot_df(stateobj, perc, 'stacked bar', inp_list_of_groups[:-1], base_group_str)  # call our plotting function
    elif plot == 'bar':
        plot_df(stateobj, perc, 'bar', inp_list_of_groups[:-1], base_group_str)
    elif plot == 'pie':
        plot_df(stateobj, counts, 'pie', inp_list_of_groups[:-1], base_group_str)
        
    return comb_df


def compare_section_to_larger_group(stateobj, section_category_name, section_name,
                                    larger_group_category_name, larger_group_name,
                                    inp_list_of_groups = ['departure'], years=None, plot=True):
    """
    Outputs bar graph, stacked bar graph, and line graph of a Judges sentencing length over specified years

    Parameters:
        stateobj: a state object
        section_category_name: the name of the category our section belongs to.  Examples: judge, district, county
        section_name: name of the judge, for formatting the title
        larger_group_category_name: the category of our larger group that we are comparing the section to.  Examples: District, county, State
        larger_group_name: name of the larger group
        inp_list_of_groups: default is the sentencing departure ranges, can add other columns values to compare
        years: the specified years.  Either a range or none
        plot: Choose type of plot based off of ('stacked bar', 'bar', 'pie')

    Returns:
        Plots of subset of specified data for judges sentencing length
    """
    section_filtered_data = stateobj.data[stateobj.data[stateobj.paths[section_category_name].df_colname] == section_name]
    rest_of_the_larger_section = None
    if larger_group_category_name not in stateobj.paths.keys():  # if we're dealing with 'state' or there's a typo
        print('large group = state')
        rest_of_the_larger_section = stateobj.data[stateobj.data[stateobj.paths[section_category_name].df_colname] != section_name]
    else:
        print('large group =', larger_group_name, larger_group_category_name)
        rest_of_the_larger_section = stateobj.data[stateobj.data[stateobj.paths[larger_group_category_name].df_colname] == larger_group_name]
        rest_of_the_larger_section = rest_of_the_larger_section[rest_of_the_larger_section[stateobj.paths[section_category_name].df_colname] != section_name]

    # get the years where the judge was active
    overlapping_years = years
    if years is None:
        section_years = section_filtered_data[stateobj.paths['year'].df_colname].unique()
        larger_years = rest_of_the_larger_section[stateobj.paths['year'].df_colname].unique()
        overlapping_years = np.sort(list(set(section_years).intersection(set(larger_years))))
    print(section_name, 'was active in the years:', overlapping_years)

    groups_to_filter_by = []  # this list keeps track of the column names in our stateobj.data we are grouping by
    # get the column names in our stateobj.data we are grouping by
    total_number_of_subgroups = 1
    for group in inp_list_of_groups:
        groups_to_filter_by.append(stateobj.paths[group].df_colname)
        total_number_of_subgroups = total_number_of_subgroups * len(stateobj.paths[group].levels)  # i.e, if race has 5 levels, sex has 2, this should be 10

    # compare the whole stretch of years

    # first, filter for the span of years we are looking at
    section_filtered_data = section_filtered_data[section_filtered_data[stateobj.paths['year'].df_colname].isin(overlapping_years)]
    rest_of_the_larger_section = rest_of_the_larger_section[rest_of_the_larger_section[stateobj.paths['year'].df_colname].isin(overlapping_years)]

    # now, we call subset data analysis to get
    section_allyr_stats = subset_data_multi_level_summary(stateobj, section_filtered_data,
                                                          section_name, inp_list_of_groups, plot=None)
    rest_allyr_stats = subset_data_multi_level_summary(stateobj, rest_of_the_larger_section,
                                                       larger_group_name, inp_list_of_groups, plot=None)

    # build unique tuples list
    unique_identifiers = []  # list of unique tuples in df.index we will need
    unique_identifier_strings = []  # string format of unique_identifiers, used in graph titles.

    if rest_allyr_stats.index.nlevels > 1:  # if we are grouping by variables other than departure
        for ind in rest_allyr_stats.index:
            if ind[
               :-1] not in unique_identifiers:  # we do ind[:-1] here because the last identifier is always departure, and we want our grops to be everything but departure
                unique_identifiers.append(ind[:-1])  # add the unique identifier tuple
                # create and add string form of the unique identifier to unique_identifier_strings
                unique_identifier_string = ''
                for string in ind[:-1]:
                    unique_identifier_string += str(string) + ' '
                unique_identifier_string = unique_identifier_string[:-1]
                unique_identifier_strings.append(unique_identifier_string)

        for unique_id in unique_identifiers:
            print('Looking at', section_name, 'vs', stateobj.name, 'for', unique_id, 's')
            for departure_type in stateobj.order_of_outputs:
                loc_id = unique_id + (departure_type,)
                if loc_id in section_allyr_stats.index and loc_id in rest_allyr_stats.index:
                    if section_allyr_stats.loc[loc_id, 'percent'] > 1.05 * rest_allyr_stats.loc[loc_id, 'percent']:
                        print(section_name, section_category_name, 'currently has an average', departure_type,
                              'rate above', larger_group_name,  larger_group_category_name,'average in years queried')
                    elif section_allyr_stats.loc[loc_id, 'percent'] < 0.95 * rest_allyr_stats.loc[loc_id, 'percent']:
                        print(section_name, section_category_name, 'currently has an average', departure_type,
                              'rate below', larger_group_name,  larger_group_category_name,'average in years queried')
                    else:
                        print(section_name, section_category_name, 'currently has an average', departure_type,
                              'rate about at', larger_group_name,  larger_group_category_name,'average in years queried')

    else:
        unique_identifier_strings = [stateobj.name]
        print('Looking at', section_name, 'vs', stateobj.name, 'all')
        for departure_type in stateobj.order_of_outputs:
            if departure_type in section_allyr_stats.index and departure_type in rest_allyr_stats.index:
                if section_allyr_stats.loc[departure_type, 'percent'] > 1.05 * rest_allyr_stats.loc[
                    departure_type, 'percent']:
                    print(section_name, section_category_name, 'currently has an average', departure_type,
                          'rate above', larger_group_name,  larger_group_category_name,'average in years queried')
                elif section_allyr_stats.loc[departure_type, 'percent'] < 0.95 * rest_allyr_stats.loc[
                    departure_type, 'percent']:
                    print(section_name, section_category_name, 'currently has an average', departure_type,
                          'rate below', larger_group_name,  larger_group_category_name,'average in years queried')
                else:
                    print(section_name, section_category_name, 'currently has an average', departure_type,
                          'rate about at', larger_group_name,  larger_group_category_name,'average in years queried')

    #  now we get the data for graphing: multiple levels in inp_list_of_groups
    if rest_allyr_stats.index.nlevels > 1:
        #  now we create the data for the by year graphs
        years_lst = []  # list of lists for each year we will append a lis tof [year, section_breakdown, rest_breakdown]
        ret_pandas_data = {}

        for year in overlapping_years:
            #  first, filter our data for the year we want
            year_section_data = section_filtered_data[section_filtered_data[stateobj.paths['year'].df_colname] == year]
            year_rest_of_larger_data = rest_of_the_larger_section[rest_of_the_larger_section[stateobj.paths['year'].df_colname] == year]

            #  now we group by to get section breakdowns
            year_section_breakdown = subset_data_multi_level_summary(stateobj, year_section_data, section_name,
                                                                     inp_list_of_groups, plot=None)
            year_restof_breakdown = subset_data_multi_level_summary(stateobj, year_rest_of_larger_data, larger_group_name,
                                                                    inp_list_of_groups, plot=None)

            section_data_percents = np.zeros((len(stateobj.order_of_outputs), len(unique_identifiers)))
            rest_of_data_percents = np.zeros((len(stateobj.order_of_outputs), len(unique_identifiers)))
            section_data_counts = np.zeros((len(stateobj.order_of_outputs), len(unique_identifiers)))
            rest_of_data_counts = np.zeros((len(stateobj.order_of_outputs), len(unique_identifiers)))

            for dep in range(len(stateobj.order_of_outputs)):
                for unique_id in range(len(unique_identifiers)):
                    loc_id = unique_identifiers[unique_id] + (stateobj.order_of_outputs[dep],)
                    if loc_id in year_section_breakdown.index:
                        section_data_percents[dep, unique_id] = year_section_breakdown.loc[loc_id, 'percent']
                        section_data_counts[dep, unique_id] = year_section_breakdown.loc[loc_id, 'count']
                    if loc_id in year_restof_breakdown.index:
                        rest_of_data_percents[dep, unique_id] = year_restof_breakdown.loc[loc_id, 'percent']
                        rest_of_data_counts[dep, unique_id] = year_restof_breakdown.loc[loc_id, 'count']

            years_lst.append({'section_percents': section_data_percents,
                                     'rest_percents': rest_of_data_percents,
                                     'section_counts': section_data_counts,
                                     'rest_counts': rest_of_data_counts})

            ret_pandas_data[year] = {'section': year_section_breakdown, 'rest': year_restof_breakdown}

        #  now it's time to make graphs

        for unique_id in range(len(unique_identifiers)):
            section_y_data = np.zeros((len(stateobj.order_of_outputs), len(overlapping_years)))
            rest_y_data = np.zeros((len(stateobj.order_of_outputs), len(overlapping_years)))
            section_y_counts = np.zeros((len(stateobj.order_of_outputs), len(overlapping_years)))

            for year in range(len(years_lst)):
                for departure_type in range(len(stateobj.order_of_outputs)):
                    section_y_data[departure_type][year] = years_lst[year]['section_percents'][departure_type][unique_id]
                    rest_y_data[departure_type][year] = years_lst[year]['rest_percents'][departure_type][unique_id]
                    section_y_counts[departure_type][year] = years_lst[year]['section_counts'][departure_type][unique_id]
            if plot:
                section_count = np.sum(section_y_counts)
                plot_section_and_rest_data(overlapping_years, section_y_data, rest_y_data, section_count, 
                                           stateobj.colors, unique_identifier_strings[unique_id], stateobj.order_of_outputs, 
                                           section_name, section_category_name,
                                           larger_group_name, larger_group_category_name)
                
        return ret_pandas_data

    else:  # this is if we are only grouping by departure
        section_y_data = np.zeros((len(stateobj.order_of_outputs), len(overlapping_years)))
        rest_y_data = np.zeros((len(stateobj.order_of_outputs), len(overlapping_years)))
        section_y_counts = np.zeros((len(stateobj.order_of_outputs), len(overlapping_years)))
        section_y_counts = np.zeros((len(stateobj.order_of_outputs), len(overlapping_years)))
        for year in range(len(overlapping_years)):
            year_section_data = section_filtered_data[section_filtered_data[stateobj.paths['year'].df_colname] == overlapping_years[year]]
            year_rest_of_larger_data = rest_of_the_larger_section[rest_of_the_larger_section[stateobj.paths['year'].df_colname] == overlapping_years[year]]

            #  now we group by to get section breakdowns
            year_section_breakdown = subset_data_multi_level_summary(stateobj, year_section_data, section_name,
                                                                     inp_list_of_groups, plot=None)
            year_restof_breakdown = subset_data_multi_level_summary(stateobj, year_rest_of_larger_data, stateobj.name,
                                                                    inp_list_of_groups, plot=None)

            for dep_type in range(len(stateobj.order_of_outputs)):
                if stateobj.order_of_outputs[dep_type] in year_section_breakdown.index:
                    section_y_data[dep_type, year] = year_section_breakdown.loc[
                        stateobj.order_of_outputs[dep_type], 'percent']
                    section_y_counts[dep_type, year] = year_section_breakdown.loc[
                        stateobj.order_of_outputs[dep_type], 'count']
                if stateobj.order_of_outputs[dep_type] in year_restof_breakdown.index:
                    rest_y_data[dep_type, year] = year_restof_breakdown.loc[stateobj.order_of_outputs[dep_type], 'percent']
        if plot:
            section_count = np.sum(section_y_counts)
            plot_section_and_rest_data(overlapping_years, section_y_data, rest_y_data, section_count, 
                                       stateobj.colors,'all', stateobj.order_of_outputs, 
                                       section_name, section_category_name,
                                       larger_group_name, larger_group_category_name)
            
        return section_allyr_stats, rest_allyr_stats
    
    
    
    