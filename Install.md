## Installation Instructions for JUSTFAIR_Toolbox


#### Works across all systems (Linux, Mac OS X, and Windows)

Programming language runs off Python and uses the Python packages Matplotlib, NumPy, and Pandas. You can choose what ever IDE you want to work with. The IDE is how you utilize the python package we created given user has access to State data. You can also use data pulled from American Community Survey (ACS) Census Bureau data given the Census object. 

--------------------------------------------------------------------------

#### 1. Open Python IDE 
    
We used Jupyterhub and a series of Jupyter notebooks to run the program. You can also use Visual Studios, Pycharm, Pydev, IDLE, Atom, etc.

#### 2. (For access to JUSTFAIR_Toolbox repository) Cloning and Installing from Github

For **cloning** the repo, open terminal in python IDE and use following command to clone repository with packages code and example notebooks. 
    
`git clone https://github.com/nitkiew2/CMSE495-QSIDE-JUSTFAIR-TOOLBOX.git`
              
For **installing** the package, within your IDE work file/cell, run the following code.
     
`! pip install 'git+https://github.com/nitkiew2/CMSE495-QSIDE-JUSTFAIR-TOOLBOX.git'`
    

#### 3. Open a notebook or file to test the package

In order to run the package after installation, you need to import *JUSTFAIR_Toolbox* using the following code 
    
`import JUSTFAIR_Tools as jt`

`from JUSTFAIR_Tools import State`

`from JUSTFAIR_Tools import Census`

`from JUSTFAIR_Tools import toolbox`


#### 4. See *Package_testing.ipynb* for examples how to use the package

Within the cloned repository from *Step 2* click on the file with the name stated above

----------------------------------------------------------------------------------------
    
    
## Advanced Details 

Description of how to use the package given the different types of data for the analysis. You can use data from a premade dataframe, prefferably a CSV file, a dataframe from a URL link, or data from the Census which is built into the JUSTFAIR_Toolbox package.

#### 1. Creating paths in python

Create dictionary objects for states (object holding the data information per state of interest) and paths (object keeping track of the column/attribute names for the state dataframe). For paths object, the key of the dictionary is the name, in string format, which the user desires to use when pulling data. The value represents the associated value, in string format, that appears on the dataframe's column. You can further translate the values connected to the column key if values follow numerical categorization. *EX: Races are ranged from 1-10 and each number represents a race... Sex is 1 for Female and 2 for Male* For state object, the key value is the name of the state, in string format, which the plotting function uses in title. The *State* function takes the **name of the state in string format**, path for the repository which the **csv/dataframe is located, in string format**, **Path** dictionary object, and an optional parameter that specifies if data is pulled from a URL **using_url =** which can be set to *True or False*. For clarification, see example code in the file ***Package_testing.ipynb***.

#### 2. Accessing Census Data

 To call data from the ACS python file, you have to call the `demographic` class. This class is the main class object that can call data from different states. This class has data from 2010 to 2021. The database per state consists of age, race, and sex classification per case. The two parameter values to associate the object to are **'state name'** and **year of analysis**. For further clarification, see example code in the file ***____***.

-------------------------------------------------------------------------------------------------------------

