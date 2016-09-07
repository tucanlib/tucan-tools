# Export your grades
... and start comparing yourself to other students. It's a totally sane thing to do.

Outputs the difference of your grades to the grades of the others.

Caveat: Only exports grades where the Notenspiegel is available. This is by choice, not accident - so technically no caveat but will be felt as one.

```bash
# Needed: python3 and pip3 or pip.exe or whatever
pip3 install mechanicalsoup
pip3 install argparse
./extract-grades.py TUCAN_USERNAME PASSWORD
# or
python3 extract-grades.py TUCAN_USERNAME PASSWORD
```

## TODO:
- Add plotting? Because why not
- Get better grades...
- Remind Micha to install a sane OS where `pip` is not `pip.exe`