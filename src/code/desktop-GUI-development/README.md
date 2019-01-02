#### This directory will host all desktop GUI code (Python)

######  Note:
It is currently required to have Python3 installed on your machine.  
In addition, pip3, python3's package manager must also be installed.   
If you are on windows, it is best to add these to your environment variables.

Once pip3 is installed, use it to install pyqt5-tools as shown below:  
`pip3 install pyqt5-tools` or `python -m pip install pyqt5-tools`  

###### Note:
Ultimately, it is intended to be delivered as a .exe file.  
Once visible, use the .exe file to launch the application rather  
than installing the above dependencies.

##### Approach:

Use `pyqt5` designer to build a healthy user interface in the form of 
a `.ui` file. From these .ui files, we can use pyuic to decipher  the them  
and generates our GUI as a .py runnable application format.  
To do this, run the following command while in 
the **python3.7/scripts** directory: `pyuic5 {'.ui file path'} -o {'output .py path'}`
