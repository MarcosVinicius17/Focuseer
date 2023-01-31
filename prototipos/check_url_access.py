import subprocess


def is_url_being_accessed(url):
    output = subprocess.run(["netstat", "-nap"], stdout=subprocess.PIPE)
    for line in output.stdout.splitlines():
        if "ESTABLISHED" in line and url in line:
            return True
    return False


if is_url_being_accessed("google.com"):
    print("URL is being accessed")
else:
    print("URL is not being accessed")
