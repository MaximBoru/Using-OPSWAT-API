# Using-OPSWAT-API

This is a python program which has been designed to use OPSWAT's Metadefender Cloud APIs to scan files against numerous engines to determine if it is clean or infected. This program enables the user to specify a file on their machine to be scanned. First, the SHA1 hash of the file is calculated to determine if the file has already been scanned and has an existing scan report, in which case that report will be retrieved and displayed to the user. If the file's hash is not found and no scan report exists for it already, the file will be scanned and uploaded to the MetaDefender Cloud. Uploading the file returns a unique data ID for the file which is then used to repeatedly poll the API and check the progress of the scan until it is complete, at which point the complete report is retrieved and presented to the user.

### Requirements to run this program:
* Have Python 3 installed on your machine
* Ensure that you have an up-to-date version of pip via "pip install --upgrade pip" in the terminal
* Install the requests library via "python -m pip install requests" in the terminal
* Place the file you wish to scan in the same working directory as the source code
* Have an OPSWAT account and APIKey (You will be prompted for it upon running the program)

### Expected results after the program is run:
* A response telling you if the file has already been scanned along with its pre-existing report or if your file is new and has been uploaded
* The scan report with overall status of the file (clean or infected) and the individual results from each scanning engine
