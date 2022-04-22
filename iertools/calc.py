import numpy as np


def wd(df):
    """ receives dataframe with u,v,w, returns ws,wd added """
    DperR = 180/np.pi
    df['ugeo'] = -df.v
    df['vgeo'] = -df.u
    df['ws'] = (df.ugeo**2 + df.vgeo**2 + df.w**2)**0.5
    df['wd'] = 270 + (np.arctan2(df.vgeo,df.ugeo)*DperR)
    df.wd    = df.wd%360.
    return df[['u','v','w','ws','wd']]

