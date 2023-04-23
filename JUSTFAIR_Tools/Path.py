#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 22:43:52 2023

@author: MSU QSIDE JUSTFAIR 2023 Team
"""

class Path:
    def __init__(self, df_colname, levels = None):
        """
        Path class.  This is a specialized storage container to represent a path to data we seek in a state's dataframe.
        Rather than have a strict format for state data, we opted to use Paths to point ot where the information we want is and not modify state data.

        Parameters
        ----------
        df_colname : string
            this is the name of the column in the state's data this path points to .
        levels : dictionary, optional
            This is a dicitionary to decode the contents of the state's data.
            Using the state's data dictionary, you can decode values if they are not what you with them to be.
            for example, in Minnesota's data, depareture is encoded in the values[0,1,2,3], 
            but the data dictionary tells us 0,1,2,3, actually mean
            ['within range','above departure','Below range','Missing / NA']
            so we would have a dictionary with keys [0,1,2,3] and values
            ['within range','above departure','Below range','Missing / NA'] to translate the information.
            The default is None.

        Returns
        -------
        None.

        """
        self.df_colname = df_colname
        self.levels = levels
