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

# In[ ]:




