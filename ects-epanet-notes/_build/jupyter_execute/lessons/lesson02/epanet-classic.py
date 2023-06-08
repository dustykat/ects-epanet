#!/usr/bin/env python
# coding: utf-8

# # 2 EPANET Intro/Examples
# 
# what is epanet?
# 
# ## Purpose
# what is it for?
# 
# versions
# 
# ### GUI Access
# 
# EPANET as supplied by URL also includes a graphical user interface (GUI) that will allow one to quickly build network simulation models, run them, and present results.  The GUI runs on Windows machines using Intel/AMD hardware.  It can be made to run on other operating systems and architectures, but not easily.
# 
# ```{admonition} Architectures and Operating Systems
# The EPANET computation engine can be made to work in different operating systems with very little fuss.  In fact the current OWS versions all employ CMAKE to build targets for the big-three Operating Systems (Windows, Mac, Linux).
# 
# Architecture refers to the underlying silicon; x86-64 is an Intel/AMD 64-bit chipset, aarch64 is the ARM 64-bit chipset.
# 
# At the time of this writing builds for aarch64 are kind of up to the end-user;  I have notes herein on how-to do so.  Why anyone would want to make such a build is to leverage embedded systems with intent to use the program to control things.  I am aware most people are going to be using a Windows machine on Intel hardware and special instructions specific to ARM hardware is meaningless.
# ```
# 
# ### EPANET On-Line Access
# 
# An on-line version herein uses the WINE application layer to run an implementation of EPANET with the "Classic" GUI on a Linux server, on an Intel x86-64 chipset.  
# 
# Access is as simple as 
# ## EPANET by Example
# 
# ## Exercises
# 

# In[ ]:




