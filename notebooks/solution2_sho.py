#!/usr/bin/env python
# coding: utf-8

# # Getting the Data
# 
# Our data comes directly from the [John Hopkins COVID-19 Github repository][1], which tracks all deaths and cases from each country in the world as well as many regions within some countries. All of the data needed for this project is within the [time series][2] directory, which contains four CSV files that summarize the deaths and cases for the world and the USA. The repository uses the word "confirmed" to refer to cases.
# 
# [1]: https://github.com/CSSEGISandData/COVID-19
# [2]: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series

# ## Reading in the data into a pandas DataFrame
# 
# The pandas `read_csv` function can read in remote CSV files by passing it the URL. The exact URL on Github is a bit tricky. You must use the "raw" data file, which can be retrieved by clicking on the file name (taking you to the next page), then right-clicking the "view raw" or "download" button and copying the link. The image below shows the screen you'll see for the first CSV.
# 
# ![1]
# 
# [1]: images/url_download.png

# ## Naming conventions
# 
# Before we write any code, let's cover some naming conventions that we will use throughout the project.
# 
# ### `group`
# 
# We will use the name `group` to refer to the two separate "groups" of data.
# 
# * `"world"` - represents all data from each country
# * `"usa"` - represents all data from each US state
# 
# ### `kind`
# 
# We will use the name `kind` to refer to the two different kinds of COVID-19 data.
# 
# * `"deaths"`
# * `"cases"`
# 
# 
# ### `area`
# 
# Occasionally, we will refer to either a specific country or state with the name `area`.
# 
# ## Downloading the data
# 
# Now that we have the URL, we can download the data with pandas. Complete the exercise below to download all four files as DataFrames.

# ### Exercise 1
# 
# <span style="color:green; font-size:16px">Write a function that reads in a single CSV and returns it as a DataFrame. This function accepts a kind and group. Use the variable `DOWNLOAD_URL` in your solution. Make sure you look at the URL in the repo from above to determine what values `kind` and `group` refer to. You'll have to reassign their values in the function so that the URL is correct. For example, the function call `download_data("world", "deaths")` should download [one of the files on this page](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series).</span>

# In[23]:


import pandas as pd

DOWNLOAD_URL = (
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/"
    "master/csse_covid_19_data/csse_covid_19_time_series/"
    "time_series_covid19_{}_{}.csv"
)


def download_data(group, kind):
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
   
 


# ### Important information on exercises - please read!
# 
# All of the exercises require you to complete the body of a function. All functions end with the `pass` keyword. **Delete** it and write your solution in the body of the function.
# 
# Solutions for all exercises are found in the [solutions.py](solutions.py) file in this directory. You can open it up in your favorite editor, or just click the link to open it in your browser.
# 
# In the code cell following each exercise, you will see a single line of code that imports the function from the solutions.py file. For example, `from solutions import download_data`. Running this statement will provide you with a version of the function that produces the correct output for the exercise.
# 
# **Comment out the import line** if you want to use and test **your version** of the function completed above. I highly recommend completing the exercises on your own. Keep the import line uncommented if you do not attempt the exercise. 
# 
# **Always check the solutions!** Make sure to check the [solutions.py](solutions.py) file for each exercise, even if you are sure you answered it correctly. Verifying solutions is one of the best known methods for internalizing new material.

# ### Verifying the `download_data` function
# 
# Let's read in the world deaths file as a DataFrame and output the head to verify that it works. 

# In[25]:


# comment out the import line below if you attempted the exercise above
# keep the line below if you did not attempt the exercise
#from solutions import download_data 
df_world_deaths = download_data('world','deaths')
df_world_deaths


# Let's write a another function which uses `download_data` to read in all four DataFrames.
# 
# ### Exercise 2
# 
# <span style="color:green; font-size:16px">Write a function that reads in all four CSVs as DataFrames returning them in a dictionary. Use the group and kind separated by an underscore as the key (i.e. `"world_deaths"`). Use the `GROUPS` and `KINDS` variables in your solution.</span>

# In[26]:


GROUPS = "world", "usa"
KINDS = "deaths", "cases"

def read_all_data():
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


# Let's use this function to read in all of the data and output the head of two of them.

# In[27]:


# remember to comment out the following line if you attempt the exercise
# this is the last exercise with this warning
#from solutions import read_all_data
data = read_all_data()
data['world_cases'].head(3)


# In[28]:


data['usa_cases'].head(3)


# In[29]:


data


# ## Saving the data locally
# 
# Since the raw data must be downloaded from the internet, let's save a copy of our current data to a local folder so that we have access to it immediately at any time.

# ### Exercise 3
# 
# <span style="color:green; font-size:16px">Write a function that accepts a dictionary of DataFrames and a directory name, and writes them to that directory as CSVs using the key as the filename. Pass the `kwargs` to the `to_csv` method.</span>

# In[53]:


def write_data(data, directory, **kwargs):
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
    
        


# Let's write those DataFrames as CSVs (without their index) to the "data/raw" directory.

# In[54]:


#from solutions import write_data
write_data(data, "data/raw", index=False)


# ### Exercise 4
# 
# <span style="color:green; font-size:16px">Write a function similar to `download_data`, but have it read in the local data that we just saved. </span>

# In[66]:


def read_local_data(group, kind, directory):
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
    
        


# In[67]:


#from solutions import read_local_data
read_local_data('usa', 'cases', 'data/raw').head(3)


# ### Exercise 5
# 
# <span style="color:green; font-size:16px">Write a function similar to `read_all_data`, but have it read in all of the local data that we just saved. The function name is `run` since we will be slowly adding all of our data cleaning and transformation steps to it in the next chapter.</span>

# In[68]:


def run():
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
            data[f'{group}_{kind}']= read_local_data(group,kind,directory)
    return data


# Here, we verify that `run` works properly.

# In[69]:


#from solutions import run
data = run()
data['usa_deaths'].tail(3)


# This concludes the section on downloading the data.
