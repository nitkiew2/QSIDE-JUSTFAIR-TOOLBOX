#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 22:43:52 2023

@author: jason
"""

class Path:
    def __init__(self, df_colname, levels = None):
        self.df_colname = df_colname
        self.levels = levels
