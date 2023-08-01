#!/usr/bin/env python
# coding: utf-8

# # 1.5 The `pipenet` module
# 
# With the entire script as a module, we just load the module when we need it.  To do this we simply took the contents of the `def pipenet()` cell and copy and paste into a text file, then name the textfile something memorableful - in my case `pipenet.py`
# 
# To use the module either load it into your python kernel or locate it in the directory where you are working and import the module as illustrated below, because our desired entry point shares the same name as the file, i used a weird syntax. The more convential method is also shown.

# In[1]:


# Now import the module (observe the semi-weird syntax)
from pipenet import pipenet
# Now run the simulation 
pipenet('PN-E2.txt') 


# In[2]:


# Now import the module (conventional syntax)
import pipenet
# Now run the simulation 
pipenet.pipenet('PN-E2.txt') 


# Now that we have a compact (to us) tool we can explore different problems.

# ## Example 2: 
# For the given source and loads shown, how will the flow be distributed in the network, and what will be the pressures at the nodes, if the source pressure is $60~psi$.  The pipes are all horizontal, and the pipes are HDPE?
# 
# ```{figure} example2-15.png
# ---
# width: 400px
# name: example2-15
# ---
# Pipe network for Example 2
# ```
# 
# ### Known
# 
# 1. Node-arc matrix
# 2. Pipe lengths
# 3. Pipe diameters
# 4. Material
# 5. Node elevations (we will have to assume a value)
# 
# ### Unknown
# 
# 1. Pressures at each node
# 2. Discharge in each pipe
# 
# ### Governing Principles
# 
# 1. Continunity at nodes
# 2. Head loss in pipes (Darcy-Weisbach model)
# 3. Energy unique at nodes
# 
# ### Analysis
# 
# Use method of [Hamam, Y.M., and Brameller, A. (1971)](http://54.243.252.9/ce-3372-webroot/3-Readings/HamamAndBrameller/).
# 
# #### Build Input File
# 
# ```{figure} IMG-6194.png
# ---
# width: 400px
# name: IMG-6194
# ---
# Pipe network notations for Example 2 input file build
# ```
# 
# - 5 nodes (plus a 6-th supply node in this example it is node 0)
# - 7 pipes (the supply pipe (pink arrow) at node 1 is set as a short  and large diameter pipe, pipe P7)
# 
# ```
# 5
# 7
# ```
# 
# - node elevations
# 
# ```
# 0 0 0 0 0 0
# ```
# 
#  Pipe diameters
# 
# ```
# 2.0 0.83 1.0 1.0 0.75 0.83 10.0
# ```
# 
# - Pipe lengths
# 
# ```
# 1000 1410 1000 1000 1000 1000 10
# ```
# 
# - Pipe roughness heights (based on material)
# 
# ```{figure} HDPE-roughness.png
# ---
# width: 400px
# name: HDPE-roughness
# ---
# Source for HDPE roughness approximation
# ```
# 
# ```
# 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001
# ```
# 
# - Viscosity
# 
# ```
# 0.000011
# ```
# 
# - Initial Discharge Vector (just use ones)
# 
# ```
# 1 1 1 1 1 1
# ```
# - The node-arc matrix
# 
# ```
# -1 -1  0  0  0  0  1
# 1 0 -1 0 1 0 0
# 0 0  1 0 0 -1 0
# 0 0  0 -1 0 1 0 
# 0 1 0 1 -1 0 0 
# ```
# 
# - The right-hand side (demands and node 0 head)
# 
# ```
# 0  0 10  5  0  0  0  0  0  0  0 -134.25  # we will change the last value to get desired pressure at node 1
# ```
# 
# Save this into a file named `L15-E2.txt`
# 
# > L15-E2.txt
# ```
# 5
# 7
# 0 0 0 0 0 0
# 2.0 0.83 1.0 1.0 0.75 0.83 10.0
# 1000 1410 1000 1000 1000 1000 10.0
# 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001
# 0.000011
# 1 1 1 1 1 1 1 1 1 1 1 1
# -1 -1  0  0  0  0  1
# 1 0 -1 0 1 0 0
# 0 0  1 0 0 -1 0
# 0 0  0 -1 0 1 0 
# 0 1 0 1 -1 0 0 
# 0  0 10  5  0  0  0  0  0  0  0 -134.25 
# 
# ```
# 
# As before now run the script to generate the input file

# In[3]:


# A simple script to generate L15-E2.txt
data = """5
7
0 0 0 0 0 0
2.0 0.83 1.0 1.0 0.75 0.83 10.0
1000 1410 1000 1000 1000 1000 10.0
0.00001 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001
0.000011
1 1 1 1 1 1 1 1 1 1 1 1
-1 -1  0  0  0  0  1
1 0 -1 0 1 0 0
0 0  1 0 0 -1 0
0 0  0 -1 0 1 0 
0 1 0 1 -1 0 0 
0  0 10  5  0  0  0  0  0  0  0 -134.25"""

with open("L15-E2.txt", "w") as file:
    file.write(data)
file.close()


# In[4]:


# Now run the simulation 
pipenet.pipenet('L15-E2.txt') 


# ### Interpret Results and Discussion
# 
# The script handles calculations, the designer has to set-up the input file and create a naming convention for building the input file.  Typically would transfer output back to a visual representation as below:
# 
# 
# ```{figure} IMG-6195.png
# ---
# width: 400px
# name: IMG-6195
# ---
# Pipe network solution for Example 2 
# ```
# 
# Professional network software makes building the input file a matter of selecting elements from a menu (i.e. nodes = hamburgers, pipes = fries) and laying them out on a table.  The FGN is a soft drink piped into the network either by a straw or a french fry.  

# ## Example 3:
# This example is just another case.
# 
# ```{figure} Example3-15.png
# ---
# width: 400px
# name: Example3-15
# ---
# Pipe network data for Example 3 
# ```
# The engineer sets up the problem
# 
# ```{figure} example3-15-setup.png
# ---
# width: 400px
# name: example3-15-setup
# ---
# Pipe network worksheet for Example 3 (US Units)
# ```

# Following the same protocol as prior examples, build an input file
# 
# > L15-E3.txt
# 
# ```
# 6
# 8
# 170.0 180.0 165.0 155.0 150.0 145.0
# 0.83 0.83 1.00 2.00 0.83 1.50 0.83 1.00
# 4000 6000 6000 6000 7000 3000 5000 300.0
# 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001
# 0.000011
# 1 1 1 1 1 1 1 1 1 1 1 1
# 1   0 -1  0  0  0  0  0
# -1 -1  0 -1  0  0  0  1
# 0   1  0  0 -1  0  0  0
# 0   0  1  0  0 -1  0  0
# 0   0  0  1  0  1  1  0
# 0   0  0  0  1  0 -1  0
# 1.114 1.114 1.114 3.347 2.228 3.347 0  0  0  0  0  0  0  -315
# ```
# 
# Then run the script

# 

# In[5]:


# A simple script to generate L15-E3.txt
data = """6
8
170.0 180.0 165.0 155.0 150.0 145.0
0.83 0.83 1.00 2.00 0.83 1.50 0.83 1.00
4000 6000 6000 6000 7000 3000 5000 300.0
0.00001 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001
0.000011
1 1 1 1 1 1 1 1 1 1 1 1
1   0 -1  0  0  0  0  0
-1 -1  0 -1  0  0  0  1
0   1  0  0 -1  0  0  0
0   0  1  0  0 -1  0  0
0   0  0  1  0  1  1  0
0   0  0  0  1  0 -1  0
1.114 1.114 1.114 3.347 2.228 3.347 0  0  0  0  0  0  0  -315"""

with open("L15-E3.txt", "w") as file:
    file.write(data)
file.close()


# In[6]:


# Now run the simulation 
pipenet.pipenet('L15-E3.txt') 


# ### Interpret Results and Discussion
# 
# The script handles calculations, the designer has to set-up the input file and create a naming convention for building the input file.  Typically would transfer output back to a visual representation as below:
# 
# 
# ```{figure} example3-15solve.png
# ---
# width: 400px
# name: example3-15solve
# ---
# Pipe network solution for Example 3 
# ```

# 
# ## Readings
# 
# 
# 1. Hibbeler, R.C, Fluid Mechanics, 2ed. Prentice Hall, 2018. ISBN: 9780134655413 pp. 469-490
# 
# 3. DF Elger, BC Williams, Crowe, CT and JA Roberson, *Engineering Fluid Mechanics 10th edition*, John Wiley & Sons, Inc., 2013. [http://54.243.252.9/ce-3305-webroot/3-Readings/EFM-15.pdf](http://54.243.252.9/ce-3305-webroot/3-Readings/EFM-15.pdf)
# 
# 4. Cleveland, T. G. (2014) *Fluid Mechanics Notes to Accompany CE 3305 at Jade-Holshule (TTU Study Abroad 2015-2019)*, Department of Civil, Environmental, and Construction Engineering, Whitacre College of Engineering. [http://54.243.252.9/ce-3305-webroot/3-Readings/ce3305-lecture12.pdf](http://54.243.252.9/ce-3305-webroot/3-Readings/ce3305-lecture12.pdf)
# 
# 4. Pipe Networks Chin, D. (2006). pp. 27-48 in "Water Resources Engineering, 2 ed." Prentice Hall, Inc. [Chin_27-48](http://54.243.252.9/ce-3372-webroot/3-Readings/Chin_27-48/)
# 
# 5. Hydraulics of Pipelines and Pipe Networks Wurbs, R.A., and James, W. P. (2002) Water Resources Engineering, Prentice Hall; pp.130-156; and 156-198. [Wurbs and James](http://54.243.252.9/ce-3372-webroot/3-Readings/Wurbs130-198/)
# 
# 6. Hamam, Y.M., and Brameller, A. (1971) "Hybrid method for the solution of piping networks." Proc. IEEE, Vol. 118, No. 11, pp 1607-1612. [HamamAndBrameller](http://54.243.252.9/ce-3372-webroot/3-Readings/HamamAndBrameller/)
# 
# 7. Jeppson, R.W. (1977) Analysis of Flow in Pipe Networks, Ann Arbor Science pp. 115-129 [NewtonRaphsonTheory](http://54.243.252.9/ce-3372-webroot/3-Readings/NewtonRaphsonTheory/)
# 
# 8. Jeppson, R.W. (1977) Analysis of Flow in Pipe Networks, Ann Arbor Science pp. 53-69 [FlowInPipeNetworks](http://54.243.252.9/ce-3372-webroot/3-Readings/FlowInPipeNetworks/)
# 
# 9. Computational Hydraulics in R (for CE 3305) [PCHinR](http://54.243.252.9/ce-3372-webroot/3-Readings/CFMinR/)
# 
# 10. Yoo, D.H. and Singh V. P. (2005) Two Methods for the Computation of Commercial Pipe Friction Factors. ASCE Journal of Hydraulic Engineering, 2005, 131(8): 694-704 [FrictionFactors](http://54.243.252.9/ce-3372-webroot/3-Readings/FrictionFactor/)
# 
#  

# In[ ]:




