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
the **python3.7/scripts** directory: `pyuic5 -x {'.ui file path'} -o {'output .py path'}`

To generate the .exe for the standalone application format:  
[Python Script to Executable (.exe)](https://medium.com/dreamcatcher-its-blog/making-an-stand-alone-executable-from-a-python-script-using-pyinstaller-d1df9170e263)  

a) `pip3 install pyinstaller`  
- Running this command will install pyinstaller to your site-packages for accesibility.  

b) `pyinstaller --onefile -w <your_script_name>.py`  
- Pyinstaller will generate two directories: **build/** and **dist/**  
- Inside the **dist/** folder will you find the executable .exe file to run the GUI.
- Additionally, a `<your_script_name>.spec` file will be generated in the desktop-GUI-development root directory  
  which describes some configuration details of .exe.
