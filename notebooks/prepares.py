#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np

DOWNLOAD_URL = (
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/"
    "master/csse_covid_19_data/csse_covid_19_time_series/"
    "time_series_covid19_{}_{}.csv")

GROUPS = "world", "usa"
KINDS = "deaths", "cases"

REPLACE_AREA = {
    "Korea, South": "South Korea",
    "Taiwan*": "Taiwan",
    "Burma": "Myanmar",
    "Holy See": "Vatican City",
    "Diamond Princess": "Cruise Ship",
    "Grand Princess": "Cruise Ship",
    "MS Zaandam": "Cruise Ship"}

class Preparedata:
    
    def __init__(self, download_new=True):
        self.download_new = download_new
    
    def download_data(self,group, kind):
        """
        Reads in a single dataset from the John Hopkins GitHub repo
        as a DataFrame

        Parameters
        ----------
        group : "world" or "usa"

        kind : "deaths" or "cases"

        Returns
        -------
        DataFrame
        """
        group= 'US' if group=='usa' else 'global'
        kind= 'confirmed' if kind=='cases' else 'deaths'
        url=DOWNLOAD_URL.format(kind,group)
        return pd.read_csv(url)

    def read_all_data(self):
        """
        Read in all four CSVs as DataFrames

        Returns
        -------
        Dictionary of DataFrames
        """
        data ={}
        for group in GROUPS:
            for kind in KINDS:
                data[f'{group}_{kind}']= download_data(group,kind)
        return data

    def write_data(self,data, directory, **kwargs):
        """
        Writes each raw data DataFrame to a file as a CSV

        Parameters
        ----------
        data : dictionary of DataFrames

        directory : string name of directory to save files i.e. "data/raw"

        kwargs : extra keyword arguments for the `to_csv` DataFrame method

        Returns
        -------
        None
        """
        for key,value in data.items():
            data[key].to_csv(f'{directory}/{key}.csv',**kwargs)
        

    def read_local_data(self,group, kind, directory):
        """
        Read in one CSV as a DataFrame from the given directory

        Parameters
        ----------
        group : "world" or "usa"

        kind : "deaths" or "cases"

        directory : string name of directory to save files i.e. "data/raw"

        Returns
        -------
        DataFrame    
        """

        return pd.read_csv(f'{directory}/{group}_{kind}.csv')

    def select_columns(self,df):
        """
        Selects the Country/Region column for world DataFrames and
        Province_State for USA

        Parameters
        ----------
        df : DataFrame

        Returns
        -------
        df : DataFrame

        """
        cols=df.columns
        labels =['Country/Region','Province_State']
        filt1 =cols.isin(labels)
        filt2 =cols.str.count('/')==2
        filt = filt1 | filt2
        return df.loc[:,filt]

    def update_areas(self,df):
        """
        Replace a few of the area names using the REPLACE_AREA dictionary.

        Parameters
        ----------
        df : DataFrame

        Returns
        -------
        df : DataFrame
        """
        first_col=df.columns[0]
        df.replace(REPLACE_AREA,inplace=True)
        filt=df[first_col] !='US'
        df=df[filt]
        return df

    def group_area(self,df):
        """
        Gets a single total for each area

        Parameters
        ----------
        df : DataFrame

        Returns
        -------
        df : DataFrame
        """
        first_col =df.columns[0]
        df=df.groupby(first_col).sum()
        return df

    def transpose_to_ts(self,df):
        """
        Transposes the DataFrame and converts the index to datetime

        Parameters
        ----------
        df : DataFrame

        Returns
        -------
        df : DataFrame
        """
        df=df.T
        time_series_col=df.columns[0]
        df.index=pd.to_datetime(df.index)
        return df

    def fix_bad_data(self,df):
        """
        Replaces all days for each country where the value of
        deaths/cases is lower than the current maximum

        Parameters
        ----------
        df : DataFrame

        Returns
        -------
        DataFrame
        """
        mask = df < df.cummax()
        return df.mask(mask).interpolate().round(0).astype('int64')

    def run(self):
        """
        Run all cleaning and transformation steps

        Returns
        -------
        Dictionary of DataFrames
        """
        directory='data/raw'
        data ={}
        for group in GROUPS:
            for kind in KINDS:
                if self.download_new:
                    df=self.download_data(group,kind)
                else:
                    df=self.read_local_data(group,kind)
                df=self.select_columns(df)
                df=self.update_areas(df)
                df=self.group_area(df)
                df=self.transpose_to_ts(df)
                df=self.fix_bad_data(df)
                data[f'{group}_{kind}']=df
        return data

        


# In[ ]:




