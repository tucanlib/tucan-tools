# Export your grades
... and start comparing yourself to other students. It's a totally sane thing to do.

Outputs the difference of your grades to the grades of the others.


```bash
# Needed: python3 and pip3 or pip.exe or whatever, and:
pip3 install mechanicalsoup
pip3 install argparse

# To export the grades:
# You will get prompted for your username/password
# or you can create a file called 'user-credentials.txt' with two lines in it:
# your username and password (trailing whitespace etc. will be stripped)
python3 grades_extractor.py
# (grades.json)

# To plot the notenspiegel:
# If there is an error that you need 'tkinter' you have to install 'python-pmw' (Arch Linux)
pip3 install matplotlib
pip3 install numpy
python3 grades_notenspiegel_plotter.py
# (plots will reside in newly created 'output' folder)

# New: exporting the VV is now possible, too:
pip3 install bs4
python3 vv_exporter.py
# (modules.json)
```

## Caveats
- Only exports grades where the Notenspiegel is available. This is by choice, not accident - so technically no caveat but will be perceived as one.
- Once the `grades.json` got extracted from TuCan, it will be reused whenever possible. So if there are grades/courses missing, just delete the `grades.json` and try again.


## TODO:
- Get better grades...
- Remind Micha to install a sane OS where `pip` is not `pip.exe`


![Notenspiegel](screenshot.png)