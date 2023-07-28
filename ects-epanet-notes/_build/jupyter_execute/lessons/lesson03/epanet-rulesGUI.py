#!/usr/bin/env python
# coding: utf-8

# # 3.2 EPANET example using Toolkit
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


# Now to manipulate the model, we will make the link twice as long.
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

# In[ ]:




