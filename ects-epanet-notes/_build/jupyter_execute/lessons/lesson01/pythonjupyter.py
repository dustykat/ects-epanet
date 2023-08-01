#!/usr/bin/env python
# coding: utf-8

# # 1.3 Python/Jupyter Introduction
# 
# ## Purpose
# 
# A really quick refresher of Python programming concepts and Jupyter Notebooks for use in this short course.
# 
# ### Install/On-Line Access
# You can use ordinary python or install Python and Jupyter using
# - [Anaconda](https://www.anaconda.com/download)
# 
# Much of the materials is adapted from:
# 
# [Theodore G. Cleveland, Farhang Forghanparast (2021), Computational Thinking and Data Science: Instructor’s Notes for ENGR 1330 at TTU, with contributions by: Dinesh Sundaravadivelu Devarajan, Turgut Batuhan Baturalp (Batu), Tanja Karp, Long Nguyen, and Mona Rizvi. Whitacre College of Engineering](http://54.243.252.9/engr-1330-webroot/engr1330jb/_build/html/intro.html)

# ## Python 
# Python is a computer programming language often used to build websites and software, automate tasks, and conduct data analysis. Python is a general-purpose language, meaning it can be used to create a variety of different programs and isn't specialized for any specific problems.
# 
# - Python is an interpreted language
# - Compilation steps are not needed; This makes it less cumbersome (e.g class files (i.e. java) are not needed)
# - Python is less complex than languages such as C++ or Java; Makes it easier to learn and use but there is a tradeoff since programs cannot be as complex
# 
# ### Running Python Scripts
# 
# The Python interpreter runs the code of a program; in this notebook its part of tha Jupyter kernel.
# 
# A quick way to check is to open a terminal window and type `python --version`.  If the response is somethink like `Python 3.8.3` you have python installed somewhere on your computer.
# 
# To run a python script interpreter on Windows (other systems are similar) with the path set correctly
# - Open a command prompt
# - Type in the command python someFileName.py; This runs the program contained in the file someFileName.py
# 
# To run python interactive
# - Open a command prompt
# - Type in python
# - This runs python in interactive mode (see References below)

# ## Readings
# 
# 1. [https://www.java.com/en/download/help/path.xml](https://www.java.com/en/download/help/path.xml) Set Environment Variables Article
# 2. [https://docs.python.org/2/tutorial/interpreter.html#](https://docs.python.org/2/tutorial/interpreter.html#) Invoking the python interpreter in interactive mode

# ## Using an Integrated Development Environment (IDE)
# - PyCharm is a good one; Jupyter (as used herein) is in some sense an IDE. IDLE is another.  
# IDEs help manage projects and assist with testing and debugging
# Minimal IDE skills you should develop:
# - Create projects and files
# - Debug the projects
# - Run the projects
# 
# ## Readings
# 1. [https://www.jetbrains.com/pycharm/](https://www.jetbrains.com/pycharm/)PyCharm
# 2. [https://docs.python.org/3/library/idle.html](https://docs.python.org/3/library/idle.html) Integrated Development and Learning Environment (IDLE).
# 
# <hr><hr>

# ## Python Variables
# Variables keep data i.e. integers, strings, floats and address memory locations used to store data
# - Python does not declare variables
# - Other languages i.e. Java do declare variables; This makes Python simpler to code
# 
# **Variable declaration and use in Java:**
# 
# <pre style="color:blue;background-color:lightgrey">
# int integer1 = 5;
# int integer2 = 6;
# float float1 = 6.75;
# String myString = "This is a string";
# String anotherString;
# 
# integer1 = integer2 + 7;
# integer2++;
# anotherString = myString + " now adding to string"; integer2++;
# </pre>
# 
# <br/>
# 
# **Variable declaration and use in Python:**
# <pre style="color:blue;background-color:lightgrey">
# variable1 = 5
# variable2 = "This is a string"
# 
# variable1 = variable2 + " now adding to string"
# </pre>
# 
# 
# Variable types are assigned when data is put into them; Variables can be moved between types. The native types are:
# - numeric - integer, long, float, complex
# - String - a contiguous set of characters
# - List - items of various types, enclosed in braces [], separated by commas
# - Tuple - items of various types, enclosed in parentheses, separated by commas, read-only
# - Dictionary - contains name values pairs, a hash table
# 

# ## Operators
# The standard unitary arithmetic operators are:
# - \+ addition
# - \- subtraction
# - \* multiplication
# - / division
# - % modulus - gives the remainder of division
# - // integer division gives the whole number (or rounded down)
# - \*\* exponentiation
# 
# The standard comparison operators are:
# - == example x == y -- is x equal to y (gives true or false)
# - != example x != y -- is x not equal to y (gives true or false)
# - <> example x <> y -- same as above is x not equal to y
# - \> example x > y -- is x greater than y
# - \< example x < y -- is x less than y
# - \>= example x >= y -- is x greater than or equal to y
# - \<= example x <= y -- is x less than or equal to y
# 
# The logical operators are:
# - **and** example x and y -- both x and y must be true to give true
# - **or** example x or y -- either x or y must be true to give true
# - **not** example not(x or y) -- reverses the condition in the parentheses
# 
# The common string operators are:
# - print (str)          # Prints complete string
# - print (str[0])       # Prints first character of the string
# - print (str[2:5])     # Prints characters starting from 3rd to 5th
# - print (str[2:])      # Prints string starting from 3rd character
# - print (str * 2)      # Prints string two times
# - print (str + "TEST") # Prints concatenated string
# 
# :::{note}
# print(*parameter list*) is an intrinsic function!  The function name is **print** the expression in the *parameter list* needs to be of correct structure or the function throws an exception (like an error) and stops execution.
# :::
# 
# List operators are:
# 
# - list = [ 'abcd', 786 , 2.23, 'john', 70.2 ]
# - tinylist = [123, 'john']
# 
# A list is a collection of values, with a common reference name; the values can be any variable type, even another list.
# 
# - print (list)          # Prints complete list
# - print (list[0])       # Prints first element of the list
# - print (list[1:3])     # Prints elements starting from 2nd till 3rd 
# - print (list[2:])      # Prints elements starting from 3rd element
# - print (tinylist * 2)  # Prints list two times
# - print (list + tinylist) # Prints concatenated lists
# 
# Dictionary Operators act on special lists called dictionaries - the lists have keys, and values.
# 
# - dict = {}
# - dict['one'] = "This is one"
# - dict[2]     = "This is two"
# 
# - tinydict = {'name': 'john','code':6734, 'dept': 'sales'}
# 
# 
# - print (dict['one'])       # Prints value for 'one' key
# - print (dict[2])           # Prints value for 2 key
# - print (tinydict)          # Prints complete dictionary
# - print (tinydict.keys())   # Prints all the keys
# - print (tinydict.values()) # Prints all the values
# 
# :::{note}
# Dictionaries and tuples are tricky critters, but quite useful.  You will pick these up as you go.  Remember Chat GPT 3.5 is really helpful here; enter a code fragment and ask for an explaination - the result is usually quite good
# :::
# 
# 
# 
# ## Readings
# 1. [http://www.tutorialspoint.com/python/python_basic_operators.htm](http://www.tutorialspoint.com/python/python_basic_operators.htm) Python Operators

# ## Python Syntax Conventions
# **Indentation**
# Indentation is used in Python to code blocks rather than beginning and ending (scope) delimiters
# >For example in Java code blocks are delimited by braces i.e. {}
# 
# All statements in a block must have the same indentation level
# The default indentation increment is four spaces
# 
# **Identifier naming convention** :
# - Class names start with an uppercase letter and all other identifiers with a lowercase letter.
# - Starting an identifier with a single leading underscore indicates by convention that the identifier is meant to be private.
# - Starting an identifier with two leading underscores indicates a strongly private identifier.
# - If the identifier also ends with two trailing underscores, the identifier is a language-defined special name.
# 
# **Multiline Statements**
# 
# :::{note}
# The continuation marker is `\`; its also the escape character.  
# :::
# 
# <pre style="color:blue;background-color:lightgrey">
# total = item_one + \
#         item_two + \
#         item_three
# </pre>
# 
# **Use of Quotes**
# Strings in Python can use single, double, or triple quotes as a way to embed the `'` marker (there are other ways to accomplish this too)
# 
# <pre style="color:blue;background-color:lightgrey">
# string1 = 'This is a string'
# string2 = "This is a string"
# string3 = '''This is a
# multiline string'''
# string4 = """This is also a
# multiline string"""
# </pre>
# 
# **Comments**
# 
# The pound sign/hash mark "#" is used for single line comments; Three single or double quotes are used for multiline comments
# 
# <pre style="color:blue;background-color:lightgrey">
# #This is a single line comment
# #This is a second single line comment
# 
# '''This is
# a multiline comment'''
# 
# """This is also
# a multiline comment"""
# </pre>
# 
# **Multiple Statement on a Single Line**
# Use semicolons as the delimiter between statements
# 
# <pre style="color:blue;background-color:lightgrey">
# a = b+1; c = d + 2; print(str(a))
# </pre>
# 
# :::{note}
# If you are familiar with the bash shell the `;` means complete the process to the left before continuation.  It means the same in the python script.
# :::

# 

# 

# 

# 

# **Control Structures (Selection)**<br>
# 
# **if statement** a conditional statement that can have an else clause; note that the sub-statements of the if statement are indented; the normal default for indenting is four spaces
# 
# <pre style="color:blue;background-color:lightgrey">
# a = 10
# if (a == 10):
#     print("In if statement")
# </pre>
# 
# <pre style="color:blue;background-color:lightgrey">
# a = 10
# if (a == 10):
#     print("In if statement")
# else:
#     print("In else statement")
# </pre>
# 
# **Control Structures (Repetition)**<br>
# 
# **while loop** a loop (repetition) that continues until the loop condition has been satisfied
# 
# <pre style="color:blue;background-color:lightgrey">
# a = 10
# while (a < 15):
#     print("in while loop")
#     a += 1
# </pre>
# 
# > while loop with else statement
# >
# ><pre style="color:blue;background-color:lightgrey">
# a = 10
# while (a < 15):
#     print("in while loop")
#     a = a + 1
# else:
#     print("while loop has ended")
# </pre>
# 
# <br>
# 
# **for loop** a loop (repetition) that is iterator (count) controlled. the general form of the for loop is
# 
# <pre style="color:blue;background-color:lightgrey">
# for iterating_var in sequence:
#     statements(s)
# </pre>
# 
# Where *iterating_var* is the name of the variable that represents the next item in the sequence to be used in the statements of the for loop
# 
# > An example of a list and iterator and a for loop that iterates through the list
# 
# <pre style="color:blue;background-color:lightgrey">
# animals = ['dog','cats','moose','deer','bear']
# 
# for theAnimal in animals:
#     print("the animal is a " + theAnimal)
# </pre>
# 
# > An example of a list and an iteration using the index in the list
# <pre style="color:blue;background-color:lightgrey">
# animals = ['dog','cat','moose','deer','bear']
# 
# for index in range (len(animals)):
#     print("Using an index the animal is a " + animals[index])
# </pre>

# ## Functions
# A function is a piece of reusable code
# - Generally it performs an identifiable action that can be reused; For example opening, writing to, or closing a file
# - It provides modularity for the code making it easier to understand
# - There are standard (intrinsic) functions provided with Python
# - New functions can be defined by programmers (user-defined functions)
# 
# **How to define a function**
# Functions begin with the keywork `def` (define), followed by the function name, and then a set of parentheses ()
# - Input parameters are placed within the parentheses ()
# - The first statement can be an optional documentation string (docstring)
# - The code block starts with a colon : and is indented
# 
# **Example of a Function**
# 
# <pre style="color:blue;background-color:khaki">
# def theFunctionName(parameters):
#    "function_docstring"
#    function statements
#    return [expression]
# </pre>
# 
# **Built-in and Standard Library Functions**
# 
# There are a number of functions that are built-in in Python
# - See the Python Documentation on Build-in Functions in the References below
# - These are part of the Standard Library; There are also a number of other modules in the standard library
# - These give solutions to many everyday programming problems
# 
# Built-in Functions can be called directly in the code
# 
# **Example of using Built-in Functions**
# <pre style="color:blue;background-color:lightgrey">
# f = open('workfile', 'w')
# f.write("this is the file output")
# f.close()
# </pre>
# 
# **Standard Library functions must be imported**
# The example below imports from the module named `math` and selects from the module the function named `sqrt`.  An alternate way is also shown
# 
# **Example of using Standard Library Functions**
# <pre style="color:blue;background-color:lightgrey">
# from math import sqrt
# a = sqrt(24)
# print (a)
# </pre>
# 
# **Alternate approach without implicit aliasing**
# <pre style="color:blue;background-color:lightgrey">
# import math 
# a = math.sqrt(24)
# print (a)
# </pre>
# 
# ## Readings
# 1. [https://docs.python.org/3/library/functions.html](https://docs.python.org/3/library/functions.html) Built-in Functions
# 2. [https://docs.python.org/3/library/](https://docs.python.org/3/library/) Standard Library Including Built-in Functions

# ## Python Scope
# Scope refers to the range within a program that a variable exists.  In general variables in a function are isolated from variables in the calling script unless otherwise defined.  
# 
# A Variable's scope
# - Python has only function, global, and class scope.
# - It does not have block scope, For example a variable first used in a for loop can be seen outside the for loop. In many other languages such as Java, C++, and C a variable declared in a block has block scope
# 
# Function scope vs global scope
# 
# <pre style="color:blue;background-color:lightgrey">
# globalVar = "this string is global" #creates a global variable
# 
# def anotherFunction ()
#     globalVar = "this string is local" #creates a variable local to the function
# </pre>

# ## Importing External Modules
# 
# The import statement brings the functions within a file into the program
# 
# **Example of code import**
# 
# <pre style="color:blue;background-color:lightgrey">
# Assume that the file importFunctions.py has the following code
# 
# def print_value(parameter):
#     print("the value is " + parameter)
#     return
# 
# To use this code in another file it must imported then used
# 
# #import the functions from importFunctions
# import importFunctions
# 
# #use the print_value function
# importFunctions.print_value("Print This String")
# </pre>
# 
# 
# **The from import statement**
# Bring the functions within a file into the program; Allow the use of the functions without the leading filename - a type of aliasing
# 
# **Example of the from import statement**
# <pre style="color:blue;background-color:lightgrey">
# Assume that the file importFunctions.py has the following code
# 
# def print_value(parameter):
#     print("the value is " + parameter)
#     return
# 
# To use this code in another file it must imported then used
# 
# #from import the functions
# from importFunctions import print_value
# 
# #use the print_value function without the leading filename
# print_value("Print This String")
# </pre>

# ## Object Oriented Classes
# 
# Python has classes which makes it object oriented; it also has functions so it is also a functional language
# 
# ### Overview of Object Oriented Programming (OOP)
# <pre style="color:blue;background-color:khaki">
# Class - a user defined template for objects.  Contains both variables and methods.
#         Classes allow libraries of well tested self contained code to be distributed.
#         Each of these self contained units is a class.
# Class Variable - In Python it is a variable that is shared by all instances of a class
#                  Objects are instances of classes.
# Data Member - A class variable or instance variable that holds data
# Functions Overloading - A set of functions of the same name with varying parameter types.
#                         Each function can have different code
# Instance Variable - a variable defined within a method of a class.  Variables defined
#                     outside of the classes methods are class variables (see above).
# Inheritance - A class will inherit the methods of a class from which it is derived.
#               See the section below on inheritance
# Instance - A object that has been created from a class template.  It is an object of
#            that class.
# Instantiation - The creation of an object from a class template
# Method - A special type of function that belongs to and is coded within a class
# Object - A unique instance of a class.  An object has both data members and methods.
# </pre>
# 
# ### Class Definitions
# The form of a class definition is as follows
# 
# <pre style="color:blue;background-color:khaki">
# class ClassName
#    classData = "this could be any data"
#    def __init__(self):
#     self.someData = []
#    def someFunction(self, parameter1, parameter2):
#        statement1
#        statement2
#        ...
#        return returnValue
# </pre>
# 
# - **self** is not a keyword it is just an indication that the first argument passed into a function is a reference to the object (it is just called self for convenience).
# - The **function __init__** is the constructor for the class that runs when a class instance is created
# - The statement **self.someData** creates a list that belongs to the instance object
# - The statement **classData = "this could be any data"** creates a class variable shared across instance objects of the class
# 
# **Class Variable Scope**
# - Class variables have a scope across all instance objects of the class
# - Instance variables have scope within an instance object of the class; Instance variable are defined within class methods (functions in the class)
# 
# ## Readings 
# 1. [https://docs.python.org/2/tutorial/classes.html](https://docs.python.org/2/tutorial/classes.html) Python Tutorial on Classes. 
# 
# **Example of a class**
# <pre style="color:blue;background-color:lightgrey">
# class Dog:
#     kind = 'canine'         # class variable shared by all instances
#     def __init__(self, name):
#         self.name = name    # instance variable unique to each instance
# </pre>
# 
# ''Use of the class to understand variable scope''
# <pre style="color:blue;background-color:lightgrey">
# dog1 = Dog('fido')
# dog2 = Dog('Buddy')
# print(dog1.name)    # will give name of Fido which is an instance variable
# print(dog1.kind)    # will give a kind of canine which is a class variable
# print(dog2.name)    # will give a name of Buddy which is an instance variable
# print(dog2.kind)    # will give a kind of canine which is a class variable
# </pre>
# 
# Note that there is no concept of public and private variables. For example java has public and private keywords, Python does not. There is a convention that states:
# Variables and functions that begin with an underscore (i.e. _variable1) should be treated as private and not public
# 
# **Class Inheritance**
# A class can inherit methods and data from other classes
# The definition of the class looks like:
# 
# <pre style="color:blue;background-color:lightgrey">
# class DerivedClassName(BaseClassName):
# 
#     def __init__(self, etc.):
#          statement1
#          ...
# 
#     def function1()
#         statement1
#         ...
#         return somevalue
# 
# 
# </pre>
# 
# Note: the class will inherit the attributes of BaseClassName
# 
# ## Readings
# 1. [https://www.python.org/](https://www.python.org/) Python main site
# 2. [https://docs.python.org/3/](https://docs.python.org/3/) Python.org Documentation
# 3. [https://wiki.python.org/moin/BeginnersGuide/Programmers](https://wiki.python.org/moin/BeginnersGuide/Programmers) Beginners Programming Guides
# 4. [http://www.tutorialspoint.com/python/index.htm](http://www.tutorialspoint.com/python/index.htm)TutorialsPoint.com Python Tutorial

# ## Jupyter
# 
# Jupyter Notebooks are interactive web-based computational environments that allow users to create and share documents containing live code, equations, visualizations, and explanatory text. They support multiple programming languages and are widely used for data analysis, scientific computing, machine learning, and data visualization tasks. Jupyter Notebooks provide an intuitive interface, enabling users to execute code in small, manageable cells and observe the output immediately, fostering an iterative and exploratory approach to programming. Their versatility, ease of use, and ability to blend code with rich media make them a popular choice among researchers, data scientists, and educators for creating reproducible and interactive data-driven workflows.
# 
# This on-line book is created using JupyterBook; when I develop the book i use JupyterHub running on a Raspberry Pi computer
# 
# ### JupyterHub
# 
# Jupyter Hub is a web-based platform that enables multiple users to access Jupyter Notebooks, an interactive computational environment, simultaneously. It allows users to write and execute code, view visualizations, and create narrative documents that combine code, text, and multimedia content. Jupyter Notebooks support various programming languages, including Python, R, and Julia, making them versatile for data analysis, scientific computing, and machine learning tasks. The Hub provides a centralized server, facilitating collaboration and resource sharing within organizations or educational institutions, making it a powerful tool for data scientists, researchers, and students. Jupyter Hub's flexibility and user-friendly interface have made it a popular choice for collaborative data exploration and analysis.
# 
# ### Python and Jupyter
# 
# IPython and Jupyter are closely related, and Jupyter Notebooks actually originated as a spin-off of IPython. Here's how they interact:
# 
# - IPython: IPython (Interactive Python) is an enhanced Python shell that provides a more interactive and powerful environment for working with Python code compared to the standard Python REPL (Read-Eval-Print Loop). It offers features such as command history, tab completion, and object introspection. IPython started as a standalone project before it became an integral part of Jupyter.
# 
# - Jupyter: Jupyter is an open-source project that evolved from IPython. It expanded its support for multiple programming languages beyond just Python, and hence the name change from "IPython" to "Jupyter" (a combination of Julia, Python, and R). Jupyter allows users to create interactive computational notebooks that combine code, text, images, and other media, making it an ideal platform for data exploration, analysis, and visualization.
# 
# - Jupyter Notebooks: Jupyter Notebooks are web-based interfaces that allow users to create and share documents containing live code, visualizations, and narrative text. They are built on top of IPython, which serves as the kernel (execution engine) for running Python code within the notebook cells.
# 
# When you run a Jupyter Notebook, it uses the IPython kernel to execute Python code inside the notebook cells. The notebook interface provides a convenient way to interact with the IPython kernel, allowing you to execute code, view output, and create documentation within the same environment.
# 
# In summary, IPython serves as the kernel that handles the execution of Python code within Jupyter Notebooks, enabling the interactive and rich computational capabilities that Jupyter provides.
# 
# There is some further discussion in: [Theodore G. Cleveland, Farhang Forghanparast (2021), Computational Thinking and Data Science: Instructor’s Notes for ENGR 1330 at TTU, with contributions by: Dinesh Sundaravadivelu Devarajan, Turgut Batuhan Baturalp (Batu), Tanja Karp, Long Nguyen, and Mona Rizvi. Whitacre College of Engineering](http://54.243.252.9/engr-1330-webroot/engr1330jb/_build/html/lessons/lesson02/lesson02.html#ipython)

# ## Some code fragments (from in-class demonstrations)

# In[1]:


# expressions
avalue = 8.0
print(avalue)


# In[2]:


alist = [1,2,3,'free','cat']
print(alist)


# In[3]:


for items in alist:
    print(items)


# In[4]:


def squareit(argument):
    squareit = argument**2
    return(squareit)


# In[5]:


print(squareit(9))


# ## Exercises
# none
# ## References
# above
