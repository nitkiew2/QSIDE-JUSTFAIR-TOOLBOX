# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 17:39:23 2023

@author: jason
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

def plot_section_vs_state(order_of_outputs, section_averages, state_avg_for_years, section_name, statename):
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

def plot_section_vs_state_trends(stateobj, overlapping_years, section_data_y, state_data_y, section_name):
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

    for col in range(len(stateobj.order_of_outputs)):
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.plot(overlapping_years, section_data_y[:,col], '-o', label=section_name, color = colors[col])
        ax.plot(overlapping_years, state_data_y[:,col], '--o', label=stateobj.name, color = colors[col])
        ttl = 'Comparing ' + section_name + ' and' + stateobj.name + ' on ' + stateobj.order_of_outputs[col]
        ax.set_title(ttl)
        ax.set_xlabel('year')
        ax.set_ylabel('percentage (%)')
        ax.legend(loc = 'upper right')


    fig, ax = plt.subplots(figsize=(10, 7))
    for col in range(len(stateobj.order_of_outputs)):
        ax.plot(overlapping_years, section_data_y[:,col] - state_data_y[:,col], '-o', 
                label=stateobj.order_of_outputs[col], color = colors[col])
    ax.axhline(y = 0, color = 'black')

    ttl = 'Comparing ' + section_name + ' difference from ' + stateobj.name + ' levels'
    ax.set_title(ttl)
    ax.set_xlabel('year')
    ax.set_ylabel('percentage (%)')
    ax.legend(loc = 'upper right')
    

    
def section_and_rest_data_plot_broken_axis_line_graph(x_data,section_y_data, rest_y_data, colors,
                               population_subset, order_of_outputs, section_name, state_name):
    
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
    
    lab = state_name + ' ' + order_of_outputs[highest_median_index]
    top.plot(x_data, rest_y_data[highest_median_index], '--o',
             color = colors[highest_median_index], label = lab)


    #plot the bottom
    for dep_type in range(len(order_of_outputs)):
        if dep_type != highest_median_index:
            lab = section_name + ' ' + order_of_outputs[dep_type]
            bot.plot(x_data, section_y_data[dep_type], '-o',
                     color = colors[dep_type], label = lab)
            
            lab = state_name + ' ' + order_of_outputs[dep_type]
            bot.plot(x_data, rest_y_data[dep_type], '--o',
                     color = colors[dep_type], label = lab)
    
    # zoom-in / limit the view to different portions of the data
    top.legend()
    bot.legend()
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
    ttl = section_name +' vs ' + state_name + ' on ' + population_subset + ' sentencing'
    fig.suptitle(ttl)
    
    
    #second graph, differences (judge data - rest of data, so if judge is higher we see a positive number)
    plt.figure(figsize = (10,4))
    diffs = section_y_data - rest_y_data
    for dep_type in range(len(order_of_outputs)):
        plt.plot(x_data, diffs[dep_type], '-o',
            color = colors[dep_type], label = order_of_outputs[dep_type])
    plt.axhline(y=0, color = 'black')
    ttl = section_name +' vs ' + state_name + ' differences on ' + population_subset + ' sentencing'
    plt.title(ttl)
    plt.legend()
        

def section_and_rest_data_plot_line_graph(x_data,section_y_data,rest_y_data, colors,
                               population_subset,order_of_outputs, section_name, state_name):
    plt.figure()
    for dep_type in range(len(order_of_outputs)):
        lab = section_name + ' ' + order_of_outputs[dep_type]
        plt.plot(x_data, section_y_data[dep_type], '-o',
                 color = colors[dep_type], label = lab)
        
        lab = state_name + ' ' + order_of_outputs[dep_type]
        plt.plot(x_data, rest_y_data[dep_type], '--o',
                 color = colors[dep_type], label = lab)
    
    ttl = section_name +' vs ' + state_name + ' on ' + population_subset + ' sentencing'
    plt.title(ttl)
    plt.legend()
    
    plt.figure()
    diffs = section_y_data - rest_y_data
    for dep_type in range(len(order_of_outputs)):
        plt.plot(x_data, diffs[dep_type], '-o',
            color = colors[dep_type], label = order_of_outputs[dep_type])
    plt.axhline(y=0, color = 'black')
    ttl = section_name +' vs ' + state_name + ' differences on ' + population_subset + ' sentencing'
    plt.title(ttl)
    plt.legend()
    

def plot_section_and_rest_data(x_data,section_y_data,rest_y_data, colors,
                               population_subset,order_of_outputs, section_name, state_name):
    
    section_y_data_medians = np.median(section_y_data, axis = 1)
    rest_y_data_medians = np.median(rest_y_data, axis = 1)
    
    comb_max = np.max([np.max(section_y_data_medians),np.max( rest_y_data_medians)])
    comb_min = np.min([np.min(section_y_data_medians), np.min(rest_y_data_medians)])
    
    if comb_max-comb_min > 0.5:
        section_and_rest_data_plot_broken_axis_line_graph(x_data,section_y_data, rest_y_data, colors,
                                       population_subset, order_of_outputs, section_name, state_name)
    else:
        section_and_rest_data_plot_line_graph(x_data,section_y_data,rest_y_data, colors,
                                       population_subset,order_of_outputs, section_name, state_name)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    