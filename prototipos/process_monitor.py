import psutil

"""
IT WORKS!!!!!

Alter the code btw, it was AI generated

"""


def check_process_running(process_name):
    for proc in psutil.process_iter(["pid", "name"]):
        if proc.info["name"] == process_name:
            return True
    return False


process_name = "mpv"
if check_process_running(process_name):
    print(f"{process_name} is running")
else:
    print(f"{process_name} is not running")
