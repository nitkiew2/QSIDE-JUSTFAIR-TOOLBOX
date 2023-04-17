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
#from JUSTFAIR_Tools.plotting import plot_section_vs_state, plot_section_vs_state_trends, plot_section_and_rest_data

### State class
class State:
    
    def __init__(self, inp_name, inp_data_url, inp_paths, 
                 order_of_outputs = ['Above Departure', 'Within Range', 'Below Range', 
                                        'Missing, Indeterminable, or Inapplicable'], 
                 colors = ['lightcoral', 'lightgrey', 'cornflowerblue', 'turquoise'],
                 using_url = True):
        """
        Constructor for the state class.  State objects are how you call analysis functions for a state's judicial data.

        Parameters
        ----------
        inp_name : str 
            the name of the state.
        inp_data_url : str
            the string to access the state's data.  either is a url from JUSTFAIR's google drive or a string for a local filepath.  
            Make sure to read the tutorial on how to make a state object if you need more infomraiton.
            Also, if using a local file, remember to set using_url to False
        inp_paths : dict
            paths dicitonary.  Paths are how we relate easy to use terms / terms we want to use to column names in the dataset
            See the Path class and the state setup guide for more info
            example:  inp_paths['name we want to use'] = Path('df_column name', levels_dict)
        order_of_outputs : list, optional
            orders the outputs of the 'departure' variable.  Note, you should name the path to your sentending departure as 'departure' 
            The default is ['Above Departure', 'Within Range', 'Below Range', 'Missing, Indeterminable, or Inapplicable'].
        colors : list, optional
            list of colors, pairs with order of outputs.  Pairingis the first item in order of outputs is the first color in colors.  MUST be the same length as order_of_outputs 
            he default is ['lightcoral', 'lightgrey', 'cornflowerblue', 'turquoise'].
        using_url : bool, optional
            If true, load assuming a url is given.  If false, assumes loading from local file. The default is True.

        Returns
        -------
        None.

        """
        self.name = inp_name  # set the name
        
        if using_url:  
            url=inp_data_url
            url='https://drive.google.com/uc?id=' + url.split('/')[-2]  # convert url to correct format
            self.data = pd.read_csv(url, low_memory = False)  # pandas dataframe object
        else:
            file_path = inp_data_url
            self.data = pd.read_csv(file_path, low_memory = False)  # just reading from a file
        
        self.paths = inp_paths  # dictionary object.  
        # Always follows the format useful_id --> (name_in_data, dict(levels)).
        # Levels doesn't always exist, but is needed for variables like departure
        #path pairs are always (name_in_data, dict(levels)) or (name_in_data, None)
        
        self.order_of_outputs = order_of_outputs
        #this is how you want to arrange your output on graphs
        #is basically the order of the levels in paths[departure][1]
        
        self.colors = colors  # assign colors here.  remember this dictates what graphs will look like
        
        self.average_percents= []  #list, for all years, state averages for all people
        self.yearly_average_percents = {}  # dictionary, state averages for all people for each year
                                             # format of: year (int) --> [averages_list]
        
        self.years = np.sort(self.data[self.paths['year'].df_colname].unique())  # generate a sorted list of years for data



        ###  get average_percents
        
        counts = self.data.groupby(self.paths['departure'].df_colname).count()  # group by each departure type
        counts = counts.rename(self.paths['departure'].levels)  # rename departure to match the levels dictionary
        counts = counts.iloc[:,0]  # pull the counts

        for item in self.order_of_outputs:
            self.average_percents.append(round((100 * counts.loc[item]  /  self.data.shape[0]),2))  # calculate the percent by dividing each subtotal by the total
        
        ### get yearly_average_percents
        for year in self.years:
            subset_dat = self.data[ self.data[self.paths['year'].df_colname ] == year]  # filter for the year
            counts = subset_dat.groupby(self.paths['departure'].df_colname).count()  # group by departure type
            counts = counts.rename(self.paths['departure'].levels)  # rename departure to match the levels dictionary 
            counts = counts.iloc[:,0]  # pull the counts
            
            percentages = []
            for item in self.order_of_outputs:
                percentages.append(round((100 * counts.loc[item]  /  subset_dat.shape[0]),2))  # calcualte percents
            self.yearly_average_percents[year] = percentages  # add the value to the dictionary


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
        """
        Note, all the heavy lifting is done by subset_data_multi_level_summary, this function just does some simple filtering and passes the information along.
        
        Grouping by any combination (or none) of factor variables.  There is only one assumption to calling this function: the last level passed into inp_list_of_groups is 
        measuring sentencing departure.  
        Basically, calling with only \['departure'\] means we are not grouping by any factor variable. Adding variables before it will break your populaiton into subgroups
        Using the plot parameter you can specify if you want a bar, stacked bar or pie. Type  None or something other then bar, stacked bar, or pie to not generate graphs
        
        Parameters:
            stateobj: the state in question.  We need the state's yearly_average_percents to plot the graph
            inp_list_of_groups: Choose path description using string name
            years: the specified years.  Either a range or none
            plot: Choose type of plot based off of ('stacked bar', 'bar', 'pie')

        Returns:
            Specified type of plot and data table of the specified data

        Parameters
        ----------
        inp_list_of_groups : list, optional
            the list of groups to group by.  Remember, keep the last values as 'departure', but you can add values from your paths object before it. The default is ['departure'].
        years : TYPE, optional
            enter a range of years you with to filter for.  If none, looks at all years. The default is None.
        plot : string, optional
            specifys the plot type.  If not 'bar', 'stacked bar', or 'pie', will not plot.  reccomend entering None if not plotting. The default is 'stacked bar'.

        Returns
        -------
        Pandas DataFrame
            returns a DataFrame that has allthe counts and percentages associated with the charts. 

        """
        # we should have a subplots vs stacked parameter here maybe?  either do lots of individual graphs or stacked
        subset_dat = filter_years(self, years)  #first, filter for the years we are looking for
        return subset_data_multi_level_summary(self, subset_dat, self.name, inp_list_of_groups, plot)



### Average from Filter Years

    def calc_state_avg_for_yearspan(self, years):
        """
        Calculates the state's averages for a select span of years.  It uses the state's yearly_average_percents 
        and calculates the mean for the selected years by using the second parameter 'years'.
        
        Parameters
        ----------
        years : list
            the specified years to get the average of.

        Returns
        -------
        rounded : float
            returns the average sentencing proportions (percentages) per year, rounded to 2 decimal places.

        """
        avg_for_yearspan = []
        for year in years:
            avg_for_yearspan.append(self.yearly_average_percents[year])
        avg_for_yearspan = np.array(avg_for_yearspan)
        means = np.mean(avg_for_yearspan, axis = 0)  # take the average of each column.  Gives the average for each departure type
        rounded = means.round(2)
        return rounded





### State Trends

    def state_trends(self, compressed = False):
        """
        Plot the departure trends for the state.  Note this is an aggregate, no subgrouping can be done with this function

        Parameters
        ----------
        compressed : bool, optional
            If true, plot all lines on one graph.  If false, plot each line on its own graph. The default is False.

        Returns
        -------
        None.

        """
        state_data_y = np.zeros((len(self.years), len(self.order_of_outputs)))
        for year in range(len(self.years)):
            state_data_y[year] = self.yearly_average_percents[self.years[year]]

        if compressed:
            fig, ax = plt.subplots(figsize=(10, 7))  # create figure
            for col in range(len(self.order_of_outputs)):  # plot each line on the same figure
                ax.plot(self.years, state_data_y[:,col], '-o', label=self.order_of_outputs[col], color = self.colors[col])
            # add title, axis, labels, legend
            ttl = self.name + ' Trends'
            ax.legend()
            ax.set_title(ttl)
            ax.set_xlabel('year')
            ax.set_ylabel('percentage (%)')
        else:
            for col in range(len(self.order_of_outputs)):  # create a graph for each depatrure type
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(self.years, state_data_y[:,col], '-o', color = self.colors[col])
                ttl = self.name + ' ' + self.order_of_outputs[col] + ' over time.'
                ax.set_title(ttl)
                ax.set_xlabel('year')
                ax.set_ylabel('percentage (%)')



    ### compare_section_to_larger_group
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
                
 
    ### compare_judge_to_county
    def compare_judge_to_county(self, judge_name, county_name,
                                        inp_list_of_groups = ['departure'], years=None, plot=True):
        """
        Compare a judge to a county they operate in. A shell function on tb_compare_section_to_larger_group, but fills in some inputs for you
    
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
 
    
    ### compare_judge_to_state 
    def compare_judge_to_state(self, judge_name, inp_list_of_groups = ['departure'], years=None, plot=True):
        """
        Compare a judge to a state they operate in. A shell function on tb_compare_section_to_larger_group, but fills in some inputs for you
    
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

        