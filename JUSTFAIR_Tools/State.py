#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:19:24 2023

@author: jason, alexis
"""
import pandas as pd
import numpy as np

# +
class State:
    def __init__(self, inp_name, inp_data_url, inp_paths, 
                 order_of_outputs = ['Above Departure', 'Within Range', 'Below Range', 
                                        'Missing, Indeterminable, or Inapplicable']):
        self.name = inp_name
        
        
        url=inp_data_url
        url='https://drive.google.com/uc?id=' + url.split('/')[-2]
        self.data = pd.read_csv(url, low_memory = False)  # pandas dataframe object
        
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
        subset_dat = filter_years(self.data, years)  #first, filter for the years we are looking for
        return subset_data_multi_level_summary(self.data, subset_dat, self.name, inp_list_of_groups, plot)

### Filter Years

    def filter_years(self, years):
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
        subset_dat = self.data
        if years is not None:  
            # if the user specifies a year range, filter the data for those years
            subset_dat = self.data[self.data[self.paths['year'][0]].isin(years)]
        return subset_dat

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

### Bar Plot

    def plot_departures_bar(self, departure_labels, departure_porportions,base_group_str, subgroup, s = True):
        '''
        Used to plot a horizontal bar graph to view results.

        Parameters:
            departure_labels: the labels on our departure variable.  This is the x labels
            departure_proportions: the proportions for each label.  This is the y label.
            subgroup: the subgroup that this bar graph corrosponds to (used in the title). Only used when looking at more than one level.
            s: for formatting, adds an s to the end of the title string

        Returns:
            A bar plot based on the input of the parameters
        '''
        subgroup_str = ''
        for item in subgroup:
            subgroup_str += str(item) + ' '
        if s:  
            subgroup_str = subgroup_str[:-1]
            subgroup_str+='s'

        fig, ax = plt.subplots(figsize = (10,7))
        colors = ['lightcoral', 'lightgrey', 'cornflowerblue', 'turquoise']

        barh = ax.barh(departure_labels, departure_porportions, color=colors)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Percentage')

        ax.bar_label(barh, fmt='%.2f%%')
        ax.set_xlim(right=100)

        ttl = 'Proportional sentences for '+ base_group_str + ' ' + subgroup_str
        ax.set_title(ttl)

### Pie Chart

    def plot_departures_pie(self, departure_labels, departure_porportions, base_group_str, subgroup, s = True):
        '''
        Used to plot a pie chart to view results.  This is just like the hoizontal bar graph, but a pie chart.

        Parameters:
            departure_labels: the labels on our departure variable.  This is the x labels
            departure_proportions: the proportions for each label.  This is the y label.
            subgroup: the subgroup that this bar graph corrosponds to (used in the title).  Only used when looking at more than one level.
            s: for formatting, adds an s to the end of the title string

        Returns:
            Pie chart based off the given input information
        '''
        subgroup_str = ''
        for item in subgroup:
            subgroup_str += str(item) + ' '
        if s:  
            subgroup_str = subgroup_str[:-1]
            subgroup_str+='s'

        fig, ax = plt.subplots(figsize = (10,7))
        colors = ['lightcoral', 'lightgrey', 'cornflowerblue', 'turquoise']

        ax.pie(departure_porportions, labels=departure_labels, autopct='%1.1f%%', colors = colors)


        ttl = 'Proportional sentences for '+ base_group_str + ' ' + subgroup_str
        ax.set_title(ttl)

### Stacked Bar Plot

    def plot_departures_stacked(self, x_values_list, y_values_list, base_group_str, subgroup, legend, s = True):
        '''
        Used to plot a stacked horizontal bar graph to view results.

        Parameters:
            x_values_list: the labels on our departure variable.  This is the x labels.  in the format of an 1 x number of subgroups
            y_values_list: the porportions for each label.  This is the y label.  In the format of (number of subgroups) x (number of items in the state's order of outouts)
            base_group_str: this is the beginning of the plot title string, some examples could be the state name, or a county or Judge name
            subgroup: the subgroup that this bar graph corrosponds to (used in the title).  Only used when looking at more than one level.
            s: for formatting, adds an s to the end of the title string

        Returns:
            Stacked bar graph based off the given input information
        '''
        subgroup_str = ''
        for item in subgroup:
            subgroup_str += str(item) + ' '
        if s:  
            subgroup_str = subgroup_str[:-1]
            subgroup_str+='s'

        fig, ax = plt.subplots(figsize = (12, 1 * len(x_values_list)))

        bar_colors = ['lightcoral', 'lightgrey', 'cornflowerblue', 'turquoise']

        b = np.zeros(len(x_values_list))
        for i in range(len(y_values_list)):
            ax.barh(x_values_list, y_values_list[i], left = b, color = bar_colors[i], label = legend[i], edgecolor='black')
            b += y_values_list[i]
        ax.set_xlabel('Percentage')
        ax.set_xlim((-5,105))
        ttl = 'Proportional sentences for '+ base_group_str[0] + ' ' + subgroup_str
        ax.set_title(ttl)
        ax.legend(bbox_to_anchor = (1.45, 0.6), loc='center right')


        # For each patch (basically each rectangle within the bar), add a label.
        #we are 
        len_to_beat = 0
        if isinstance(y_values_list[0], float):
            len_to_beat = 1
        else:
            len_to_beat = len(y_values_list[0])

        for i in range(len(ax.patches)):
            bar = ax.patches[i]
            if i < len_to_beat:  # above departure / first bar
                ax.text(
                  bar.get_x() + bar.get_width()/2,
                  bar.get_y() + bar.get_height() / 2,
                  # This is actual value we'll show.
                  str(round(bar.get_width(),2)) + '%',
                  # Center the labels and style them a bit.
                  ha='right',
                  weight='bold',
                  size=11)
            elif i < 3 * len_to_beat:  # second and third bars (in range, below range)
                ax.text(
                  bar.get_x() + bar.get_width()/2,
                  bar.get_y() + bar.get_height() / 2,
                  # This is actual value we'll show.
                  str(round(bar.get_width(),2)) + '%',
                  # Center the labels and style them a bit.
                  ha='center',
                  weight='bold',
                  size=11)
            else: # i % 4 == 3  last bar (missing, indeterminable, inapplicable)
                ax.text(
                  bar.get_x() + bar.get_width()/2,
                  bar.get_y() + bar.get_height() / 2,
                  # This is actual value we'll show.
                  str(round(bar.get_width(),2)) + '%',
                  # Center the labels and style them a bit.
                  ha='left',
                  weight='bold',
                  size=11)

### Judge vs State Bar Graph

    def plot_section_vs_state(self, order_of_outputs, section_averages, state_avg_for_years, section_name, statename):
        '''
        Plots a comparison horizontal bar graph comparing the state to the judge in question.

        Parameters:
            order_of_outputs: a state objects order_of_outputs variable, used to deterimine the order of bars on the chart
            section_averages: the judge's averages.  In the shape of 1 x (length of order of outputs)
            state_avg_for_years: the state's averages.  In the shape of 1 x (length of order of outputs)
            section_name: name of the judge, for formatting the title
            statename: name of the state, for formatting the title

        Returns:
            Bar plot of the justice sentencing based on input parameter criteria
        '''
        x = np.arange(len(order_of_outputs))
        y_data = {}
        y_data[section_name] = section_averages
        y_data[statename] = state_avg_for_years

        width = 0.35
        multiplier = 0

        bar_colors = ['lightcoral', 'lightgrey', 'cornflowerblue', 'turquoise']

        fig, ax = plt.subplots(figsize = (10,7))

        for attribute, measurement in y_data.items():
            offset = width * multiplier
            rects = ax.barh(x + offset, measurement, width, label=attribute, color = bar_colors, edgecolor='black')
            ax.bar_label(rects, padding=3, fmt='%.2f%%' + '   ('+ attribute+')')
            multiplier += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_xlabel('percentage (%)')
        ttl = 'Comparing ' + section_name + ' sentencing to ' + statename + ' sentencing'
        ax.set_title(ttl)
        ax.set_yticks(x + width/2)
        ax.set_yticklabels(order_of_outputs)
        ax.set_xlim(0, 119)

### Judge vs State Line Graph

    def plot_section_vs_state_trends(self, overlapping_years, section_data_y, state_data_y, section_name):
        '''
        Plots a line graphs comparing the state to the judge in question.

        Parameters:
            stateobj:  A state object.  Used to access the state's anme and order of outputs.
            ovarlapping years:  The years that the judge worked (whaich years of the state's data did the judge work in?)
            section_data_y: the section's averages.  In the shape of (number of overlapping years) x (length of order of outputs)
            state_data_y: the state's averages.  In the shape of (number of overlapping years) x (length of order of outputs)
            section_name: name of the judge, for formatting the title

        Returns:
            Line graph of the justice sentencing based on input parameter criteria
        '''
        colors = ['lightcoral', 'lightgrey', 'cornflowerblue', 'turquoise']

        for col in range(len(self.order_of_outputs)):
            fig, ax = plt.subplots(figsize=(10, 7))
            ax.plot(overlapping_years, section_data_y[:,col], '-o', label=section_name, color = colors[col])
            ax.plot(overlapping_years, state_data_y[:,col], '--o', label=self.name, color = colors[col])
            ttl = 'Comparing ' + section_name + ' and' + self.name + ' on ' + self.order_of_outputs[col]
            ax.set_title(ttl)
            ax.set_xlabel('year')
            ax.set_ylabel('percentage (%)')
            ax.legend(loc = 'upper right')


        fig, ax = plt.subplots(figsize=(10, 7))
        for col in range(len(self.order_of_outputs)):
            ax.plot(overlapping_years, section_data_y[:,col] - state_data_y[:,col], '-o', 
                    label=self.order_of_outputs[col], color = colors[col])
        ax.axhline(y = 0, color = 'black')

        ttl = 'Comparing ' + section_name + ' difference from ' + self.name + ' levels'
        ax.set_title(ttl)
        ax.set_xlabel('year')
        ax.set_ylabel('percentage (%)')
        ax.legend(loc = 'upper right')

### Plotting Data

    def plot_df(self, df, plot_type, groups, base_group_str):
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
            unique_identifier_strings = [self.data.order_of_outputs]

        # plotting time.
        if plot_type == 'stacked bar':
            if len(groups) > 0:  #we're dealing with more then one grouping variable
                porportions = np.zeros((len(self.order_of_outputs), len(unique_identifiers)))
                for dep in range(len(self.order_of_outputs)):
                    for unique_id in range(len(unique_identifiers)):
                        loc_id = unique_identifiers[unique_id] + (self.order_of_outputs[dep],)
                        if loc_id in df.index:
                            porportions[dep, unique_id] = df.loc[loc_id,]
                #plot
                plot_departures_stacked(unique_identifier_strings, porportions, base_group_str, groups, self.order_of_outputs)
            else:  # just departure
                porportions = []
                for departure_type in self.order_of_outputs:
                    porportions.append(df.loc[departure_type,])
                #plot
                groups.insert(0, self.name)  # we need the state name for plotting purposes
                plot_departures_stacked([self.name], porportions, base_group_str, groups, self.order_of_outputs, s = False)

        if plot_type == 'bar' or plot_type == 'pie':  # not stacked bars
            if len(groups) > 0:  #we're dealing with more then one grouping variable
                for unique_id in unique_identifiers:
                    porportions = [0,0,0,0]
                    pos = 0
                    for deperture_type in self.order_of_outputs:
                        comb_ind = unique_id + (deperture_type,)
                        if comb_ind in df.index:
                            porportions[pos] = df.loc[comb_ind,]
                        pos += 1

                    unique_id = (self.name,) + unique_id
                    if plot_type == 'bar':
                        plot_departures_bar(self.order_of_outputs, porportions, base_group_str, unique_id)
                    else:  # pie
                        plot_departures_pie(self.order_of_outputs, porportions, base_group_str, unique_id)
            else:
                porportions = []
                for departure_type in self.order_of_outputs:
                    porportions.append(df.loc[departure_type,])
                if plot_type == 'bar':
                    plot_departures_bar(self.order_of_outputs, porportions, base_group_str, [], s = False) 
                else:  # pie
                    plot_departures_pie(self.order_of_outputs, porportions, base_group_str, [], s = False)  

### Filtered Multilevel Summary

    def subset_data_multi_level_summary(self, subset_dat, base_group_str, inp_list_of_groups = ['departure'], plot = 'stacked bar'):
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
            groups_to_filter_by.append(self.paths[group][0])
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
            if self.paths[group][1] is not None:
                perc = perc.rename(self.paths[group][1], level = l)
                counts = counts.rename(self.paths[group][1], level = l)
            l += 1
        # pull the data we need from our dataframes    
        perc = perc.iloc[:,0]  # all columns are the same, so we pull the first one
        counts = counts.iloc[:,0]  # all columns are the same, so we pull the first one

        #create an output dataframe to return
        comb_df = pd.concat([counts,perc],axis=1)  # combine our two columns into a dataframe
        comb_df.columns = ['count', 'percent']  # rename columns 
        if plot == 'stacked bar':
            plot_df(self.data, perc, 'stacked bar', inp_list_of_groups[:-1], base_group_str)  # call our plotting function
        elif plot == 'bar':
            plot_df(self.data, perc, 'bar', inp_list_of_groups[:-1], base_group_str)
        elif plot == 'pie':
            plot_df(self.data, counts, 'pie', inp_list_of_groups[:-1], base_group_str)

        return comb_df

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
            for col in range(len(stateobj.order_of_outputs)):
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

    def individual_section_analysis(stateobj, section_name, inp_list_of_groups = ['departure'], years = None, plot = True):
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
        section_filtered_data = self.data[self.data[self.paths['judge'][0]]== section_name]
        # get the years where the judge was active
        overlapping_years = years
        if years is None:
            overlapping_years = np.sort(section_filtered_data[self.paths['year'][0]].unique())
        print(section_name, 'was active in the years:', overlapping_years)

        groups_to_filter_by = []  # this list keeps track of the column names in our stateobj.data we are grouping by
        # get the column names in our stateobj.data we are grouping by
        for group in inp_list_of_groups:
            groups_to_filter_by.append(self.paths[group][0])
        #groups_to_filter_by.append(stateobj.paths['departure'][0])  # add departure as a group by on the end, as that is our 
                                                                    # the variable we are looking at

        #time to get the aggregate


        #grouping by 
        #divide by count(all_items_but_daparture) for departure percentages for each subgroup
        counts = section_filtered_data.groupby(self.paths['departure'][0]).count()
        perc = round( (100 * counts/ section_filtered_data.shape[0]),2)  #if we are just grouping by departure, 
                                                                       #we divide by data frame length
        # renames the values that have levels
        perc = perc.rename(self.paths['departure'][1], level = 0)
        counts = counts.rename(self.paths['departure'][1], level = 0)

        # pull the data we need from our dataframes    
        perc = perc.iloc[:,0]  # all columns are the same, so we pull the first one
        counts = counts.iloc[:,0]  # all columns are the same, so we pull the first one

        #create an output dataframe to return
        agg_comb_df = pd.concat([counts,perc],axis=1)  # combine our two columns into a dataframe
        agg_comb_df.columns = ['count', 'percent']  # rename columns 

        state_avg_for_years = calc_state_avg_for_yearspan(overlapping_years)
        section_averages = []
        for departure_type in self.order_of_outputs:
            section_averages.append(perc.loc[departure_type,])

        if plot:
            plot_judge_vs_state(self.order_of_outputs, section_averages, 
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

