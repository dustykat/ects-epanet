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
# 
# A simple model to consider is a single pipe connecting two reservoirs.
# 
# A **problem statement** might be something like:
# 
# > A 5-foot diameter, enamel coated, steel pipe carries 60oF water at a dis-
# charge of 295 cubic-feet per second (cfs). Using the Moody chart, estimate
# the head loss in a 10,000 foot length of this pipe.
# 
# :::{note}
# This example is verbatim from the references in the previous section, here the examples are presented using the freeswmm interface.  Be aware that the files are pre-placed, so one could simply open and go without building a model.
# :::
# 
# In EPANET we will start the program, build a tank-pipe system and find the head
# loss in a 10,000 foot length of the pipe. The program will compute the friction factor
# for us (and we can check on the Moody chart if we wish).
# 
# The main trick in EPANET is going to be the friction coefficient, in the EPANET
# manual on page 30 and 31, the author indicates that the program expects a roughness
# coefficient based on the head loss equation. The units of the roughness coefficient for
# a steel pipe are $0.15 \times 10^{-3}$ feet. On page 71 of the user manual the author states
# that roughness coefficients are in millifeet (millimeters) when the Darcy-Weisbach
# head loss model is used. So keeping that in mind we proceed with the example.
# 
# Figure xx is a screen capture of the EPANET program after connecting in freeswmm.
# 
# ![](./ex1/ex1ss1.png)
# 
# The program starts as a blank slate and we will select a reservoir and a node from
# the tool bar at the top and place these onto the design canvas.
# 
# 
# 
# Figure 37 is a screen capture of the EPANET program after setting defaults for the
# simulation. 
# 
# ![](./ex1/ex1ss2.png)
# 
# Failure to set correct units for your problem are sometimes hard to detect
# (if the model runs), so best to make it a habit to set defaults for all new projects.
# 
# Next we add the reservoir and the node. Figure 41 is a screen capture after the reservoir and node are placed.  
# 
# ![](./ex1/ex1ss3.png)
# 
# :::{note}
# The text tool was used to annotate the nodes - these are simply text blocks, and are not node labels, which is also a way to annotate.
# :::
# 
# We will specify a total head at the reservoir (value is unimportant as long as it is big enough to overcome the head loss and not result in a
# negative pressure at the node. We will specify the demand at the node equal to the
# desired 
# flow in the pipe. 
# 
# Next we will add the pipe.  Figure 43 is a screen capture after the pipe is placed. 
# 
# ![](./ex1/ex1ss4.png)
# 
# The sense of flow in this example is from reservoir to node, but if we had it backwards we could either accept a negative flow in the pipe, or right-click the pipe and reverse the start and end node connections.
# 
# Now we can go back to each hydraulic element in the model and edit the properties.
# We supply pipe properties (diameter, length, roughness height) as in Figure 45. 
# 
# ![](./ex1/ex1ss5.png)
# 
# We supply the reservoir total head as in Figure 47.
# 
# ![](./ex1/ex1ss6.png)
# 
# We set the demand node elevation and the actual desired flow rate as in Figure 49. 
# 
# ![](./ex1/ex1ss7.png)
# 
# The program is now ready to run, next step would be to save the input file.
# 
# :::{note}
# I will save an input file and a "network" file.  The network file can be run using a command-line version or using the programmers toolkit.  We will use this toolkit later on in the short course
# :::
# 
# > Saving the network file <br>
# > ![](./ex1/ex1ss8.png)
# 
# Now we can run the program by selecting the lightning bolt icon (or menu item "/Project/Run Analysis").
# 
# ![](./ex1/ex1ss9.png)
# 
# Upon completion
# 
# ![](./ex1/ex1ss10.png)
# 
# Yay! A sucessful run, which means that the nodal connectivity is OK and there are no computed negative pressures. A successful run means the program found an answer to the problem you provided - whether it is the correct answer to your problem requires the engineer to interpret results and decide if they make sense. 
# 
# The more common conceptualization errors are incorrect units and head loss equation for the supplied roughness values, missed connections, and forgetting demand somewhere.
# With practice these kind of errors are straightforward to detect. In the present
# example we select the pipe and the solution values are reported at the bottom of a dialog box.
# 
# Figure 54 is the result of turning on the computed head values at the node (and
# reservoir) and the flow value for the pipe in the Map tab of the browser tool. 
# 
# ![](./ex1/ex1ss11.png)
# 
# The dialog box reports about 7.2 feet
# of head loss per 1000 feet of pipe for a total of 72 feet of head loss in the system.
# The total head at the demnad node is about 28 feet, so the head loss plus remaining
# head at the node is equal to the 100 feet of head at the reservoir, the anticipated
# result.
# The computed friction factor is 0.010, which we could check against the Moody chart
# if we wished to adjust the model to agree with some other known friction factor.
# 
# #### Files
# 
# 1. [EX1.bmp](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/lesson02/ex1/EX1.bmp) The base image file
# 2. [EX1.net](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/lesson02/ex1/EX1.net) An EPANET input file (binary .net file, readable by the GUI)
# 3. [EX1.net](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/lesson02/ex1/EX1.net) A different EPANET input file (binary .net file, readable by the GUI)

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
