#!/usr/bin/env python
# coding: utf-8

# # 2.2 EPANET GUI Examples
# 
# ## Purpose
# 
# Present several examples using the GUI (freeswmm.ddns.net) to get users familiar with EPANET concepts
# 
# ## Examples
# 
# 

# ### Example 1

# ### Example 2

# ### Example 3 : Three-Reservoir-Problem
# 
# This example is a pretty classic hydraulics problem, that appears in some form in most if not all hydraulics textbooks.  Here it is useful to introduce the concept of a basemap (image) to help draw the network. 
# 
# First the **problem statement**:
# 
# Reservoirs A, B, and C are connected as shown. 
# The water elevations in reservoirs A, B, and C are 100 m, 80 m, and 60 m. 
# The three pipes connecting the reservoirs meet at junction J, with pipe AJ being 900
# m long, BJ being 800 m long, and CJ being 700 m long. The diameters of
# all the pipes are 850 mm. If all the pipes are ductile iron, and the water
# temperature is 293$^o$K, find the direction and magnitude of flow in each
# pipe.
# 
# ![](./ex3/EX3.bmp)
# 
# Here we will first convert the image into a bitmap (.bmp) file so EPANET can import
# the background image and we can use it to help draw the network. The remainder of
# the problem is reasonably simple and is an extension of the previous problem.
# 
# The steps to model the situation are:
# 
# 1. Convert the image into a bitmap, place the bitmap into a directory where the model input file will be stored.
# 2. Start EPANET
# 3. Set defaults
# 4. Import the background.
# 5. Select the reservoir tool. Put three reservoirs on the map.
# 6. Select the node tool, put the node on the map.
# 7. Select the link (pipe) tool, connect the three reservoirs to the node.
# 8. Set the total head each reservoir.
# 9. Set the pipe length, roughness height, and diameter in each pipe.
# 10. Save the input file.
# 11. Run the program.
# 
# Below is the result of the above steps run on a laptop. 
# 
# ![](./ex3/3reservoir-epanet.png)
# 
# In this case the default units were changed to
# LPS (liters per second). The roughness height is about 0.26 millimeters (if converted from the 0.85 millifeet unit).
# 
# A you-tube video [FREESWMM-EPANET-EX3](https://youtu.be/xeHs2C4UiGY) shows the example run on the (freeswmm.ddns.net) web interface.  A screen capture of the result is below:
# 
# ![](./ex3/EX3-GUI.png)
# 
# :::{note}
# The results should be identical.  The video was not made at the same time as the screen capture, so there may be slight differences.  The input files are pre-loaded onto the webserver implementation.  In the face-to-face course, the actual modeling building process will be deomnstrated.
# :::
# 
# The requestite files are listed below.
# 
# #### Files
# 
# 1. [EX3.bmp](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/lesson02/ex3/EX3.bmp) The base image file
# 2. [EX3.net](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/lesson02/ex3/EX3.net) An EPANET input file (binary .net file, readable by the GUI)
# 3. [EX3-1.net](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/lesson02/ex3/EX3-1.net) A different EPANET input file (binary .net file, readable by the GUI)

# In[ ]:





# ### Example 4

# ### Example 5

# 

# 

# 

# 
