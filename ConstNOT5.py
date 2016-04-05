# -*- coding: utf-8 -*-
"""
Created on Thu May 21 15:12:00 2015

@author: Rob
"""

from databaker.constants import *

def per_file(tabs):
    return "Table 5"
    
def per_tab(tab):
    
    anchor = tab.excel_ref('A').filter(contains_string("PUBLIC HOUSING")).assert_one()
    obs = anchor.shift(1,-1).fill(RIGHT).fill(DOWN).is_not_blank()
    
    anchor.expand(DOWN).is_not_blank().dimension("Type", DIRECTLY, LEFT)
    
    #messy bit  
    rows = tab.excel_ref("C1").fill(DOWN).is_number()
    rows = rows.fill(LEFT)
    allrows = anchor.fill(DOWN).is_not_blank()
    rows = allrows - rows
    rows = rows | tab.excel_ref("A2")
    rows.dimension("Category", CLOSEST, ABOVE)
    
    anchor.shift(0, -3).fill(RIGHT).is_not_blank().dimension("Year",CLOSEST, LEFT)
    anchor.shift(0, -2).fill(RIGHT).is_not_blank().dimension("Quarter",DIRECTLY, ABOVE)
    
    yield obs