#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:20:21 2023

@author: jason
"""
import numpy as np
import pandas as pd
from JUSTFAIR_Tools.plotting import plot_departures_bar, plot_departures_stacked, plot_departures_pie



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
            plot_departures_stacked(unique_identifier_strings, porportions, base_group_str, groups, stateobj.order_of_outputs)
        else:  # just departure
            porportions = []
            for departure_type in stateobj.order_of_outputs:
                porportions.append(df.loc[departure_type,])
            #plot
            groups.insert(0, stateobj.name)  # we need the state name for plotting purposes
            plot_departures_stacked([stateobj.name], porportions, base_group_str, groups, stateobj.order_of_outputs, s = False)

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
                    plot_departures_bar(stateobj.order_of_outputs, porportions, base_group_str, unique_id)
                else:  # pie
                    plot_departures_pie(stateobj.order_of_outputs, porportions, base_group_str, unique_id)
        else:
            porportions = []
            for departure_type in stateobj.order_of_outputs:
                porportions.append(df.loc[departure_type,])
            if plot_type == 'bar':
                plot_departures_bar(stateobj.order_of_outputs, porportions, base_group_str, [], s = False) 
            else:  # pie
                plot_departures_pie(stateobj.order_of_outputs, porportions, base_group_str, [], s = False)  

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
        plot_df(stateobj, perc, stateobj.colors, 'stacked bar', inp_list_of_groups[:-1], base_group_str)  # call our plotting function
    elif plot == 'bar':
        plot_df(stateobj, perc, stateobj.colors, 'bar', inp_list_of_groups[:-1], base_group_str)
    elif plot == 'pie':
        plot_df(stateobj, counts, stateobj.colors, 'pie', inp_list_of_groups[:-1], base_group_str)

    return comb_df