# -*- coding: utf-8 -*-
"""
Created on Thu May 21 15:12:00 2015

@author: Rob
"""

from databaker.constants import *

def per_file(tabs):
    return "Table 1"
    
def per_tab(tab):
    
    anchor = tab.excel_ref("B10")
    
    obs = anchor.fill(RIGHT).fill(DOWN).is_not_blank() - anchor.shift(UP).fill(RIGHT).parent().filter(contains_string("eriod")).fill(DOWN)
    
    tab.excel_ref("6").parent().is_not_blank().dimension("Sector", CLOSEST, LEFT)
    tab.excel_ref("7").parent().is_not_blank().dimension("Sector 2", CLOSEST, LEFT)
    tab.excel_ref("8").dimension("Sector 3", DIRECTLY, ABOVE)
    tab.excel_ref("9").dimension("Sector 4", DIRECTLY, ABOVE)
    
    tab.excel_ref("A").is_not_blank().dimension("Year", CLOSEST, ABOVE)
    tab.excel_ref("B").dimension("Quarter", DIRECTLY, LEFT)
    
    yield obs