#!/usr/bin/env python3

import os
import pandas as pd
import numpy as np
import glob
import pandas as pd

def design_df(df):
    
    '''
    a) The dataframe contains more regions and hight levels than I need, 
    so only particular will be selected
    b) some Variables will be renamed

    This is the header:
    file,year,month,exp,RCM,region,height,
    snw_1972-2001,pr_1972-2001,tas_1972-2001,snowday_1972-2001,sca_1972-2001,
    snw_2022-2051,pr_2022-2051,tas_2022-2051,snowday_2022-2051,sca_2022-2051,
    snw_2070-2099,pr_2070-2099,tas_2070-2099,snowday_2070-2099,sca_2070-2099,
    GCM,diff_snw_2022-2051,pro_diff_snw_2022-2051,diff_pr_2022-2051,
    pro_diff_pr_2022-2051,diff_tas_2022-2051,diff_snowday_2022-2051,
    pro_diff_snowday_2022-2051,diff_sca_2022-2051,pro_diff_sca_2022-2051,
    diff_snw_2070-2099,pro_diff_snw_2070-2099,diff_pr_2070-2099,
    pro_diff_pr_2070-2099,diff_tas_2070-2099,diff_snowday_2070-2099,
    pro_diff_snowday_2070-2099,diff_sca_2070-2099,pro_diff_sca_2070-2099
    '''

    # rename
    
    df['region'].replace('AL','Alps', inplace = True)
    df['region'].replace('EA','Eastern E.', inplace = True)
    df['region'].replace('IP','Iberian P.', inplace = True)
    df['region'].replace('SC','Scandinavia', inplace = True)

    print('subroutine',df['height'].unique())
    
    df['height']=df['height'].apply(str)

    print('subroutine-string',df['height'].unique())
    
    df['height'].replace('0','500', inplace = True)
    df['height'].replace('1','1000', inplace = True)
    df['height'].replace('2','1500', inplace = True)
    df['height'].replace('3','2000', inplace = True)
    df['height'].replace('4','2500', inplace = True)
    df['height'].replace('5','3000', inplace = True)
    
    #    write correct height level:
    #    Elevation classes (0: [-500, 500 m], 1: [500, 1000 m], 
    #    2: [1000, 1500 m], 3: [1500, 2000 m], 4: [2000, 2500 m], 
    #    5: [2500, 3000 m], 6: [3000, 3500 m], 
    #    7: [3500, 4000 m], 8: [4000, 4500 m], 9: [4500, 5000 m]
    #    mean: [-500 to top]

    # select
    
    sel=df.loc[df['region'].isin(['Alps', 'Scandinavia', 'Eastern E.', 'Iberian P.'])]
    
    df=sel.loc[sel['height'].isin(['500','1000', '1500', '2000', '2500','3000'])]            

    return(df)


def design_df_mean(df):
    
    '''
    a) The dataframe contains more regions and hight levels than I need, 
    so only particular will be selected
    b) some Variables will be renamed

    '''

    # rename

    df['region'].replace('AL','Alps', inplace = True)
    df['region'].replace('EA','Eastern E.', inplace = True)
    df['region'].replace('IP','Iberian P.', inplace = True)
    df['region'].replace('SC','Scandinavia', inplace = True)

    # select
    
    sel=df.loc[df['region'].isin(['Alps', 'Scandinavia', 'Eastern E.', 'Iberian P.'])]

    df['height']=df['height'].apply(str)
    df=sel.loc[sel['height'].isin(['mean'])]            

    return(df)
