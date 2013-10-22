Group Members:
--------------
Vincent Canlas, He Ma, Alyssa Parker, Carl Shan  

How to run our code:
--------------------
1. Our code is **Recent\_Earthquakes_Group7.ipynb**. You need to open this file in ipython notebook.  
2. We used `urllib`, `read_csv` from `pandas`, `csv`, `json`, `time`,`re` and `folium`.  
   To run our code, please **install** `folium` via:  
        `sudo pip install folium` and `sudo pip install jinja2`  
    More information at: https://folium.readthedocs.org/en/latest/  
    `csv`, `json`, `time` and `re` are standard packages for Python 2.7+.  
    You should already have `urlib` and `pandas`.  
3. The code uses `live data` of feeds in the past day for 1.0+ earthquakes.  
   For other settings, please change the variables in **Part 0** of the code.  
   Instructions are in the comment for each variable.

Due Date
--------
Monday, October 21st, 2013 (2013-10-21) at 11:59pm. On Tuesday Oct
22nd in class we will **not** have a formal presentation. Instead we
will conduct a code review together.

Questions or Problems?
----------------------
Open an item in the Github issue tracker of this repository:

https://github.com/stat157/recent-quakes/issues

Preliminary Setup Steps
-----------------------
To run this example you'll need to install the following packages
inside your virtual machine:

    sudo apt-get install libgeos-3.3.3 python-mpltoolkits.basemap python-mpltoolkits.basemap-data python-mpltoolkits.basemap-doc

Then run the notebook from your machine with this command:

    ipython notebook --no-browser --ip=0.0.0.0 --script --pylab=inline

Objective
---------

The first objective of this assignment is to improve the data handling
of the code by upgrading from the deprecated data source to the new
data source which uses a different data format called
[JSON](http://en.wikipedia.org/wiki/JSON).

Since we are working with live data we also need to cache the data so
that we can reliably re-run the code using the same data (or
optionally with the live data).

The second objective is that we would like to be able to see data for
earthquakes in states other than Alaska, so the next part of the
assignment requires
[refactoring](http://en.wikipedia.org/wiki/Code_refactoring) the code
to parameterize the function definition instead of relying on the
hard-coded values for latitude and longitude of the bounding box
around the region of interest.

This assignment features two main roles: the Data Curator and the
Visualizer. All 4 members of your vertical group should work together
no matter what individual roles you have assigned.

Your task
---------

1) Data Curation

The USGS [eqa7day-M1.txt data
url](http://earthquake.usgs.gov/earthquakes/catalogs/eqs7day-M1.txt)
used in this program has been deprecated.

As suggested by the warning message in the data feed:

    This USGS data file has been deprecated. To continue receiving
    updates for earthquake information you must switch to the new data
    format [http://earthquake.usgs.gov/earthquakes/feed/]. In the
    future, data feeds will be updated and deprecated following our
    official deprecation policy
    [http://earthquake.usgs.gov/earthquakes/feed/policy.php].

you need to upgrade this program to use the new USGS data feed:

http://earthquake.usgs.gov/earthquakes/feed/

The new data feed includes a link for [Programmatic
Access](http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php).
You should use the [pandas JSON
parser](http://pandas.pydata.org/pandas-docs/dev/io.html) to read the
data instead of the `read_csv` function in the original code.

You will also need to find a way to cache the data locally so that
your runs are exactly reproducible since the live data gets updated in
real-time. You should write a program which can use the live data, but
also optionally can store data from previous runs so that we can
re-run the program in either mode using *cached data* or *live data*.

Start simple, keep the data isolated/separate from the source code,
and remember that the goal is to make it reproducible by someone else.

**The duty of the Data Curator is to write a new version of the code
that reproduces the same output as the old version of the code, but
using the new data source.** Note, it may *not* be possible to do that
exactly if the new data and the old data are substantially different,
but hopefully they are exact in content, and differ only in format
(CSV vs JSON).

2) Visualization

The definition of `plot_ak()` has a *very bad code smell*! What if we
want to plot the earthquakes in California where I live now instead of
in my home state of Alaska? Can you spot the *code smell*? How can you
fix it so that given any arbitrary list of earthquakes you can plot
the bounding box around the location (e.g. the whole state) where the
quakes occured?

**The duty of the Visualizer is to refactor the hard-coded values out
of the program and instead parameterize the function so that for any
list of earthquakes in a particular region (i.e. California) it will
generate a map showing the correct location.** Instead of including
the lat/lon bounding box values in the body of the program you might
consider storing that data in some format on disk and read it back
into the program as a dataframe to pass to the function as a
parameter.

Also plot the quakes so we can see the magnitude and depth of each dot
instead of the way they are plotted now which only shows the location;
all the dots are the same color and the same size, but could be varied
to represent more information in the same amount of space.
