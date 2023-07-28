#!/usr/bin/env python
# coding: utf-8

# # 1.4 Hydraulics in Python
# 
# ## Purpose
# 
# This section introduces multi-variate Newton's Methods for solving well behaved non-linear systems.  A key feature of pipeline networks is that the Jacobian is relatively easy to construct and is essentially analytical.  To generalize the method one would have to employ numerical derivatives to construct the Jacobian matrix at each step - that's for readers to learn elsewhere.
# 
# The method herein is appliciable to hydraulics network simulation, albeit somewhat crude, it is a reasonable approximation of the method employed in EPANET and similar computation engines.

# ## Method and Scripts
# A script (program) will need to accomplish several tasks including reading the node-arc incidence matrix supplied as a file and convert the strings into numeric values.  The script will also need some support functions defined before constructing the matrix. 
# 
# First the file for the example is:
# 
# > PipeNetworkExample1.txt
# ```
# 4
# 6
# 200.0 200.0 200.0 200.0 
# 1.00 0.67 0.67 0.67 0.67 0.5
# 800 800 700 700 800 600
# 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001
# 0.000011
# 1 1 1 1 1 1
# 1 -1 0 -1 0 0
# 0 1 -1 0 0 1
# 0 0 0 1 -1 -1
# 0 0 1 0 1 0
# 0 4 3 1 -300 0 0 0 0 0 
# ```
# 
# The rows of the input file are:
# - The node count, in this case 4.
# - The link (pipe) count, in this case 6.
# - Node elevations, in feet (units can be changed as needed).
# - Pipe diameters, in feet.
# - Pipe lengths, in feet.
# - Pipe roughness heights, in feet.
# - Kinematic viscosity in feet$^2$/second.
# - An initial guess of flow rates (unbalanced OK, non-zero vital!), in this case 1 everywhere.
# - The next four rows are the node-arc incidence matrix.
# - The last row is the RHS demand (and fixed-grade node total head) vector.
# 
# The script below will generate the file.

# In[1]:


# A simple script to generate PipeNetworkExample1.txt
data = """4
6
200.0 200.0 200.0 200.0 
1.00 0.67 0.67 0.67 0.67 0.5
800 800 700 700 800 600
0.00001 0.00001 0.00001 0.00001 0.00001 0.00001
0.000011
1 1 1 1 1 1
1 -1 0 -1 0 0
0 1 -1 0 0 1
0 0 0 1 -1 -1
0 0 1 0 1 0
0 4 3 1 -300 0 0 0 0 0"""

with open("PipeNetworkExample1.txt", "w") as file:
    file.write(data)
file.close()


# ### Support Functions
# 
# The Reynolds number will need to be calculated for each pipe at each iteration of the solution, so a Reynolds number function will be useful.  For circular pipes, the following equation should work,
# 
# $Re_D=\frac{V_i \cdot D_i }{\mu}$
# 
# 
# The Jain equation (Jain, 1976) that directly computes friction factor from Reynolds number, diameter, and roughness is 
# 
# $f= \frac{0.25}{(log_{10}(\frac{\epsilon}{3.7D}+\frac{5.74}{Re_D^{0.9}}))^2}$
# 
# :::{note}
# This friction factor function could be changed to the unified model of friction in [Pomerenk, et al. (2023)](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/hydrodynamics-of-finitelength-pipes-at-intermediate-reynolds-numbers/D7BBD977E0A615A3194E664D8752E1CB), likely involving additional support functions; the general idea is the same.
# :::
# 
# Once you have the Reynolds number for a pipe, and the friction factor, then the head loss factor that will be used in the coefficient matrix (and the Jacobian) is 
# 
# $k_i = \frac{8 \cdot L_i}{\pi^2 g  D_i^5}$
# 
# We will also find it handy to be able to compute velocity heads from discharge and pipe diameters so we can have a velocity function as
# 
# $V_i = \frac{Q_i}{0.25 \cdot \pi D_i^2}$
# 
# 
# Scripts for these support functions are listed below:

# In[2]:


# hydraulic elements prototype functions
# Jain Friction Factor Function -- Tested OK 23SEP16
import math   # This will import math module

def friction_factor(roughness,diameter,reynolds):
    temp1 = roughness/(3.7*diameter)
    temp2 = 5.74/(reynolds**(0.9))
    temp3 = math.log10(temp1+temp2)
    temp3 = temp3**2
    friction_factor = 0.25/temp3
    return(friction_factor)

# Velocity Function
def velocity(diameter,discharge):
    velocity=discharge/(0.25*math.pi*diameter**2)
    return(velocity)

# Reynolds Number Function  
def reynolds_number(velocity,diameter,mu):
    reynolds_number = abs(velocity)*diameter/mu
    return(reynolds_number)

# Geometric factor function
def k_factor(howlong,diameter,gravity):
    k_factor = (16*howlong)/(2.0*gravity*math.pi**2*diameter**5)
    return(k_factor)


# We will need a linear solver, we can write our own or use **numpy** and employ the linear algebra package that is part of **numpy** and the function below is completely replaced by that function; additionally the reading and writing of files is considerably simplified, and the vector-matrix multiplication functions (next code block) are not necessary (numpy has such arithmetic already defined).  The remainder is essentially unchanged.  The script below however works using just python core (and math.pi).

# In[3]:


# SolveLinearSystem.py
# Solve Ax = b for x by Gaussian elimination with back substitution.
# Method returns solution as a list
# Method preserves A
##########
def linearsolver(A,b):
    n = len(A)
#    M = A  #this is object to object equivalence
# copy A into M element by element - to operate on M without destroying A
    M=[[0.0 for jcol in range(n)]for irow in range(n)]
    for irow in range(n):
        for jcol in range(n):
            M[irow][jcol]=A[irow][jcol]

#
    i = 0
    for x in M:
     x.append(b[i])
     i += 1

    for k in range(n):
     for i in range(k,n):
       if abs(M[i][k]) > abs(M[k][k]):
          M[k], M[i] = M[i],M[k]
       else:
          pass

     for j in range(k+1,n):
         q = float(M[j][k]) / M[k][k]
         for m in range(k, n+1):
            M[j][m] -=  q * M[k][m]

    x = [0 for i in range(n)]

    x[n-1] =float(M[n-1][n])/M[n-1][n-1]
    for i in range (n-1,-1,-1):
      z = 0
      for j in range(i+1,n):
          z = z  + float(M[i][j])*x[j]
      x[i] = float(M[i][n] - z)/M[i][i]
#    print (x)
    return(x)
#


# We will also find some vector-matrix manipulation functions handy

# In[4]:


def writeM(M,ir,jc,label):
    print ("------",label,"------")
    for i in range(0,ir,1):
        print (M[i][0:jc])
    print ("-----------------------------")
    return()

def writeV(V,ir,label):
    print ("------",label,"------")
    for i in range(0,ir,1):
        print (V[i])
    print ("-----------------------------")
    return()

def matrixmatrixmult(amatrix,bmatrix,rowNumA,colNumA,rowNumB,colNumB):
    AB =[[0.0 for j in range(colNumB)] for i in range(rowNumA)]
    for i in range(0,rowNumA):
        for j in range(0,colNumB):
            for k in range(0,colNumA):
                AB[i][j]=AB[i][j]+amatrix[i][k]*bmatrix[k][j]
    return(AB)

def matrixvectormult(amatrix,xvector,rowNumA,colNumA):
    bvector=[0.0 for i in range(rowNumA)]
    for i in range(0,rowNumA):
        for j in range(0,1):
            for k in range(0,colNumA):
                bvector[i]=bvector[i]+amatrix[i][k]*xvector[k]
    return(bvector)

def vectoradd(avector,bvector,length):
    cvector=[]
    for i in range(length):
        cvector.append(avector[i]+bvector[i])
    return(cvector)

def vectorsub(avector,bvector,length):
    cvector=[]
    for i in range(length):
        cvector.append(avector[i]-bvector[i])
    return(cvector)
             
def vdotv(avector,bvector,length):
    adotb=0.0
    for i in range(length):
        adotb=adotb+avector[i]*bvector[i]
    return(adotb)


# ### Augmented and Jacobian Matrices
# The $\textbf{A(x)}$ matrix (Section 1.2) is built using the node-arc incidence matrix (which does not change), and the current values of $L_i$.   
# We also need to build the Jacobian of $\textbf{A(x)}$ to implement the update as-per Newton-Raphson.
# 
# ## Newton-Raphson Method
# 
# Assume we have the solution vector, then the following would be anticipated:
# 
# $\begin{equation}
# [\mathbf{A}(\mathbf{x})] \cdot \mathbf{x} - \mathbf{b} = \mathbf{f}(\mathbf{x}) = \mathbf{0}
# \end{equation}
# $
# 
# Lets assume we are not at the solution, so we need a way to update the current value of $\textbf{x}$.
# Recall from Newton's method (for univariate cases) that the update formula is
# 
# $
# \begin{equation}
# x_{k+1}=x_{k} - (\frac{df}{dx}\mid_{x_k})^{-1} f(x_k)
# \end{equation}
# $
# 
# The Jacobian will play the role of the derivative, and $\textbf{x}$ is now a vector (instead of a single variable).
# Division is not defined for matrices, but the multiplicative inverse is (the inverse matrix), and plays the role of division.
# Hence, the extension to the pipeline case is
# 
# $
# \begin{equation}
# \mathbf{x}_{k+1}=\mathbf{x}_{k} - [\mathbf{J}(\mathbf{x}_{k})]^{-1} \mathbf{f}(\mathbf{x}_k) 
# \end{equation}
# $
# 
# where $\mathbf{J}(\mathbf{x}_{k})$ is the Jacobian of the coefficient matrix $\mathbf{A}$ evaluated at $\mathbf{x}_{k}$.   
# Although a bit cluttered, here is the formula for a single update step, with the matrix, demand vector, and the solution vector in their proper places.
# 
# $
# \begin{equation}
# \mathbf{x}_{k+1}=\mathbf{x}_{k} - [\mathbf{J}(\mathbf{x}_{k})]^{-1} \{[\mathbf{A}(\mathbf{x}_k)] \cdot \mathbf{x}_k - \mathbf{b}\}
# \end{equation}
# $
# 
# As a practical matter we actually never invert the Jacobian, instead we solve the related Linear system of 
# 
# $
# [\mathbf{J}(\mathbf{x}_{k})] \cdot \Delta \mathbf{x} = \{[\mathbf{A}(\mathbf{x}_k)] \cdot \mathbf{x}_k - \mathbf{b}\}
# $
# 
# for $\Delta\textbf{x}$, then perform the update as $\textbf{x}_{k+1} = \textbf{x}_{k} - \Delta\textbf{x}$
# 
# :::{note}
# Inverting the matrix every step is computationally inefficient, and unnecessary.  As an example, solving the system in this case would at worst take 10 row operations each step, but nearly 100 row operations to invert at each step -- to accomplish the same result, generate an update.  Now imagine when there are hundreds of nodes and pipes!
# :::
# 
# The Jacobian of the pipe network model is itself a matrix with the following properties:
# - The partition of the matrix that corresponds to the node formulas (upper left partition) is identical to the original coefficient matrix --- it will be comprised of $0~\text{or}~\pm~1$ in the same pattern at the equivalent partition of the $\mathbf{A}$ matrix.
# - The partition of the matrix that corresponds to the pipe head loss terms (lower left partition), will consist of values that are twice the values of the coefficients in the original coefficient matrix (at any supplied value of $\mathbf{x}_k$.
# - The partition of the matrix that corresponds to the head terms (lower right partition), will consist of values that are identical to the original matrix. 
# - The partition of the matrix that corresponds to the head coefficients in the node equations (upper right partition) will also remain unchanged.
# 
# We will want to take advantage of problem structure to build the Jacobian (you could just finite-difference the coefficient matrix to approximate the partial derivatives, but that is terribly inefficient if you already know the Jacobian structure).
# 
# Now lets complete our scripting; First allocate some memory

# In[5]:


bvector = []
rowNumA = 0
colNumA = 0
rowNumB = 0
verbose = 'false' # set to true for in-class demonstration
#############################################

elevation = [] # null list node elevations
diameter =  [] # null list pipe diameters
distance =  [] # null list pipe lengths
roughness = [] # null list pipe roughness
flowguess = [] # null list pipe flow rates
nodearcs =  [] # node-arc incidence matrix
rhs_true =  [] # null list for nodal demands
tempvect = [] # null list for reading from external file, then recasting into one of the above lists


# Now read in the data from a file (useful to expand problem scale to many,many pipes and nodes).

# In[6]:


##############################################
# connect and read file for Pipeline Network #
##############################################
afile = open("PipeNetworkExample1.txt","r")
nnodes = int(afile.readline())
npipes = int(afile.readline())
# read elevation vector
tempvect.append([float(n) for n in afile.readline().strip().split()])
for i in range(0,nnodes,1):
    elevation.append(float(tempvect[0][i]))
tempvect = [] # reset vector
# read diameter vector
tempvect.append([float(n) for n in afile.readline().strip().split()])
for i in range(0,npipes,1):
    diameter.append(float(tempvect[0][i]))
tempvect = [] # reset vector
# read length vector
tempvect.append([float(n) for n in afile.readline().strip().split()])
for i in range(0,npipes,1):
    distance.append(float(tempvect[0][i]))
tempvect = [] # reset vector
# read roughness vector
tempvect.append([float(n) for n in afile.readline().strip().split()])
for i in range(0,npipes,1):
    roughness.append(float(tempvect[0][i]))
tempvect = [] # reset vector
# read viscosity (scalar)
viscosity = float(afile.readline())
# read current flow guess
tempvect.append([float(n) for n in afile.readline().strip().split()])
for i in range(0,npipes,1):
    flowguess.append(float(tempvect[0][i]))
tempvect = [] # reset vector
# read nodearc incidence matrix
## future revisions read directly into augmented matrix, or find way to release nodearc from stack
for irow in range(0,nnodes,1):  # then read each row
    nodearcs.append([float(n) for n in afile.readline().strip().split()])
# read demands guess
tempvect.append([float(n) for n in afile.readline().strip().split()])
for i in range(0,nnodes+npipes,1):
    rhs_true.append(float(tempvect[0][i]))
tempvect = [] # reset vector      
######################################
# end file read ,disconnect file     #
######################################
afile.close() # Disconnect the file


# Echo the data just read, could put into a conditional and choose not to display except for debugging.  The output is kind of crude, but with some formatting decoration could be made nicely lined up.

# In[7]:


######################################
# echo the input in human readable   #
######################################
print('number of nodes : ',nnodes)
print('number of pipes : ',npipes)
print('viscosity       : ',viscosity)
print ("-----------------------------")
for irow in range(0,nnodes):
    print('node id:',irow, ', elevation :',elevation[irow],' head :',rhs_true[irow+npipes])
print ("-----------------------------")
for jcol in range(0,npipes):
    print('pipe id:',jcol,', diameter : ' ,diameter[jcol],', distance : ',distance[jcol],
          ', roughness : ',roughness[jcol],', flow  : ',flowguess[jcol])
print ("-----------------------------")
##for jcol in range(0,nnodes+npipes):
##    print('irow :',jcol,' RHS True :',rhs_true[jcol])
##print ("-----------------------------")
print("node-arc incidence matrix")
for i in range(0,nnodes,1):
    print (nodearcs[i][0:npipes])
print ("-----------------------------")


# Now create the augmented matrix using known Jacobian structure for pipe networks.

# In[8]:


# create augmented matrix
colNumA = npipes+nnodes
rowNumA = nnodes+npipes
augmentedMat = [] # null list to store augmented matrix

#######################################################################################
augmentedMat = [[0.0 for j in range(colNumA)]for i in range(rowNumA)] #fill with zeroes
#build upper left partition -- from nodearcs
for ir in range(0,nnodes):
    for jc in range (0,npipes):
        augmentedMat[ir][jc] = nodearcs[ir][jc]
istart=nnodes
iend=nnodes+npipes
jstart=npipes
jend=npipes+nnodes
for ir in range(istart,iend):
    for jc in range (jstart,jend):
        augmentedMat[ir][jc] = -1.0*nodearcs[jc-jstart][ir-istart] + 0.0
if verbose == 'true' :
    print("augmented matrix before loss factors")
    writeM(augmentedMat,rowNumA,colNumA,"augmented matrix")


# ### Stopping Criteria, and Solution Report:
# 
# You will need some way to stop the process -- the three most obvious (borrowed from Newton's method) are:
# 
# - Approaching the correct solution (e.g. $[\mathbf{A}(\mathbf{x})] \cdot \mathbf{x} - \mathbf{b} = \mathbf{f}(\mathbf{x}) = \mathbf{0}$).
# - Update vector is not changing (e.g. $\mathbf{x}_{k+1}=\mathbf{x}_{k}$), so either have an answer, or the algorithm is stuck.
# - You have done a lot of iterations (say 100).
# 
# We want to have the script determine when to stop and report the conditions (which stopping criterion was used), and the values of flows and heads in the system.
# 
# Fisrt lets set some tolerances and an iteration limit, as well as allocate memory to store the auxiliary functions results

# In[9]:


#######################################################################################
howmany=50 #iterations max
tolerance1 = 1e-24
tolerance2 = 1e-24
velocity_pipe = [0 for i in range(npipes)]  # null list velocities
reynolds      = [0 for i in range(npipes)]  # null list reynolds numbers
friction      = [0 for i in range(npipes)]  # null list friction 
geometry      = [0 for i in range(npipes)]  # null list geometry
lossfactor    = [0 for i in range(npipes)]  # null list loss
jacbMat = [] # null list to store jacobian matrix
jacbMat = [[0.0 for j in range(colNumA)]for i in range(rowNumA)] #fill with zeroes


solvecguess =[ 0.0 for i in range(rowNumA)] 
solvecnew =[ 0.0 for i in range(rowNumA)]
for i in range(0,npipes,1):
    solvecguess[i] = flowguess[i]
    geometry[i] = k_factor(distance[i],diameter[i],32.2)
#solvecguess is a current guess -- wonder if more pythonic way for this assignment
##    print('irow :',i,' Geometry Factor :',geometry[i])
##print ("-----------------------------")


# And finally the money shot; where we wrap everything into a for loop to iteratively find a solution

# In[10]:


###############################################################
## ITERATION LOOP                                             #
###############################################################
for iteration in range(howmany): # iteration outer loop
    if verbose == 'true' :
        print("solutions at begin of iteration",iteration)
        for jcol in range(0,nnodes+npipes):
            print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
        print ("-----------------------------")
    for i in range(0,npipes,1):
        velocity_pipe[i] = velocity(diameter[i],flowguess[i])    
        reynolds[i]=reynolds_number(velocity_pipe[i],diameter[i],viscosity)
        friction[i]=friction_factor(roughness[i],diameter[i],reynolds[i])
        lossfactor[i]=friction[i]*geometry[i]*abs(flowguess[i])
    if verbose == 'true' :
        for jcol in range(0,npipes):
            print('pipe id:',jcol,', velocity : ' ,velocity_pipe[jcol],', reynolds : ',reynolds[jcol],
          ', friction : ',friction[jcol],', loss factor : ',lossfactor[jcol],'flow guess',flowguess[jcol])
################################################################
# BUILD AUGMENTED MATRIX CURRENT Q+H SOLUTION                  #
################################################################
    augmentedMat = [[0.0 for j in range(colNumA)]for i in range(rowNumA)] #fill with zeroes
    #build upper left partition -- from nodearcs
    for ir in range(0,nnodes):
        for jc in range (0,npipes):
            augmentedMat[ir][jc] = nodearcs[ir][jc]
    #build lower right == transpose of upper left
    istart=nnodes
    iend=nnodes+npipes
    jstart=npipes
    jend=npipes+nnodes
    for ir in range(istart,iend):
        for jc in range (jstart,jend):
            augmentedMat[ir][jc] = -1.0*nodearcs[jc-jstart][ir-istart] + 0.0
    # build lower left partition of the matrix
    istart = nnodes
    iend = nnodes+npipes
    jstart = 0
    jend = npipes
    for i in range(istart,iend ):
        for j in range(jstart,jend ):
    #        print('i =',i,'j=',j)
            if (i-istart) == j :
    #            print('i =',i,'j=',j)
                augmentedMat[i][j] = -1.0*lossfactor[j] + 0.0
    if verbose == 'true' :
        print("updated augmented matrix in iteration",iteration)
        writeM(augmentedMat,rowNumA,colNumA,"augmented matrix")
################################################################
# BUILD JACOBIAN MATRIX CURRENT Q+H SOLUTION                   #
################################################################        
    # now build current jacobian
    for i in range(rowNumA):
        for j in range(colNumA):
            jacbMat[i][j] = augmentedMat[i][j]
    # modify lower left partition
    istart = nnodes
    iend = nnodes+npipes
    jstart = 0
    jend = npipes
    for i in range(istart,iend ):
        for j in range(jstart,jend ):
    #        print('i =',i,'j=',j)
            if (i-istart) == j :
    #            print('i =',i,'j=',j)
                jacbMat[i][j] = 2.0*jacbMat[i][j]
##        for jcol in range(0,nnodes+npipes):
##            print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
##        print ("-----------------------------")
# matrix multiply augmentedMat*solvecguess to get current g(Q)
#    gq = [0.0 for i in range(rowNumA)] # zero gradient vector
##    if verbose == 'true' :
##        print("augmented matrix in iteration",iteration)
##        writeM(augmentedMat,rowNumA,colNumA,"augmented matrix before mmult")
    gq = matrixvectormult(augmentedMat,solvecguess,rowNumA,colNumA)
##    if verbose == 'true' :
##        writeV(gq,rowNumA,"gq vectorbefore subtract rhs_true")
# subtract rhs
#    for i in range(rowNumA):
    gq = vectorsub(gq,rhs_true,rowNumA)#vector subtract
    if verbose == 'true' :
        print("computed g(q) in iteration",iteration)
        writeV(gq,rowNumA,"gq vector")
        print("compare current and new guess")
        for jcol in range(0,nnodes+npipes):
            print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
        print ("-----------------------------")
    dq = [0.0 for i in range(rowNumA)] # zero update vector
    if verbose == 'true' :
        writeV(dq,rowNumA,"dq vector before linear solve")
    if verbose == 'true' :
        print("jacobian before linearsolve in iteration",iteration)
        writeM(jacbMat,rowNumA,colNumA,"jabobian matrix")
    dq = linearsolver(jacbMat,gq) # memory leak after this call - linearsolve clobbers input lists
#    dq = numpy.linalg.solve(jacbMat,gq) #the numpy equivalent
    if verbose == 'true' :
        print("jacobian after linearsolve in iteration",iteration)
        writeM(jacbMat,rowNumA,colNumA,"jabobian matrix")

    if verbose == 'true' :
        writeV(dq,rowNumA,"dq vector -after linear solve")
    solvecnew = vectorsub(solvecguess,dq,rowNumA)#vector subtract
    if verbose == 'true' :
        print("Q_new = Q_old - DQ")
        writeV(solvecnew,rowNumA,"new guess vector")
#    tempvect =[ 0.0 for i in range(rowNumA)]
##        tempvect = matrixvectormult(jacbMat,dq,rowNumA,colNumA)
##        writeV(tempvect,rowNumA,"J*dq vector")
##        tempvect = vectorsub(tempvect,gq,rowNumA)
##        writeV(tempvect,rowNumA,"J*dq - gq vector")
        print("just after computing new guess, should be different")
        for jcol in range(0,nnodes+npipes):
            print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
        print ("-----------------------------")
#test for stopping
    tempvect =[ 0.0 for i in range(rowNumA)]
    for i in range(rowNumA):
        tempvect[i] = abs(solvecnew[i] - solvecguess[i])
    test1 = vdotv(tempvect,tempvect,rowNumA)
    if verbose == 'true' :
        print('test1',test1)
    tempvect =[ 0.0 for i in range(rowNumA)]
    for i in range(rowNumA):
        tempvect[i] = abs(gq[i])
    test2 = vdotv(tempvect,tempvect,rowNumA)
    if verbose == 'true' :
        print('test2',test2)
    if test1 < tolerance1 :
        print("update not changing --exit and report current update")
        print("iteration",iteration)
# update guess
        solvecguess[:] = solvecnew[:]
        for i in range(0,npipes,1):
            flowguess[i] = solvecguess[i]

        break
    if test2 < tolerance2 :
        print("gradient near zero --exit and report current update")
        print("iteration",iteration)
# update guess
        solvecguess[:] = solvecnew[:]
        for i in range(0,npipes,1):
            flowguess[i] = solvecguess[i]

        break
    if verbose == 'true' :
        print("solution continuing")
        print("iteration",iteration)
    # update guess
    solvecguess[:] = solvecnew[:]
    if verbose == 'true' :
        for i in range(0,npipes,1):
            flowguess[i] = solvecguess[i]
## Write Current State ######################
        gq = matrixvectormult(augmentedMat,solvecguess,rowNumA,colNumA)
        print('number of nodes : ',nnodes)
        print('number of pipes : ',npipes)
        print('viscosity       : ',viscosity)
        print ("-----------------------------")
        for irow in range(0,nnodes):
            print('node id:',irow, ', elevation :',elevation[irow])
        print ("-----------------------------")
        for jcol in range(0,npipes):
            print('pipe id:',jcol,', diameter : ' ,diameter[jcol],', distance : ',distance[jcol],
          ', roughness : ',roughness[jcol],', flow guess : ',round(flowguess[jcol],3))
        print ("-----------------------------")
        for jcol in range(0,nnodes+npipes):
            print('irow :',jcol,' RHS True :',rhs_true[jcol],"RHS Current",round(gq[jcol],3))
        print ("-----------------------------")
        for jcol in range(0,nnodes+npipes):
            print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
        print ("-----------------------------")   
################################################
# end of outer loop


# Finally write the results and exit the process

# In[11]:


print("results at iteration = :",iteration)
for i in range(0,npipes,1):
    flowguess[i] = solvecguess[i]
print('number of nodes : ',nnodes)
print('number of pipes : ',npipes)
print('viscosity       : ',viscosity)
print ("-----------------------------")
istart = int(npipes)
for irow in range(0,nnodes):
    print('node id:',irow, ', elevation :',elevation[irow],' head :',round(solvecnew[irow+npipes],3))
print ("-----------------------------")
for jcol in range(0,npipes):
    print('pipe id:',jcol,', diameter : ' ,diameter[jcol],', distance : ',distance[jcol],
  ', roughness : ',roughness[jcol],', flow  : ',round(flowguess[jcol],3))
print ("-----------------------------")
if verbose == 'true' :
    for jcol in range(0,nnodes+npipes):
        print('irow :',jcol,' RHS True :',rhs_true[jcol],"RHS Current",gq[jcol])
    print ("-----------------------------")
    for jcol in range(0,nnodes+npipes):
        print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
    print ("-----------------------------")


# **Ta da!** a homebrew network simulator.  Now if we trust our work, we can handle lots of different networks simply by changing the contents of the input file.  EPANET handles this is a similar fashion, in fact the GUI is mostly dedicated to helping build the input file and query the results to produce tabular and graphical outputs.  The underlying computation engine is not a whole lot more complicated than the crude script above.

# ## Example 2:
# 
# This example is a simple modification of the previous example, involving some minor input file content changes, and a bit of trial and error.  It is presented as a typical **homework** type problem one would encounter in a Civil Engineering hydraulics course.
# 
# ### Problem Statement
# 
# {numref}`SimpleNetwork` is a five-pipe network with a water supply source at Node 1, and demands at Nodes 1-4.  The pipe dimensions are shown in  the figure.
# 
# ```{figure} SimpleNetwork.png
# ---
# width: 400px
# name: SimpleNetwork
# ---
# Pipe network for 
# ```
# 
# 1.  Make a table that lists each node name, node elevation, and the resultant pressure in U.S. Customary units.
# 
# 2.  Make a table that lists each pipe name,  length,  diameter,  roughness height, and the resultant flow rate in U.S. Customary units.
# 
# 3.  Determine the flow rate in each pipe of the network, for the case where the total head at Node 1 is 100 feet.
# 
# 4.  Determine the Darcy-Weisbach friction factor in each pipe of the network.
# 
# 5.  Using the results of your flow distribution, determine the head loss from Node 1 to Node 4.
# 
# 6.  Determine the head at Node 4
# 
# 7.  Identify the node with the lowest **pressure** in your solution.
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
# - 4 nodes (plus a 5-th supply node in this example it is node 0)
# - 6 pipes (the supply pipe (red arrow) at node 1 is set as a short  and large diameter pipe)
# 
# ```
# 4
# 6
# ```
# 
# - node elevations
# 
# ```
# 0 0 0 0 0
# ```
# 
# - Pipe diameters
# 
# ```
# 10.00 0.67 0.67 0.67 0.67 0.5
# ```
# 
# - Pipe lengths
# 
# ```
# 10 800 700 700 800 600
# ```
# 
# - Pipe roughness heights (based on material)
# 
# ```
# 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001
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
# 9. The node-arc matrix
# 
# ```
# 1 -1 0 -1 0 0 # node 1 
# 0 1 -1 0 0 1  # node 2
# 0 0 0 1 -1 -1 # node 3
# 0 0 1 0 1 0   # node 4
# ```
# 
# - The right-hand side (demands and node 0 head)
# 
# ```
# 2 4 3 1 -100 0 0 0 0 0 # we will change the node 0 value to get desired pressure at node 1
# ```
# 
# Save this into a file named `PN-E2.txt`
# 
# > PN-E2.txt
# ```
# 4
# 6
# 0.0 0.0 0.0 0.0 
# 10.00 0.67 0.67 0.67 0.67 0.5
# 10 800 700 700 800 600
# 0.00001 0.00001 0.00001 0.00001 0.00001 0.00001
# 0.000011
# 1 1 1 1 1 1
# 1 -1 0 -1 0 0
# 0 1 -1 0 0 1
# 0 0 0 1 -1 -1
# 0 0 1 0 1 0
# 2 4 3 1 -100 0 0 0 0 0 
# 
# ```
# 
# As above, we will include a file generator script to make cut-and-paste easier

# In[12]:


# A simple script to generate PN-E2.txt
data = """4
6
0.0 0.0 0.0 0.0 
10.00 0.67 0.67 0.67 0.67 0.5
10 800 700 700 800 600
0.00001 0.00001 0.00001 0.00001 0.00001 0.00001
0.000011
1 1 1 1 1 1
1 -1 0 -1 0 0
0 1 -1 0 0 1
0 0 0 1 -1 -1
0 0 1 0 1 0
2 4 3 1 -100 0 0 0 0 0"""

with open("PN-E2.txt", "w") as file:
    file.write(data)
file.close()


# ## A `pipenet` function
# 
# To allow for simple changes to input files, turing the entire script into a function is handy.  All we really need is to just indent everything a single tab block, and provide an entry point for input file name and we have a function.  
# 
# For this specific problem we can use trial and error to get total head at Node 1 (Node 0 in the script) to a value of 100 as specified in the problem statement.

# In[13]:


def pipenet(infilename): # pass input file name as a parameter
    
    ########## Initial Memory Allocations ###############
    bvector = []
    rowNumA = 0
    colNumA = 0
    rowNumB = 0
    verbose = 'false' # set to true for in-class demonstration
    #############################################

    elevation = [] # null list node elevations
    diameter =  [] # null list pipe diameters
    distance =  [] # null list pipe lengths
    roughness = [] # null list pipe roughness
    flowguess = [] # null list pipe flow rates
    nodearcs =  [] # node-arc incidence matrix
    rhs_true =  [] # null list for nodal demands
    tempvect = [] # null list for reading from external file, then recasting into one of the above lists

    ##############################################
    # connect and read file for Pipeline Network #
    ##############################################
#    infilename="PN-E2.txt"
    afile = open(infilename,"r")
    #afile = open("PipeNetworkLesson15.txt","r")
    nnodes = int(afile.readline())
    npipes = int(afile.readline())
    # read elevation vector
    tempvect.append([float(n) for n in afile.readline().strip().split()])
    for i in range(0,nnodes,1):
        elevation.append(float(tempvect[0][i]))
    tempvect = [] # reset vector
    # read diameter vector
    tempvect.append([float(n) for n in afile.readline().strip().split()])
    for i in range(0,npipes,1):
        diameter.append(float(tempvect[0][i]))
    tempvect = [] # reset vector
    # read length vector
    tempvect.append([float(n) for n in afile.readline().strip().split()])
    for i in range(0,npipes,1):
        distance.append(float(tempvect[0][i]))
    tempvect = [] # reset vector
    # read roughness vector
    tempvect.append([float(n) for n in afile.readline().strip().split()])
    for i in range(0,npipes,1):
        roughness.append(float(tempvect[0][i]))
    tempvect = [] # reset vector
    # read viscosity (scalar)
    viscosity = float(afile.readline())
    # read current flow guess
    tempvect.append([float(n) for n in afile.readline().strip().split()])
    for i in range(0,npipes,1):
        flowguess.append(float(tempvect[0][i]))
    tempvect = [] # reset vector
    # read nodearc incidence matrix
    ## future revisions read directly into augmented matrix, or find way to release nodearc from stack
    for irow in range(0,nnodes,1):  # then read each row
        nodearcs.append([float(n) for n in afile.readline().strip().split()])
    # read demands guess
    tempvect.append([float(n) for n in afile.readline().strip().split()])
    for i in range(0,nnodes+npipes,1):
        rhs_true.append(float(tempvect[0][i]))
    tempvect = [] # reset vector      
    ######################################
    # end file read ,disconnect file     #
    ######################################
    afile.close() # Disconnect the file

    ######################################
    # echo the input in human readable   #
    ######################################
    print('####ECHO INPUT################\nInput File: ',infilename)
    print('number of nodes : ',nnodes)
    print('number of pipes : ',npipes)
    print('viscosity       : ',viscosity)
    print ("-----------------------------")
    for irow in range(0,nnodes):
        print('node id:',irow, ', elevation :',elevation[irow],' head :',rhs_true[irow+npipes])
    print ("-----------------------------")
    for jcol in range(0,npipes):
        print('pipe id:',jcol,', diameter : ' ,diameter[jcol],', distance : ',distance[jcol],
              ', roughness : ',roughness[jcol],', flow  : ',flowguess[jcol])
    print ("-----------------------------")
    ##for jcol in range(0,nnodes+npipes):
    ##    print('irow :',jcol,' RHS True :',rhs_true[jcol])
    ##print ("-----------------------------")
    print("node-arc incidence matrix")
    for i in range(0,nnodes,1):
        print (nodearcs[i][0:npipes])
    print ("-----------------------------")

    # create augmented matrix
    colNumA = npipes+nnodes
    rowNumA = nnodes+npipes
    augmentedMat = [] # null list to store augmented matrix

    #######################################################################################
    augmentedMat = [[0.0 for j in range(colNumA)]for i in range(rowNumA)] #fill with zeroes
    #build upper left partition -- from nodearcs
    for ir in range(0,nnodes):
        for jc in range (0,npipes):
            augmentedMat[ir][jc] = nodearcs[ir][jc]
    istart=nnodes
    iend=nnodes+npipes
    jstart=npipes
    jend=npipes+nnodes
    for ir in range(istart,iend):
        for jc in range (jstart,jend):
            augmentedMat[ir][jc] = -1.0*nodearcs[jc-jstart][ir-istart] + 0.0
    if verbose == 'true' :
        print("augmented matrix before loss factors")
        writeM(augmentedMat,rowNumA,colNumA,"augmented matrix")

    #########Simulation Constants and Additional Memory Allocation #######
    howmany=50 #iterations max
    tolerance1 = 1e-24
    tolerance2 = 1e-24
    velocity_pipe = [0 for i in range(npipes)]  # null list velocities
    reynolds      = [0 for i in range(npipes)]  # null list reynolds numbers
    friction      = [0 for i in range(npipes)]  # null list friction 
    geometry      = [0 for i in range(npipes)]  # null list geometry
    lossfactor    = [0 for i in range(npipes)]  # null list loss
    jacbMat = [] # null list to store jacobian matrix
    jacbMat = [[0.0 for j in range(colNumA)]for i in range(rowNumA)] #fill with zeroes


    solvecguess =[ 0.0 for i in range(rowNumA)] 
    solvecnew =[ 0.0 for i in range(rowNumA)]
    for i in range(0,npipes,1):
        solvecguess[i] = flowguess[i]
        geometry[i] = k_factor(distance[i],diameter[i],32.2)
    #solvecguess is a current guess -- wonder if more pythonic way for this assignment
    ##    print('irow :',i,' Geometry Factor :',geometry[i])
    ##print ("-----------------------------")

    ###############################################################
    ## ITERATION LOOP                                             #
    ###############################################################
    for iteration in range(howmany): # iteration outer loop
        if verbose == 'true' :
            print("solutions at begin of iteration",iteration)
            for jcol in range(0,nnodes+npipes):
                print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
            print ("-----------------------------")
        for i in range(0,npipes,1):
            velocity_pipe[i] = velocity(diameter[i],flowguess[i])    
            reynolds[i]=reynolds_number(velocity_pipe[i],diameter[i],viscosity)
            friction[i]=friction_factor(roughness[i],diameter[i],reynolds[i])
            lossfactor[i]=friction[i]*geometry[i]*abs(flowguess[i])
        if verbose == 'true' :
            for jcol in range(0,npipes):
                print('pipe id:',jcol,', velocity : ' ,velocity_pipe[jcol],', reynolds : ',reynolds[jcol],
              ', friction : ',friction[jcol],', loss factor : ',lossfactor[jcol],'flow guess',flowguess[jcol])
    ################################################################
    # BUILD AUGMENTED MATRIX CURRENT Q+H SOLUTION                  #
    ################################################################
        augmentedMat = [[0.0 for j in range(colNumA)]for i in range(rowNumA)] #fill with zeroes
        #build upper left partition -- from nodearcs
        for ir in range(0,nnodes):
            for jc in range (0,npipes):
                augmentedMat[ir][jc] = nodearcs[ir][jc]
        #build lower right == transpose of upper left
        istart=nnodes
        iend=nnodes+npipes
        jstart=npipes
        jend=npipes+nnodes
        for ir in range(istart,iend):
            for jc in range (jstart,jend):
                augmentedMat[ir][jc] = -1.0*nodearcs[jc-jstart][ir-istart] + 0.0
        # build lower left partition of the matrix
        istart = nnodes
        iend = nnodes+npipes
        jstart = 0
        jend = npipes
        for i in range(istart,iend ):
            for j in range(jstart,jend ):
        #        print('i =',i,'j=',j)
                if (i-istart) == j :
        #            print('i =',i,'j=',j)
                    augmentedMat[i][j] = -1.0*lossfactor[j] + 0.0
        if verbose == 'true' :
            print("updated augmented matrix in iteration",iteration)
            writeM(augmentedMat,rowNumA,colNumA,"augmented matrix")
    ################################################################
    # BUILD JACOBIAN MATRIX CURRENT Q+H SOLUTION                   #
    ################################################################        
        # now build current jacobian
        for i in range(rowNumA):
            for j in range(colNumA):
                jacbMat[i][j] = augmentedMat[i][j]
        # modify lower left partition
        istart = nnodes
        iend = nnodes+npipes
        jstart = 0
        jend = npipes
        for i in range(istart,iend ):
            for j in range(jstart,jend ):
        #        print('i =',i,'j=',j)
                if (i-istart) == j :
        #            print('i =',i,'j=',j)
                    jacbMat[i][j] = 2.0*jacbMat[i][j]
    ##        for jcol in range(0,nnodes+npipes):
    ##            print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
    ##        print ("-----------------------------")
    # matrix multiply augmentedMat*solvecguess to get current g(Q)
    #    gq = [0.0 for i in range(rowNumA)] # zero gradient vector
    ##    if verbose == 'true' :
    ##        print("augmented matrix in iteration",iteration)
    ##        writeM(augmentedMat,rowNumA,colNumA,"augmented matrix before mmult")
        gq = matrixvectormult(augmentedMat,solvecguess,rowNumA,colNumA)
    ##    if verbose == 'true' :
    ##        writeV(gq,rowNumA,"gq vectorbefore subtract rhs_true")
    # subtract rhs
    #    for i in range(rowNumA):
        gq = vectorsub(gq,rhs_true,rowNumA)#vector subtract
        if verbose == 'true' :
            print("computed g(q) in iteration",iteration)
            writeV(gq,rowNumA,"gq vector")
            print("compare current and new guess")
            for jcol in range(0,nnodes+npipes):
                print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
            print ("-----------------------------")
        dq = [0.0 for i in range(rowNumA)] # zero update vector
        if verbose == 'true' :
            writeV(dq,rowNumA,"dq vector before linear solve")
        if verbose == 'true' :
            print("jacobian before linearsolve in iteration",iteration)
            writeM(jacbMat,rowNumA,colNumA,"jabobian matrix")
        dq = linearsolver(jacbMat,gq) # memory leak after this call - linearsolve clobbers input lists
    #    dq = numpy.linalg.solve(jacbMat,gq) #the numpy equivalent
        if verbose == 'true' :
            print("jacobian after linearsolve in iteration",iteration)
            writeM(jacbMat,rowNumA,colNumA,"jabobian matrix")

        if verbose == 'true' :
            writeV(dq,rowNumA,"dq vector -after linear solve")
        solvecnew = vectorsub(solvecguess,dq,rowNumA)#vector subtract
        if verbose == 'true' :
            print("Q_new = Q_old - DQ")
            writeV(solvecnew,rowNumA,"new guess vector")
    #    tempvect =[ 0.0 for i in range(rowNumA)]
    ##        tempvect = matrixvectormult(jacbMat,dq,rowNumA,colNumA)
    ##        writeV(tempvect,rowNumA,"J*dq vector")
    ##        tempvect = vectorsub(tempvect,gq,rowNumA)
    ##        writeV(tempvect,rowNumA,"J*dq - gq vector")
            print("just after computing new guess, should be different")
            for jcol in range(0,nnodes+npipes):
                print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
            print ("-----------------------------")
    #test for stopping
        tempvect =[ 0.0 for i in range(rowNumA)]
        for i in range(rowNumA):
            tempvect[i] = abs(solvecnew[i] - solvecguess[i])
        test1 = vdotv(tempvect,tempvect,rowNumA)
        if verbose == 'true' :
            print('test1',test1)
        tempvect =[ 0.0 for i in range(rowNumA)]
        for i in range(rowNumA):
            tempvect[i] = abs(gq[i])
        test2 = vdotv(tempvect,tempvect,rowNumA)
        if verbose == 'true' :
            print('test2',test2)
        if test1 < tolerance1 :
            print("###EXIT TYPE###\nUpdate not changing --exit and report current update")
            print("iteration",iteration)
    # update guess
            solvecguess[:] = solvecnew[:]
            for i in range(0,npipes,1):
                flowguess[i] = solvecguess[i]

            break
        if test2 < tolerance2 :
            print("###EXIT TYPE###\nGradient near zero --exit and report current update")
            print("iteration",iteration)
    # update guess
            solvecguess[:] = solvecnew[:]
            for i in range(0,npipes,1):
                flowguess[i] = solvecguess[i]

            break
        if verbose == 'true' :
            print("solution continuing")
            print("iteration",iteration)
        # update guess
        solvecguess[:] = solvecnew[:]
        if verbose == 'true' :
            for i in range(0,npipes,1):
                flowguess[i] = solvecguess[i]
    ## Write Current State ######################
            gq = matrixvectormult(augmentedMat,solvecguess,rowNumA,colNumA)
            print('number of nodes : ',nnodes)
            print('number of pipes : ',npipes)
            print('viscosity       : ',viscosity)
            print ("-----------------------------")
            for irow in range(0,nnodes):
                print('node id:',irow, ', elevation :',elevation[irow])
            print ("-----------------------------")
            for jcol in range(0,npipes):
                print('pipe id:',jcol,', diameter : ' ,diameter[jcol],', distance : ',distance[jcol],
              ', roughness : ',roughness[jcol],', flow guess : ',round(flowguess[jcol],3))
            print ("-----------------------------")
            for jcol in range(0,nnodes+npipes):
                print('irow :',jcol,' RHS True :',rhs_true[jcol],"RHS Current",round(gq[jcol],3))
            print ("-----------------------------")
            for jcol in range(0,nnodes+npipes):
                print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
            print ("-----------------------------")   
    ################################################
    # end of outer loop
    ################################################

# Report Results
    print("#####SIMULATION RESULTS#####\nResults at iteration = :",iteration)
    for i in range(0,npipes,1):
        flowguess[i] = solvecguess[i]
    print('number of nodes : ',nnodes)
    print('number of pipes : ',npipes)
    print('viscosity       : ',viscosity)
    print ("-----------------------------")
    istart = int(npipes)
    for irow in range(0,nnodes):
        print('node id:',irow+1, ', elevation (feet) :',elevation[irow],' head (feet) :',round(solvecnew[irow+npipes],3),' pressure (psi) :', round((14.75/33)*(solvecnew[irow+npipes]-elevation[irow]),3))
    print ("-----------------------------")
    for jcol in range(0,npipes):
        print('pipe id:',jcol+1,', diameter (feet) : ' ,diameter[jcol],', distance (feet) : ',distance[jcol],
      ', friction factor : ',round(friction[jcol],3),', flow (cfs) : ',round(flowguess[jcol],3))
    print ("-----------------------------")
    if verbose == 'true' :
        for jcol in range(0,nnodes+npipes):
            print('irow :',jcol,' RHS True :',rhs_true[jcol],"RHS Current",gq[jcol])
        print ("-----------------------------")
        for jcol in range(0,nnodes+npipes):
            print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
        print ("-----------------------------")


# Now simply call the function with the input file name to run the simulation.

# In[14]:


pipenet('PN-E2.txt')


# Our next step might be to try to make the pipenet function contain all its dependencies within the function. First lets clear the notebook (wipes the workspace)

# In[15]:


# This clears the notebook
get_ipython().run_line_magic('reset', '-f')


# Now a complete function that does everything as above, but entirely self contained.

# In[16]:


def pipenet(infilename): # pass input file name as a parameter
    
    # hydraulic elements prototype functions
    # Jain Friction Factor Function -- Tested OK 23SEP16
    import math   # This will import math module

    def friction_factor(roughness,diameter,reynolds):
        temp1 = roughness/(3.7*diameter)
        temp2 = 5.74/(reynolds**(0.9))
        temp3 = math.log10(temp1+temp2)
        temp3 = temp3**2
        friction_factor = 0.25/temp3
        return(friction_factor)

    # Velocity Function
    def velocity(diameter,discharge):
        velocity=discharge/(0.25*math.pi*diameter**2)
        return(velocity)

    # Reynolds Number Function  
    def reynolds_number(velocity,diameter,mu):
        reynolds_number = abs(velocity)*diameter/mu
        return(reynolds_number)

    # Geometric factor function
    def k_factor(howlong,diameter,gravity):
        k_factor = (16*howlong)/(2.0*gravity*math.pi**2*diameter**5)
        return(k_factor)
    
    # SolveLinearSystem.py
    # Solve Ax = b for x by Gaussian elimination with back substitution.
    # Method returns solution as a list
    # Method preserves A
    ##########
    def linearsolver(A,b):
        n = len(A)
    #    M = A  #this is object to object equivalence
    # copy A into M element by element - to operate on M without destroying A
        M=[[0.0 for jcol in range(n)]for irow in range(n)]
        for irow in range(n):
            for jcol in range(n):
                M[irow][jcol]=A[irow][jcol]

    #
        i = 0
        for x in M:
         x.append(b[i])
         i += 1

        for k in range(n):
         for i in range(k,n):
           if abs(M[i][k]) > abs(M[k][k]):
              M[k], M[i] = M[i],M[k]
           else:
              pass

         for j in range(k+1,n):
             q = float(M[j][k]) / M[k][k]
             for m in range(k, n+1):
                M[j][m] -=  q * M[k][m]

        x = [0 for i in range(n)]

        x[n-1] =float(M[n-1][n])/M[n-1][n-1]
        for i in range (n-1,-1,-1):
          z = 0
          for j in range(i+1,n):
              z = z  + float(M[i][j])*x[j]
          x[i] = float(M[i][n] - z)/M[i][i]
    #    print (x)
        return(x)
    #

    def writeM(M,ir,jc,label):
        print ("------",label,"------")
        for i in range(0,ir,1):
            print (M[i][0:jc])
        print ("-----------------------------")
        return()

    def writeV(V,ir,label):
        print ("------",label,"------")
        for i in range(0,ir,1):
            print (V[i])
        print ("-----------------------------")
        return()

    def matrixmatrixmult(amatrix,bmatrix,rowNumA,colNumA,rowNumB,colNumB):
        AB =[[0.0 for j in range(colNumB)] for i in range(rowNumA)]
        for i in range(0,rowNumA):
            for j in range(0,colNumB):
                for k in range(0,colNumA):
                    AB[i][j]=AB[i][j]+amatrix[i][k]*bmatrix[k][j]
        return(AB)

    def matrixvectormult(amatrix,xvector,rowNumA,colNumA):
        bvector=[0.0 for i in range(rowNumA)]
        for i in range(0,rowNumA):
            for j in range(0,1):
                for k in range(0,colNumA):
                    bvector[i]=bvector[i]+amatrix[i][k]*xvector[k]
        return(bvector)

    def vectoradd(avector,bvector,length):
        cvector=[]
        for i in range(length):
            cvector.append(avector[i]+bvector[i])
        return(cvector)

    def vectorsub(avector,bvector,length):
        cvector=[]
        for i in range(length):
            cvector.append(avector[i]-bvector[i])
        return(cvector)

    def vdotv(avector,bvector,length):
        adotb=0.0
        for i in range(length):
            adotb=adotb+avector[i]*bvector[i]
        return(adotb)
    
    ########## Initial Memory Allocations ###############
    bvector = []
    rowNumA = 0
    colNumA = 0
    rowNumB = 0
    verbose = 'false' # set to true for in-class demonstration
    #############################################

    elevation = [] # null list node elevations
    diameter =  [] # null list pipe diameters
    distance =  [] # null list pipe lengths
    roughness = [] # null list pipe roughness
    flowguess = [] # null list pipe flow rates
    nodearcs =  [] # node-arc incidence matrix
    rhs_true =  [] # null list for nodal demands
    tempvect = [] # null list for reading from external file, then recasting into one of the above lists

    ##############################################
    # connect and read file for Pipeline Network #
    ##############################################
#    infilename="PN-E2.txt"
    afile = open(infilename,"r")
    #afile = open("PipeNetworkLesson15.txt","r")
    nnodes = int(afile.readline())
    npipes = int(afile.readline())
    # read elevation vector
    tempvect.append([float(n) for n in afile.readline().strip().split()])
    for i in range(0,nnodes,1):
        elevation.append(float(tempvect[0][i]))
    tempvect = [] # reset vector
    # read diameter vector
    tempvect.append([float(n) for n in afile.readline().strip().split()])
    for i in range(0,npipes,1):
        diameter.append(float(tempvect[0][i]))
    tempvect = [] # reset vector
    # read length vector
    tempvect.append([float(n) for n in afile.readline().strip().split()])
    for i in range(0,npipes,1):
        distance.append(float(tempvect[0][i]))
    tempvect = [] # reset vector
    # read roughness vector
    tempvect.append([float(n) for n in afile.readline().strip().split()])
    for i in range(0,npipes,1):
        roughness.append(float(tempvect[0][i]))
    tempvect = [] # reset vector
    # read viscosity (scalar)
    viscosity = float(afile.readline())
    # read current flow guess
    tempvect.append([float(n) for n in afile.readline().strip().split()])
    for i in range(0,npipes,1):
        flowguess.append(float(tempvect[0][i]))
    tempvect = [] # reset vector
    # read nodearc incidence matrix
    ## future revisions read directly into augmented matrix, or find way to release nodearc from stack
    for irow in range(0,nnodes,1):  # then read each row
        nodearcs.append([float(n) for n in afile.readline().strip().split()])
    # read demands guess
    tempvect.append([float(n) for n in afile.readline().strip().split()])
    for i in range(0,nnodes+npipes,1):
        rhs_true.append(float(tempvect[0][i]))
    tempvect = [] # reset vector      
    ######################################
    # end file read ,disconnect file     #
    ######################################
    afile.close() # Disconnect the file

    ######################################
    # echo the input in human readable   #
    ######################################
    print('####ECHO INPUT################\nInput File: ',infilename)
    print('number of nodes : ',nnodes)
    print('number of pipes : ',npipes)
    print('viscosity       : ',viscosity)
    print ("-----------------------------")
    for irow in range(0,nnodes):
        print('node id:',irow, ', elevation :',elevation[irow],' head :',rhs_true[irow+npipes])
    print ("-----------------------------")
    for jcol in range(0,npipes):
        print('pipe id:',jcol,', diameter : ' ,diameter[jcol],', distance : ',distance[jcol],
              ', roughness : ',roughness[jcol],', flow  : ',flowguess[jcol])
    print ("-----------------------------")
    ##for jcol in range(0,nnodes+npipes):
    ##    print('irow :',jcol,' RHS True :',rhs_true[jcol])
    ##print ("-----------------------------")
    print("node-arc incidence matrix")
    for i in range(0,nnodes,1):
        print (nodearcs[i][0:npipes])
    print ("-----------------------------")

    # create augmented matrix
    colNumA = npipes+nnodes
    rowNumA = nnodes+npipes
    augmentedMat = [] # null list to store augmented matrix

    #######################################################################################
    augmentedMat = [[0.0 for j in range(colNumA)]for i in range(rowNumA)] #fill with zeroes
    #build upper left partition -- from nodearcs
    for ir in range(0,nnodes):
        for jc in range (0,npipes):
            augmentedMat[ir][jc] = nodearcs[ir][jc]
    istart=nnodes
    iend=nnodes+npipes
    jstart=npipes
    jend=npipes+nnodes
    for ir in range(istart,iend):
        for jc in range (jstart,jend):
            augmentedMat[ir][jc] = -1.0*nodearcs[jc-jstart][ir-istart] + 0.0
    if verbose == 'true' :
        print("augmented matrix before loss factors")
        writeM(augmentedMat,rowNumA,colNumA,"augmented matrix")

    #########Simulation Constants and Additional Memory Allocation #######
    howmany=50 #iterations max
    tolerance1 = 1e-24
    tolerance2 = 1e-24
    velocity_pipe = [0 for i in range(npipes)]  # null list velocities
    reynolds      = [0 for i in range(npipes)]  # null list reynolds numbers
    friction      = [0 for i in range(npipes)]  # null list friction 
    geometry      = [0 for i in range(npipes)]  # null list geometry
    lossfactor    = [0 for i in range(npipes)]  # null list loss
    jacbMat = [] # null list to store jacobian matrix
    jacbMat = [[0.0 for j in range(colNumA)]for i in range(rowNumA)] #fill with zeroes


    solvecguess =[ 0.0 for i in range(rowNumA)] 
    solvecnew =[ 0.0 for i in range(rowNumA)]
    for i in range(0,npipes,1):
        solvecguess[i] = flowguess[i]
        geometry[i] = k_factor(distance[i],diameter[i],32.2)
    #solvecguess is a current guess -- wonder if more pythonic way for this assignment
    ##    print('irow :',i,' Geometry Factor :',geometry[i])
    ##print ("-----------------------------")

    ###############################################################
    ## ITERATION LOOP                                             #
    ###############################################################
    for iteration in range(howmany): # iteration outer loop
        if verbose == 'true' :
            print("solutions at begin of iteration",iteration)
            for jcol in range(0,nnodes+npipes):
                print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
            print ("-----------------------------")
        for i in range(0,npipes,1):
            velocity_pipe[i] = velocity(diameter[i],flowguess[i])    
            reynolds[i]=reynolds_number(velocity_pipe[i],diameter[i],viscosity)
            friction[i]=friction_factor(roughness[i],diameter[i],reynolds[i])
            lossfactor[i]=friction[i]*geometry[i]*abs(flowguess[i])
        if verbose == 'true' :
            for jcol in range(0,npipes):
                print('pipe id:',jcol,', velocity : ' ,velocity_pipe[jcol],', reynolds : ',reynolds[jcol],
              ', friction : ',friction[jcol],', loss factor : ',lossfactor[jcol],'flow guess',flowguess[jcol])
    ################################################################
    # BUILD AUGMENTED MATRIX CURRENT Q+H SOLUTION                  #
    ################################################################
        augmentedMat = [[0.0 for j in range(colNumA)]for i in range(rowNumA)] #fill with zeroes
        #build upper left partition -- from nodearcs
        for ir in range(0,nnodes):
            for jc in range (0,npipes):
                augmentedMat[ir][jc] = nodearcs[ir][jc]
        #build lower right == transpose of upper left
        istart=nnodes
        iend=nnodes+npipes
        jstart=npipes
        jend=npipes+nnodes
        for ir in range(istart,iend):
            for jc in range (jstart,jend):
                augmentedMat[ir][jc] = -1.0*nodearcs[jc-jstart][ir-istart] + 0.0
        # build lower left partition of the matrix
        istart = nnodes
        iend = nnodes+npipes
        jstart = 0
        jend = npipes
        for i in range(istart,iend ):
            for j in range(jstart,jend ):
        #        print('i =',i,'j=',j)
                if (i-istart) == j :
        #            print('i =',i,'j=',j)
                    augmentedMat[i][j] = -1.0*lossfactor[j] + 0.0
        if verbose == 'true' :
            print("updated augmented matrix in iteration",iteration)
            writeM(augmentedMat,rowNumA,colNumA,"augmented matrix")
    ################################################################
    # BUILD JACOBIAN MATRIX CURRENT Q+H SOLUTION                   #
    ################################################################        
        # now build current jacobian
        for i in range(rowNumA):
            for j in range(colNumA):
                jacbMat[i][j] = augmentedMat[i][j]
        # modify lower left partition
        istart = nnodes
        iend = nnodes+npipes
        jstart = 0
        jend = npipes
        for i in range(istart,iend ):
            for j in range(jstart,jend ):
        #        print('i =',i,'j=',j)
                if (i-istart) == j :
        #            print('i =',i,'j=',j)
                    jacbMat[i][j] = 2.0*jacbMat[i][j]
    ##        for jcol in range(0,nnodes+npipes):
    ##            print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
    ##        print ("-----------------------------")
    # matrix multiply augmentedMat*solvecguess to get current g(Q)
    #    gq = [0.0 for i in range(rowNumA)] # zero gradient vector
    ##    if verbose == 'true' :
    ##        print("augmented matrix in iteration",iteration)
    ##        writeM(augmentedMat,rowNumA,colNumA,"augmented matrix before mmult")
        gq = matrixvectormult(augmentedMat,solvecguess,rowNumA,colNumA)
    ##    if verbose == 'true' :
    ##        writeV(gq,rowNumA,"gq vectorbefore subtract rhs_true")
    # subtract rhs
    #    for i in range(rowNumA):
        gq = vectorsub(gq,rhs_true,rowNumA)#vector subtract
        if verbose == 'true' :
            print("computed g(q) in iteration",iteration)
            writeV(gq,rowNumA,"gq vector")
            print("compare current and new guess")
            for jcol in range(0,nnodes+npipes):
                print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
            print ("-----------------------------")
        dq = [0.0 for i in range(rowNumA)] # zero update vector
        if verbose == 'true' :
            writeV(dq,rowNumA,"dq vector before linear solve")
        if verbose == 'true' :
            print("jacobian before linearsolve in iteration",iteration)
            writeM(jacbMat,rowNumA,colNumA,"jabobian matrix")
        dq = linearsolver(jacbMat,gq) # memory leak after this call - linearsolve clobbers input lists
    #    dq = numpy.linalg.solve(jacbMat,gq) #the numpy equivalent
        if verbose == 'true' :
            print("jacobian after linearsolve in iteration",iteration)
            writeM(jacbMat,rowNumA,colNumA,"jabobian matrix")

        if verbose == 'true' :
            writeV(dq,rowNumA,"dq vector -after linear solve")
        solvecnew = vectorsub(solvecguess,dq,rowNumA)#vector subtract
        if verbose == 'true' :
            print("Q_new = Q_old - DQ")
            writeV(solvecnew,rowNumA,"new guess vector")
    #    tempvect =[ 0.0 for i in range(rowNumA)]
    ##        tempvect = matrixvectormult(jacbMat,dq,rowNumA,colNumA)
    ##        writeV(tempvect,rowNumA,"J*dq vector")
    ##        tempvect = vectorsub(tempvect,gq,rowNumA)
    ##        writeV(tempvect,rowNumA,"J*dq - gq vector")
            print("just after computing new guess, should be different")
            for jcol in range(0,nnodes+npipes):
                print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
            print ("-----------------------------")
    #test for stopping
        tempvect =[ 0.0 for i in range(rowNumA)]
        for i in range(rowNumA):
            tempvect[i] = abs(solvecnew[i] - solvecguess[i])
        test1 = vdotv(tempvect,tempvect,rowNumA)
        if verbose == 'true' :
            print('test1',test1)
        tempvect =[ 0.0 for i in range(rowNumA)]
        for i in range(rowNumA):
            tempvect[i] = abs(gq[i])
        test2 = vdotv(tempvect,tempvect,rowNumA)
        if verbose == 'true' :
            print('test2',test2)
        if test1 < tolerance1 :
            print("###EXIT TYPE###\nUpdate not changing --exit and report current update")
            print("iteration",iteration)
    # update guess
            solvecguess[:] = solvecnew[:]
            for i in range(0,npipes,1):
                flowguess[i] = solvecguess[i]

            break
        if test2 < tolerance2 :
            print("###EXIT TYPE###\nGradient near zero --exit and report current update")
            print("iteration",iteration)
    # update guess
            solvecguess[:] = solvecnew[:]
            for i in range(0,npipes,1):
                flowguess[i] = solvecguess[i]

            break
        if verbose == 'true' :
            print("solution continuing")
            print("iteration",iteration)
        # update guess
        solvecguess[:] = solvecnew[:]
        if verbose == 'true' :
            for i in range(0,npipes,1):
                flowguess[i] = solvecguess[i]
    ## Write Current State ######################
            gq = matrixvectormult(augmentedMat,solvecguess,rowNumA,colNumA)
            print('number of nodes : ',nnodes)
            print('number of pipes : ',npipes)
            print('viscosity       : ',viscosity)
            print ("-----------------------------")
            for irow in range(0,nnodes):
                print('node id:',irow, ', elevation :',elevation[irow])
            print ("-----------------------------")
            for jcol in range(0,npipes):
                print('pipe id:',jcol,', diameter : ' ,diameter[jcol],', distance : ',distance[jcol],
              ', roughness : ',roughness[jcol],', flow guess : ',round(flowguess[jcol],3))
            print ("-----------------------------")
            for jcol in range(0,nnodes+npipes):
                print('irow :',jcol,' RHS True :',rhs_true[jcol],"RHS Current",round(gq[jcol],3))
            print ("-----------------------------")
            for jcol in range(0,nnodes+npipes):
                print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
            print ("-----------------------------")   
    ################################################
    # end of outer loop
    ################################################

# Report Results
    print("#####SIMULATION RESULTS#####\nResults at iteration = :",iteration)
    for i in range(0,npipes,1):
        flowguess[i] = solvecguess[i]
    print('number of nodes : ',nnodes)
    print('number of pipes : ',npipes)
    print('viscosity       : ',viscosity)
    print ("-----------------------------")
    istart = int(npipes)
    for irow in range(0,nnodes):
        print('node id:',irow+1, ', elevation (feet) :',elevation[irow],' head (feet) :',round(solvecnew[irow+npipes],3),' pressure (psi) :', round((14.75/33)*(solvecnew[irow+npipes]-elevation[irow]),3))
    print ("-----------------------------")
    for jcol in range(0,npipes):
        print('pipe id:',jcol+1,', diameter (feet) : ' ,diameter[jcol],', distance (feet) : ',distance[jcol],
      ', friction factor : ',round(friction[jcol],3),', flow (cfs) : ',round(flowguess[jcol],3))
    print ("-----------------------------")
    if verbose == 'true' :
        for jcol in range(0,nnodes+npipes):
            print('irow :',jcol,' RHS True :',rhs_true[jcol],"RHS Current",gq[jcol])
        print ("-----------------------------")
        for jcol in range(0,nnodes+npipes):
            print('irow :',jcol,' solvecnew :',solvecnew[jcol]," solvecguess ",solvecguess[jcol])
        print ("-----------------------------")
    return


# In[17]:


# Now run the simulation
pipenet('PN-E2.txt') 


# Now will save the `pipenet()` function to a file named `pipenet.py` which we can now import as needed.

# In[ ]:




