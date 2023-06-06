import requests

"""
Alter the code btw, it was AI generated
"""


def check_internet():
    try:
        response = requests.get("https://www.google.com")
        if response.status_code == 200:
            return True
    except:
        pass
    return False


# Check internet connection
if check_internet():
    print("Internet is connected.")
else:
    print("Internet is not connected.")
