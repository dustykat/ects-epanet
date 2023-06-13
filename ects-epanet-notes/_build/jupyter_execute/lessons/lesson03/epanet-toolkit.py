#!/usr/bin/env python
# coding: utf-8

# # 3 EPANET Programmers Toolkit
# 
# The EPANET Programmer's Toolkit is a software applications programming interface (API) designed to facilitate the analysis and simulation of water distribution networks. Developed by the United States Environmental Protection Agency (EPA), EPANET is widely recognized as a comprehensive and reliable hydraulic and water quality modeling tool. The EPANET Programmer's Toolkit offers engineers and researchers the ability to harness the full potential of EPANET's capabilities, providing a platform for advanced water network analysis and optimization, directly accessing the computation engine without requiring the Graphical User Interface (GUI), or running the program in a batch mode with a prebuilt input file.

# ## Overview
# 
# The EPANET Programmer's Toolkit provides essential functions that allow users to manipulate EPANET models and retrieve critical information for hydraulic and water quality analysis. With the toolkit, users can access network data such as pipe and node properties, demand patterns, and control settings. This information can be modified or updated programmatically, enabling engineers to conduct what-if scenarios, optimize system design, and assess the impact of various operational strategies on network performance.
# 
# One of the toolkit's key features is its ability to perform hydraulic and water quality simulations. Users can dynamically simulate water flow and pressure behavior in the network, enabling accurate prediction of system performance under different operating conditions. Moreover, the toolkit allows for the analysis of water quality parameters, such as chlorine concentration and contaminant transport, aiding in the evaluation of water safety and compliance with regulatory standards.
# 
# The EPANET Programmer's Toolkit empowers water industry professionals to tackle complex water network challenges with greater efficiency and accuracy. By leveraging its capabilities, engineers can optimize pipe sizing, evaluate system resilience, and assess the impact of infrastructure changes on network performance. The toolkit's ability to perform advanced simulations and analysis aids in the identification of potential issues, facilitating proactive decision-making and improving overall water network management. Furthermore, the EPANET Programmer's Toolkit plays a crucial role in supporting research and innovation in the field of water distribution system analysis, fostering the development of new methodologies and solutions to address emerging challenges in water management.
# 
# :::{note} link to EPANET toolkit description here :::

# ## Purpose
# 
# The primary purpose of the EPANET Programmer's Toolkit is to enhance the functionality of EPANET and enable users to access its full potential in water distribution network analysis. The Toolkit serves as an **interface** that allows engineers and researchers to programmatically access and manipulate EPANET models, retrieve critical information, and perform hydraulic and water quality simulations without having to access the model through the Graphical User Interface (GUI). By providing essential modeling access functions, integration capabilities, and customization options, the toolkit enables analysts to conduct in-depth analysis, optimize system design, and evaluate the performance of water networks under various operational conditions.
# 
# The EPANET Programmer's Toolkit supports integration with various programming languages, including C, C++, and Python, making it end-user adaptable to different software development environments. This flexibility allows engineers and researchers to leverage their preferred programming languages and frameworks, facilitating seamless integration with existing tools and workflows. Additionally, the toolkit's extensive Application Programming Interface (API) documentation and code examples provide valuable resources for developers, enabling them to extend EPANET's functionality and customize the software to meet specific project requirements.

# ## Installing on a Raspberry Pi 
# 
# This section is specific to my development computer - the process is:
# 
# 1. Download source files.
# 2. Build a shared object library.
# 2. Copy the library (or path to the library) into a working directory where you intend to run scripts.
# 3. Write and run your scripts to implement EPANET from python.
# 
# ### Download source files
# 
# Easiest is to create a directory, navigate to that directory, then clone the GitHub repository.
# 
# ```
# # As regular user or root user
# mkdir en2toolkit
# cd en2toolkit 
# git clone https://github.com/OpenWaterAnalytics/EPANET.git  #clone the remote into the directory
# ```
# 
# After the repository is cloned, step 1 above is complete

# ### Build a shared object library
# 
# From here need to work as superuser, so either change to root or use sudoprefix to the directives. I switched to the root user because my regular user cannot issue superuser commands.  Then issue the `cmake ..` directive to compile the objects for linking into the package.  After that completes then issue the `cmake --build . --config Release` directive and let it run to (hopefully successful) completion.
# 
# ![](buildtools1of2.png)
# 
# After that completes then the library is found in the `\lib` directory.  Simply copy it into the work directory where you want to model.  A symbolic link added into the `PATH` environment variable is another way to proceede.
# 
# ![](buildtools2of2.png)
# 
# Now to test the build of the shared object modules.  Import the interface module (listing below) which is stored as a file in our workspace.
# 
# [epamodule.py (from OWA GitHub)](epamodule.py) 
# 
# ### Copy the library to the working directory
# 
# For my example herein, I copied the build into:
# `/home/sensei/ects-epanet/ects-epanet-notes/lessons/lesson03/`
# 
# I also copied two EPANET input files `Net1.inp` and `Net1g.inp`  
# 
# The listing below shows the directory, you can see the shared object library at the end of the listing, as well as the two input files for subsequent examples.  Also note the presence of a file named `epamodule.py` which is used below to access the toolkit.

# In[1]:


get_ipython().system(' ls -la')


# ### Write and run your scripts to implement EPANET from python.
# 
# Below we demonstrate the last step, to write and run scripts that implement EPANET from our iPython kernel.
# 
# First import the `epamodule.py` package.

# In[2]:


import epamodule as em  # import the package


# Then run an example

# In[3]:


em.ENepanet("Net1.inp", "Net1.rpt") # runs a complete simulation. input file must exist and have contents.


# Now same example but more granular control.  

# In[4]:


#Open the EPANET toolkit & hydraulics solver   
em.ENopen("Net1g.inp", "Net1g.rpt")
em.ENopenH()
em.ENsolveH()
em.ENsaveH() # need to save to a binary file before write
em.ENcloseH()
em.ENopenQ()
em.ENsolveQ()
em.ENreport() # now write report
# Close hydraulics solver & toolkit */
em.ENclose()


# ## References
# 
# 1. [OpenWaterAnalytics(epanet-python)](https://github.com/OpenWaterAnalytics/epanet-python/) The GitHub source for the `epamodule.py` above.
# 3. [https://github.com/OpenWaterAnalytics/epanet/](https://github.com/OpenWaterAnalytics/epanet/) The GitHub source for the code and build instructions for the shared object library above.
# 4. [EPANET (EPA website)](https://www.epa.gov/water-research/epanet)  Links to current EPA distributed EPANET programs and source files.
# 5. [EPANET2.2](https://github.com/USEPA/EPANET2.2)  EPA GitHub source.
# 6. [EPANETTOOLS1.0.0 (A pypi.org package) ](https://pypi.org/project/EPANETTOOLS/)  A package manager for EPANETTOOLS.
# 7. [mycopy](http://#) Link to modified copy of `epamodule.py`
# 8. [Net1.inp](http://#) Link to modified copy of
# 9. [Net1g.inp](http://#) Link to modified copy of
# 
# :::{note}
# Most of these sites cross-share content, so whether using OWA or EPA official you are likely getting the same program; if its use is for some official capacity (like a water utility) use the EPA sites as your source.
# :::

# 

# 

# 
