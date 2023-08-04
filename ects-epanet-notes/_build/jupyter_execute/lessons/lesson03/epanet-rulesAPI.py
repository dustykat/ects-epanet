#!/usr/bin/env python
# coding: utf-8

# # 3.4 EPANET Control Rules using the Toolkit
# 
# ## Purpose
# 
# ## Installation
# 
# ## Examples
# 
# The script below manipulates the `Net1.inp` example.

# In[1]:


## simple rules
import epamodule as em  # import the package
#Open the EPANET toolkit & hydraulics solver   
em.ENopen("./ex1-cr/Net1.inp", "./ex1-cr/Net1-tk.rpt")
# build report command strings Keyword  Action see user manual
command0 = "Status     Yes"
command1 = "Summary            	Yes"
command2 = "Nodes            	ALL"
command3 = "Links            	ALL"
#em.ENsetstatusreport(2) # full status report
em.ENsetreport(command0)
em.ENsetreport(command1)
em.ENsetreport(command2)
em.ENsetreport(command3)
em.ENsaveinpfile("./ex1-cr/Net1-tk.inp") #overwrite the input file
nodej = em.ENgetnodeindex("2")
linkp = em.ENgetlinkindex("9")
print("Control Sensor Node: ",nodej,"Controlled Link: ",linkp)
outstr = em.ENgetcontrol(1)
print("Control Type: ",outstr[0]," Controlled Link: ",      outstr[1]," Control Action: ",outstr[2]," Control Sensor Node: ",      outstr[3],"Control Value: ",outstr[4])
outstr = em.ENgetcontrol(2)
print("Control Type: ",outstr[0]," Controlled Link: ",      outstr[1]," Control Action: ",outstr[2]," Control Sensor Node: ",      outstr[3],"Control Value: ",outstr[4])
#print(outstr)
em.ENclose()
# now run from the new file
# now run from the new file
em.ENopen("./ex1-cr/Net1-tk.inp", "./ex1-cr/Net1-tk.rpt")
em.ENopenH()
em.ENsolveH()
em.ENsaveH() # need to save to a binary file before write
em.ENcloseH()
em.ENopenQ()
em.ENsolveQ()
em.ENreport() # now write report
# Close hydraulics solver & toolkit */
em.ENclose()
get_ipython().system(' cat ./ex1-cr/Net1-tk.rpt')


# ## Links to Server 
# 
# 1. [Control Example Files (above)](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/lesson03/ex1-cr)

# In[ ]:




