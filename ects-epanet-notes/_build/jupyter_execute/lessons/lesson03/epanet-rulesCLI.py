#!/usr/bin/env python
# coding: utf-8

# # 3.3 EPANET (Examples 3-5) using the Toolkit
# 
# ## Purpose
# 
# ## Installation
# 
# ## Examples
# 
# 

# ### Example 3 : Three-Reservoir-Problem
# 
# This example is a the classic hydraulics problem, that appears in some form in most if not all hydraulics textbooks; here we will use the already built input file - and note we wont use any of the basemap capabilities, as the Toolkit is not really intended for such direct graphics.
# 
# Recall the **problem statement**:
# 
# Reservoirs A, B, and C are connected as shown. 
# The water elevations in reservoirs A, B, and C are 100 m, 80 m, and 60 m. 
# The three pipes connecting the reservoirs meet at junction J, with pipe AJ being 900
# m long, BJ being 800 m long, and CJ being 700 m long. The diameters of
# all the pipes are 850 mm. If all the pipes are ductile iron, and the water
# temperature is 293$^o$K, find the direction and magnitude of flow in each
# pipe.
# 
# ![](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/lesson02/ex3/EX3.bmp)
# 
# The input file from earlier is copiec to our work directory; let's list it

# In[1]:


get_ipython().system(' cat ./ex3-tk/EX3.inp')


# Now we will run it as supplied, then modify using the Toolkit for more useful purposes.

# In[2]:


import epamodule as em  # import the package
#Open the EPANET toolkit & hydraulics solver   
em.ENopen("./ex3-tk/EX3.inp", "./ex3-tk/EX3-tk.rpt")
# build report command strings Keyword  Action see user manual
#command0 = "Status     Yes"
command1 = "Summary            	Yes"
command2 = "Nodes            	ALL"
command3 = "Links            	ALL"
em.ENsetstatusreport(2) # full status report
#em.ENsetreport(command0)
em.ENsetreport(command1)
em.ENsetreport(command2)
em.ENsetreport(command3)
em.ENsaveinpfile("./ex3-tk/EX3-tk.inp") #overwrite the input file
em.ENclose()
# now run from the new file
em.ENopen("./ex3-tk/EX3-tk.inp", "./ex3-tk/EX3-tk.rpt")
em.ENopenH()
em.ENsolveH()
em.ENsaveH() # need to save to a binary file before write
em.ENcloseH()
em.ENopenQ()
em.ENsolveQ()
em.ENreport() # now write report
# Close hydraulics solver & toolkit */
em.ENclose()


# In[3]:


# Check the output
get_ipython().system(' cat ./ex3-tk/EX3-tk.rpt')


# Nice!  Seems like we have kind of got the hang of the Toolkit.  
# 
# :::{note}
# In class we will draw the actual network simulated above - notice the three extra links, we put these there intentionally (check the video), to be able to interpret pressures at Nodes A,B,C, and J.  In the above example, Nodes A,B, and C are all at zero elevation. Node J is at 110 - so any flow towards J must be uphill.  Lets use the toolbox to help us find the elevation Node J would need to be, to have a pressure of +1 meters.
# 
# First lets manipulate Node J elevation to produce a pressure of 0.

# In[4]:


import epamodule as em  # import the package
#Open the EPANET toolkit & hydraulics solver   
em.ENopen("./ex3-tk/EX3-tk.inp", "./ex3-tk/EX3-tk.rpt") # The modified file
# build report command strings Keyword  Action see user manual
#command0 = "Status     Yes"
#command1 = "Summary            	Yes"
#command2 = "Nodes            	ALL"
#command3 = "Links            	ALL"
#em.ENsetstatusreport(2) # full status report
#em.ENsetreport(command0)
#em.ENsetreport(command1)
#em.ENsetreport(command2)
#em.ENsetreport(command3)
#em.ENsaveinpfile("./ex3-tk/EX3-tk.inp") #overwrite the input file
#em.ENclose()
# now run from the new file
#em.ENopen("./ex3-tk/EX3-tk.inp", "./ex3-tk/EX3-tk.rpt")
em.ENopenH()
nodej = em.ENgetnodeindex("J") # Get the index of Node J in the internal database
elevj = em.ENgetnodevalue(nodej,0)
# wrap this into a little search loop
em.ENsetnodevalue(nodej, 0, elevj) # set nodej to elevation (code 0) of 100.0
em.ENsolveH()
presj = em.ENgetnodevalue(nodej,11)
print("Initial Values")
print("Elevation J: " + str(round(elevj,3)) + " Pressure J: " + str(round(presj,3)) )
# Lets do a crude search
tol = 1e-3
for iter in range(100):
    if abs(presj) <= tol:
        print("tolerance met",iter)
        break
    if presj < 0.0 :
        elevj = elevj*0.99
    if presj > 0.0 :
        elevj = elevj*1.01
    em.ENsetnodevalue(nodej, 0, elevj) # set nodej to elevation (code 0) of 100.0 
    em.ENsolveH()
    presj = em.ENgetnodevalue(nodej,11)
print("Elevation J: " + str(round(elevj,3)) + " Pressure J: " + str(round(presj,3)) )
# end search
em.ENsaveH() # need to save to a binary file before write
em.ENcloseH()
em.ENopenQ()
em.ENsolveQ()
em.ENreport() # now write report
# Close hydraulics solver & toolkit */
em.ENclose()


# Now we modify for the target pressure, supplied as a variable - obviously searching as illustrated is terribly inefficient, but does illustrate the utility of the toolkit.  We are using the computer to make adjustments and test outputs rather than doing it ourselves using the GUI; for a complex problem, its far faster to do such exercises programmatically rather then trial-and-error in a GUI.

# In[5]:


import epamodule as em  # import the package
#Open the EPANET toolkit & hydraulics solver   
em.ENopen("./ex3-tk/EX3-tk.inp", "./ex3-tk/EX3-tk.rpt") # The modified file
em.ENopenH()
nodej = em.ENgetnodeindex("J") # Get the index of Node J in the internal database
elevj = em.ENgetnodevalue(nodej,0)
# wrap this into a little search loop
em.ENsetnodevalue(nodej, 0, elevj) # set nodej to elevation (code 0) of 100.0
em.ENsolveH()
presj = em.ENgetnodevalue(nodej,11)
print("Initial Values")
print("Elevation J: " + str(round(elevj,3)) + " Pressure J: " + str(round(presj,3)) )
# Lets do a crude search
tol = 1e-3
targetp = 1.0
for iter in range(1000):
    if abs(presj-targetp) <= tol:
        print("tolerance met",iter)
        break
    if presj < targetp :
        elevj = elevj*0.99
    if presj > targetp :
        elevj = elevj*1.11
    em.ENsetnodevalue(nodej, 0, elevj) # set nodej to elevation (code 0) of 100.0 
    em.ENsolveH()
    presj = em.ENgetnodevalue(nodej,11)
print(str(iter) + " Elevation J: " + str(round(elevj,3)) + " Pressure J: " + str(round(presj,3)) )
# end search
em.ENsaveH() # need to save to a binary file before write
em.ENcloseH()
em.ENopenQ()
em.ENsolveQ()
em.ENreport() # now write report
# Close hydraulics solver & toolkit */
em.ENclose()


# ## Exercise
# A better way for the example above would be some version of bisection. Modify the script to search for the desired elevation using bisection; select a reasonable tolerance to stop.  You may find Chat-GPT 4.0 useful to construct a working script.
# 
# A bisection solver could be adapted from [Cleveland, T.G. (2022) Hydraulic System Design JupyterBook notes to accompany CE 4353/CE 5360 at TTU; Example 1 in specific energy section](http://54.243.252.9/ce-4353-webroot/ce4353jb/ce4353workbook/_build/html/lessons/specificenergy/specificenergy1.html)

# ### Example 4 - A simple looped network
# 
# Expanding the examples, we will next consider a looped network. As before we will use an exercise as the motivating example.
# 
# **Problem Statement**
# > The water-supply network shown in Figure 61 has constant-head elevated storage tanks at A and C, with inflow and outflow at B and D. ![](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/lesson02/ex4/ex4.png) The network is on flat terrain with node elevations all equal to 50 meters. If all pipes are ductile iron, compute the inflows/outflows to the storage tanks. Assume that 
# flow in all pipes are fully turbulent.
# 
# As before we will use the previously prepared input file and modify to explore the Toolkit.  By this point its legitimately a lot of cut and paste.

# In[6]:


import epamodule as em  # import the package
#Open the EPANET toolkit & hydraulics solver   
em.ENopen("./ex4-tk/EX4-JB.inp", "./ex4-tk/EX4-tk.rpt")
# build report command strings Keyword  Action see user manual
command0 = "Status     Yes"
command1 = "Summary            	Yes"
command2 = "Nodes            	ALL"
command3 = "Links            	ALL"
em.ENsetstatusreport(2) # full status report
em.ENsetreport(command0)
em.ENsetreport(command1)
em.ENsetreport(command2)
em.ENsetreport(command3)
em.ENsaveinpfile("./ex4-tk/EX4-tk.inp") #overwrite the input file
em.ENclose()
# now run from the new file
em.ENopen("./ex4-tk/EX4-tk.inp", "./ex4-tk/EX4-tk.rpt")
em.ENopenH()
em.ENsolveH()
em.ENsaveH() # need to save to a binary file before write
em.ENcloseH()
em.ENopenQ()
em.ENsolveQ()
em.ENreport() # now write report
# Close hydraulics solver & toolkit */
em.ENclose()

get_ipython().system(' cat ./ex4-tk/EX4-tk.rpt')


# Now lets use some of the tools to get more than one thing.  First we will get the count of some objects, then we will change the diameter of one pipe and examine the effect.  Notice how we can repeatedly change things and rerun the hydraulic module (as above) almost without effort using the Toolkit.

# In[7]:


#ENgetcount(countcode)

import epamodule as em  # import the package
#Open the EPANET toolkit & hydraulics solver   
em.ENopen("./ex4-tk/EX4-tk.inp", "./ex4-tk/EX4-tk.rpt")
howmanynodes = em.ENgetcount(0) # Code 0 == nodes
howmanylinks = em.ENgetcount(2) # Code 2 == links
howmanyFGN   = em.ENgetcount(1) # Code 1 == Tanks/Reservoirs
print(" System Topology is:\n")
print(" Node count: " + str(howmanynodes))
print(" Link count: " + str(howmanylinks))
print(" FGN count : " + str(howmanyFGN))
diameter = [] # create empty list
for ilink in range(howmanylinks):
    diameter.append(em.ENgetlinkvalue(ilink+1,0)) # Code 0 == diameter
    print("Link :" + str(ilink+1) + " Diameter(mm) : " + str(diameter[ilink]))
em.ENopenH()
em.ENsolveH()
hloss = [] # create empty list
for ilink in range(howmanylinks):
    hloss.append(em.ENgetlinkvalue(ilink+1,10)) # Code 10 == head loss
    print("Link :" + str(ilink+1) + " Head loss (m/1000m) : " + str(round(hloss[ilink],4)))
print("Change diameter link 4")
em.ENsetlinkvalue(4, 0, 100)
diameter = [] # create empty list
for ilink in range(howmanylinks):
    diameter.append(em.ENgetlinkvalue(ilink+1,0)) # Code 0 == diameter
    print("Link :" + str(ilink+1) + " Diameter(mm) : " + str(diameter[ilink]))
em.ENsolveH()
nhloss = [] # create empty list
for ilink in range(howmanylinks):
    nhloss.append(em.ENgetlinkvalue(ilink+1,10)) # Code 10 == head loss
    print("Link :" + str(ilink+1) + " Head loss (m/1000m) : " + str(round(nhloss[ilink],4)))
em.ENsaveH() # need to save to a binary file before write
em.ENcloseH()
em.ENopenQ()
em.ENsolveQ()
em.ENreport() # now write report
# Close hydraulics solver & toolkit */
em.ENclose()


# ## Exercise
# Change the parameter code to recover flow instead of head loss and rerun the example, what effect does shrinking pipe 4 have on flow rate?

# ### Example 5 - Simulating a Pump
# 
# This example repeats the same problem as before, but using the Toolkit to load and run the model.  A bit of the earlier example is replicated below:
# 
# >Figure XX is a conceptual model of a pump lifting water through a 100 mm diameter, 100 meter long, ductile iron pipe from a lower elevation reservoir to an upper reservoir. <br><br>![](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/lesson02/ex5/P2-39.png)<br><br>The suction side of the pump is a 100 mm diameter, 4-meter long ductile iron pipe. The difference in reservoir free-surface elevations is 10 meters. <br><br>The pump performance curve is given
# as 
# $$hp = 15.0-0.1Q^2 $$
# where the added head is in meters and the flow rate is in liters per second (lps). 
# The analysis goal is to estimate the flow rate in the system.
# 
# To use the Toolkit we more or less just repeat from the above examples, here I run the entire simulation as some adjustments are left as exercises.

# In[8]:


import epamodule as em  # import the package
# Run a complete simulation. input file must already exist
em.ENepanet("./ex5-tk/EX5-tk.inp", "./ex5-tk/EX5-tk.rpt") 
# Print the output report (it will be sparse)
get_ipython().system('cat ./ex5-tk/EX5-tk.rpt')


# ## Exercise
# Use the Toolkit to modify the input file (EX5-tk) to produce a more useful output file.

# In[9]:


# one possible solution
import epamodule as em  # import the package
#Open the EPANET toolkit & hydraulics solver   
em.ENopen("./ex5-tk/EX5-tk.inp", "./ex5-tk/EX5-tk.rpt")
# build report command strings Keyword  Action see user manual
command0 = "Status     Yes"
command1 = "Summary            	Yes"
command2 = "Nodes            	ALL"
command3 = "Links            	ALL"
em.ENsetstatusreport(2) # full status report
em.ENsetreport(command0)
em.ENsetreport(command1)
em.ENsetreport(command2)
em.ENsetreport(command3)
em.ENsaveinpfile("./ex5-tk/EX5-tkmod.inp") #overwrite the input file
em.ENclose()
# now run from the new file
em.ENepanet("./ex5-tk/EX5-tkmod.inp", "./ex5-tk/EX5-tkmod.rpt")
get_ipython().system(' cat ./ex5-tk/EX5-tkmod.rpt')


# ## Exercise
# Modify the upstream pool elevation so it is at 14.999 meters.  The pump flowrate should go down a lot (but not to zero).  

# In[10]:


# one possible solution
import epamodule as em  # import the package
#Open the EPANET toolkit & hydraulics solver   
em.ENopen("./ex5-tk/EX5-tkmod.inp", "./ex5-tk/EX5-tkmod.rpt")
# The upper reservoir is Node 2 in the input file
nodej = em.ENgetnodeindex("2") # Get the index of Node 2 in the internal database
elevj = em.ENgetnodevalue(nodej,0) # Get the elevation and check
print("Internal Node: ",nodej," Initial Head: ",round(elevj,3))
elevj=24.9999 # Change so thet DeltaH is 14.999
print("Increase Head to ", round(elevj,3))
em.ENsetnodevalue(nodej,0,elevj)
em.ENsaveinpfile("./ex5-tk/EX5-tkmod.inp") #overwrite the input file
em.ENclose()
# now run from the new file
em.ENepanet("./ex5-tk/EX5-tkmod.inp", "./ex5-tk/EX5-tkmod.rpt")
get_ipython().system(' cat ./ex5-tk/EX5-tkmod.rpt')


# ## Exercise
# Now modify the pump curve to approximately recover the flowrate.
# 
# :::{warning}
# At the time of writing, pump curves are edited outside of the Toolkit - you would search the input file for the section
# ```
# [CURVES]
# ;ID              	X-Value     	Y-Value
# ;PUMP: 
#  1               	0           	15          
#  1               	1           	14.9        
#  1               	10          	5   
#  ```
#  Then edit the indicated curve - for this exercise, manual edits would be OK.
# :::
# 
# :::{note}
# Probably just do this in class and leave the file on the server
# :::
# 

# In[ ]:





# ## Files
# 
# The files used in the above examples are located at:
# 
# 1. [EX3.inp](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/lesson03/ex3-tk/EX3.inp)
# 2. [EX4-JB.inp](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/lesson03/ex4-tk/EX4-JB.inp)
# 3. [EX5-tk.inp](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/lesson03/ex5-tk/EX5-tk.inp)

# In[ ]:




