import hashlib
import requests

def hashFile(filename):
    # This function returns the hash of the file passed into it
    # hash object
    hash = hashlib.sha1()
    # opens file to be read in binary mode
    with open(filename, "rb") as file:
        # loop till eof
        chunk = 0
        while chunk != b"":
            # read 1024 bytes at a time
            chunk = file.read(1024)
            hash.update(chunk)
    return hash.hexdigest()

def uploadFile(filename, endpoint, apiKey):
    # Uploads file to server
    file = open(filename, "rb")
    uploadResponse = requests.post(endpoint, headers=queryHeaders, files={"form_field_name:": file})
    if uploadResponse.ok:
        print("Upload Success!")
        return uploadResponse
    else:
        print("Error: Upload Failed! The server returned a " + uploadResponse.status_code)
        exit()

apiKey = input("Please enter your apiKey: ")
filename = input("Please enter the name of the file you would like to check the hash of: ")

# Gets the sha1 hash of the input file and stores the hash value
hash = hashFile(filename)

# Checking if the file exists in the database based on its hash
queryHeaders = {"apikey": apiKey}
endpoint = "https://api.metadefender.com/v4/hash/" + hash
try:
    response = requests.get(endpoint, headers=queryHeaders)
except:
    print("The server returned a " + response.status_code + "exiting program...")
    exit()

# Checks if hash exists in the opswat database to see if file is present
if (response.ok):
    print("Corresponding hash exists in the database")
# If hash does not exist in the opswat database, upload it and poll its dataID repeatedly
else:
    endpoint = "https://api.metadefender.com/v4/file"
    uploadResponse = uploadFile(filename, endpoint, apiKey)

    # User input for decoding
    encoding = input("What charset should be used to decode? press enter for default (utf-8)") or "utf-8"
    print(encoding)

    # This gets the data ID from byte format to string for later use
    stringResp = uploadResponse.content.decode(encoding)
    split1 = stringResp.split('data_id":"')
    split2 = split1[1].split('"')
    dataId = split2[0]
    print(dataId)

    # Sets up the dataId URL endpoint for requests
    dataIdEndpoint = "https://api.metadefender.com/v4/file/" + str(dataId)
    try:
        response = requests.get(dataIdEndpoint, headers=queryHeaders)
    except:
        print("The server returned a " + response.status_code + "exiting program...")
        exit()

    # Repeatedly polling on the dataID to retrieve results when finished
    progress = response.json()["scan_results"]["progress_percentage"]
    while progress != 100:
        try:
            response = requests.get(dataIdEndpoint, headers=queryHeaders)
        except:
            print("The server returned a " + response.status_code + "exiting program...")
            exit()
        progress = response.json()["scan_results"]["progress_percentage"]
        print("Scanning is " + str(progress) + "% done")

# Get list of engines for printing output cleanly
engineListEndpoint = "https://api.metadefender.com/v4/status/engines-cloud"
engineResponse = requests.get(engineListEndpoint)
engineList = (engineResponse.json()["commercial"])

# Determining overallStatus
overallStatus = response.json()["scan_results"]["scan_all_result_a"]
if overallStatus == "No Threat Detected":
    overallStatus = "Clean"

# displaying overall status - clean or not:
print("\nfilename: " + filename)
print("overall_status: " + overallStatus)

# displaying all results
for engine in engineList:
    # First several arguments to be reused are stored in resp
    resp = response.json()["scan_results"]["scan_details"][engine]
    print("\nengine: " + engine)
    # If no threat is found, print clean for threat_found
    threatFound = (resp["threat_found"])
    if not threatFound:
        threatFound = "Clean"
    print("threat_found: " + threatFound)
    print("scan_result: " + str(resp["scan_result_i"]))
    print("def_time: " + str(resp["def_time"]))