#### How to Run:

1. Ensure you have the most recent version of Python3 installed on your machine.
2. Once you have python installed, you should also naturally have installed **pip**.
   - pip is included in all python downloadable versions above 3.4
3. Set up a virtual python environment for version safety.
   - `pip install virtualenv`
   - `virtualenv venv`
   - `source venv/scripts/activate` or `source venv/bin/activate`
4. Run the command `pip3 install -r requirements.txt` in the current directory path to
   install all necessary packages for the project. Depending on your network connection,
   this may take up to 5 minutes.
5. Navigate to the **main/** directory and run `python application.py` or `python3 application.py`. This will start the application successfully.