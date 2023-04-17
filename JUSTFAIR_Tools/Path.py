#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 22:43:52 2023

@author: jason
"""

class Path:
    def __init__(self, df_colname, levels = None):
        """
        Path class.  This is a specialized storage container to represent a path 

        Parameters
        ----------
        df_colname : TYPE
            DESCRIPTION.
        levels : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        self.df_colname = df_colname
        self.levels = levels
