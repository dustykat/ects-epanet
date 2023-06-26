#!/usr/bin/env python
# coding: utf-8

# # 2.3 Extended period simulation (EPS)
# 
# ## Purpose
# EPS is a representation is used to mimic dynamic behavior in a system.  Not strictly transient, but changes are tracked to approximate filling/draining of tanks and discharge moving along a pump curve.  EPS is also the fundamental concept needed to allow for water quality simulations in EPANET.
# 
# ### Background
# 
# Quoting from [Bhave, P. R. (1988)](http://freeswmm.ddns.net/ects-epanet/ects-epanet-notes/lessons/readings/(ASCE)0733-9372(1988)114-5(1146).pdf)
# 
# >The common practice  of analyzing  flow  in water-distribution  systems  is to model the flow to be in a steady-state condition. This is "static  analysis."  However,  neither  the nodal demands nor the reservoir water levels  remain  constant  over  a period  of time.  To  ensure  an  adequate  level  of  service  to  the  consumers  under  varying  conditions  of  demands  and  reservoir  water  levels, proper  operation  of the  distribution  system  is  necessary.  From  an  operational  point  of  view,  it  is necessary  to  adequately  maintain  the  flow  rates  and pressures  (residual  heads) at  all nodes  at various times; it  is also necessary  to  manage  the  storage  to  balance  the  supply  and  distribution.  These  objectives   can  be  achieved  by  carrying  out  the  analysis  of  the  network  over  a  period  of  24-48  hr  under  varying  nodal  demands  and  reservoir  water  levels.  Such  an  analysis  of  the  distribution  system  is  an  **extended  period  simulation**  or  simply  a  "dynamic  analysis." 
# 
# ## Examples
# 
# ## References
# 
# 1. [Bhave, P. R. (1988)"Extended Period Simulation of Water Systems—Direct Solution." Journal of Environmental Engineering Vol. 114, No. 5, pp.1146-1159 (doi:10.1061/(ASCE)0733-9372(1988)114:5(1146))](https://ascelibrary.org/doi/epdf/10.1061/%28ASCE%290733-9372%281988%29114%3A5%281146%29)  

# In[ ]:




