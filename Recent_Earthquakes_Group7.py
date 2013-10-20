# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Recent Earthquakes: Group 7

# <markdowncell>

# He Ma: data curation  
# Carl Shan: data visualization  
# Alyssa Parker:?  
# Vincent Canlas:?

# <headingcell level=2>

# Part 0: User Input:

# <markdowncell>

# **This section is for user configuration:**  
# **Please check they are correct before running the code**

# <codecell>

# Decide whether to use live data or read from file. Modify 2nd and 3rd cell accordingly.
LIVE_DATA = True

# <codecell>

# fill in the fields below only if you are going to use live-data
CACHE_NAME = 'default.json' # the file name you want to cache the data to. The name is suggested to have ".json" at the end
DURATION = 'D' # type 'H', 'D', 'W', or 'M' for feeds in past hour, day, week, or month
MAGNITUDE = 1 # type 1, 2, 3, 4, or 5 for earthquakes that are significant, 4.5+, 2.5+, 1.0+, or all

# <codecell>

# fill in the field below only if you are going to read data from file.
FILE_NAME = 'default.json' # the full name of the file you want to read from. It has to be in the same directory as the code.

# <headingcell level=2>

# Part 1: Data Curation: Produce the data frame for visualization

# <markdowncell>

# Import modules:

# <codecell>

import IPython.core.display
import urllib
from pandas import read_csv
import csv
import json
import time
import re

# <markdowncell>

# Set all the global variabes:

# <codecell>

data_json = None # the original file from url
data_csv = None # a intermediate file
data_cleaned = None # the final file for visualization
# some keys in Json we are going to use
FEATURE = 'features'
PROP = 'properties'
GEO = 'geometry'
COORD = 'coordinates'
PLACE = 'place'
# all the fields we are interested in
SRC = 'net'
ID = 'code'
TIME = 'time'
LON = 'longitude'
LAT = 'latitude'
DEP = 'depth'
MAG = 'mag'
NST = 'nst'
REGION = 'region'
DISTANCE = 'distance'
DIRECTION = 'direction'
# all urls
# 'H', 'D', 'W', or 'M' for feeds in past hour, day, week, or month
# 1, 2, 3, 4, or 5 for earthquakes that are significant, 4.5+, 2.5+, 1.0+, or all
URLs = {'H':{5: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_hour.geojson',
             4 : 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_hour.geojson',
             3: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_hour.geojson',
             2: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_hour.geojson',
             1: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson'},
        'D':{5: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_day.geojson',
             4: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson',
             3: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson',
             2: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_day.geojson',
             1: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson'},
        'W':{5: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.geojson',
             4: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.geojson',
             3: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson',
             2: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.geojson',
             1: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson'},
        'M':{5: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson',
             4: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_month.geojson',
             3: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson',
             2: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_month.geojson',
             1: 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson'}
        }

# <markdowncell>

# Function for getting live data and cache it:

# <codecell>

def getLiveData():
    url = URLs[DURATION][MAGNITUDE] # the url depending on user input
    global data_json
    data_json = json.loads(urllib.urlopen(url).read()) # read in json
    with open(CACHE_NAME, 'w') as outfile:
      json.dump(data_json, outfile) # cache the data depending on user input

# <markdowncell>

# Function for getting data from file:

# <codecell>

def readFromFile():
    global data_json
    data_json = json.loads(open(FILE_NAME, 'r').read()) # read in the cache depending on user input

# <markdowncell>

# Function for parsing the time in Json to desired format:

# <codecell>

def parseTime(timeSinceEpoch):
    dayTime = time.strftime('%A, %B %d, %Y %H:%M:%S UTC', time.gmtime(timeSinceEpoch/1000)) 
    # to [weekday, month day, year hour:minute:second timeZone]
    return dayTime

# <markdowncell>

# Function for parsing place to desired format:

# <codecell>

def parsePlace(place):
    match = re.match('(.+km) ([NEWS]+) of (.*)', place) # to (distance, direcion, region)
    if match:
        return (match.group(1), match.group(2), match.group(3))
    else:
        return ('NA', 'NA', place) # put everything to region if it is not of the desired format

# <markdowncell>

# Function for parsing the Json file to [{Key:Value....},{Key:Value...},...]:  

# <codecell>

def parseData():
    global data_csv
    data_csv = [] # representing a row
    for feature in data_json[FEATURE]: # add the fields to row
        dataRow = {}
        prop = feature[PROP]
        dataRow[MAG] = prop[MAG]
        placeInfo = parsePlace(prop[PLACE])
        dataRow[DISTANCE] = placeInfo[0]
        dataRow[DIRECTION] = placeInfo[1]
        dataRow[REGION] = placeInfo[2]
        dataRow[TIME] = parseTime(prop[TIME])
        dataRow[SRC] = prop[SRC]
        dataRow[ID] = prop[ID]
        dataRow[NST] = prop[NST]
        coord = feature[GEO][COORD]
        dataRow[LON] = coord[0]
        dataRow[LAT] = coord[1]
        dataRow[DEP] = coord[2]
        data_csv.append(dataRow) # add the row to list

# <markdowncell>

# Function to produce the Pandas data frame:

# <codecell>

def getCleanedData(): # kind of a hack. convert it to csv first, then to pandas data frame using read_csv
    names = [SRC, ID, TIME, LAT, LON, MAG, DEP, NST, REGION, DISTANCE, DIRECTION]
    f = open('tem.csv', 'w')
    dict_writer = csv.DictWriter(f, names, restval='NA')
    dict_writer.writeheader()
    dict_writer.writerows(data_csv)
    f.close()
    global data_cleaned
    data_cleaned = read_csv('tem.csv')

# <headingcell level=3>

# The 'main' function:

# <codecell>

if LIVE_DATA: # access live data and save locally
    getLiveData()
else: # read from file
    readFromFile()
parseData()
getCleanedData()

# <headingcell level=3>

# What the data frame look like:

# <codecell>

data_cleaned[0:10]

# <headingcell level=3>

# Example for doing subset:

# <codecell>

data_cleaned[data_cleaned[REGION] == 'The Geysers, California']

# <headingcell level=2>

# Part 2: Data Visualization

# <codecell>

# More code here

