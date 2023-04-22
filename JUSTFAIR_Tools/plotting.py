# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 17:39:23 2023

@author: MSU QSIDE JUSTFAIR 2023 Team
"""

import matplotlib.pyplot as plt
import numpy as np

### Bar Plot

def plot_departures_bar(departure_labels, departure_porportions, colors, base_group_str, subgroup, s = True):
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

    barh = ax.barh(departure_labels, departure_porportions, color=colors)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Percentage')

    ax.bar_label(barh, fmt='%.2f%%')
    ax.set_xlim(right=100)

    ttl = 'Proportional sentences for '+ base_group_str + ' ' + subgroup_str
    ax.set_title(ttl)

### Pie Chart

def plot_departures_pie(departure_labels, departure_porportions, colors, base_group_str, subgroup, s = True):
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

    ax.pie(departure_porportions, labels=departure_labels, autopct='%1.1f%%', colors = colors)


    ttl = 'Proportional sentences for '+ base_group_str + ' ' + subgroup_str
    ax.set_title(ttl)

### Stacked Bar Plot

def plot_departures_stacked(x_values_list, y_values_list, colors, base_group_str, subgroup, legend, s = True):
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


    b = np.zeros(len(x_values_list))
    for i in range(len(y_values_list)):
        ax.barh(x_values_list, y_values_list[i], left = b, color = colors[i], label = legend[i], edgecolor='black')
        b += y_values_list[i]
    ax.set_xlabel('Percentage')
    ax.set_xlim((-5,105))
    ttl = 'Proportional sentences for '+ base_group_str + ' ' + subgroup_str
    ax.set_title(ttl)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


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

    

    
def section_and_rest_data_plot_broken_axis_line_graph(x_data,section_y_data, rest_y_data, count, 
                                                      colors,population_subset, order_of_outputs, 
                                                      section_name, section_category_name,
                                                      larger_group_name, larger_group_category_name):
    """
    Plot the sentencing trends for a unique identifier for both a section and a larger group.
    
    Creates two graphs:
        the top graph will plot the trends for the section and the rest over time
            this will be a split axis graph
        the bottom graph shows the section vs larger group differeence (section - rest)

    Parameters
    ----------
    x_data : list
        the overlapping year data between the section and the rest of the larger section it is aprt of.
    section_y_data : numpy array: 2 dimensional 
        a two dimentional list to hold the section's sentencing breakdown. I
        n the shape of (length(x_data) * length(state.order_of_outputs)).
    rest_y_data : numpy array: 2 dimensional 
        a two dimentional list to hold the larger group's sentencing breakdown. I
        n the shape of (length(x_data) * length(state.order_of_outputs)).
    count : int
        the total number of people sentenced for this unique identifier.
    colors : list
        DESCRIPTION.
    population_subset : string
        the name of the unique identifier.  for example 'white female'
    order_of_outputs : list
        a state object's order of outputs.
    section_name : string
        the name of the section being analyzed.
    section_category_name : string
        the name of the category the section is a part of.  MUST be in the satate's paths.
    larger_group_name : string
        the name of the larger group in the analysis.
    larger_group_category_name : string
        the category of the larger group.

    Returns
    -------
    None.

    """
    
    # seeing which row goes on the top graph
    section_y_data_medians = np.median(section_y_data, axis = 1)
    highest_median_index = np.argmax(section_y_data_medians)
    
    section_y_upper = section_y_data[highest_median_index,:]
    section_y_lower = np.delete(section_y_data,highest_median_index, axis = 0)
    rest_y_upper = rest_y_data[highest_median_index,:]
    rest_y_lower = np.delete(rest_y_data,highest_median_index, axis = 0)
    
    upper_max = np.max([np.max(section_y_upper), np.max(rest_y_upper)])
    upper_min = np.min([np.min(section_y_upper), np.min(rest_y_upper)])
    lower_max = np.max([np.max(section_y_lower), np.max(rest_y_lower)])
    lower_min = np.min([np.min(section_y_lower), np.min(rest_y_lower)])
    
    
    # source: https://matplotlib.org/stable/gallery/subplots_axes_and_figures/broken_axis.html
    
    fig, (top, bot) = plt.subplots(2, 1, sharex=True, figsize = (10,8))
    fig.subplots_adjust(hspace=0.05)  # adjust space between axes
    
    #plot the top
    lab = section_name + ' ' + order_of_outputs[highest_median_index]
    top.plot(x_data, section_y_data[highest_median_index], '-o',
             color = colors[highest_median_index], label = lab)
    
    lab = larger_group_name + ' ' + order_of_outputs[highest_median_index]
    top.plot(x_data, rest_y_data[highest_median_index], '--o',
             color = colors[highest_median_index], label = lab)


    #plot the bottom
    for dep_type in range(len(order_of_outputs)):
        if dep_type != highest_median_index:
            lab = section_name + ' ' + order_of_outputs[dep_type]
            bot.plot(x_data, section_y_data[dep_type], '-o',
                     color = colors[dep_type], label = lab)
            
            lab = larger_group_name + ' ' + order_of_outputs[dep_type]
            bot.plot(x_data, rest_y_data[dep_type], '--o',
                     color = colors[dep_type], label = lab)
    
    # zoom-in / limit the view to different portions of the data
    top.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    bot.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    top.set_ylim(upper_min*0.95, np.max([upper_max*1.05,1]))  # top section
    bot.set_ylim(lower_min*0.95, lower_max*1.05)  #bottom section
    
    # hide the spines between top and bot
    top.spines.bottom.set_visible(False)
    bot.spines.top.set_visible(False)
    top.xaxis.tick_top()
    top.tick_params(labeltop=False)  # don't put tick labels at the top
    bot.xaxis.tick_bottom()
    
    #this part creates the split
    
    d = .5  # proportion of vertical to horizontal extent of the slanted line
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
                  linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    top.plot([0, 1], [0, 0], transform=top.transAxes, **kwargs)
    bot.plot([0, 1], [1, 1], transform=bot.transAxes, **kwargs)
    
    # add titles and labels
    bot.set(xlabel='year', ylabel='percentage')
    ttl = section_name +' vs ' + larger_group_name + ' on ' + population_subset + ' sentencing.  N=' + str(count)
    fig.suptitle(ttl)
    
    
    #second graph, differences (section data - rest of data, so if judge is higher we see a positive number)
    plt.figure(figsize = (10,4))
    diffs = section_y_data - rest_y_data
    for dep_type in range(len(order_of_outputs)):
        plt.plot(x_data, diffs[dep_type], '-o',
            color = colors[dep_type], label = order_of_outputs[dep_type])
    plt.axhline(y=0, color = 'black')
    ttl = section_name +' vs ' + larger_group_name + ' differences on ' + population_subset + ' sentencing'
    plt.title(ttl)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        

def section_and_rest_data_plot_line_graph(x_data,section_y_data,rest_y_data, count, 
                                          colors, population_subset,order_of_outputs, 
                                          section_name, section_category_name,
                                          larger_group_name, larger_group_category_name):
    """
    Plot the sentencing trends for a unique identifier for both a section and a larger group.
    
    Creates two graphs:
        the top graph will plot the trends for the section and the rest over time
            this will be one single, normal plot
        the bottom graph shows the section vs larger group differeence (section - rest)

    Parameters
    ----------
    x_data : list
        the overlapping year data between the section and the rest of the larger section it is aprt of.
    section_y_data : numpy array: 2 dimensional 
        a two dimentional list to hold the section's sentencing breakdown. I
        n the shape of (length(x_data) * length(state.order_of_outputs)).
    rest_y_data : numpy array: 2 dimensional 
        a two dimentional list to hold the larger group's sentencing breakdown. I
        n the shape of (length(x_data) * length(state.order_of_outputs)).
    count : int
        the total number of people sentenced for this unique identifier.
    colors : list
        DESCRIPTION.
    population_subset : string
        the name of the unique identifier.  for example 'white female'
    order_of_outputs : list
        a state object's order of outputs.
    section_name : string
        the name of the section being analyzed.
    section_category_name : string
        the name of the category the section is a part of.  MUST be in the satate's paths.
    larger_group_name : string
        the name of the larger group in the analysis.
    larger_group_category_name : string
        the category of the larger group.

    Returns
    -------
    None.

    """
    plt.figure()
    for dep_type in range(len(order_of_outputs)):
        lab = section_name + ' ' + order_of_outputs[dep_type]
        plt.plot(x_data, section_y_data[dep_type], '-o',
                 color = colors[dep_type], label = lab)
        
        lab = larger_group_name + ' ' + order_of_outputs[dep_type]
        plt.plot(x_data, rest_y_data[dep_type], '--o',
                 color = colors[dep_type], label = lab)
    
    ttl = section_name +' vs ' + larger_group_name + ' on ' + population_subset + ' sentencing' +'.  N=' + str(count)
    plt.title(ttl)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.figure()
    diffs = section_y_data - rest_y_data
    for dep_type in range(len(order_of_outputs)):
        plt.plot(x_data, diffs[dep_type], '-o',
            color = colors[dep_type], label = order_of_outputs[dep_type])
    plt.axhline(y=0, color = 'black')
    ttl = section_name +' vs ' + larger_group_name + ' ' +  ' differences on ' + population_subset + ' sentencing'
    plt.title(ttl)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    

def plot_section_and_rest_data(x_data, section_y_data, rest_y_data, count, 
                               colors, population_subset,order_of_outputs, 
                               section_name, section_category_name,
                               larger_group_name, larger_group_category_name):
    """
    Plot the sentencing trends for a unique identifier for both a section and a larger group.
    
    Measures the difference between the max and min values, and decides if
    the graph should be split or not, then calls one of the two functions:
        section_and_rest_data_plot_line_graph
        section_and_rest_data_plot_broken_axis_line_graph

    Parameters
    ----------
    x_data : list
        the overlapping year data between the section and the rest of the larger section it is aprt of.
    section_y_data : numpy array: 2 dimensional 
        a two dimentional list to hold the section's sentencing breakdown. I
        n the shape of (length(x_data) * length(state.order_of_outputs)).
    rest_y_data : numpy array: 2 dimensional 
        a two dimentional list to hold the larger group's sentencing breakdown. I
        n the shape of (length(x_data) * length(state.order_of_outputs)).
    count : int
        the total number of people sentenced for this unique identifier.
    colors : list
        DESCRIPTION.
    population_subset : string
        the name of the unique identifier.  for example 'white female'
    order_of_outputs : list
        a state object's order of outputs.
    section_name : string
        the name of the section being analyzed.
    section_category_name : string
        the name of the category the section is a part of.  MUST be in the satate's paths.
    larger_group_name : string
        the name of the larger group in the analysis.
    larger_group_category_name : string
        the category of the larger group.

    Returns
    -------
    None.

    """
    
    section_y_data_medians = np.median(section_y_data, axis = 1)
    rest_y_data_medians = np.median(rest_y_data, axis = 1)
    
    comb_max = np.max([np.max(section_y_data_medians),np.max( rest_y_data_medians)])
    comb_min = np.min([np.min(section_y_data_medians), np.min(rest_y_data_medians)])
    
    if comb_max-comb_min > 0.5: # difference is big enought ot warrent a split axis graph
        section_and_rest_data_plot_broken_axis_line_graph(x_data,section_y_data, rest_y_data,count,  colors,
                                       population_subset, order_of_outputs, section_name, section_category_name,
                                       larger_group_name, larger_group_category_name)
    else:
        section_and_rest_data_plot_line_graph(x_data,section_y_data,rest_y_data, count, colors,
                                       population_subset,order_of_outputs, section_name, section_category_name,
                                       larger_group_name, larger_group_category_name)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    