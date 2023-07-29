#!/usr/bin/env python
# coding: utf-8

# # 3.2 EPANET (Examples 1 and 2) using the Toolkit
# 
# ## Purpose
# This section demonstrates the various previous examples using the Toolkit to run the example and make changes to inputs and rerun the examples.  The main concept is that the Toolkit allows manipulation of models independent of a GUI which when combined with either Toolkit supplied control rules, or external "control" lets one model and interpret (assuming IF-THEN interpretation is amenable) many changes automatically.
# 
# ## Installation
# The examples herein are on the developmental computer (a Raspberry Pi).  The scripts should work fine on another computer with the toolkit installed (Windows probably takes a bit more fussing to get the Linux subsystem to call to the Toolkit). 
# 
# ### Example 1 - Head Loss in a Pipeline 
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
# This example is verbatim from the previous sections, here the examples are presented using the Toolkit interface.  The ASCII (.net) input file is taken from the previous section. Then manipulated in the example - it is the essence of the Toolkit.  Many of the steps below, are repetitive so I don't forget the steps myself. As one gets familiar with the process, I would suspect it becomes second nature.  
# :::
# 
# #### Copy the library 
# Copy the library into the working directory which on the development machine is `ects-epanet/ects-epanet-notes/lessons/lesson03/ex1-tk` or adapt the path to the already installed working directory, in this example we will take the second approach.  Here is the directory listing before running the example .
# 
# :::{note}
# The file removal step is to delete any existing output files.  Its not necessary except to ensure this notebook builds in a fashion that tells the manipulation story well.
# :::

# In[1]:


get_ipython().system('rm -rf ./ex1-tk/*.rpt')
get_ipython().system('ls -la ./ex1-tk')


# And a look at the contents of the input file

# In[2]:


get_ipython().system(' cat ./ex1-tk/EX1tk.inp')


# The library `epamodule.py` and the shared object library (similar to a DLL) are already installed at `ects-epanet/ects-epanet-notes/lessons/lesson03` which houses the examples. Next we build and run the necessary script(s)

# In[3]:


import epamodule as em  # import the package


# In[4]:


#em.ENepanet("./ex1-tk/EX1tk.inp", "./ex1-tk/EX1tk.rpt") # runs a complete simulation. input file must exist and have contents.


# In[5]:


#Open the EPANET toolkit & hydraulics solver   
em.ENopen("./ex1-tk/EX1tk.inp", "./ex1-tk/EX1tk.rpt")
em.ENopenH()
em.ENsolveH()
em.ENsaveH() # need to save to a binary file before write
em.ENcloseH()
em.ENopenQ()
em.ENsolveQ()
em.ENreport() # now write report
# Close hydraulics solver & toolkit */
em.ENclose()


# Now can look at simulation results

# In[6]:


get_ipython().system(' cat ./ex1-tk/EX1tk.rpt')


# Now to manipulate the model, we will make the link half as long.
# 
# 
# :::{note}
# The python module seems a little different from `C` and `R` scripting examples and uses numeric codes in place of the string codes in the online examples of the Toolkit. Maybe its an IQ test; but here are the codes for links:
# 
# ```
# EN_DIAMETER      = 0      # /* Link parameters */
# EN_LENGTH        = 1
# EN_ROUGHNESS     = 2
# EN_MINORLOSS     = 3
# EN_INITSTATUS    = 4
# EN_INITSETTING   = 5
# EN_KBULK         = 6
# EN_KWALL         = 7
# EN_FLOW          = 8
# EN_VELOCITY      = 9
# EN_HEADLOSS      = 10
# EN_STATUS        = 11
# EN_SETTING       = 12
# EN_ENERGY        = 13
# ```
# :::
# 

# In[7]:


import epamodule as em  # import the package
#Open the EPANET toolkit & hydraulics solver   
em.ENopen("./ex1-tk/EX1tk.inp", "./ex1-tk/EX1-1tk.rpt")
em.ENopenH()
linkname = em.ENgetlinkid(1) # get the name of the link - numbering starts at 1, linkname is a byte literal
decoded_linkname = linkname.decode('utf-8')
print("linkname is :" + decoded_linkname)
# now lets get the length of the link
parmcode=1 # this is the code for length - a table exists in the epamodule.py file
linklong = em.ENgetlinkvalue(1,parmcode)
print("link length is: " + str(linklong) + ' feet')
print("lets decrease the length and re-run the model")
linklong = 0.5*linklong
print("link length is: " + str(linklong) + ' feet')
em.ENsetlinkvalue(1, parmcode, linklong)
print("verify the reset")
newlinklong = em.ENgetlinkvalue(1,parmcode)
print("new link length is: " + str(newlinklong) + ' feet')
em.ENsolveH()
em.ENsaveH() # need to save to a binary file before write
em.ENcloseH()
em.ENopenQ()
em.ENsolveQ()
em.ENreport() # now write report
# Close hydraulics solver & toolkit */
em.ENclose()


# Now look at the output and observe the changes - in this instance the pressure head is larger at the node than in the longer pipe case; an anticipated result.

# In[8]:


get_ipython().system(' cat ./ex1-tk/EX1-1tk.rpt')


# That concludes this simple (not intrinsicly usefull just yet) example.  Lets continue with another one from our GUI cases.

# ### Example 2 Flow Rate in a Pipeline
# 
# This example represents the situation where the total head is known at two points on a pipeline, and one wishes to determine the flow rate (or specify a flow rate and solve for a pipe diameter). Like the prior example it is contrived, but follows the same general modeling process.
# 
# As in the prior example, we will use EPANET to solve a problem we have already solved by hand.
# 
# The **problem statement** is:
# >Using the Moody chart, and the energy equation, estimate the diameter
# of a cast-iron pipe needed to carry 60oF water at a discharge of 10 cubic-
# feet per second (cfs) between two reservoirs 2 miles apart. The elevation
# difference between the water surfaces in the two reservoirs is 20 feet.
# > A sketch of the situation is ![](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/lesson02/ex2/EX2.bmp)
# 
# As in the prior example, we will start with the ASCII input file and manipulate the model with the Toolkit.  The default input file will produce very little output other than to acknowledge the simulation ran to completion.  So we will manipulate the output instructions.  First we start with the input file, in this case it is named `EX2-JB-Copy1.inp`

# In[9]:


get_ipython().system(' cat ./ex2-tk/EX2-JB-Copy1.inp')


# Now lets examine the section regarding the report.
# 
# ```
# [REPORT]
#  Status             	No
#  Summary            	No
#  Page               	0
# ```
# 
# This pretty much says report nothing - we can see the impact by running the model and examining the output report.

# In[10]:


import epamodule as em  # import the package
#Open the EPANET toolkit & hydraulics solver   
em.ENopen("./ex2-tk/EX2-JB-Copy1.inp", "./ex2-tk/EX2-JB-Copy1.rpt")
em.ENopenH()
em.ENsolveH()
em.ENsaveH() # need to save to a binary file before write
em.ENcloseH()
em.ENopenQ()
em.ENsolveQ()
em.ENreport() # now write report
# Close hydraulics solver & toolkit */
em.ENclose()


# Examine the output file

# In[11]:


get_ipython().system(' cat ./ex2-tk/EX2-JB-Copy1.rpt')


# Observe not much of a report.  Lets use the toolkit to enhance the report output.

# In[12]:


import epamodule as em  # import the package
#Open the EPANET toolkit & hydraulics solver   
em.ENopen("./ex2-tk/EX2-JB-Copy1.inp", "./ex2-tk/EX2-JB-Copy1.rpt")
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
em.ENsaveinpfile("./ex2-tk/EX2-tkmodify.inp") #write to a new file
em.ENclose()
# now run from the new file
em.ENopen("./ex2-tk/EX2-tkmodify.inp", "./ex2-tk/EX2-tkmodify.rpt")
em.ENopenH()
em.ENsolveH()
em.ENsaveH() # need to save to a binary file before write
em.ENcloseH()
em.ENopenQ()
em.ENsolveQ()
em.ENreport() # now write report
# Close hydraulics solver & toolkit */
em.ENclose()


# In[13]:


# The old file
get_ipython().system(' cat ./ex2-tk/EX2-JB-Copy1.rpt')


# In[14]:


# The new file
get_ipython().system(' cat ./ex2-tk/EX2-tkmodify.rpt')


# So we have the ability to modify important parts of input files to meet our needs.  We could have also overwritten to the original file and juct run everything in a single pass, but for clarity we have kept the files separate.  Naturally, we are now responsible for our own "graphics" if thats of interest (later on we can try to adapt EPyT scripts)

# ## References

# ## Exercises
