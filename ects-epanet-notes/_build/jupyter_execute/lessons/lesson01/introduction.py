#!/usr/bin/env python
# coding: utf-8

# # 1 Hydraulic Networks and Python
# 
# ## Purpose and Scope
# 
# The purpose of the course is demonstrate how to operate predictive tools for pipe network hydraulics; apply these tools to the simulation of distribution and pumping systems; install the tools onto a single board computer and demonstrate distributed automated control of the distribution and pumping system.
# 
# The course is intended for learners who may not have a hydraulics background, but do have an information technology background. The course examines the vital linkage between information technology and physical infrastructure in the built environment.
# 
# This book is simply a collection of the course notes, mostly organized, for documenting the goals outlined above. 
# 
# :::{warning}
# All the Toolkit examples are in this notebook are run on builds of EPANET and the Toolkit for the aarch (Raspberry Pi, Arduino, etc.) chipset.  The examples run on a GUI (using http:\\freeswmm.ddns.net web access) are using the x86 chipset and I did nothing other than use a WINE application layer to make the server provide a desktop to the web interface.
# :::
# 
# The layout of the notebook is the course scope.  
# 
# - Part 1 is an introduction to hydraulics as applied to networks of conduits (pipes).  For many participants it will be a refresher, for some entirely new material - but the concepts are straightforward.  Networks have links (flow paths, roads, etc ..) and junctions (nodes, intersections, etc.).  It takes energy to move along links, and we can only enter and leave the network at junctions.  From here some relatively mature physics is used to describe behavior.  After the introduction to hydraulics, we spend some time on Jupyter (yes thats a pun!) and python mostly a very cursory overview, then onward to implementing network hydraulics in DIY python, creation of a module, incorporating pumps.  At this point we could quit, but the point is to illustrate what is going on to some extent in the EPANET program.
# - Part 2 Introduction to the EPANET program, and an online implementation with the EPA supplied interface. Then a series of examples.  After the first five examples, we examine the concept of extended period simulation, constituient transport (water quality), and finally control rules in the simultion.
# - Part 3 Introduces the Toolkit, a way to incorporate EPANET into other programs to use it as a simulator or control guide.
# - Part 4 Continues with examination of ways to use the tools for control or optimization.

# ## References

# 

# In[ ]:




