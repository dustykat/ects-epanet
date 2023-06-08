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