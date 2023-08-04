#!/usr/bin/env python
# coding: utf-8

# # 2 EPANET Intro/Examples
# 
# EPANET is a widely used computer software developed by the United States Environmental Protection Agency (EPA) for modeling water distribution systems. It enables engineers and researchers to simulate and analyze the flow of water in pipes, tanks, and other components of a water distribution network. The software helps to assess water quality, identify potential issues such as leaks and pressure deficiencies, and optimize system performance. With its user-friendly interface and powerful capabilities, EPANET plays a crucial role in designing and managing efficient and reliable water supply systems in both urban and rural settings.
# 
# ## Purpose
# Beyond the purposes alluded to in the previous description, EPANET is used for a variety of other applications, including:
# 
# - Water Quality Analysis: EPANET allows for water quality modeling by simulating the transport and fate of contaminants within the distribution system. This helps in evaluating water disinfection processes, predicting water age, and identifying potential issues related to water quality such as the formation of disinfection by-products.
# - System Expansion and Rehabilitation: Engineers use EPANET to assess the impact of system expansion or rehabilitation projects, such as adding new pipes, storage tanks, or pumps. The software helps in evaluating the performance of the modified system and ensures that the changes meet the required demands and constraints.
# - Emergency Response Planning: During emergencies or contamination events, EPANET can be used to model the effects of system disruptions, identify areas vulnerable to water quality degradation, and plan for effective response strategies to safeguard public health.
# - Water Loss Management: EPANET aids in managing and reducing water losses in distribution systems due to leaks and other inefficiencies. By simulating the system under different scenarios, engineers can identify areas with high leakage rates and develop strategies to mitigate water losses.
# - Hydraulic Model Calibration: The software is used to calibrate hydraulic models by comparing simulation results with real-world data. Calibration ensures that the model accurately represents the behavior of the actual water distribution system, enhancing its reliability for decision-making.
# - Optimization Studies: EPANET can be employed for optimizing various aspects of water distribution systems, such as pump scheduling, valve operation, and tank storage levels, with the goal of minimizing energy consumption and operational costs while maintaining system performance.
# - Sustainable Design: Engineers use EPANET to support sustainable design practices by evaluating the impact of green infrastructure, rainwater harvesting systems, and other water conservation measures on the overall performance of the distribution network.
# - Water Resource Planning: EPANET can be utilized in water resource planning to assess the availability and distribution of water resources for a given region, taking into account population growth, climate change, and other factors affecting water demand and supply.
# 
# Overall, EPANET is a tool for water utilities, researchers, and policymakers to understand, optimize, and manage water distribution systems in a wide range of scenarios and contexts.
# 
# ### GUI Access
# 
# EPANET as supplied by [https://www.epa.gov/water-research/epanet](https://www.epa.gov/water-research/epanet) also includes a graphical user interface (GUI) that will allow one to quickly build network simulation models, run them, and present results.  The GUI runs on Windows machines using Intel/AMD hardware.  It can be made to run on other operating systems and architectures, but not easily.
# 
# ```{admonition} Architectures and Operating Systems
# The EPANET computation engine can be made to work in different operating systems with very little fuss.  In fact the current OWS versions all employ CMAKE to build targets for the big-three Operating Systems (Windows, Mac, Linux).
# 
# Architecture refers to the underlying silicon; x86-64 is an Intel/AMD 64-bit chipset, aarch64 is the ARM 64-bit chipset.
# 
# At the time of this writing builds for aarch64 are kind of up to the end-user;  I have notes herein on how-to do so.  Why anyone would want to make such a build is to leverage embedded systems with intent to use the program to control things.  I am aware most people are going to be using a Windows machine on Intel hardware and special instructions specific to ARM hardware is meaningless.
# ```
# 
# The EPANET Toolkit used in this notebook was obtained  from [https://github.com/OpenWaterAnalytics](https://github.com/OpenWaterAnalytics) and built on a Raspberry Pi 4 for this book; all the GUI examples use the EPA sourced builds.

# ## Installing EPANET
# Follow the guidelines on the [https://www.epa.gov/water-research/epanet](https://www.epa.gov/water-research/epanet) or watch [https://www.youtube.com/watch?v=HoZC4FPBQzI](https://www.youtube.com/watch?v=HoZC4FPBQzI)
# 
# You can also examine [https://epanet22.readthedocs.io/en/latest/2_quickstart.html](https://epanet22.readthedocs.io/en/latest/2_quickstart.html)
# 
# ## Installing the Toolkit
# 
# A bit more elaborate. You don't need it initially, but will need it in a few sections.  

# ## EPANET On-Line Access
# 
# An on-line version is hosted at [http://freeswmm.ddns.net](http://freeswmm.ddns.net) described herein uses the WINE application layer to run an implementation of EPANET with the "Classic" GUI on a Linux server, on an Intel x86-64 chipset.  
# 
# :::{Note}
# The on-line version is really for the author of this book to demonstrate EPANET but also allow workshop participants to also use the environment.  End users are far better off using their own hardware, but the shared space is a reasonable training option - host to workstation file transfer is via a JupyterHub instance on the FreeSWMM host (user is **antares**; password is **freeswmm**) which I will demonstrate in-class.
# :::
# 
# ## Accessing the FreeSWMM host
# 
# To access the FreeSWMM site use the link: [FreeSWMM (via NoVNC)](http://freeswmm.ddns.net:6082/vnc.html?host=freeswmm.ddns.net&port=6082) you will encounter the NoVNC interface pictured below:
# 
# :::{note}
# > Alternate entry using the assigned public IP:<br>
# > [User](http://18.210.253.169:6082/vnc.html?host=18.210.253.169&port=6082)<br>
# > VNC Services (Run as root or sudo)<br>
# > sudo snap set novnc services.n6081.listen=6081 services.n6081.vnc=localhost:5901<br>
# > sudo snap set novnc services.n6082.listen=6082 services.n6082.vnc=localhost:5902<br>
# :::
# 
# ![](novnc.png)
# 
# When you when you click on "Connect" you will encounter a simple password challenge as pictured below:
# 
# :::{note}
# You may get a red warning bar across the top telling you the access is unsecure, but it will still work, just ignore the warning and proceede as shown below. The warning arises because the the server uses a self-signed certificate instead of certificate from a recoginized certificating authority and most corporate networks will not allow TLS handshake to complete (so end user cannot really access anything).  
# 
# In most cases you will also observe a security warning that obscures the password dialog, simply click on some part of the dialog to background the warning and proceede.
# :::
# 
# ![](challenge.png)
# 
# ```{admonition} Send the Password
# Enter the password **freeswmm** and select "SEND CREDENTIALS" 
# ```
# 
# Upon sucessful connection you will be attached to an XFCE desktop on the remote server as pictured below:
# 
# ![](xfcedesktop.png)
# 
# To start EPANET navigate to the WINE application and select EPANET2 to launch the interface, as pictured below:
# 
# ![](epanet2w.png)
# 
# When EPANET starts you should be presented with a clean interface as pictured below:
# 
# ![](epanet2go.png)
# 
# :::{note}
# EPANET is running in the WINE application layer on a linux server, it is similar to windows in terms of file management, resizing and moving the window showing EPANET is accomplished by right-click in the application tab in the upper part of the web interface; otherwise it is ordinary EPANET as one would experience on a Windows computer
# :::

# ## Running Existing Examples
# 
# The existing examples are all stored in the EPANET-Files Directory on the XFCE desktop (as well as some pre-installed examples).  As new examples are added they will be located in that directory.  
# 
# ![](epanet-ex1.png)

# ## Moving files to/from the host
# 
# :::{warning}
# Moving files to/from the remote server is non-trivial.
# :::
# 
# File upload/download is by a JupyterHub instance running on the host.  On your computer access the JupyterHub server at [http://freeswmm.ddns.net:8000](http://freeswmm.ddns.net:8000) you should get a login window unless someone else is connected (or left a running instance) that looks like:
# 
# ![](antaresfreeswmm.png)
# 
# Enter the credentials from above and you will get a JupyterHub interface like below (it may take awhile to load)
# 
# ![](antaresjhub.png)
# 
# The EPANET files are located in `/Desktop/EPANET-Files` and to upload drag and drop from your computer to this directory (or a subdirectory).  A screen capture is below:
# 
# ![](jhepanetfiles.png)
# 
# To download, navigate to the target file in the JupyterHub, then select the file, right-click and download.
# 
# :::{note}
# I will demonstrate in class, its easy to accomplish, but also easy to confuse yourself as you have two entirely different browser windows accessing the same location. After the demonstration it will be obvious.
# :::
# 
# When you are done, simply choose log-out from the JupyterHub menu (File Tab), or just close the browser window.

# ## Exiting FreeSWMM
# 
# When you are done using the application, save your work then exit EPANET in the usual fashion. 
# 
# ![](endepanet.png)
# 
# Then select disconnect to close the web interface as pictured below:
# 
# ![](disconnect.png)
# 
# :::{warning}
# Failure to exit EPANET before disconnecting will frequently stall the server.  It won't hurt anything, but is not end user fixable.
# :::
# 
# :::{note}
# The server is programmed to disconnect every hour and restart one minute later; if you are in the middle of something your work should be preserved, just wait the minute and reconnect.  This annoying behavior is to mitigate loss of CPU allocation on AWS because of an idle XFCE window being left open.   Please remember to disconnect your sessions, there are only about 2.4 hours/day of computation time available and the connection itself uses a fair portion of that allocation.
# :::
# 
# The next section (of this notebook) works the examples in the document below.

# ## References
# 
# 1. [https://github.com/OpenWaterAnalytics](https://github.com/OpenWaterAnalytics) Open Water Analytics Github Landing Page
# 
# 2. [http://wateranalytics.org/EPANET/](http://wateranalytics.org/EPANET/) Open Water Analytics (.org) landing page.
# 
# 3. [https://www.epa.gov/water-research/epanet](https://www.epa.gov/water-research/epanet) EPANET landing page.
# 
# 4. [https://epanet-python-toolkit-epyt.readthedocs.io/en/latest/index.html](https://epanet-python-toolkit-epyt.readthedocs.io/en/latest/index.html) EPANET python toolkit (looks like a work-in-progress)
# 
# 5. [https://epanet-matlab-toolkit.readthedocs.io/en/latest/](https://epanet-matlab-toolkit.readthedocs.io/en/latest/) EPANET MatLab toolkit (looks like a work-in-progress; further along than above)
# 
# 6. [https://wntr.readthedocs.io/en/stable/overview.html](https://wntr.readthedocs.io/en/stable/overview.html) EPANET Water Network Tool for Resilience (WNTR) python toolkit extensions. <hr>
# 
# 7. [Cleveland, T.G., Tay, C.C., and Neale, C.M. (2015) EPANET by Example. Department of Civil and Environmental Engineering, Texas Tech University. (original publication)](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/readings/EPANETbyExampleV1.pdf)
# 
# 8. [Cleveland, T.G., and Neale, C.M., and Tay, C.C. (2018) EPANET by Example. Department of Civil and Environmental Engineering, Texas Tech University. (restored publication)](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/readings/enbyexample/enbyexample.pdf)  same as above, but different cover graphic.  The files to build the document are contained in the [hosting directory](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/readings/enbyexample/)
# 
# 
# ## Exercise
# 
# Examine the last two document(s) above familarize yourself with the examples, these are worked in the next section using the On-Line EPANET implementation.  The files are pre-placed in those examples. 

# 

# In[ ]:




